from ultralytics import YOLO

# Load the base YOLOv8 model
model = YOLO('yolov8n.pt')  # Load the nano model

# Train the model with CPU-optimized parameters
results = model.train(
    data='data.yaml',          # Path to data config file
    epochs=100,                # Number of training epochs
    imgsz=640,                 # Image size
    batch=8,                   # Reduced batch size for CPU
    patience=20,               # Early stopping patience
    device='cpu',              # Use CPU
    workers=4,                 # Reduced number of worker threads for CPU
    project='runs/train',      # Save results to project/name
    name='helmet_detection',   # Save to project/name
    exist_ok=True,             # Overwrite existing experiment
    pretrained=True,           # Use pretrained weights
    optimizer='Adam',          # Optimizer
    verbose=True,              # Print verbose output
    seed=42,                   # Random seed for reproducibility
    lr0=0.001,                # Initial learning rate
    lrf=0.01,                 # Final learning rate
    momentum=0.937,           # SGD momentum/Adam beta1
    weight_decay=0.0005,      # Optimizer weight decay
    warmup_epochs=3,          # Warmup epochs
    warmup_momentum=0.8,      # Warmup momentum
    warmup_bias_lr=0.1,       # Warmup bias learning rate
    box=7.5,                  # Box loss gain
    cls=0.5,                  # Class loss gain
    dfl=1.5,                  # Distribution focal loss gain
    close_mosaic=10,          # Disable mosaic augmentation for final epochs
    hsv_h=0.015,             # Image HSV-Hue augmentation
    hsv_s=0.7,               # Image HSV-Saturation augmentation
    hsv_v=0.4,               # Image HSV-Value augmentation
    degrees=0.0,             # Image rotation (+/- deg)
    translate=0.1,           # Image translation (+/- fraction)
    scale=0.5,               # Image scale (+/- gain)
    shear=0.0,               # Image shear (+/- deg)
    perspective=0.0,         # Image perspective (+/- fraction)
    flipud=0.0,              # Image flip up-down (probability)
    fliplr=0.5,              # Image flip left-right (probability)
    mosaic=1.0,              # Image mosaic (probability)
    mixup=0.0,               # Image mixup (probability)
    copy_paste=0.0           # Segment copy-paste (probability)
)

# Save the trained model
model.save('runs/train/helmet_detection/weights/best.pt') 