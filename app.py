from flask import Flask, render_template, request
from models import generate_answer  # Import the BERT answer generation function

app = Flask(__name__)

# Route to display the chatbox
@app.route('/')
def index():
    return render_template('index.html')

# Route to handle the question and answer functionality
@app.route('/send_message', methods=['POST'])
def send_message():
    question = request.form['message']  # The message is treated as the question
    
    # Use the BERT model to generate an answer
    answer = generate_answer(question)
    
    # Return the processed answer to the frontend
    return answer

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0')
