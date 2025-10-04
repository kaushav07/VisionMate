import pytesseract
import cv2
import numpy as np

def extract_text_from_image(image: 'np.ndarray') -> str:
    """
    Extract text from a given image using pytesseract OCR.

    Args:
        image: Input image as a numpy array (OpenCV format)

    Returns:
        Extracted text as a string
    """
    # Convert image to grayscale (OCR works better on gray)
    gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)

    # Use pytesseract to extract text
    text = pytesseract.image_to_string(gray)

    return text
