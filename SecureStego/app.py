import os
import cv2
import numpy as np
from flask import Flask, render_template, request, redirect, send_file, flash
from cryptography.fernet import Fernet
from werkzeug.utils import secure_filename
import io

# ----------------- Steganography functions -----------------

def generate_key():
    if not os.path.exists("secret.key"):
        key = Fernet.generate_key()
        with open("secret.key", "wb") as key_file:
            key_file.write(key)
    return load_key()  # Always load the existing key

def load_key():
    if not os.path.exists("secret.key"):
        generate_key()  # Ensure key is created before loading
    return open("secret.key", "rb").read()

def encrypt_message(message, key):
    cipher = Fernet(key)
    return cipher.encrypt(message.encode())

def decrypt_message(encrypted_message, key):
    cipher = Fernet(key)
    return cipher.decrypt(encrypted_message).decode()

def message_to_binary(message):
    return ''.join(format(byte, '08b') for byte in message)

def binary_to_message(binary_data):
    if len(binary_data) % 8 != 0:
        binary_data = binary_data[:-(len(binary_data) % 8)]
    byte_data = [binary_data[i:i+8] for i in range(0, len(binary_data), 8)]
    try:
        return bytes([int(byte, 2) for byte in byte_data])
    except ValueError:
        print("Error: Invalid binary-to-byte conversion. Data may be corrupted.")
        return b""

def hide_data(image_path, secret_message, output_path):
    image = cv2.imread(image_path)
    if image is None:
        return "Error: Image not found."
    
    key = load_key()
    encrypted_message = encrypt_message(secret_message, key)
    message_binary = message_to_binary(encrypted_message)
    
    message_bit_length = format(len(message_binary), '032b')
    STOP_MARKER = "1111111111111110"
    binary_message = message_bit_length + message_binary + STOP_MARKER
    
    total_bits = len(binary_message)
    total_bits_header = format(total_bits, '032b')
    embedded_data = total_bits_header + binary_message
    
    data_index = 0
    height, width, channels = image.shape
    
    for row in range(height):
        for col in range(width):
            for channel in range(channels):
                if data_index < len(embedded_data):
                    bit_value = int(embedded_data[data_index])
                    pixel_value = int(image[row, col, channel]) & ~1
                    image[row, col, channel] = np.clip(pixel_value | bit_value, 0, 255)
                    data_index += 1
                else:
                    break
            if data_index >= len(embedded_data):
                break
        if data_index >= len(embedded_data):
            break

    cv2.imwrite(output_path, image)
    return "Data hidden successfully!"

def extract_data(image_path):
    image = cv2.imread(image_path)
    if image is None:
        return "Error: Image not found."
    
    key = load_key()
    flat_bits = []
    height, width, channels = image.shape
    for row in range(height):
        for col in range(width):
            for channel in range(channels):
                flat_bits.append(str(image[row, col, channel] & 1))
    binary_data = ''.join(flat_bits)
    
    if len(binary_data) < 32:
        return "Error: Not enough data."
    total_bits = int(binary_data[:32], 2)
    if len(binary_data) < 32 + total_bits:
        return "Error: Not enough embedded data."
    embedded_data = binary_data[32:32+total_bits]
    
    try:
        header = embedded_data[:32]
        message_bit_length = int(header, 2)
        expected_total = 32 + message_bit_length + 16
        if expected_total != len(embedded_data):
            return "Error: Embedded data length does not match expected format. Possible corruption."
    except ValueError:
        return "Error: Failed to interpret message length. Possible corruption."
    
    message_bits = embedded_data[32:32+message_bit_length]
    stop_marker_extracted = embedded_data[32+message_bit_length:expected_total]
    STOP_MARKER = "1111111111111110"
    if stop_marker_extracted != STOP_MARKER:
        return "Error: Stop marker does not match. Possible corruption."
    
    encrypted_message = binary_to_message(message_bits)
    expected_length = message_bit_length // 8
    if len(encrypted_message) != expected_length:
        return f"Warning: Expected {expected_length} bytes, but got {len(encrypted_message)} bytes."
    
    try:
        decrypted_message = decrypt_message(encrypted_message, key)
        return f"Extracted Message: {decrypted_message}"
    except Exception as e:
        return "Error decrypting message. Possible incorrect key."

# ----------------- Flask Web Application -----------------

app = Flask(__name__)
app.secret_key = os.environ.get('FLASK_SECRET_KEY', os.urandom(24))
UPLOAD_FOLDER = 'uploads'
OUTPUT_FOLDER = 'outputs'
os.makedirs(UPLOAD_FOLDER, exist_ok=True)
os.makedirs(OUTPUT_FOLDER, exist_ok=True)
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        # This example assumes separate forms post to /hide and /extract, but you could combine logic here if needed.
        # For instance, check the form fields or a hidden field to distinguish actions.
        pass
    return render_template('index.html')

@app.route('/hide', methods=['POST'])
def hide():
    if 'cover_image' not in request.files:
        flash('No cover image file provided')
        return redirect('/')
    file = request.files['cover_image']
    if file.filename == '':
        flash('No selected file')
        return redirect('/')
    secret_message = request.form.get('secret_message', '')
    if not secret_message:
        flash('Secret message is required')
        return redirect('/')
    filename = secure_filename(file.filename)
    input_path = os.path.join(app.config['UPLOAD_FOLDER'], filename)
    file.save(input_path)
    output_filename = "stego_" + filename
    output_path = os.path.join(OUTPUT_FOLDER, output_filename)
    result = hide_data(input_path, secret_message, output_path)
    flash(result)
    return send_file(output_path, as_attachment=True)

@app.route('/extract', methods=['GET', 'POST'])
def extract():
    if request.method == 'POST':
        if 'stego_image' not in request.files:
            flash('No stego image file provided')
            return redirect('/')
        file = request.files['stego_image']
        if file.filename == '':
            flash('No selected file')
            return redirect('/')
        filename = secure_filename(file.filename)
        input_path = os.path.join(app.config['UPLOAD_FOLDER'], filename)
        file.save(input_path)
        result = extract_data(input_path)
        # Pass active_tab variable to keep the "Extract Data" tab active
        return render_template('index.html', result=result, active_tab="extract")
    else:
        return render_template('index.html', active_tab="hide")


if __name__ == "__main__":
    app.run(debug=True)