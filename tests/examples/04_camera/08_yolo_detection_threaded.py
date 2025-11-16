# -*-coding:utf-8-*-
"""
Threaded YOLO Object Detection Test
BEST PERFORMANCE - Uses background thread to continuously read frames
This fixes the slow camera sync by always using the latest frame
"""

import sys
import cv2
import time
import threading
from pathlib import Path

# Add project root to path
project_root = Path(__file__).parent.parent.parent.parent
sys.path.insert(0, str(project_root))
sys.path.insert(0, str(project_root / "src"))

from robomaster import robot, camera
from src.vision.detection import ObjectDetector


class ThreadedCamera:
    """
    Camera reader that runs in background thread
    Always provides the latest frame
    """

    def __init__(self, ep_camera):
        self.ep_camera = ep_camera
        self.frame = None
        self.stopped = False
        self.lock = threading.Lock()

    def start(self):
        """Start background thread"""
        threading.Thread(target=self._update, daemon=True).start()
        return self

    def _update(self):
        """Background thread - continuously reads frames"""
        while not self.stopped:
            try:
                frame = self.ep_camera.read_cv2_image()
                if frame is not None:
                    with self.lock:
                        self.frame = frame
            except:
                pass
            time.sleep(0.01)  # Small delay

    def read(self):
        """Get the latest frame"""
        with self.lock:
            return self.frame

    def stop(self):
        """Stop the thread"""
        self.stopped = True


def main():
    print("=" * 60)
    print("THREADED YOLO Detection - FASTEST MODE")
    print("=" * 60)
    print("\nThis uses a background thread to always get fresh frames")
    print("= BEST PERFORMANCE for real-time detection =")
    print("\nPress 'q' to quit")
    print("=" * 60 + "\n")

    # Connect to robot
    print("Connecting to robot...")
    ep_robot = robot.Robot()
    ep_robot.initialize(conn_type="sta")
    print("✓ Connected!\n")

    # Initialize camera
    ep_camera = ep_robot.camera

    # Load YOLO
    print("Loading YOLO model...")
    detector = ObjectDetector(confidence_threshold=0.5)

    if not detector.load_model():
        print("✗ Failed to load YOLO model!")
        ep_robot.close()
        return

    print("✓ YOLO model loaded!\n")

    # Start camera with LOW RESOLUTION
    print("Starting camera stream (360P)...")
    ep_camera.start_video_stream(display=False, resolution=camera.STREAM_360P)
    time.sleep(2)

    # Start threaded camera
    print("Starting background frame reader...")
    threaded_cam = ThreadedCamera(ep_camera).start()
    time.sleep(1)
    print("✓ Threaded camera ready!\n")

    print("Running detection...\n")

    frame_count = 0
    detection_count = 0
    start_time = time.time()

    # Detection every N frames
    DETECTION_INTERVAL = 10  # Detect every 10th frame

    # Store detections persistently
    detections = []

    try:
        while True:
            # Get latest frame from thread
            img = threaded_cam.read()

            if img is None:
                time.sleep(0.01)
                continue

            frame_count += 1

            # Run detection periodically
            if frame_count % DETECTION_INTERVAL == 0:
                detections = detector.detect_objects(img)

                if detections:
                    detection_count += len(detections)
                    print(f"Frame {frame_count}: Found {len(detections)} objects")
                    for det in detections:
                        print(f"  - {det.class_name}: {det.confidence:.2f}")

            # Draw detections
            output = img.copy()
            if detections:
                for det in detections:
                    x1, y1, x2, y2 = det.bbox

                    # Draw box
                    cv2.rectangle(output, (x1, y1), (x2, y2), (0, 255, 0), 3)

                    # Draw label
                    label = f"{det.class_name}: {det.confidence:.2f}"
                    cv2.putText(
                        output,
                        label,
                        (x1, y1 - 10),
                        cv2.FONT_HERSHEY_SIMPLEX,
                        0.8,
                        (0, 255, 0),
                        2
                    )

            # Calculate FPS
            elapsed = time.time() - start_time
            fps = frame_count / elapsed if elapsed > 0 else 0

            # Show FPS
            cv2.putText(
                output,
                f"FPS: {fps:.1f}",
                (10, 30),
                cv2.FONT_HERSHEY_SIMPLEX,
                1,
                (0, 255, 0),
                2
            )

            # Show frame count
            cv2.putText(
                output,
                f"Frame: {frame_count}",
                (10, 70),
                cv2.FONT_HERSHEY_SIMPLEX,
                0.7,
                (0, 255, 0),
                2
            )

            # Show
            cv2.imshow("Threaded YOLO Detection - FAST", output)

            if cv2.waitKey(1) & 0xFF == ord('q'):
                break

    except KeyboardInterrupt:
        print("\nInterrupted")

    finally:
        # Cleanup
        print("\nCleaning up...")
        threaded_cam.stop()
        cv2.destroyAllWindows()
        ep_camera.stop_video_stream()
        ep_robot.close()

        # Stats
        elapsed = time.time() - start_time
        fps = frame_count / elapsed if elapsed > 0 else 0

        print("\n" + "=" * 60)
        print("Session Statistics:")
        print("=" * 60)
        print(f"Total Frames: {frame_count}")
        print(f"Total Detections: {detection_count}")
        print(f"Average FPS: {fps:.1f}")
        print(f"Duration: {elapsed:.1f}s")
        print("=" * 60)
        print("\n✓ Much faster, right? 🚀")


if __name__ == '__main__':
    main()
