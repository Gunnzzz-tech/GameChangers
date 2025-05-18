import cv2
from speed_detection import SpeedDetector
import argparse
import os

def process_video(input_path, output_path):
    # Initialize speed detector
    detector = SpeedDetector()
    
    # Open video file
    cap = cv2.VideoCapture(input_path)
    if not cap.isOpened():
        print(f"Error: Could not open video file {input_path}")
        return
    
    # Get video properties
    frame_width = int(cap.get(cv2.CAP_PROP_FRAME_WIDTH))
    frame_height = int(cap.get(cv2.CAP_PROP_FRAME_HEIGHT))
    fps = int(cap.get(cv2.CAP_PROP_FPS))
    
    # Create video writer
    fourcc = cv2.VideoWriter_fourcc(*'mp4v')
    out = cv2.VideoWriter(output_path, fourcc, fps, (frame_width, frame_height))
    
    frame_count = 0
    
    while cap.isOpened():
        ret, frame = cap.read()
        if not ret:
            break
            
        frame_count += 1
        print(f"Processing frame {frame_count}", end='\r')
        
        # Process frame
        processed_frame = detector.process_frame(frame)
        
        # Write frame
        out.write(processed_frame)
        
        # Display frame (optional)
        cv2.imshow('Speed Detection', processed_frame)
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break
    
    # Cleanup
    cap.release()
    out.release()
    cv2.destroyAllWindows()
    print(f"\nProcessing complete. Output saved to {output_path}")

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description='Process traffic video for speed detection')
    parser.add_argument('input', help='Path to input video file')
    parser.add_argument('--output', help='Path to output video file', default='output.mp4')
    
    args = parser.parse_args()
    process_video(args.input, args.output) 