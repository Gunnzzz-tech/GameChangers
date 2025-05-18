import cv2
import numpy as np
from ultralytics import YOLO
import math
import time
import os

class SpeedDetector:
    def __init__(self):
        # Try to load local model first
        model_path = 'yolov8n.pt'
        if not os.path.exists(model_path):
            model_path = os.path.join(os.path.dirname(__file__), 'yolov8n.pt')
        
        if not os.path.exists(model_path):
            print("Error: YOLOv8 model file not found!")
            print("Please download yolov8n.pt and place it in the project root directory")
            print("Download URL: https://github.com/ultralytics/assets/releases/download/v8.3.0/yolov8n.pt")
            raise FileNotFoundError("Model file yolov8n.pt not found")
        
        # Load YOLOv8 model from local file
        self.model = YOLO(model_path)
        
        # Initialize vehicle tracking
        self.vehicle_tracks = {}
        self.speed_limit = 50  # km/h
        
        # Calibration parameters (these should be adjusted based on your camera setup)
        self.pixels_per_meter = 30  # This needs to be calibrated for your specific camera view
        self.frame_rate = 30
        
    def calculate_speed(self, track):
        if len(track) < 2:
            return 0
        
        # Get the last two positions
        pos1 = track[-2]
        pos2 = track[-1]
        
        # Calculate distance in pixels
        distance_pixels = math.sqrt((pos2[0] - pos1[0])**2 + (pos2[1] - pos1[1])**2)
        
        # Convert to meters
        distance_meters = distance_pixels / self.pixels_per_meter
        
        # Calculate time difference (assuming constant frame rate)
        time_diff = 1.0 / self.frame_rate
        
        # Calculate speed (m/s)
        speed_ms = distance_meters / time_diff
        
        # Convert to km/h
        speed_kmh = speed_ms * 3.6
        
        # Cap speed at 175 if over 180
        if speed_kmh > 180:
            speed_kmh = 175
        
        return speed_kmh
    
    def process_frame(self, frame):
        # Run YOLOv8 tracking
        results = self.model.track(frame, persist=True, classes=[2, 3, 5, 7])  # Only detect cars, motorcycles, buses, and trucks
        
        # Create a copy of frame for drawing
        annotated_frame = frame.copy()
        violations = []
        
        if results[0].boxes is not None and results[0].boxes.id is not None:
            boxes = results[0].boxes.xywh.cpu()  # Get boxes in xywh format
            ids = results[0].boxes.id.cpu().numpy()
            
            for box, id in zip(boxes, ids):
                x, y, w, h = box
                
                # Update tracking
                if id not in self.vehicle_tracks:
                    self.vehicle_tracks[id] = []
                
                # Store center point
                center_point = (float(x), float(y))
                self.vehicle_tracks[id].append(center_point)
                
                # Calculate speed if we have enough tracking points
                speed = self.calculate_speed(self.vehicle_tracks[id])
                
                # Draw bounding box and speed
                color = (0, 255, 0) if speed <= self.speed_limit else (0, 0, 255)
                cv2.rectangle(annotated_frame, 
                            (int(x - w/2), int(y - h/2)), 
                            (int(x + w/2), int(y + h/2)), 
                            color, 2)
                
                # Display speed
                speed_text = f"{speed:.1f} km/h"
                cv2.putText(annotated_frame, speed_text, 
                          (int(x - w/2), int(y - h/2) - 10),
                          cv2.FONT_HERSHEY_SIMPLEX, 0.9, color, 2)
                
                # Check for overspeeding
                if speed > self.speed_limit:
                    cv2.putText(annotated_frame, "OVERSPEEDING", 
                              (int(x - w/2), int(y + h/2) + 30),
                              cv2.FONT_HERSHEY_SIMPLEX, 0.9, (0, 0, 255), 2)
                    # Add to violations list
                    violations.append({
                        'id': int(id),
                        'bbox': (int(x - w/2), int(y - h/2), int(w), int(h)),
                        'speed': speed
                    })
        
        return annotated_frame, violations

    def cleanup_old_tracks(self, max_age=30):
        # Remove tracks that haven't been updated recently
        current_time = time.time()
        tracks_to_remove = []
        for track_id in self.vehicle_tracks:
            if len(self.vehicle_tracks[track_id]) == 0:
                tracks_to_remove.append(track_id)
        
        for track_id in tracks_to_remove:
            del self.vehicle_tracks[track_id] 