from ultralytics import YOLO

# Load the YOLOv8 model
model = YOLO('yolov8n.pt')  # Load the base YOLOv8 nano model

# Train the model with optimized parameters
model.train(
    data='data.yaml',  # Path to data config file
    epochs=100,        # Increased epochs for better learning
    imgsz=640,         # Image size
    batch=16,          # Batch size
    patience=20,       # Early stopping patience
    device='0',        # Use GPU if available
    workers=8,         # Number of worker threads
    project='runs/train',  # Save results to project/name
    name='helmet_detection',  # Save to project/name
    exist_ok=True,     # Overwrite existing experiment
    pretrained=True,   # Use pretrained weights
    optimizer='Adam',  # Optimizer
    verbose=True,      # Print verbose output
    seed=42           # Random seed for reproducibility
) 