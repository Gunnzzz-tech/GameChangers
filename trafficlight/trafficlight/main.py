import cv2
import numpy as np
import time

def detect_vehicles(frame):
    # Placeholder for your actual detection logic
    # Returns a mock count; replace this with your detection model
    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
    return np.count_nonzero(gray > 100) // 1000  # Basic simulation

def draw_signal(frame, color, position):
    color_map = {"GREEN": (0, 255, 0), "RED": (0, 0, 255)}
    signal_color = color_map.get(color, (255, 255, 255))
    cv2.circle(frame, position, 20, signal_color, -1)
    cv2.putText(frame, f"{color}", (position[0] - 30, position[1] - 30),
                cv2.FONT_HERSHEY_SIMPLEX, 0.6, signal_color, 2)


def display_4_videos(frames):
    # Resize all frames to 480x270
    resized = [cv2.resize(f, (480, 270)) for f in frames]

    top = np.hstack((resized[0], resized[1]))
    bottom = np.hstack((resized[2], resized[3]))
    combined = np.vstack((top, bottom))

    cv2.imshow("Traffic Monitor", combined)


def main():
    caps = [cv2.VideoCapture(f"lane{i+1}.mp4") for i in range(4)]
    pause_frames = [None] * 4

    # Preload 2 seconds
    preload_start = time.time()
    while time.time() - preload_start < 2:
        lane_frames = []
        for i, cap in enumerate(caps):
            ret, frame = cap.read()
            if not ret or frame is None:
                frame = np.zeros((240, 320, 3), dtype=np.uint8)
            else:
                pause_frames[i] = frame.copy()
            lane_frames.append(frame)
        display_4_videos(lane_frames)
        if cv2.waitKey(33) & 0xFF == ord('q'):
            return

    start_time = time.time()
    base_group = 0  # 0: group 1&3, 1: group 2&4

    while True:
        elapsed = time.time() - start_time

        # Every 20s, re-evaluate traffic and decide which group gets first green
        if int(elapsed) % 20 == 0 and int(elapsed) != 0:
            crowd_levels = []
            for i, cap in enumerate(caps):
                ret, frame = cap.read()
                if not ret or frame is None:
                    frame = pause_frames[i] if pause_frames[i] is not None else np.zeros((240, 320, 3), dtype=np.uint8)
                else:
                    pause_frames[i] = frame.copy()
                count = detect_vehicles(pause_frames[i])
                crowd_levels.append(count)

            group0_sum = crowd_levels[0] + crowd_levels[2]
            group1_sum = crowd_levels[1] + crowd_levels[3]
            base_group = 0 if group0_sum >= group1_sum else 1

        # For 10s: base_group green, next 10s: opposite green
        current_cycle = int(elapsed // 10)
        green_group = base_group if current_cycle % 2 == 0 else 1 - base_group

        lane_frames = []
        for i in range(4):
            if (green_group == 0 and i in [0, 2]) or (green_group == 1 and i in [1, 3]):
                ret, frame = caps[i].read()
                if not ret or frame is None:
                    frame = pause_frames[i] if pause_frames[i] is not None else np.zeros((240, 320, 3), dtype=np.uint8)
                else:
                    pause_frames[i] = frame.copy()
                draw_signal(frame, "GREEN", (50, 50))
            else:
                frame = pause_frames[i] if pause_frames[i] is not None else np.zeros((240, 320, 3), dtype=np.uint8)
                draw_signal(frame, "RED", (frame.shape[1] - 50, 50))
            lane_frames.append(frame)

        display_4_videos(lane_frames)
        if cv2.waitKey(33) & 0xFF == ord('q'):
            break

    for cap in caps:
        cap.release()
    cv2.destroyAllWindows()


if __name__ == "__main__":
    main()
