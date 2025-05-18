import cv2
import numpy as np
from ultralytics import YOLO

class AmbulanceDetector:
    def __init__(self):
        # Load YOLOv8 model
        self.model = YOLO('yolov8n.pt')  # Using nano model for speed
        self.confidence_threshold = 0.5
        
        # Define ambulance color range (red and white)
        self.lower_red = np.array([0, 100, 100])
        self.upper_red = np.array([10, 255, 255])
        self.lower_white = np.array([0, 0, 200])
        self.upper_white = np.array([180, 30, 255])
        
    def detect_ambulance_colors(self, frame, bbox):
        x, y, w, h = bbox
        roi = frame[y:y+h, x:x+w]
        
        # Convert to HSV
        hsv = cv2.cvtColor(roi, cv2.COLOR_BGR2HSV)
        
        # Create masks for red and white
        red_mask = cv2.inRange(hsv, self.lower_red, self.upper_red)
        white_mask = cv2.inRange(hsv, self.lower_white, self.upper_white)
        
        # Calculate percentage of red and white pixels
        total_pixels = w * h
        red_percentage = (np.sum(red_mask > 0) / total_pixels) * 100
        white_percentage = (np.sum(white_mask > 0) / total_pixels) * 100
        
        # Check if the color distribution matches an ambulance
        return (red_percentage > 10 and white_percentage > 10)
    
    def detect(self, frame):
        """
        Detect ambulances in the frame
        Returns True if ambulance is detected, False otherwise
        """
        # Run YOLOv8 inference
        results = self.model(frame, conf=self.confidence_threshold)
        
        for result in results:
            boxes = result.boxes
            for box in boxes:
                # Get class and confidence
                cls = int(box.cls[0])
                conf = float(box.conf[0])
                
                # Check if it's a vehicle (class 2, 3, 5, 7 in COCO dataset - car, motorcycle, bus, truck)
                if cls in [2, 3, 5, 7] and conf > self.confidence_threshold:
                    # Get bounding box
                    x1, y1, x2, y2 = map(int, box.xyxy[0])
                    bbox = (x1, y1, x2-x1, y2-y1)
                    
                    # Check for ambulance colors
                    if self.detect_ambulance_colors(frame, bbox):
                        return True
        
        return False 