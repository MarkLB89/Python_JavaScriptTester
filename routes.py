#routes.py
from flask import Blueprint, jsonify, request, render_template, current_app
from pathlib import Path
from models import generate_answer
from models_image import detect_and_count_objects, generate_user_friendly_response, extract_text_from_image
from PIL import Image
import io

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

# Route to handle sending a message and retrieving the answer (original functionality)
@routes.route('/send_message', methods=['POST'])
def send_message():
    text_files_dir = Path(current_app.root_path) / 'text_files'

    message = request.form.get('message')
    selected_file = request.form.get('file')

    if not message:
        return jsonify({"error": "No message provided"}), 400

    if not selected_file:
        return jsonify({"error": "No file selected"}), 400

    try:
        # Load the content of the selected file
        file_path = text_files_dir / selected_file
        with open(file_path, 'r') as file:
            passage = file.read()

    except FileNotFoundError:
        return jsonify({"error": "File not found"}), 404
    except Exception as e:
        return jsonify({"error": str(e)}), 500

    # Use the generate_answer function to find the answer
    try:
        answer = generate_answer(message, passage)
        return jsonify({"question": message, "answer": answer})
    except Exception as e:
        return jsonify({"error": "Failed to generate an answer: " + str(e)}), 500

# Route to handle sending a message, image, or both
@routes.route('/process_input', methods=['POST'])
def process_input():
    message = request.form.get('message')
    file = request.files.get('file')

    if not message and not file:
        return jsonify({"error": "No message or image provided"}), 400

    response = {}

    # Process the message if it exists
    if message:
        response['question'] = message
        response['answer'] = f"Message received: {message}"

    # Process the image if it exists
    if file and file.filename != '':
        try:
            # Open the image and process it
            image = Image.open(io.BytesIO(file.read()))

            # Detect objects in the image
            class_counts = detect_and_count_objects(image)
            object_detection_response = generate_user_friendly_response(class_counts)
            response['object_detection'] = object_detection_response

            # Extract text from the image (if any)
            extracted_text = extract_text_from_image(image)
            if extracted_text:
                response['extracted_text'] = f"The text found in the image is: {extracted_text}"
            else:
                response['extracted_text'] = "No readable text was found in the image."

        except Exception as e:
            return jsonify({"error": str(e)}), 500

    return jsonify(response), 200
