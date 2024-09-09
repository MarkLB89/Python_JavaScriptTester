export default class API {
    constructor() {}

    // Method to send a message and the selected file to the Flask backend
    async sendMessage(message, selectedFile) {
        const response = await fetch('/send_message', {
            method: 'POST',
            headers: { 'Content-Type': 'application/x-www-form-urlencoded' },
            body: `message=${encodeURIComponent(message)}&file=${encodeURIComponent(selectedFile)}`
        });

        if (!response.ok) {
            throw new Error(`HTTP error! status: ${response.status}`);
        }

        const responseData = await response.json();  // Parse the response as JSON
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
