# /workspaces/Python_JavaScriptTester/models_image.py

import tensorflow as tf  # TensorFlow for building and running models
import tensorflow_hub as hub  # TensorFlow Hub for pre-trained models
import numpy as np  # Numpy for numerical operations
from PIL import Image, ImageEnhance, ImageFilter  # Pillow for image processing
import cv2  # OpenCV for advanced image processing
import inflect  # Inflect for pluralization and linguistic processing
import easyocr  # EasyOCR for text extraction
from spellchecker import SpellChecker  # SpellChecker for correcting text

# Initialize the object detection model once to avoid reloading
# Loading the pre-trained SSD MobileNetV2 model from TensorFlow Hub
MODEL_URL = 'https://tfhub.dev/tensorflow/ssd_mobilenet_v2/fpnlite_320x320/1'
model = hub.load(MODEL_URL)

# Define the object classes for the COCO dataset
COCO_CLASSES = [
    None,  # Placeholder for 0 index
    "person", "bicycle", "car", "motorcycle", "airplane", "bus", "train",
    "truck", "boat", "traffic light", "fire hydrant", "stop sign",
    "parking meter", "bench", "bird", "cat", "dog", "horse", "sheep",
    "cow", "elephant", "bear", "zebra", "giraffe", "backpack", "umbrella",
    "handbag", "tie", "suitcase", "frisbee", "skis", "snowboard",
    "sports ball", "kite", "baseball bat", "baseball glove", "skateboard",
    "surfboard", "tennis racket", "bottle", "wine glass", "cup", "fork",
    "knife", "spoon", "bowl", "banana", "apple", "sandwich", "orange",
    "broccoli", "carrot", "hot dog", "pizza", "donut", "cake", "chair",
    "couch", "potted plant", "bed", "dining table", "toilet", "tv",
    "laptop", "mouse", "remote", "keyboard", "cell phone", "microwave",
    "oven", "toaster", "sink", "refrigerator", "book", "clock", "vase",
    "scissors", "teddy bear", "hair drier", "toothbrush"
]

# Initialize the inflect engine for pluralization
inflect_engine = inflect.engine()

# Initialize the spell checker
spell = SpellChecker()

# Initialize the EasyOCR reader once to avoid reloading
# Limiting to English language; add more languages if needed
reader = easyocr.Reader(['en'], gpu=True)  # Set gpu=False if GPU is not available

def detect_and_count_objects(image):
    """
    Detects objects in an image and counts occurrences of each class.

    Parameters:
        image (PIL.Image.Image): The input image in PIL format.

    Returns:
        dict: A dictionary with class names as keys and their counts as values.
    """
    # Ensure the image is in RGB format
    if image.mode != 'RGB':
        image = image.convert('RGB')

    # Convert the image into a tensor
    image_np = np.array(image)
    input_tensor = tf.convert_to_tensor(image_np)
    input_tensor = input_tensor[tf.newaxis, ...]  # Add batch dimension

    # Run the object detection model
    detections = model(input_tensor)

    # Extract detection classes and scores
    detection_classes = detections['detection_classes'][0].numpy().astype(int)
    detection_scores = detections['detection_scores'][0].numpy()

    # Filter results by confidence threshold
    threshold = 0.5
    detected_classes = [
        detection_classes[i]
        for i in range(len(detection_classes)) if detection_scores[i] > threshold
    ]

    # Count the number of occurrences for each class
    class_counts = {}
    for class_id in detected_classes:
        if 1 <= class_id < len(COCO_CLASSES):
            class_name = COCO_CLASSES[class_id].capitalize()
        else:
            class_name = "Unknown"

        if class_name in class_counts:
            class_counts[class_name] += 1
        else:
            class_counts[class_name] = 1

    return class_counts

def generate_user_friendly_response(class_counts):
    """
    Generates a user-friendly response based on detected object counts.

    Parameters:
        class_counts (dict): A dictionary with class names as keys and their counts as values.

    Returns:
        str: A user-friendly sentence describing the detected objects.
    """
    # Handle edge case: no objects detected
    if not class_counts:
        return "No recognizable objects were found in the image."

    # Special case: more than 3 people
    if "Person" in class_counts and class_counts["Person"] > 3:
        return "There is a gathering of people in the image."

    # Create a list of phrases for each detected class
    phrases = []
    for class_name, count in class_counts.items():
        # Pluralize the class name appropriately
        if count == 1:
            phrase = f"{count} {class_name.lower()}"
        else:
            plural_class_name = inflect_engine.plural(class_name.lower(), count)
            phrase = f"{count} {plural_class_name}"
        phrases.append(phrase)

    # Handle grammar for singular vs. plural cases
    if len(phrases) == 1:
        response = f"There is {phrases[0]} in the image."
    elif len(phrases) == 2:
        response = f"There are {phrases[0]} and {phrases[1]} in the image."
    else:
        response = f"There are {', '.join(phrases[:-1])}, and {phrases[-1]} in the image."

    return response

def preprocess_image(image):
    """
    Preprocesses the image to enhance text detection.

    Parameters:
        image (PIL.Image.Image): The input image in PIL format.

    Returns:
        numpy.ndarray: The preprocessed image suitable for OCR.
    """
    # Ensure the image is in RGB format
    if image.mode != 'RGB':
        image = image.convert('RGB')

    # Convert the image to grayscale
    gray_image = image.convert('L')

    # Enhance the contrast
    enhancer = ImageEnhance.Contrast(gray_image)
    enhanced_image = enhancer.enhance(2)  # Factor >1 increases contrast

    # Apply median filtering to reduce noise
    filtered_image = enhanced_image.filter(ImageFilter.MedianFilter())

    # Convert the PIL image to a NumPy array
    open_cv_image = np.array(filtered_image)

    # Ensure the image is single-channel (grayscale)
    if len(open_cv_image.shape) == 3:
        open_cv_image = cv2.cvtColor(open_cv_image, cv2.COLOR_BGR2GRAY)

    # Apply thresholding to binarize the image
    _, thresholded_image = cv2.threshold(open_cv_image, 150, 255, cv2.THRESH_BINARY + cv2.THRESH_OTSU)

    return thresholded_image

def clean_text(text):
    """
    Cleans and corrects the extracted text.

    Parameters:
        text (str): The raw extracted text.

    Returns:
        str: The cleaned and corrected text.
    """
    # Split text into words
    words = text.split()

    # Correct misspelled words
    corrected_words = [spell.correction(word) for word in words]

    # Filter out nonsense words or single characters
    meaningful_words = [word for word in corrected_words if len(word) > 1]

    # Join the words back into a sentence
    cleaned_text = ' '.join(meaningful_words)

    return cleaned_text.lower()  # Convert the cleaned text to lowercase

def extract_text_from_image(image):
    """
    Extracts and cleans text from an image using OCR.

    Parameters:
        image (PIL.Image.Image): The input image in PIL format.

    Returns:
        str: The cleaned extracted text.
    """
    # Preprocess the image before OCR
    processed_image = preprocess_image(image)

    # Perform OCR on the preprocessed image
    try:
        result = reader.readtext(processed_image, detail=0)
    except Exception as e:
        print(f"OCR Error: {e}")
        return "Error in text extraction."

    # Combine the results into a single string
    raw_text = ' '.join(result).strip()

    # Clean up the detected text
    cleaned_text = clean_text(raw_text)

    return cleaned_text
