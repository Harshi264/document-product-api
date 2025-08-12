
const CHAT_API_URL = "http://localhost:8000/query"; // Replace with your FastAPI backend URL
let currentProductId = null; // Will be set dynamically from outside

function initChatWidget(productId) {
    currentProductId = productId;

    // Create widget container
    const widgetContainer = document.createElement("div");
    widgetContainer.id = "chat-widget";
    widgetContainer.innerHTML = `
        <style>
            #chat-widget {
                position: fixed;
                bottom: 20px;
                right: 20px;
                width: 350px;
                height: 450px;
                background: white;
                border-radius: 12px;
                box-shadow: 0 4px 10px rgba(0,0,0,0.2);
                display: flex;
                flex-direction: column;
                font-family: Arial, sans-serif;
                overflow: hidden;
                z-index: 9999;
            }
            #chat-header {
                background: #4a90e2;
                color: white;
                padding: 10px;
                text-align: center;
                font-weight: bold;
            }
            #chat-messages {
                flex: 1;
                padding: 10px;
                overflow-y: auto;
                font-size: 14px;
            }
            .message {
                margin: 5px 0;
                padding: 8px;
                border-radius: 8px;
                max-width: 80%;
            }
            .user-message {
                background: #DCF8C6;
                align-self: flex-end;
            }
            .bot-message {
                background: #F1F0F0;
                align-self: flex-start;
            }
            #chat-input {
                display: flex;
                border-top: 1px solid #ddd;
            }
            #chat-text {
                flex: 1;
                padding: 10px;
                border: none;
                outline: none;
            }
            #chat-send {
                background: #4a90e2;
                color: white;
                border: none;
                padding: 0 15px;
                cursor: pointer;
            }
        </style>
        <div id="chat-header">Product Assistant</div>
        <div id="chat-messages"></div>
        <div id="chat-input">
            <input type="text" id="chat-text" placeholder="Type your question...">
            <button id="chat-send">Send</button>
        </div>
    `;
    
    document.body.appendChild(widgetContainer);

    // Event listeners
    document.getElementById("chat-send").addEventListener("click", sendMessage);
    document.getElementById("chat-text").addEventListener("keypress", function (e) {
        if (e.key === "Enter") sendMessage();
    });
}

async function sendMessage() {
    const input = document.getElementById("chat-text");
    const message = input.value.trim();
    if (!message) return;

    addMessage(message, "user-message");
    input.value = "";

    const typingEl = addMessage("Typing...", "bot-message");

    try {
        const response = await fetch(CHAT_API_URL, {
            method: "POST",
            headers: {
                "Content-Type": "application/json"
            },
            body: JSON.stringify({
                question: message, // <-- KEY CHANGE HERE
                product_id: currentProductId
            })
        });

        const data = await response.json();
        typingEl.remove();
        addMessage(data.answer || "No response from server", "bot-message");

    } catch (error) {
        typingEl.remove();
        addMessage("Error contacting server.", "bot-message");
        console.error("Chat error:", error);
    }
}

function addMessage(text, className) {
    const chatMessages = document.getElementById("chat-messages");
    const msgEl = document.createElement("div");
    msgEl.className = `message ${className}`;
    msgEl.innerText = text;
    chatMessages.appendChild(msgEl);
    chatMessages.scrollTop = chatMessages.scrollHeight;
    return msgEl;
}

window.initChatWidget = initChatWidget; // Make the init function globally available

