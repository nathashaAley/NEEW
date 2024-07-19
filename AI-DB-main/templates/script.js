// Chatbot functionality
const chatbotIcon = document.getElementById('chatbot-icon');
const chatbotInterface = document.getElementById('chatbot-interface');
const closeChatbotBtn = document.getElementById('close-chatbot');
const chatbotForm = document.getElementById('chatbot-form');
const chatbotInput = document.getElementById('chatbot-input');
const chatbotMessages = document.getElementById('chatbot-messages');

chatbotIcon.addEventListener('click', function() {
    chatbotInterface.style.display = 'block';
});

closeChatbotBtn.addEventListener('click', function() {
    chatbotInterface.style.display = 'none';
});

chatbotForm.addEventListener('submit', function(event) {
    event.preventDefault();
    const userMessage = chatbotInput.value;
    addMessage('user-message', userMessage);
    chatbotInput.value = '';

    // Simulate AI response (replace with actual AI integration)
    setTimeout(() => {
        const aiMessage = 'AI Response to: ' + userMessage;
        addMessage('ai-message', aiMessage);
    }, 1000);
});

function addMessage(className, message) {
    const messageElement = document.createElement('div');
    messageElement.className = className;
    messageElement.textContent = message;
    chatbotMessages.appendChild(messageElement);
    chatbotMessages.scrollTop = chatbotMessages.scrollHeight; // Auto-scroll to the bottom
}
