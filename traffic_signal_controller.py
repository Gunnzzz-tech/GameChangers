import cv2
import numpy as np
from collections import deque
from ultralytics import YOLO

class TrafficSignalController:
    def __init__(self, model_path=None):
        if model_path is None:
            self.model = YOLO('yolov8n.pt')
        else:
            self.model = YOLO(model_path)
        self.confidence_threshold = 0.5
        
        # Traffic signal parameters
        self.min_green_time = 30  # seconds
        self.max_green_time = 90  # seconds
        self.yellow_time = 3  # seconds
        self.current_phase = 0  # 0: North-South, 1: East-West
        self.phase_timer = 0
        self.ambulance_detected = False
        
        # Density thresholds
        self.low_density_threshold = 5
        self.medium_density_threshold = 15
        self.high_density_threshold = 25
        
        # Store recent density measurements
        self.density_history = deque(maxlen=10)
        
    def detect_vehicles(self, frame):
        # Run YOLOv8 inference
        results = self.model(frame, conf=self.confidence_threshold)
        
        vehicles = []
        
        for result in results:
            for box in result.boxes:
                # Get class and confidence
                cls = int(box.cls[0])
                conf = float(box.conf[0])
                
                # Check if it's a vehicle (class 2, 3, 5, 7 in COCO dataset - car, motorcycle, bus, truck)
                if cls in [2, 3, 5, 7] and conf > self.confidence_threshold:
                    # Get bounding box
                    x1, y1, x2, y2 = map(int, box.xyxy[0])
                    w = x2 - x1
                    h = y2 - y1
                    center_x = x1 + w//2
                    center_y = y1 + h//2
                    
                    vehicles.append({
                        'class': cls,
                        'bbox': (x1, y1, w, h),
                        'center': (center_x, center_y)
                    })
        
        return vehicles
    
    def calculate_density(self, frame):
        """
        Calculate vehicle density in the frame
        Returns density level (0-3) and vehicle count
        """
        vehicles = self.detect_vehicles(frame)
        vehicle_count = len(vehicles)
        
        # Calculate density based on frame size
        frame_area = frame.shape[0] * frame.shape[1]
        density = (vehicle_count / frame_area) * 1000000  # Normalize to vehicles per million pixels
        
        self.density_history.append(density)
        avg_density = sum(self.density_history) / len(self.density_history)
        
        # Determine density level
        if avg_density < self.low_density_threshold:
            level = 0
        elif avg_density < self.medium_density_threshold:
            level = 1
        elif avg_density < self.high_density_threshold:
            level = 2
        else:
            level = 3
        
        return level, vehicle_count
    
    def calculate_green_time(self, density_level):
        """
        Calculate green time based on density level
        """
        if density_level == 0:
            return self.min_green_time
        elif density_level == 1:
            return int(self.min_green_time * 1.5)
        elif density_level == 2:
            return int(self.min_green_time * 2)
        else:
            return self.max_green_time
    
    def handle_ambulance(self):
        """
        Handle ambulance detection by prioritizing its direction
        """
        self.ambulance_detected = True
        # Force green signal in the direction of the ambulance
        # This is a simplified version - in reality, you'd need to track ambulance direction
    
    def update_signal(self, density_level):
        """
        Update traffic signal based on density and timing
        """
        if self.ambulance_detected:
            # Handle ambulance priority
            self.ambulance_detected = False
            return
        
        # Calculate green time for current phase
        green_time = self.calculate_green_time(density_level)
        
        # Update phase timer
        self.phase_timer += 1
        
        # Check if it's time to change phase
        if self.phase_timer >= green_time:
            self.phase_timer = 0
            self.current_phase = (self.current_phase + 1) % 2  # Toggle between 0 and 1
    
    def get_current_signal_state(self):
        """
        Get current signal state for visualization
        """
        if self.phase_timer < self.yellow_time:
            return "YELLOW"
        elif self.current_phase == 0:
            return "GREEN_NS"
        else:
            return "GREEN_EW" 