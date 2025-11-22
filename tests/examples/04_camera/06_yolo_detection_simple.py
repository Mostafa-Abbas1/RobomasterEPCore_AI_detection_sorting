# -*-coding:utf-8-*-
"""
Simple YOLO Object Detection Test
Minimal version - just shows detections
"""

import sys
import cv2
import time
from pathlib import Path

# Add project root to path
project_root = Path(__file__).parent.parent.parent.parent
sys.path.insert(0, str(project_root))
sys.path.insert(0, str(project_root / "src"))

from robomaster import robot
from src.vision.detection import ObjectDetector


def main():
    print("Simple YOLO Detection Test")
    print("Press 'q' to quit\n")

    # Connect to robot
    print("Connecting...")
    ep_robot = robot.Robot()
    ep_robot.initialize(conn_type="sta")
    ep_camera = ep_robot.camera

    # Load YOLO
    print("Loading YOLO...")
    detector = ObjectDetector(confidence_threshold=0.5)
    detector.load_model()

    # Start camera
    print("Starting camera...")
    ep_camera.start_video_stream(display=False)
    time.sleep(2)
    print("Ready! Press 'q' to quit\n")

    try:
        while True:
            # Get frame
            frame = ep_camera.read_cv2_image()
            if frame is None:
                continue

            # Detect objects
            detections = detector.detect_objects(frame)

            # Draw detections
            output = detector.draw_detections(frame, detections)

            # Print to console
            if detections:
                print(f"Detected {len(detections)} objects:")
                for det in detections:
                    print(f"  - {det.class_name}: {det.confidence:.2f}")

            # Show
            cv2.imshow("YOLO Detection", output)

            if cv2.waitKey(1) & 0xFF == ord('q'):
                break

    except KeyboardInterrupt:
        pass

    finally:
        cv2.destroyAllWindows()
        ep_camera.stop_video_stream()
        ep_robot.close()
        print("\nDone!")


if __name__ == '__main__':
    main()
