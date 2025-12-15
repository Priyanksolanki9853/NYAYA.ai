// This URL must match where Member A is running the backend
const API_URL = "http://127.0.0.1:8000"; 
async function sendMessage() {
    const inputField = document.getElementById("user-input");
    const modeSelect = document.getElementById("mode-select"); // Get the switch
    const chatContainer = document.getElementById("chat-container");
    
    const message = inputField.value.trim();
    const mode = modeSelect.value; // Get the selected mode ("constitution" or "bns")

    if (message === "") return;

    // Add User Message
    addMessage(message, "user-message");
    inputField.value = "";

    // Add Loading Animation
    const loadingId = addMessage('<span class="typing-indicator">Consulting Legal Archives...</span>', "bot-message");

    try {
        // SEND MODE TO BACKEND
        const response = await fetch(`http://127.0.0.1:8000/search?query=${encodeURIComponent(message)}&mode=${mode}`);
        const data = await response.json();

        // Remove loading
        const loadingMsg = document.getElementById(loadingId);
        if (loadingMsg) loadingMsg.remove();

        // Format and Show Bot Message
        // Convert **bold** markdown to HTML bold
        let formattedText = data.result.replace(/\*\*(.*?)\*\*/g, '<b>$1</b>');
        formattedText = formattedText.replace(/\n/g, '<br>'); // Handle newlines

        addMessage(formattedText, "bot-message");
        
        if (data.source) {
            addMessage(`<small style="color: #666; font-size: 0.8em;">📚 ${data.source}</small>`, "bot-message");
        }

    } catch (error) {
        console.error(error);
        const loadingMsg = document.getElementById(loadingId);
        if (loadingMsg) loadingMsg.remove();
        addMessage("⚠️ Connection Error. Ensure Backend is running.", "bot-message");
    }
}

function addMessage(text, className) {
    const chatContainer = document.getElementById("chat-container");
    const div = document.createElement("div");
    div.className = `message ${className}`;
    div.innerHTML = text; // Use innerHTML to render bold tags
    chatContainer.appendChild(div);
    chatContainer.scrollTop = chatContainer.scrollHeight;
    return div.id = "msg-" + Date.now();
}

// --- SPEECH TO TEXT FUNCTION ---
function startListening() {
    const micBtn = document.getElementById("mic-btn");
    const inputField = document.getElementById("user-input");

    if (!("webkitSpeechRecognition" in window || "SpeechRecognition" in window)) {
        alert("Your browser does not support Voice Search. Please use Google Chrome.");
        return;
    }

    const SpeechRecognition = window.SpeechRecognition || window.webkitSpeechRecognition;
    const recognition = new SpeechRecognition();

    recognition.lang = "en-IN"; 
    recognition.interimResults = false;

    recognition.onstart = function() {
        micBtn.classList.add("listening");
        inputField.placeholder = "Listening... (Check Mic Permission)";
    };

    recognition.onend = function() {
        micBtn.classList.remove("listening");
        inputField.placeholder = "Ask e.g., 'What is Article 21?'";
    };

    recognition.onresult = function(event) {
        const transcript = event.results[0][0].transcript;
        inputField.value = transcript;
        console.log("Heard:", transcript);
    };

    recognition.onerror = function(event) {
        console.error("Mic Error:", event.error); // <--- CHECK THIS IN CONSOLE
        
        if (event.error === 'not-allowed') {
            alert("Microphone access blocked. Please click the Lock icon 🔒 in the URL bar and Allow Microphone.");
        } else if (event.error === 'no-speech') {
            alert("No speech detected. Please speak closer to the mic.");
        } else {
            alert("Voice Error: " + event.error);
        }
    };

    recognition.start();
}