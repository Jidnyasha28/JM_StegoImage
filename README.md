# JM_StegoImage
JM_StegoImage is a project that securely embeds secret messages within images by combining robust encryption with advanced steganography techniques. By encrypting a secret message and then hiding it within the least significant bits of an image, the project provides an extra layer of security for sensitive data. The project also includes a Flask-based web interface that makes it easy for users to hide and extract messages.

Table of Contents
Overview
Features
Technologies Used
Installation
Usage
Future Scope
Contact

Overview
JM_StegoImage addresses the need for secure data transmission by integrating encryption and steganography. The project encrypts the user's secret message using Python's Cryptography (Fernet) library before embedding it into a cover image using an LSB (Least Significant Bit) technique. A web interface built with Flask and Bootstrap offers a user-friendly way to hide and extract secret messages, ensuring that even if hidden data is discovered, it remains protected.

Most Useful when taken PNG Images.

Features
Dual-layer Security: Encrypts the message using secure Fernet encryption before embedding it into an image.

Robust Steganography: Uses a header and stop marker system to maintain data integrity during extraction.

User-friendly Web Interface: Built using Flask, Bootstrap, HTML, and CSS for an attractive and responsive design.

Versatility: Suitable for educational, research, and practical applications in digital security and watermarking.

All Rights Reserved: The project is not open-source unless explicitly licensed; all rights are reserved by the author.


Technologies Used

Programming Language: Python

Libraries:
OpenCV for image processing
NumPy for numerical operations
Cryptography (Fernet) for encryption and decryption

Web Framework: Flask

Front-End: HTML, CSS, JavaScript, Bootstrap, Google Fonts

Installation

Clone the Repository:

git clone https://github.com/Jidnyasha28/JM_StegoImage.git

cd JM_StegoImage

Create and Activate a Virtual Environment (optional but recommended):

python -m venv venv

# On Windows:
venv\Scripts\activate

# On macOS/Linux:
source venv/bin/activate

Install Required Packages:

pip install flask opencv-python numpy cryptography
Set Environment Variables (Optional):

For production, you may set your Flask secret key:

Usage
Run the Flask Application:
python app.py

Access the Web Interface:
Open your browser and navigate to http://127.0.0.1:5000.

Hide Data:
Go to the "Hide Data" tab.
Upload a cover image and enter your secret message.
Click "Hide Data" to generate a stego image, which you can then download.

Extract Data:
Switch to the "Extract Data" tab.
Upload the stego image.
Click "Extract Data" to display the hidden secret message.


Future Scope
AI-Based Detection Prevention: Integrate adversarial noise techniques to further protect against steganalysis.

Mobile Application: Develop a cross-platform mobile app for on-the-go data hiding and extraction.

Enhanced Encryption: Experiment with more advanced cryptographic algorithms.

User Customization: Offer options for different cover images, encryption settings, and steganographic techniques.

Contact
For any questions or suggestions, please contact:

Your Name
Email: mangelajidu@gmail.com

