import cv2
import numpy as np
from ultralytics import YOLO
import time

class SpeedDetector:
    def __init__(self):
        # Load YOLOv8 model for vehicle detection
        self.model = YOLO('yolov8n.pt')
        self.track_history = {}  # Dictionary to store tracking history
        self.speed_threshold = 50  # Speed threshold in km/h
        self.pixel_to_kmh_ratio = 0.1  # Conversion factor (adjust based on your setup)
        self.last_time = time.time()

    def calculate_speed(self, track_id, current_pos, current_time):
        if track_id not in self.track_history:
            self.track_history[track_id] = []
        
        # Add current position and time to history
        self.track_history[track_id].append((current_pos, current_time))
        
        # Keep only last 2 positions for speed calculation
        if len(self.track_history[track_id]) > 2:
            self.track_history[track_id].pop(0)
        
        # Calculate speed if we have enough history
        if len(self.track_history[track_id]) == 2:
            prev_pos, prev_time = self.track_history[track_id][0]
            curr_pos, curr_time = self.track_history[track_id][1]
            
            # Calculate distance in pixels
            distance = np.sqrt((curr_pos[0] - prev_pos[0])**2 + (curr_pos[1] - prev_pos[1])**2)
            
            # Calculate time difference in hours
            time_diff = (curr_time - prev_time) / 3600
            
            if time_diff > 0:
                # Calculate speed in km/h
                speed = (distance * self.pixel_to_kmh_ratio) / time_diff
                return speed
        
        return 0

    def detect(self, frame):
        results = []
        
        # Run YOLOv8 detection
        detections = self.model(frame, classes=[2, 3, 5, 7])  # Classes for cars, motorcycles, buses, trucks
        
        current_time = time.time()
        
        for detection in detections:
            boxes = detection.boxes
            for box in boxes:
                x1, y1, x2, y2 = box.xyxy[0].cpu().numpy()
                track_id = int(box.id[0]) if box.id is not None else None
                
                if track_id is not None:
                    # Calculate center point of the bounding box
                    center_x = (x1 + x2) / 2
                    center_y = (y1 + y2) / 2
                    
                    # Calculate speed
                    speed = self.calculate_speed(track_id, (center_x, center_y), current_time)
                    
                    # Only include vehicles exceeding speed threshold
                    if speed > self.speed_threshold:
                        results.append((x1, y1, x2, y2, speed))
        
        # Clean up old tracks
        current_time = time.time()
        for track_id in list(self.track_history.keys()):
            if current_time - self.track_history[track_id][-1][1] > 5:  # Remove tracks older than 5 seconds
                del self.track_history[track_id]
        
        return results 