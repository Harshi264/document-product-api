import os
from dotenv import load_dotenv
from pinecone import Pinecone
from groq import Groq
from langchain.text_splitter import RecursiveCharacterTextSplitter
from typing import List, Optional

load_dotenv()

class RAGService:
    def __init__(self):
        self.embedding_model = None
        self.pinecone_index = None
        self.llm_client = None

    def _get_embedding_model(self):
        if not self.embedding_model:
            from langchain_huggingface import HuggingFaceEmbeddings
            model_name = "all-MiniLM-L6-v2"
            self.embedding_model = HuggingFaceEmbeddings(model_name=model_name)
        return self.embedding_model

    def _get_pinecone_index(self):
        if not self.pinecone_index:
            api_key = os.getenv("PINECONE_API_KEY")
            index_name = os.getenv("PINECONE_INDEX")
            pc = Pinecone(api_key=api_key)
            self.pinecone_index = pc.Index(index_name)
        return self.pinecone_index

    def _get_llm_client(self):
        if not self.llm_client:
            api_key = os.getenv("GROQ_API_KEY")
            self.llm_client = Groq(api_key=api_key)
        return self.llm_client

    def _ingest_document(self, file, user_id: str, product_id: str):
        import fitz  # PyMuPDF
        doc = fitz.open(stream=file.read(), filetype="pdf")
        text = "".join([page.get_text() for page in doc])
        doc.close()
        if not text.strip():
            return

        chunks = RecursiveCharacterTextSplitter(chunk_size=1000, chunk_overlap=200).split_text(text)
        embeddings = self._get_embedding_model().embed_documents(chunks)
        vectors = [
            {
                "id": f"{user_id}_{product_id}_chunk_{i}",
                "values": embeddings[i],
                "metadata": {"text": chunk, "user_id": user_id, "product_id": product_id}
            }
            for i, chunk in enumerate(chunks)
        ]
        self._get_pinecone_index().upsert(vectors=vectors)
        return len(vectors)

    def _generate_llm_response(self, query: str, context_chunks: List[str], history: Optional[list] = None) -> str:
        history_str = "\n".join(f"{m.role}: {m.content}" for m in (history or []))
        prompt = f"""
        You are a helpful AI assistant. Use the context to answer the question.
        If no relevant info, say you don't know.

        HISTORY:
        {history_str}

        CONTEXT:
        {"\n---\n".join(context_chunks)}

        QUESTION:
        {query}
        """
        try:
            client = self._get_llm_client()
            chat_completion = client.chat.completions.create(
                messages=[{"role": "user", "content": prompt}],
                model="llama3-8b-8192",
            )
            return chat_completion.choices[0].message.content
        except Exception:
            return "Sorry, I had trouble generating a response."

    def search(self, query: str, user_id: str, product_id: str, history: Optional[list] = None) -> str:
        query_embedding = self._get_embedding_model().embed_query(query)
        try:
            results = self._get_pinecone_index().query(
                vector=query_embedding,
                top_k=3,
                include_metadata=True,
                filter={"user_id": {"$eq": user_id}, "product_id": {"$eq": product_id}}
            )
            matches = results.get("matches", [])
            if not matches:
                return "No relevant information found."
            return self._generate_llm_response(query, [m["metadata"]["text"] for m in matches], history)
        except Exception:
            return "Error while searching."
         
# import os
# from pinecone import Pinecone, ServerlessSpec
# from langchain_huggingface import HuggingFaceEmbeddings
# from langchain.text_splitter import RecursiveCharacterTextSplitter
# from dotenv import load_dotenv
# from groq import Groq
# from typing import List, Optional


# class RAGService:
#     def __init__(self):
#         load_dotenv()

#         self.embedding_model = self._get_embedding_model()
#         self.pinecone_index = self._get_pinecone_index()
#         self.llm_client = self._get_llm_client()

#     def _get_embedding_model(self):
#         model_name = "all-MiniLM-L6-v2"
#         return HuggingFaceEmbeddings(model_name=model_name)

#     def _get_pinecone_index(self):
#         api_key = os.getenv("PINECONE_API_KEY")
#         index_name = os.getenv("PINECONE_INDEX")

#         pc = Pinecone(api_key=api_key)

#         # Check if index exists
#         existing_indexes = [idx['name'] for idx in pc.list_indexes()]
#         if index_name not in existing_indexes:
#             raise ValueError(f"Pinecone index '{index_name}' does not exist. Please ensure it's created.")

#         return pc.Index(index_name)

#     def _ingest_document(self, file, user_id: str, product_id: str):
#         """
#         Processes a single PDF document and upserts its chunks to Pinecone.
#         """
#         import fitz  # PyMuPDF
#         doc = fitz.open(stream=file.read(), filetype="pdf")
#         text = ""
#         for page in doc:
#             text += page.get_text()
#         doc.close()

#         if not text.strip():
#             print("No text found in PDF. Ingestion skipped.")
#             return

#         # Split into chunks
#         text_splitter = RecursiveCharacterTextSplitter(chunk_size=1000, chunk_overlap=200)
#         chunks = text_splitter.split_text(text)

#         # Embed chunks
#         embeddings = self.embedding_model.embed_documents(chunks)

#         # Prepare vectors
#         vectors_to_upsert = []
#         for i, chunk in enumerate(chunks):
#             vector_id = f"{user_id}_{product_id}_chunk_{i}"
#             vectors_to_upsert.append({
#                 "id": vector_id,
#                 "values": embeddings[i],
#                 "metadata": {
#                     "text": chunk,
#                     "user_id": user_id,
#                     "product_id": product_id
#                 }
#             })

#         # Upsert to Pinecone
#         self.pinecone_index.upsert(vectors=vectors_to_upsert)
#         return len(vectors_to_upsert)

#     def _get_llm_client(self):
#         api_key = os.getenv("GROQ_API_KEY")
#         return Groq(api_key=api_key)

#     def _generate_llm_response(self, query: str, context_chunks: List[str], history: Optional[list] = None) -> str:
#         context = "\n---\n".join(context_chunks)

#         history_str = ""
#         if history:
#             for msg in history:
#                 history_str += f"{msg.role}: {msg.content}\n"

#         prompt = f"""
#         You are a helpful AI assistant. Use the following context to answer the user's question.
#         If the context doesn't contain the answer, state that you don't have enough information.
#         Be concise and direct.

#         PREVIOUS CHAT HISTORY:
#         {history_str}

#         CONTEXT FROM KNOWLEDGE BASE:
#         {context}

#         LATEST USER'S QUESTION:
#         {query}

#         YOUR ANSWER:
#         """

#         try:
#             chat_completion = self.llm_client.chat.completions.create(
#                 messages=[{"role": "user", "content": prompt}],
#                 model="llama3-8b-8192",
#             )
#             return chat_completion.choices[0].message.content
#         except Exception:
#             return "Sorry, I had trouble generating a response."

#     def search(self, query: str, user_id: str, product_id: str, history: Optional[list] = None) -> str:
#         query_embedding = self.embedding_model.embed_query(query)

#         try:
#             results = self.pinecone_index.query(
#                 vector=query_embedding,
#                 top_k=3,
#                 include_metadata=True,
#                 filter={
#                     "user_id": {"$eq": user_id},
#                     "product_id": {"$eq": product_id}
#                 }
#             )

#             matches = results.get("matches", [])
#             if not matches:
#                 return "I couldn't find any relevant information for your query."

#             context_chunks = [match["metadata"]["text"] for match in matches]

#             return self._generate_llm_response(
#                 query=query,
#                 context_chunks=context_chunks,
#                 history=history
#             )
#         except Exception:
#             return "Sorry, an error occurred while searching."
