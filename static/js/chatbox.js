// /workspaces/Python_JavaScriptTester/static/js/chatbox.js

import API from './api.js';
import UI from './ui.js';

export default class Chatbox {
    constructor() {
        this.api = new API();
        this.ui = new UI();
        this.imageFile = null; // Store the selected image file
        this.imageURL = null; // Store the Object URL of the uploaded image
    }

    /**
     * Initializes the chatbox by setting up event listeners and loading available files.
     */
    initialize() {
        const sendButton = document.querySelector('.send-button'); // Ensure the button has the correct class
        const fileInput = document.getElementById('file-upload');  // File input for image upload
        const removePreviewButton = document.querySelector('.remove-preview');  // Red X button for image removal

        sendButton.addEventListener('click', () => this.handleSendMessage());
        fileInput.addEventListener('change', (event) => this.handleFileSelection(event));
        removePreviewButton.addEventListener('click', () => this.removeImagePreview());

        // Fetch available files from the backend and populate the select element
        this.api.getFiles()
            .then(files => {
                this.ui.populateFileSelector(files);
            })
            .catch(error => {
                console.error("Error fetching files:", error);
                this.ui.displayError("Failed to load available files.");
            });
    }

    /**
     * Handles the selection of an image file, displaying a preview.
     * @param {Event} event - The file input change event.
     */
    handleFileSelection(event) {
        const file = event.target.files[0];
        if (file && file.type.startsWith('image/')) {
            this.imageFile = file; // Store the selected image file
            this.imageURL = URL.createObjectURL(file); // Create a temporary URL for the image
            this.ui.displayImagePreview(this.imageURL); // Display image preview
            this.ui.showImagePreview(); // Ensure the preview container is visible
        } else {
            this.ui.displayError('Please select a valid image file.');
        }
    }

    /**
     * Removes the currently selected image, clearing the preview and resetting the input.
     */
    removeImagePreview() {
        this.imageFile = null; // Clear the image file from memory
        if (this.imageURL) {
            URL.revokeObjectURL(this.imageURL); // Release the Object URL
            this.imageURL = null;
        }
        this.ui.clearImagePreview(); // Clear image preview from UI
        document.getElementById('file-upload').value = ''; // Clear the file input
    }

    /**
     * Handles sending a message, selected file (topic), and optionally an image to the backend.
     */
    async handleSendMessage() {
        const messageInput = this.ui.getMessageInput();
        const selectedFile = this.ui.getSelectedFile();

        // Debugging: Log the message and file to ensure they are correctly captured
        console.log("Message Input:", messageInput);
        console.log("Selected File:", selectedFile);
        console.log("Image File:", this.imageFile);

        // Show loading spinner and disable send button
        this.ui.showLoading();
        this.ui.disableSendButton();

        try {
            let response;

            // Determine the type of request based on user inputs
            if (messageInput && selectedFile && this.imageFile) {
                // Case 3: Both message and image
                response = await this.api.sendMessageWithImage(messageInput, selectedFile, this.imageFile);
            } else if (messageInput && selectedFile) {
                // Case 1: Message with selected file, without image
                response = await this.api.sendMessage(messageInput, selectedFile);
            } else if (this.imageFile) {
                // Case 2: Image without a message
                response = await this.api.sendImage(this.imageFile);
            } else if (messageInput) {
                // Case 4: Only message, without selecting a file
                this.ui.displayError('Please select a file (topic) for your message.');
                return;
            } else {
                // Case 5: Neither message nor image
                this.ui.displayError('Please enter a message, select a topic, or upload an image.');
                return;
            }

            // Handle the server response
            this.handleResponse(response);
        } catch (error) {
            console.error("Error sending request:", error);
            this.ui.displayError("An error occurred while processing your request. Please try again.");
        } finally {
            // Hide loading spinner and enable send button
            this.ui.hideLoading();
            this.ui.enableSendButton();
        }
    }

    /**
     * Processes the server response and displays the results in the chatbox.
     * @param {Object} response - The JSON response from the backend.
     */
    handleResponse(response) {
        // Debugging: Log the response to inspect its structure
        console.log("Server Response:", response);

        // Display user's message and bot's answer if available
        if (response.question && response.answer) {
            this.ui.displayMessage(`You: ${response.question}`);
            this.ui.displayMessage(`Bot: ${response.answer}`);
        } else if (response.question) {
            this.ui.displayMessage(`You: ${response.question}`);
        } else if (response.answer) {
            this.ui.displayMessage(`Bot: ${response.answer}`);
        }

        /* Display object detection results if available
        if (response.object_detection) {
            this.ui.displayMessage(`Bot: ${response.object_detection}`);
        }

        // Display extracted text if available
        if (response.extracted_text) {
            this.ui.displayMessage(`Bot: ${response.extracted_text}`);
        }*/

        // Optionally, display the image alongside the messages
        if (response.object_detection || response.extracted_text) {
            if (this.imageURL) {
                // Create an image element
                const imgElement = document.createElement('img');
                imgElement.src = this.imageURL;
                imgElement.alt = "Processed Image";
                imgElement.classList.add('chat-image');

                // Append the image to the chat display
                this.ui.getChatDisplay().appendChild(imgElement);

                // Optionally, append responses below the image
                if (response.object_detection) {
                    const detectionResponse = document.createElement('p');
                    detectionResponse.textContent = `Bot: ${response.object_detection}`;
                    detectionResponse.classList.add('chat-response');
                    this.ui.getChatDisplay().appendChild(detectionResponse);
                }

                if (response.extracted_text) {
                    const extractedText = document.createElement('p');
                    extractedText.textContent = `Bot: ${response.extracted_text}`;
                    extractedText.classList.add('chat-response');
                    this.ui.getChatDisplay().appendChild(extractedText);
                }

                // Scroll to the bottom of the chat display
                this.ui.getChatDisplay().scrollTop = this.ui.getChatDisplay().scrollHeight;

                // Revoke the Object URL to free memory
                imgElement.onload = () => {
                    URL.revokeObjectURL(this.imageURL);
                };
                this.imageURL = null; // Reset the imageURL after revoking
            }
        }

        // Clear the message input field
        this.ui.clearMessageInput();

        // Clear the image preview and file input
        this.imageFile = null;
        this.ui.clearImagePreview();
        document.getElementById('file-upload').value = ''; // Clear the file input after sending the message
    }
}

// Initialize the chatbox when the page loads
document.addEventListener('DOMContentLoaded', () => {
    const chatbox = new Chatbox();
    chatbox.initialize();
});
