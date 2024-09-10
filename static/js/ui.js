export default class UI {
    constructor() {
        this.chatDisplay = document.getElementById('chat-display');
        this.messageInput = document.getElementById('message-input');
        this.fileSelect = document.getElementById('file-select');
        this.imagePreview = document.getElementById('image-preview'); // Image preview element
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
    }

    // Method to clear the message input after sending
    clearMessageInput() {
        this.messageInput.value = '';
    }

    // Optional method to reset the file selector
    clearFileSelector() {
        this.fileSelect.selectedIndex = 0;
    }

    // Method to display the selected image for preview
    displayImagePreview(imageURL) {
        if (this.imagePreview) {
            this.imagePreview.src = imageURL;
            this.imagePreview.style.display = 'block'; // Show the image preview
        }
    }

    // Method to clear the image preview
    clearImagePreview() {
        if (this.imagePreview) {
            this.imagePreview.src = ''; // Clear the image source
            this.imagePreview.style.display = 'none'; // Hide the image preview
        }
    }
}
