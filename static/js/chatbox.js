import API from './api.js';
import UI from './ui.js';

export default class Chatbox {
    constructor() {
        this.api = new API();
        this.ui = new UI();
    }

    // Method to initialize the chatbox event listeners
    initialize() {
        const sendButton = document.querySelector('button');
        sendButton.addEventListener('click', () => this.handleSendMessage());
    }

    // Method to handle sending a message
    handleSendMessage() {
        const messageInput = this.ui.getMessageInput();
        if (messageInput) {
            this.api.sendMessage(messageInput)
                .then(response => {
                    this.ui.displayMessage(response);
                    this.ui.clearMessageInput();
                })
                .catch(error => {
                    console.error("Error sending message:", error);
                });
        }
    }
}

// Initialize the chatbox when the page loads
document.addEventListener('DOMContentLoaded', () => {
    const chatbox = new Chatbox();
    chatbox.initialize();
});
