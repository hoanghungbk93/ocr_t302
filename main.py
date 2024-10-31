from flask import Flask, request, jsonify
from PIL import Image
import pytesseract
import os
import time
pytesseract.pytesseract.tesseract_cmd = '/usr/bin/tesseract'

app = Flask(__name__)

# Directory to save uploaded images
UPLOAD_FOLDER = "/home/pi/uploads"
os.makedirs(UPLOAD_FOLDER, exist_ok=True)

# Define bounding boxes for each temperature field (replace with actual coordinates)
bounding_boxes = {
    "Dryer": (0, 0, 1824, 200)
}

@app.route('/upload', methods=['POST'])
def upload_and_process_image():
    # Check if an image file is in the request
    if 'file' not in request.files:
        return jsonify({"error": "No file provided"}), 400

    file = request.files['file']
    if file.filename == '':
        return jsonify({"error": "No file selected"}), 400

    # Save the uploaded image
    image_path = os.path.join(UPLOAD_FOLDER, file.filename)
    file.save(image_path)

    # Perform OCR and extract temperature values
    temperature_values = process_image(image_path)
    
    # Clean up: delete the image after processing
    os.remove(image_path)
    
    # Return the extracted temperature values as JSON
    return jsonify(temperature_values)

def process_image(image_path):
    # Start timing for performance monitoring
    start_time = time.time()

    # Load the image
    image = Image.open(image_path)

    # Extract temperature values using bounding boxes
    temperature_values = {}
    for label, box in bounding_boxes.items():
        cropped_image = image.crop(box)
        text = pytesseract.image_to_string(cropped_image, config='--psm 6').strip()
        temperature_values[label] = text

    # Print processing time
    print("Processing time: %s seconds" % (time.time() - start_time))
    
    return temperature_values

if __name__ == '__main__':
    # Run the Flask server on all network interfaces at port 5000
    app.run(host='0.0.0.0', port=5000)
