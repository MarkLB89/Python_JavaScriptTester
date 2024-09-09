export default class API {
    constructor() {}

    // Method to send a message to the Flask backend
    async sendMessage(message) {
        const response = await fetch('/send_message', {
            method: 'POST',
            headers: { 'Content-Type': 'application/x-www-form-urlencoded' },
            body: `message=${encodeURIComponent(message)}`
        });

        if (!response.ok) {
            throw new Error(`HTTP error! status: ${response.status}`);
        }

        const responseText = await response.text();
        return responseText;
    }
}
