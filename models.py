#models.py
from transformers import BertTokenizer, TFBertForQuestionAnswering
import tensorflow as tf
import json
from pathlib import Path

# Load the BERT model and tokenizer
print("Loading the BERT large model...")
model_name = "bert-large-uncased-whole-word-masking-finetuned-squad"
model = TFBertForQuestionAnswering.from_pretrained(model_name)
tokenizer = BertTokenizer.from_pretrained(model_name)
print("BERT model and tokenizer successfully loaded.")

# Directory where the text files and JSON files are located
text_files_dir = Path(__file__).parent / 'text_files'

# Load entities from the JSON file
def load_entities_from_json(json_filename):
    json_path = text_files_dir / json_filename
    if json_path.exists():
        with open(json_path, 'r') as f:
            return json.load(f)
    return None

# Load the passage from a .txt file in the text_files directory
def load_text_file(filename):
    file_path = text_files_dir / filename
    with open(file_path, 'r', encoding='utf-8') as file:
        return file.read()

# Function to generate answers using the BERT model
def generate_answer(question, passage):
    # Print question and passage for debugging
    print(f"Question: {question}")
    #print(f"Passage: {passage}")

    inputs = tokenizer(
        question,
        passage,
        return_tensors='tf',
        truncation=True,
        padding=True,
        max_length=512
    )

    outputs = model(inputs)
    start_logits = outputs.start_logits
    end_logits = outputs.end_logits

    start_position = tf.argmax(start_logits, axis=-1).numpy()[0]
    end_position = tf.argmax(end_logits, axis=-1).numpy()[0] + 1

    answer_tokens = inputs['input_ids'][0][start_position:end_position]
    answer = tokenizer.decode(answer_tokens)

    # Print answer tokens and decoded answer for debugging
    print(f"Answer tokens: {answer_tokens}")
    print(f"Answer: {answer}")

    # Remove [SEP] token from the answer
    answer = answer.replace("[SEP]", "").strip()

    # Remove the question from the answer if necessary
    if answer.lower().startswith(question.lower()):
        answer = answer[len(question):].strip()

    # Ensure a proper sentence is returned
    if ',,' in answer:
        response = answer.split(',,')[0].strip() + ','
    elif ',' in answer:
        response = answer.split(',')[0].strip() + ','
    else:
        response = answer.split('.')[0].strip() + '.'

    # If the answer is too short, prompt the user to rephrase
    if len(response.strip()) <= 1:
        return "I couldn't find an answer for your question. Can you please rephrase?"

    return response

# Function to use entities to find the relevant part of the text and answer the question
def process_question_with_entities(txt_filename, question):
    # Load the corresponding JSON file for entities
    json_filename = txt_filename.replace('.txt', '_Extraction.json')
    entities = load_entities_from_json(json_filename)

    # If no entities exist, return an error
    if not entities:
        return "No entities extracted for this file."

    # Load the original text file
    text = load_text_file(txt_filename)

    # Search for relevant entities in the question
    for entity in entities:
        if entity['text'].lower() in question.lower():
            # Debug: Print the keyword (entity) found in the question
            print(f"Matched entity found in question: {entity['text']}")

            # If entity is found in the question, extract a larger part of the text for more context
            start_index = text.lower().find(entity['text'].lower())
            # Extract the next sentence or paragraph
            end_index = text.find('.', start_index) + 100  # Extend the context by 100 characters after the period

            # Ensure valid indices
            if end_index == -1:
                end_index = len(text)
            passage = text[start_index:end_index]

            # Print extracted passage for debugging
            print(f"Extracted passage: {passage}")

            # Generate the answer using the BERT model
            answer = generate_answer(question, passage)
            return answer

    # If no relevant entity is found in the question, prompt the user to rephrase
    return "Can you please rephrase the question or be more specific?"
