export default class UI {
    constructor() {
        this.chatDisplay = document.getElementById('chat-display');
        this.messageInput = document.getElementById('message-input');
    }

    // Method to retrieve the user's message input
    getMessageInput() {
        return this.messageInput.value.trim();
    }

    // Method to display the message in the chatbox
    displayMessage(message) {
        this.chatDisplay.innerHTML += `<p>${message}</p>`;
    }

    // Method to clear the message input after sending
    clearMessageInput() {
        this.messageInput.value = '';
    }
}
