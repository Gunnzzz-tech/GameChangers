import cv2
import numpy as np
from ultralytics import YOLO
from pathlib import Path

class HelmetDetector:
    def __init__(self, model_path=None):
        """
        Initialize the helmet detector with a custom trained model
        Args:
            model_path: Path to the custom trained model (e.g., 'path/to/your/model.pt')
        """
        # Always use the custom helmet detection model unless a different model_path is provided
        if model_path is None:
            model_path = r"C:\Users\Gayatri Gurugubelli\Desktop\f1\Helmet_Detection.v5i.yolov8\yolov8n.pt"
        model_path = Path(model_path)
        if not model_path.exists():
            raise FileNotFoundError(f"Model file not found at {model_path}")
        self.model = YOLO(str(model_path))
        self.confidence_threshold = 0.5
        
    def detect(self, frame):
        """
        Detect helmet violations in the frame
        Args:
            frame: Input frame (numpy array)
        Returns:
            List of dictionaries containing violation information
        """
        violations = []
        
        # Run inference
        results = self.model(frame, conf=self.confidence_threshold)[0]
        
        # Process results
        for result in results.boxes.data.tolist():
            x1, y1, x2, y2, confidence, class_id = result
            
            # Convert to integers
            x1, y1, x2, y2 = map(int, [x1, y1, x2, y2])
            
            # Get class name
            class_name = self.model.names[int(class_id)]
            
            # Check if it's a person without helmet
            if class_name == 'no_helmet':  # Adjust this based on your model's class names
                violations.append({
                    'bbox': (x1, y1, x2-x1, y2-y1),
                    'confidence': confidence,
                    'class': class_name
                })
        
        return violations 