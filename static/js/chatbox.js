import API from './api.js';
import UI from './ui.js';

export default class Chatbox {
    constructor() {
        this.api = new API();
        this.ui = new UI();
    }

    // Method to initialize the chatbox event listeners and load files
    initialize() {
        const sendButton = document.querySelector('button');
        const fileSelect = document.getElementById('file-select');

        sendButton.addEventListener('click', () => this.handleSendMessage());

        // Fetch available files from the backend and populate the select element
        this.api.getFiles()
            .then(files => {
                this.ui.populateFileSelector(files);
            })
            .catch(error => console.error("Error fetching files:", error));
    }

    // Method to handle sending a message
    handleSendMessage() {
        const messageInput = this.ui.getMessageInput();
        const selectedFile = this.ui.getSelectedFile();

        // Debugging: Log the message and file to ensure they are correctly captured
        console.log("Message Input:", messageInput);
        console.log("Selected File:", selectedFile);

        if (messageInput && selectedFile) {
            this.api.sendMessage(messageInput, selectedFile)
                .then(response => {
                    console.log("Response from server:", response);  // Debugging: Log the server response

                    // Ensure the question and answer are correctly captured from the response
                    const question = response.question ? response.question : "Unknown question";
                    const answer = response.answer ? response.answer : "I couldn't find an answer.";

                    // Display the question and answer in the chatbox
                    this.ui.displayMessage(`You: ${question}`);
                    this.ui.displayMessage(`Bot: ${answer}`);
                    this.ui.clearMessageInput();
                })
                .catch(error => {
                    console.error("Error sending message:", error);
                });
        } else {
            alert('Please enter a message and select a topic.');
        }
    }
}

// Initialize the chatbox when the page loads
document.addEventListener('DOMContentLoaded', () => {
    const chatbox = new Chatbox();
    chatbox.initialize();
});
