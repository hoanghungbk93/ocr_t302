from PIL import Image
import pytesseract
import time
start_time = time.time()
# Load the captured image
image_path = '/Users/admin/Desktop/dryer.png'  # Replace with the path to the captured image
image = Image.open(image_path)

# Define bounding boxes for each temperature field (x, y, width, height)
bounding_boxes = {
    "Dryer": (1780, 95, 1824, 128),   # Replace with actual coordinates
    "HotBin": (1784, 132, 1819, 157),
    "Ap": (1790, 161, 1821, 190),
    "Exit": (1790, 194, 1819, 221),
    "HotMix": (1790, 228, 1819, 254),
    "Mixture": (1790, 259, 1817, 285)
}

# Extract temperature values
temperature_values = {}
for label, box in bounding_boxes.items():
    # Crop the region and perform OCR
    cropped_image = image.crop(box)
    text = pytesseract.image_to_string(cropped_image, config='--psm 6').strip()
    temperature_values[label] = text

print("time : %s", time.time()- start_time )

# Display the extracted temperature values
for label, value in temperature_values.items():
    print(f"{label}: {value}")
