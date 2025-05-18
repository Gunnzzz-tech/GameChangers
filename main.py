import sys
sys.path.append(r"C:\Users\Gayatri Gurugubelli\Desktop\f1\Speed\Speed\src\server")
from speed_detection import SpeedDetector
import cv2
import time
import requests
import os
from datetime import datetime, timedelta
from pathlib import Path
from collections import defaultdict
from helmet_detector import HelmetDetector
from ambulance_detector import AmbulanceDetector
from plate_reader import PlateReader
from traffic_signal_controller import TrafficSignalController

class SmartTrafficAI:
    def __init__(self, helmet_model_path=None):
        # Initialize detectors
        self.helmet_detector = HelmetDetector(model_path=helmet_model_path)
        self.speed_detector = SpeedDetector()  # Use custom SpeedDetector
        self.ambulance_detector = AmbulanceDetector()
        self.plate_reader = PlateReader()
        self.signal_controller = TrafficSignalController()  # Use default YOLOv8
        
        # Create assets directory if it doesn't exist
        self.assets_dir = Path("assets")
        self.assets_dir.mkdir(exist_ok=True)
        
        # API endpoint for violation logging
        self.api_url = "http://localhost:5000"
        
        # Violation tracking
        self.violations_by_plate = defaultdict(lambda: {
            'helmet_violations': [],
            'speed_violations': [],
            'last_seen': None
        })
        
        # Check if OpenCV GUI is available
        self.gui_available = self._check_gui_available()

    def _check_gui_available(self):
        try:
            cv2.namedWindow("test")
            cv2.destroyWindow("test")
            return True
        except Exception:
            return False

    def process_frame(self, frame, frame_number, timestamp):
        violations = []
        
        # Run helmet detection
        helmet_violations = self.helmet_detector.detect(frame)
        
        # Run speed detection
        annotated_frame, speed_violations = self.speed_detector.process_frame(frame)
        
        # Draw helmet violations on the same frame
        for violation in helmet_violations:
            x, y, w, h = violation['bbox']
            # Draw red rectangle for helmet violations
            cv2.rectangle(annotated_frame, (x, y), (x + w, y + h), (0, 0, 255), 2)
            # Add "No Helmet" label
            cv2.putText(annotated_frame, "No Helmet", (x, y - 10),
                       cv2.FONT_HERSHEY_SIMPLEX, 0.9, (0, 0, 255), 2)
            
            # Add to violations list
            plate_number = self.plate_reader.read_plate(frame, violation['bbox'])
            if plate_number:
                violations.append({
                    'type': 'helmet',
                    'plate_number': plate_number,
                    'bbox': violation['bbox'],
                    'timestamp': timestamp
                })
        
        # Process speed violations
        if speed_violations:
            for violation in speed_violations:
                plate_number = self.plate_reader.read_plate(frame, violation['bbox'])
                if plate_number:
                    violations.append({
                        'type': 'speed',
                        'plate_number': plate_number,
                        'speed': violation['speed'],
                        'bbox': violation['bbox'],
                        'timestamp': timestamp
                    })
        
        # Process ambulance detection
        ambulance_detected = self.ambulance_detector.detect(frame)
        if ambulance_detected:
            self.signal_controller.handle_ambulance()
            # Add ambulance detection indicator
            cv2.putText(annotated_frame, "Ambulance Detected", (10, 30),
                       cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 0, 255), 2)
        
        # Update traffic signal based on density
        vehicle_density = self.signal_controller.calculate_density(frame)
        self.signal_controller.update_signal(vehicle_density)
        
        return violations, annotated_frame
    
    def save_violation_image(self, frame, violation):
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        filename = f"violation_{timestamp}_{violation['type']}.jpg"
        filepath = self.assets_dir / filename
        
        # Extract region of interest
        x, y, w, h = violation['bbox']
        roi = frame[y:y+h, x:x+w]
        
        cv2.imwrite(str(filepath), roi)
        return str(filepath)
    
    def log_violation(self, violation, image_path):
        data = {
            'timestamp': violation['timestamp'].isoformat(),
            'violation_type': violation['type'],
            'plate_number': violation['plate_number'],
            'image_path': image_path,
            'speed': violation.get('speed', None)
        }
        
        try:
            response = requests.post(f"{self.api_url}/log_violation", json=data)
            response.raise_for_status()
            print(f"Logged violation: {violation['type']} - {violation['plate_number']}")
            
            # Update violation tracking
            plate_data = self.violations_by_plate[violation['plate_number']]
            if violation['type'] == 'helmet':
                plate_data['helmet_violations'].append(violation['timestamp'])
            else:  # speed violation
                plate_data['speed_violations'].append({
                    'timestamp': violation['timestamp'],
                    'speed': violation['speed']
                })
            plate_data['last_seen'] = violation['timestamp']
            
        except requests.exceptions.RequestException as e:
            print(f"Error logging violation: {e}")
    
    def serialize_datetimes(self, obj):
        if isinstance(obj, dict):
            return {k: self.serialize_datetimes(v) for k, v in obj.items()}
        elif isinstance(obj, list):
            return [self.serialize_datetimes(v) for v in obj]
        elif isinstance(obj, datetime):
            return obj.isoformat()
        else:
            return obj

    def send_report(self, current_time):
        """Send report to the server"""
        two_mins_ago = current_time - timedelta(minutes=2)
        
        # Prepare report data
        report_data = {
            'timestamp': current_time.isoformat(),
            'violations': {},
            'summary': {
                'total_violations': 0,
                'helmet_violations': 0,
                'speed_violations': 0
            }
        }
        
        # Process violations in the last 2 minutes
        for plate, data in self.violations_by_plate.items():
            if data['last_seen'] and data['last_seen'] >= two_mins_ago:
                helmet_violations = [v for v in data['helmet_violations'] if v >= two_mins_ago]
                speed_violations = [v for v in data['speed_violations'] if v['timestamp'] >= two_mins_ago]
                
                if helmet_violations or speed_violations:
                    report_data['violations'][plate] = {
                        'helmet_violations': helmet_violations,
                        'speed_violations': speed_violations,
                        'last_seen': data['last_seen']
                    }
                    
                    report_data['summary']['helmet_violations'] += len(helmet_violations)
                    report_data['summary']['speed_violations'] += len(speed_violations)
        
        report_data['summary']['total_violations'] = (
            report_data['summary']['helmet_violations'] + 
            report_data['summary']['speed_violations']
        )
        
        # Serialize datetimes before sending
        report_data = self.serialize_datetimes(report_data)
        
        # Send report to server
        try:
            response = requests.post(f"{self.api_url}/log_report", json=report_data)
            response.raise_for_status()
            print("\nReport sent to server successfully!")
        except requests.exceptions.RequestException as e:
            print(f"\nError sending report to server: {e}")
    
    def run(self, video_path):
        cap = cv2.VideoCapture(video_path)
        if not cap.isOpened():
            print(f"Error: Could not open video file: {video_path}")
            return
        
        # Get video properties
        fps = cap.get(cv2.CAP_PROP_FPS)
        total_frames = int(cap.get(cv2.CAP_PROP_FRAME_COUNT))
        duration = total_frames / fps
        
        print(f"\nProcessing video: {video_path}")
        print(f"Duration: {duration:.1f} seconds")
        print(f"FPS: {fps}")
        print("\nOpen http://localhost:5000 in your browser to view the dashboard")
        
        frame_count = 0
        start_time = datetime.now()
        last_report_time = start_time
        
        while True:
            ret, frame = cap.read()
            if not ret:
                break
            
            frame_count += 1
            current_time = start_time + timedelta(seconds=frame_count/fps)
            
            # Process every 5th frame to reduce computational load
            if frame_count % 5 == 0:
                violations, annotated_frame = self.process_frame(frame, frame_count, current_time)
                # Handle violations
                for violation in violations:
                    image_path = self.save_violation_image(frame, violation)
                    self.log_violation(violation, image_path)
            else:
                annotated_frame = frame  # Always assign annotated_frame
            
            # Show live video with detections if GUI is available
            if self.gui_available:
                cv2.imshow('Helmet/Speed Detection - Live', annotated_frame)
                if cv2.waitKey(1) & 0xFF == ord('q'):
                    print("\nQuitting early by user request.")
                    break
            
            # Generate report every 2 minutes
            if (current_time - last_report_time) >= timedelta(minutes=2):
                self.send_report(current_time)
                last_report_time = current_time
            
            # Print progress
            if frame_count % 30 == 0:  # Update progress every second
                progress = (frame_count / total_frames) * 100
                print(f"\rProgress: {progress:.1f}%", end="")
        
        # Send final report
        self.send_report(current_time)
        
        cap.release()
        if self.gui_available:
            cv2.destroyAllWindows()
        print("\nVideo processing completed!")
        print("Visit http://localhost:5000 to view the final report and graphs")

def get_video_path():
    while True:
        print("\nPlease enter the path to your video file:")
        video_path = input("> ").strip()
        
        # Remove quotes if present
        video_path = video_path.strip('"').strip("'")
        
        if os.path.exists(video_path):
            return video_path
        else:
            print(f"Error: File not found at {video_path}")
            print("Please enter a valid file path.")

if __name__ == "__main__":
    print("Smart Traffic AI - Video Processing")
    print("===================================")
    
    # No prompt for helmet model path; always use the default in helmet_detector.py
    video_path = get_video_path()
    
    traffic_ai = SmartTrafficAI()
    traffic_ai.run(video_path) 