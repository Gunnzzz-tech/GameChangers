from ultralytics import YOLO
import cv2
import os

# Load the base YOLOv8 model
print("Loading YOLOv8 model...")
model = YOLO('runs/train/helmet_detection/weights/best.pt')  # Using the trained model

# Path to test images
test_images_dir = 'test/images'

# Create output directory for results
os.makedirs('test_results', exist_ok=True)

print(f"Looking for images in: {os.path.abspath(test_images_dir)}")

# Check if test directory exists
if not os.path.exists(test_images_dir):
    print(f"Error: Test directory '{test_images_dir}' not found!")
    exit(1)

# Get list of images
image_files = [f for f in os.listdir(test_images_dir) if f.lower().endswith(('.png', '.jpg', '.jpeg'))]

if not image_files:
    print(f"Error: No images found in '{test_images_dir}'!")
    exit(1)

print(f"Found {len(image_files)} images to process")

# Process each image in the test directory
for image_name in image_files:
    # Load image
    image_path = os.path.join(test_images_dir, image_name)
    print(f"\nProcessing: {image_path}")
    
    img = cv2.imread(image_path)
    
    if img is None:
        print(f"Could not load image: {image_path}")
        continue
        
    # Run inference
    print("Running inference...")
    results = model(img)
    
    # Process results
    detections = 0
    for result in results:
        boxes = result.boxes  # Boxes object for bbox outputs
        for box in boxes:
            # Get box coordinates
            x1, y1, x2, y2 = box.xyxy[0]
            x1, y1, x2, y2 = int(x1), int(y1), int(x2), int(y2)
            
            # Get confidence score
            conf = float(box.conf[0])
            
            # Get class name
            cls = int(box.cls[0])
            class_name = result.names[cls]
            
            # Draw bounding box
            cv2.rectangle(img, (x1, y1), (x2, y2), (0, 255, 0), 2)
            
            # Add label
            label = f'{class_name} {conf:.2f}'
            cv2.putText(img, label, (x1, y1 - 10), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 255, 0), 2)
            detections += 1
    
    # Save the result
    output_path = os.path.join('test_results', f'result_{image_name}')
    cv2.imwrite(output_path, img)
    print(f'Found {detections} objects - Saved result to {output_path}')

print("\nTesting complete! Check the 'test_results' directory for the processed images.") 