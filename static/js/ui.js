// /workspaces/Python_JavaScriptTester/static/js/ui.js

export default class UI {
    constructor() {
        this.chatDisplay = document.getElementById('chat-display');
        this.messageInput = document.getElementById('message-input');
        this.fileSelect = document.getElementById('file-select');
        this.imagePreview = document.getElementById('image-preview'); // Image preview element
        this.imagePreviewContainer = document.querySelector('.image-preview-container'); // Container for image preview
        this.fileInput = document.getElementById('file-upload'); // File input element for image upload
        this.errorMessage = document.getElementById('error-message'); // Error message element
        this.errorText = document.getElementById('error-text'); // Error text span
        this.closeErrorButton = this.errorMessage.querySelector('.close-error'); // Close button for error
        this.loadingSpinner = document.getElementById('loading-spinner'); // Loading spinner element
        this.sendButton = document.querySelector('.send-button'); // Send button element

        // Bind the close button event
        if (this.closeErrorButton) {
            this.closeErrorButton.addEventListener('click', () => this.clearError());
        }
    }

    // Method to retrieve the user's message input
    getMessageInput() {
        return this.messageInput.value.trim();
    }

    // Method to retrieve the selected file (topic)
    getSelectedFile() {
        return this.fileSelect.value;
    }

    // Method to populate the file selector with available files
    populateFileSelector(files) {
        // Clear any existing options
        this.fileSelect.innerHTML = '<option value="">--Select a file--</option>';

        // Populate the select element with files from the server
        files.forEach(file => {
            const option = document.createElement('option');
            option.value = file;
            option.textContent = file;
            this.fileSelect.appendChild(option);
        });
    }

    // Method to display the message in the chatbox
    displayMessage(message) {
        const messageParagraph = document.createElement('p');
        messageParagraph.textContent = message;
        this.chatDisplay.appendChild(messageParagraph);
        // Scroll to the bottom of the chat display
        this.chatDisplay.scrollTop = this.chatDisplay.scrollHeight;
    }

    // Method to display the image and corresponding response in the chatbox
    displayImageAndResponse(imageURL, responseText) {
        // Create and append the image element
        const imgElement = document.createElement('img');
        imgElement.src = imageURL;
        imgElement.alt = "Uploaded Image";
        imgElement.classList.add('chat-image');
        this.chatDisplay.appendChild(imgElement);

        // Create and append the response text
        const responseParagraph = document.createElement('p');
        responseParagraph.textContent = `Bot: ${responseText}`;
        responseParagraph.classList.add('chat-response');
        this.chatDisplay.appendChild(responseParagraph);

        // Scroll to the bottom of the chat display
        this.chatDisplay.scrollTop = this.chatDisplay.scrollHeight;
    }

    // Method to clear the message input after sending
    clearMessageInput() {
        this.messageInput.value = '';
    }

    // Method to display the selected image for preview
    displayImagePreview(imageURL) {
        if (this.imagePreview) {
            this.imagePreview.src = imageURL;
            this.imagePreview.style.display = 'block'; // Show the image preview
        }

        if (this.imagePreviewContainer) {
            this.imagePreviewContainer.style.display = 'inline-block'; // Ensure the container is visible
        }
    }

    // Method to show the image preview container
    showImagePreview() {
        if (this.imagePreviewContainer) {
            this.imagePreviewContainer.style.display = 'inline-block';
        }
    }

    // Method to clear the image preview
    clearImagePreview() {
        if (this.imagePreview) {
            this.imagePreview.src = ''; // Clear the image source
            this.imagePreview.style.display = 'none'; // Hide the image preview
        }

        if (this.imagePreviewContainer) {
            this.imagePreviewContainer.style.display = 'none'; // Hide the container
        }

        // Clear the file input so it won't interfere with the next image upload
        if (this.fileInput) {
            this.fileInput.value = ''; // Reset the file input element
        }
    }

    // Method to display error messages
    displayError(message) {
        if (this.errorMessage) {
            this.errorText.textContent = message;
            this.errorMessage.style.display = 'block';
            // Automatically hide the error after 5 seconds
            setTimeout(() => this.clearError(), 5000);
        }
    }

    // Method to clear error messages
    clearError() {
        if (this.errorMessage) {
            this.errorText.textContent = '';
            this.errorMessage.style.display = 'none';
        }
    }

    // Method to show the loading spinner
    showLoading() {
        if (this.loadingSpinner) {
            this.loadingSpinner.style.display = 'flex';
        }
    }

    // Method to hide the loading spinner
    hideLoading() {
        if (this.loadingSpinner) {
            this.loadingSpinner.style.display = 'none';
        }
    }

    // Method to disable the send button
    disableSendButton() {
        if (this.sendButton) {
            this.sendButton.disabled = true;
            this.sendButton.classList.add('disabled'); // Optional: Add a class for styling
        }
    }

    // Method to enable the send button
    enableSendButton() {
        if (this.sendButton) {
            this.sendButton.disabled = false;
            this.sendButton.classList.remove('disabled'); // Optional: Remove the disabled styling
        }
    }

    // Method to get the chat display element
    getChatDisplay() {
        return this.chatDisplay;
    }
}
