// This URL must match where Member A is running the backend
const API_URL = "http://127.0.0.1:8000"; 

async function sendMessage() {
    const inputField = document.getElementById("user-input");
    const question = inputField.value;

    if (question.trim() === "") return;

    // 1. Show User Message on Screen
    addMessage(question, "user-message");
    inputField.value = ""; // Clear input

    // 2. Show "Thinking..." temporary message
    const loadingId = addMessage('<span class="typing-indicator">Analyzing Constitution</span>', "bot-message");

    try {
        // 3. Send Request to Backend
        const response = await fetch(`${API_URL}/search?query=${encodeURIComponent(question)}`);
        const data = await response.json();

        // 4. Remove "Thinking..."
        removeMessage(loadingId);
        
        // 5. Format the Answer
        // 'marked.parse' converts **bold** to <b>bold</b> and * lists to <li>
        let formattedText = "";
        if (data.result) {
            formattedText = marked.parse(data.result);
        } else {
            formattedText = "I could not find an answer.";
        }

        // Create the final HTML structure
        const finalHTML = `
            <div class="formatted-content">${formattedText}</div>
            <div class="source-citation"><small>Source: ${data.source || "Samvidhan AI Legal Database"}</small></div>
        `;

        addMessage(finalHTML, "bot-message");

    } catch (error) {
        removeMessage(loadingId);
        addMessage("Error: Could not connect to backend. Is the Python server running?", "bot-message");
        console.error(error);
    }
}

// Helper function to add bubbles to the chat
function addMessage(text, className) {
    const chatBox = document.getElementById("chat-box");
    const msgDiv = document.createElement("div");
    msgDiv.className = `message ${className}`;
    msgDiv.innerHTML = text; // Using innerHTML to allow bold text/breaks
    msgDiv.id = "msg-" + Date.now();
    chatBox.appendChild(msgDiv);
    chatBox.scrollTop = chatBox.scrollHeight; // Auto-scroll to bottom
    return msgDiv.id;
}

function removeMessage(id) {
    const msg = document.getElementById(id);
    if (msg) msg.remove();
}

// Allow pressing "Enter" key to send
document.getElementById("user-input").addEventListener("keypress", function(event) {
    if (event.key === "Enter") {
        sendMessage();
    }
});