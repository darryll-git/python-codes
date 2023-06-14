import pytesseract
from PIL import Image

# Path to the Tesseract OCR executable
pytesseract.pytesseract.tesseract_cmd = r'C:\Program Files\Tesseract-OCR\tesseract.exe'

# Path to the input image
image_path = 'path_to_your_image.jpg'

# Open the image using PIL
image = Image.open(image_path)

# Perform OCR using pytesseract
text = pytesseract.image_to_string(image)

# Print the extracted text
print(text)
