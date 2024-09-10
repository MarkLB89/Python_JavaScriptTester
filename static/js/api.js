// /workspaces/Python_JavaScriptTester/static/js/api.js
export default class API {
    constructor() {}

    // Method to send a message to the Flask backend
    async sendMessage(message, selectedFile = null) {
        const response = await fetch('/send_message', {
            method: 'POST',
            headers: { 'Content-Type': 'application/x-www-form-urlencoded' },
            body: `message=${encodeURIComponent(message)}&file=${encodeURIComponent(selectedFile || '')}`
        });

        if (!response.ok) {
            throw new Error(`HTTP error! status: ${response.status}`);
        }

        const responseData = await response.json();  // Parse the response as JSON
        return responseData;
    }

    // Method to send an image with a message
    async sendMessageWithImage(message, imageFile) {
        const formData = new FormData();

        formData.append('message', message); // Include the message
        formData.append('file', imageFile);  // Include the image

        const response = await fetch('/process_input', {
            method: 'POST',
            body: formData
        });

        if (!response.ok) {
            throw new Error(`HTTP error! status: ${response.status}`);
        }

        const responseData = await response.json();
        return responseData;
    }

    // Method to send just an image without a message
    async sendImage(imageFile) {
        const formData = new FormData();
        formData.append('file', imageFile);

        const response = await fetch('/process_input', {
            method: 'POST',
            body: formData
        });

        if (!response.ok) {
            throw new Error(`HTTP error! status: ${response.status}`);
        }

        const responseData = await response.json();
        return responseData;
    }

    // Method to retrieve the list of files from the Flask backend
    async getFiles() {
        const response = await fetch('/get_files', {
            method: 'GET'
        });

        if (!response.ok) {
            throw new Error(`HTTP error! status: ${response.status}`);
        }

        const files = await response.json();  // Parse the response as JSON
        return files;
    }
}
