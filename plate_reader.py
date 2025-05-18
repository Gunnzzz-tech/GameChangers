import cv2
import numpy as np
import easyocr

class PlateReader:
    def __init__(self):
        # Initialize EasyOCR reader
        self.reader = easyocr.Reader(['en'])
        
        # Plate detection parameters
        self.min_plate_width = 60
        self.min_plate_height = 20
        
    def preprocess_image(self, image):
        # Convert to grayscale
        gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
        
        # Apply bilateral filter to remove noise while keeping edges sharp
        filtered = cv2.bilateralFilter(gray, 11, 17, 17)
        
        # Apply adaptive thresholding
        thresh = cv2.adaptiveThreshold(
            filtered, 255, cv2.ADAPTIVE_THRESH_GAUSSIAN_C, 
            cv2.THRESH_BINARY_INV, 11, 2
        )
        
        return thresh
    
    def find_plate_contours(self, image):
        # Find contours
        contours, _ = cv2.findContours(
            image, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE
        )
        
        # Filter contours based on size and aspect ratio
        plate_contours = []
        for contour in contours:
            x, y, w, h = cv2.boundingRect(contour)
            aspect_ratio = w / float(h)
            
            if (w >= self.min_plate_width and h >= self.min_plate_height and
                2.0 <= aspect_ratio <= 5.0):
                plate_contours.append((x, y, w, h))
        
        return plate_contours
    
    def read_plate(self, frame, bbox):
        """
        Extract and read license plate from the given bounding box
        Returns the plate number if found, None otherwise
        """
        x, y, w, h = bbox
        
        # Extract region of interest
        roi = frame[y:y+h, x:x+w]
        
        # Preprocess the image
        processed = self.preprocess_image(roi)
        
        # Find potential plate regions
        plate_regions = self.find_plate_contours(processed)
        
        if not plate_regions:
            return None
        
        # Try to read text from each potential plate region
        for px, py, pw, ph in plate_regions:
            plate_roi = roi[py:py+ph, px:px+pw]
            
            # Use EasyOCR to read text
            results = self.reader.readtext(plate_roi)
            
            if results:
                # Get the text with highest confidence
                text = max(results, key=lambda x: x[2])[1]
                
                # Clean and validate the plate number
                cleaned_text = self.clean_plate_number(text)
                if self.is_valid_plate_number(cleaned_text):
                    return cleaned_text
        
        return None
    
    def clean_plate_number(self, text):
        """
        Clean the detected text to match license plate format
        """
        # Remove special characters and spaces
        cleaned = ''.join(c for c in text if c.isalnum())
        
        # Convert to uppercase
        cleaned = cleaned.upper()
        
        return cleaned
    
    def is_valid_plate_number(self, text):
        """
        Validate if the text matches a typical license plate format
        """
        # Basic validation - at least 5 characters
        if len(text) < 5:
            return False
        
        # Check if it contains both letters and numbers
        has_letters = any(c.isalpha() for c in text)
        has_numbers = any(c.isdigit() for c in text)
        
        return has_letters and has_numbers 