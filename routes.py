from flask import Blueprint, jsonify, request, render_template, current_app
from pathlib import Path
from models import generate_answer

# Create a Blueprint
routes = Blueprint('routes', __name__)

# Route for the home page
@routes.route('/')
def index():
    return render_template('index.html')

# Route to get available text files
@routes.route('/get_files', methods=['GET'])
def get_files():
    text_files_dir = Path(current_app.root_path) / 'text_files'

    # Get a list of all text files in the directory
    try:
        files = [file.name for file in text_files_dir.glob('*.txt')]
        return jsonify(files)
    except Exception as e:
        return jsonify({"error": str(e)}), 500

# Route to handle sending a message and retrieving the answer
@routes.route('/send_message', methods=['POST'])
def send_message():
    text_files_dir = Path(current_app.root_path) / 'text_files'

    message = request.form['message']
    selected_file = request.form['file']

    # Debugging: Log the message and file received
    print(f"Received message: {message}")
    print(f"Selected file: {selected_file}")

    try:
        # Load the content of the selected file
        file_path = text_files_dir / selected_file
        print(f"File path: {file_path}")  # Log file path

        with open(file_path, 'r') as file:
            passage = file.read()
        #print(f"File content (passage): {passage}")  # Log the content of the file

    except FileNotFoundError:
        print("Error: File not found")  # Log file not found error
        return jsonify({"error": "File not found"}), 404
    except Exception as e:
        print(f"Error reading file: {str(e)}")  # Log any other errors
        return jsonify({"error": str(e)}), 500

    # Use the generate_answer function to find the answer
    try:
        answer = generate_answer(message, passage)
        print(f"Generated answer: {answer}")  # Log the generated answer
        return jsonify({"question": message, "answer": answer})
    except Exception as e:
        print(f"Error generating answer: {str(e)}")  # Log error during answer generation
        return jsonify({"error": "Failed to generate an answer: " + str(e)}), 500
