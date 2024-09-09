import os
import subprocess

# List of packages to install
packages = [
    "tensorflow",
    "Pillow",
    "numpy",
    "tensorflow-hub",
    "opencv-python-headless",
    "inflect",
    "easyocr",
    "pyspellchecker",
    "transformers",
    "torch",
    "flask",
    "spacy"
]

# Function to install a package using pip
def install_package(package):
    try:
        print(f"Installing {package}...")
        result = subprocess.run(f"pip install {package}", shell=True, check=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        print(result.stdout.decode('utf-8'))  # Output from pip
        print(f"{package} installed successfully.")
    except subprocess.CalledProcessError as e:
        print(f"Error installing {package}: {e.stderr.decode('utf-8')}")

# Install each package
for package in packages:
    install_package(package)

# Special case for spaCy model installation
try:
    print("Downloading spaCy language model 'en_core_web_sm'...")
    result = subprocess.run("python -m spacy download en_core_web_sm", shell=True, check=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    print(result.stdout.decode('utf-8'))
    print("spaCy model 'en_core_web_sm' installed successfully.")
except subprocess.CalledProcessError as e:
    print(f"Error downloading spaCy model: {e.stderr.decode('utf-8')}")

print("All packages processed.")
