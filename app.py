from flask import Flask, render_template, request

app = Flask(__name__)

# Route to display the chatbox
@app.route('/')
def index():
    return render_template('index.html')

# Route to handle the message sending
@app.route('/send_message', methods=['POST'])
def send_message():
    message = request.form['message']
    
    # Process the message here (e.g., modify, log, respond)
    processed_message = f"You said: {message}"
    
    # Return the processed message to the frontend
    return processed_message

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0')
