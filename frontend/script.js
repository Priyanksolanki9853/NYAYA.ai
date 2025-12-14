// This URL must match where Member A is running the backend
const API_URL = "http://127.0.0.1:8000"; 

async function sendMessage() {
    const inputField = document.getElementById("user-input");
    const chatBox = document.getElementById("chat-box");
    const question = inputField.value;

    if (question.trim() === "") return;

    // 1. Show User Message on Screen
    addMessage(question, "user-message");
    inputField.value = ""; // Clear input

    // 2. Show "Thinking..." temporary message
    const loadingId = addMessage("Thinking...", "bot-message");

    try {
        // 3. Send Request to Member A's Backend
        const response = await fetch(`${API_URL}/search?query=${encodeURIComponent(question)}`);
        const data = await response.json();

        // 4. Remove "Thinking..." and Show Real Answer
        removeMessage(loadingId);
        
        // Format the answer nicely
        const finalAnswer = `<strong>${data.result}</strong><br><br><small>Source: ${data.source}</small>`;
        addMessage(finalAnswer, "bot-message");

    } catch (error) {
        removeMessage(loadingId);
        addMessage("Error: Could not connect to backend. Is Member A's server running?", "bot-message");
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