import cv2
import numpy as np
import time
from helmet_detector import HelmetDetector
import sys
import os
import threading
import queue
import matplotlib
matplotlib.use('Agg')  # Use non-GUI backend
import matplotlib.pyplot as plt
from datetime import datetime, timedelta
import json
import random
import string
from matplotlib.animation import FuncAnimation

# Add the Speed directory to the Python path
sys.path.append(os.path.join(os.path.dirname(__file__), 'Speed', 'Speed', 'src', 'server'))
from speed_detection import SpeedDetector

class DummyPlateReader:
    def read_plate(self, frame, bbox):
        # Generate a fake but realistic Indian number plate
        state = random.choice(['KA', 'MH', 'DL', 'TN', 'AP', 'GJ', 'RJ', 'UP', 'WB', 'PB'])
        rto = f"{random.randint(1, 99):02d}"
        letters = ''.join(random.choices(string.ascii_uppercase, k=2))
        digits = f"{random.randint(0, 9999):04d}"
        return f"{state}{rto}{letters}{digits}"

class IntegratedDetector:
    def __init__(self):
        try:
            self.helmet_detector = HelmetDetector()
            self.speed_detector = SpeedDetector()
            self.plate_reader = DummyPlateReader()
            self.frame_queues = [queue.Queue(maxsize=2) for _ in range(4)]
            self.running = True
            self.pause_frames = [np.zeros((480, 640, 3), dtype=np.uint8) for _ in range(4)]
            self.violation_lock = threading.Lock()
            self.violations = []
            self.helmet_violations = []
            self.quit_event = threading.Event()
            self.speed_threshold = 60
            
            # Initialize graph data
            self.graph_times = []
            self.graph_counts = []
            self.start_time = datetime.now()
            self.last_graph_update = time.time()
            self.graph_update_interval = 1.0  # Update graph every second
            
            # Create necessary directories
            os.makedirs('dashboard_data', exist_ok=True)
            os.makedirs('static', exist_ok=True)
            
        except Exception as e:
            print(f"Error initializing detector: {e}")
            raise

    def generate_dummy_violations(self, num=10):
        now = datetime.now()
        self.violations = []
        for i in range(num):
            # Generate a fake timestamp spaced by 1 minute
            t = now + timedelta(minutes=i)
            timestamp = t.strftime("%Y-%m-%d %H:%M:%S")
            lane = random.randint(1, 4)
            speed = random.randint(self.speed_threshold + 1, self.speed_threshold + 40)
            plate = self.plate_reader.read_plate(None, None)
            self.violations.append((timestamp, lane, speed, plate))
        self.update_graph()

    def detect_vehicles(self, frame):
        gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
        return np.count_nonzero(gray > 100) // 1000

    def draw_signal(self, frame, color, position):
        color_map = {"GREEN": (0, 255, 0), "RED": (0, 0, 255)}
        signal_color = color_map.get(color, (255, 255, 255))
        cv2.circle(frame, position, 20, signal_color, -1)
        cv2.putText(frame, f"{color}", (position[0] - 30, position[1] - 30),
                    cv2.FONT_HERSHEY_SIMPLEX, 0.6, signal_color, 2)

    def init_graph(self):
        """Initialize the graph in the main thread"""
        self.fig, self.ax = plt.subplots(figsize=(8, 4))
        self.fig.canvas.manager.set_window_title('Real-time Violations Graph')
        self.line, = self.ax.plot([], [], 'b-', marker='o')
        self.ax.set_title('Violations Over Time')
        self.ax.set_xlabel('Time (s)')
        self.ax.set_ylabel('Total Violations')
        self.ax.grid(True)
        self.fig.tight_layout()
        plt.ion()
        plt.show(block=False)

    def update_realtime_graph(self):
        """Queue a graph update"""
        with self.violation_lock:
            if not self.violations:
                return
            
            # Calculate time points and counts
            times = []
            counts = []
            for i, v in enumerate(self.violations):
                t = datetime.strptime(v[0], '%Y-%m-%d %H:%M:%S')
                delta = (t - self.start_time).total_seconds()
                times.append(delta)
                counts.append(i + 1)
            
            # Put the update data in the queue
            self.graph_update_queue.put((times, counts))

    def process_graph_updates(self):
        """Process graph updates from the queue"""
        try:
            while not self.graph_update_queue.empty():
                times, counts = self.graph_update_queue.get_nowait()
                self.line.set_data(times, counts)
                self.ax.relim()
                self.ax.autoscale_view()
                self.fig.canvas.draw()
                self.fig.canvas.flush_events()
        except queue.Empty:
            pass

    def update_graph(self):
        """Update the graph and save it to file"""
        try:
            with self.violation_lock:
                if not self.violations:
                    return
                
                # Calculate time points and counts
                times = []
                counts = []
                for i, v in enumerate(self.violations):
                    t = datetime.strptime(v[0], '%Y-%m-%d %H:%M:%S')
                    delta = (t - self.start_time).total_seconds()
                    times.append(delta)
                    counts.append(i + 1)
                
                # Create the figure
                plt.figure(figsize=(10, 6))
                plt.plot(times, counts, 'b-', marker='o')
                plt.title('Violations Over Time')
                plt.xlabel('Time (s)')
                plt.ylabel('Total Violations')
                plt.grid(True)
                plt.tight_layout()
                
                # Save the figure
                plt.savefig('dashboard_data/violations_graph.png', dpi=100, bbox_inches='tight')
                plt.close()
                
                # Copy to static directory
                try:
                    import shutil
                    shutil.copy('dashboard_data/violations_graph.png', 'static/violations_graph.png')
                except Exception as copy_err:
                    print(f"Error copying graph to static: {copy_err}")
                
        except Exception as e:
            print(f"Error updating graph: {e}")

    def process_frame(self, frame, lane_id):
        if frame is None:
            return None
        try:
            # Process helmet detection
            try:
                helmet_results = self.helmet_detector.detect(frame)
            except Exception as e:
                print(f"Error in helmet detection: {e}")
                helmet_results = []

            # Process speed detection
            try:
                processed_frame, speed_violations = self.speed_detector.process_frame(frame)
            except Exception as e:
                print(f"Error in speed detection: {e}")
                processed_frame = frame.copy()
                speed_violations = []

            now = datetime.now().strftime('%H:%M:%S')
            violation_added = False
            
            # Record helmet violations
            for result in helmet_results:
                try:
                    x1, y1, x2, y2, conf, cls = result
                    if str(cls).lower() == 'no-helmet' or str(cls).lower() == 'no_helmet':
                        with self.violation_lock:
                            self.helmet_violations.append({
                                'time': now,
                                'lane': lane_id+1,
                                'bbox': [int(x1), int(y1), int(x2), int(y2)],
                                'confidence': float(conf),
                                'class': str(cls)
                            })
                            violation_added = True
                except Exception as e:
                    print(f"Error processing helmet result: {e}")
                    continue
            
            # Record speed violations
            for v in speed_violations:
                try:
                    if v['speed'] > self.speed_threshold:
                        now = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
                        plate_number = self.plate_reader.read_plate(frame, v['bbox'])
                        with self.violation_lock:
                            self.violations.append((now, lane_id+1, v['speed'], plate_number))
                            violation_added = True
                        print(f"Speed violation detected: {v['speed']} km/h, Lane {lane_id+1}, Plate: {plate_number}")
                except Exception as e:
                    print(f"Error processing speed violation: {e}")
                    continue
            
            # Update graph periodically
            current_time = time.time()
            if violation_added or (current_time - self.last_graph_update) >= self.graph_update_interval:
                self.update_graph()
                self.last_graph_update = current_time
            
            # Draw helmet boxes
            for result in helmet_results:
                try:
                    x1, y1, x2, y2, conf, cls = result
                    cv2.rectangle(processed_frame, (int(x1), int(y1)), (int(x2), int(y2)), (0, 255, 0), 2)
                    cv2.putText(processed_frame, f"{cls}: {conf:.2f}", (int(x1), int(y1) - 10),
                               cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 255, 0), 2)
                except Exception as e:
                    print(f"Error drawing helmet box: {e}")
                    continue

            return processed_frame
        except Exception as e:
            print(f"Error in process_frame: {e}")
            return frame

    def display_4_videos(self, frames):
        # Resize all frames to the same size
        resized = [cv2.resize(f, (480, 270)) for f in frames]
        # Create 2x2 grid
        top = np.hstack((resized[0], resized[1]))
        bottom = np.hstack((resized[2], resized[3]))
        combined = np.vstack((top, bottom))
        # Add lane numbers
        for i, pos in enumerate([(240, 30), (720, 30), (240, 300), (720, 300)]):
            cv2.putText(combined, f"Lane {i+1}", pos, cv2.FONT_HERSHEY_SIMPLEX, 1, (255, 255, 255), 2)
        cv2.imshow("Integrated Traffic Monitor", combined)
        cv2.waitKey(1)  # Ensure the frame is displayed

    def display_dashboard(self):
        dashboard = np.ones((400, 600, 3), dtype=np.uint8) * 255
        y = 30
        cv2.putText(dashboard, "Recent Violations (Time, Lane, Speed)", (10, y), cv2.FONT_HERSHEY_SIMPLEX, 0.7, (0,0,0), 2)
        y += 30
        with self.violation_lock:
            recent = self.violations[-10:]
        for v in recent:
            text = f"{v[0]} | Lane {v[1]} | {v[2]:.1f} km/h"
            cv2.putText(dashboard, text, (10, y), cv2.FONT_HERSHEY_SIMPLEX, 0.6, (0,0,255), 2)
            y += 30
        cv2.imshow("Violations Dashboard", dashboard)

    def process_video(self, video_path, lane_id):
        cap = cv2.VideoCapture(video_path)
        if not cap.isOpened():
            print(f"Error: Could not open video {video_path}")
            return

        while not self.quit_event.is_set():
            ret, frame = cap.read()
            if not ret:
                cap.set(cv2.CAP_PROP_POS_FRAMES, 0)
                continue

            processed_frame = self.process_frame(frame, lane_id)
            if processed_frame is not None:
                self.pause_frames[lane_id] = processed_frame

            time.sleep(0.001)  # Reduced sleep for smoother video
        cap.release()

    def save_dashboard_data(self):
        os.makedirs('dashboard_data', exist_ok=True)
        # Save speed violations
        with self.violation_lock:
            speed_data = [
                {'time': v[0], 'lane': v[1], 'speed': v[2], 'plate': v[3]} for v in self.violations
            ]
            with open('dashboard_data/speed_violations.json', 'w') as f:
                json.dump(speed_data, f, indent=2)
            with open('dashboard_data/helmet_violations.json', 'w') as f:
                json.dump(self.helmet_violations, f, indent=2)
            # Save summary
            summary = {
                'total_speed_violations': len(self.violations),
                'total_helmet_violations': len(self.helmet_violations),
                'speed_violations_per_lane': {},
                'helmet_violations_per_lane': {}
            }
            for v in self.violations:
                summary['speed_violations_per_lane'][str(v[1])] = summary['speed_violations_per_lane'].get(str(v[1]), 0) + 1
            for v in self.helmet_violations:
                lane = str(v['lane'])
                summary['helmet_violations_per_lane'][lane] = summary['helmet_violations_per_lane'].get(lane, 0) + 1
            with open('dashboard_data/summary.json', 'w') as f:
                json.dump(summary, f, indent=2)
        
        # Update graph after saving data
        self.update_graph()

    def periodic_save(self):
        """Periodically save dashboard data"""
        while not self.quit_event.is_set():
            self.save_dashboard_data()
            time.sleep(5)  # Save every 5 seconds

    def run(self):
        video_paths = [
            'trafficlight/trafficlight/lane1.mp4',
            'trafficlight/trafficlight/lane2.mp4',
            'trafficlight/trafficlight/lane3.mp4',
            'trafficlight/trafficlight/lane4.mp4'
        ]

        self.pause_frames = [np.zeros((480, 640, 3), dtype=np.uint8) for _ in range(4)]

        threads = []
        for i, video_path in enumerate(video_paths):
            thread = threading.Thread(target=self.process_video, args=(video_path, i))
            thread.daemon = True
            thread.start()
            threads.append(thread)

        save_thread = threading.Thread(target=self.periodic_save, daemon=True)
        save_thread.start()

        try:
            while not self.quit_event.is_set():
                self.display_4_videos(self.pause_frames)
                if cv2.waitKey(1) & 0xFF == ord('q'):
                    self.quit_event.set()
                    break
                time.sleep(0.001)
        except KeyboardInterrupt:
            self.quit_event.set()
        except Exception as e:
            print(f"Error in main loop: {e}")
            self.quit_event.set()

        for thread in threads:
            thread.join(timeout=1)
        cv2.destroyAllWindows()
        self.save_dashboard_data()

if __name__ == "__main__":
    detector = IntegratedDetector()
    detector.run() 