import spacy
import json
from pathlib import Path

# Load Spacy model for named entity recognition (NER)
nlp = spacy.load("en_core_web_sm")

# Directory where the text files and JSON files are located
text_files_dir = Path(__file__).parent / 'text_files'

# Check if the text_files_dir exists
if not text_files_dir.exists():
    print(f"Directory {text_files_dir} does not exist. Please create it.")
else:
    print(f"Directory found: {text_files_dir}")

# List files in the directory
files = list(text_files_dir.glob("*.txt"))
if not files:
    print("No .txt files found in the directory.")
else:
    print(f"Found the following .txt files: {[f.name for f in files]}")

# Load the passage from a .txt file in the text_files directory
def load_text_file(filename):
    file_path = text_files_dir / filename
    with open(file_path, 'r', encoding='utf-8') as file:
        return file.read()

# Save extracted entities to a JSON file
def save_entities_to_json(entities, json_filename):
    json_path = text_files_dir / json_filename
    
    try:
        with open(json_path, 'w') as f:
            json.dump(entities, f, indent=4)
        print(f"Entities extracted and saved to {json_filename}")
    except Exception as e:
        print(f"Failed to save entities to {json_filename}: {e}")

# Load entities from the corresponding JSON file if it exists
def load_entities_from_json(json_filename):
    json_path = text_files_dir / json_filename
    if json_path.exists():
        with open(json_path, 'r') as f:
            return json.load(f)
    return None

# Function to extract named entities using Spacy
def extract_entities(text):
    doc = nlp(text)
    entities = []
    for ent in doc.ents:
        entities.append({
            "text": ent.text,
            "label": ent.label_,
            "start_char": ent.start_char,
            "end_char": ent.end_char
        })
    return entities

# Automatically generate the JSON file name based on the .txt file
def get_json_filename(txt_filename):
    return txt_filename.replace('.txt', '_Extraction.json')

# Extract entities from the selected file and save/update the corresponding JSON file
def extract_and_save_entities(txt_filename):
    print(f"Processing file: {txt_filename}")
    # Load the text from the selected .txt file
    text = load_text_file(txt_filename)
    
    # Automatically determine the corresponding JSON file name
    json_filename = get_json_filename(txt_filename)
    
    # Try to load entities from the JSON file, or extract and save them if the JSON doesn't exist
    entities = load_entities_from_json(json_filename)
    if not entities:
        print(f"Extracting entities for {txt_filename}...")
        entities = extract_entities(text)
        
        # Check if entities were actually extracted
        if entities:
            print(f"Entities extracted: {entities}")
            save_entities_to_json(entities, json_filename)
        else:
            print(f"No entities were extracted from {txt_filename}.")
    else:
        print(f"Entities already exist for {txt_filename}. File: {json_filename}")

# Processing all .txt files in the directory
for txt_file in files:
    extract_and_save_entities(txt_file.name)
