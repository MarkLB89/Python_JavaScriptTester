import os

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
    "torch"
]

# Install each package using pip
for package in packages:
    print(f"Installing {package}...")
    os.system(f"pip install {package}")

print("All packages installed successfully.")
