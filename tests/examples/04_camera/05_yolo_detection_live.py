# -*-coding:utf-8-*-
"""
Live YOLO Object Detection Test
Shows camera stream with real-time object detection
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
from config import settings

# Import vision components
from src.vision.detection import ObjectDetector


def main():
    print("=" * 60)
    print("RoboMaster EP - Live YOLO Object Detection Test")
    print("=" * 60)
    print("\nTarget Classes:", settings.OBJECT_CLASSES)
    print("\nPress 'q' to quit")
    print("=" * 60 + "\n")

    # Connect to robot
    print("Connecting to robot...")
    ep_robot = robot.Robot()
    ep_robot.initialize(conn_type="sta")
    print("✓ Connected!\n")

    # Initialize camera
    ep_camera = ep_robot.camera

    # Initialize YOLO detector
    print("Loading YOLO model...")
    detector = ObjectDetector(confidence_threshold=0.5)

    if not detector.load_model():
        print("✗ Failed to load YOLO model!")
        ep_robot.close()
        return

    print("✓ YOLO model loaded!")
    print(f"Model can detect {len(detector.get_supported_classes())} classes")
    print()

    # Start video stream
    print("Starting camera stream...")
    ep_camera.start_video_stream(display=False)
    time.sleep(2)  # Wait for stream to stabilize
    print("✓ Camera stream started!\n")

    frame_count = 0
    detection_count = 0
    start_time = time.time()

    print("Running detection... (Press 'q' to quit)\n")

    try:
        while True:
            # Get frame from camera
            img = ep_camera.read_cv2_image()

            if img is None:
                print("Warning: No frame received")
                continue

            frame_count += 1

            # Run detection every frame (you can reduce this for performance)
            detections = detector.detect_objects(img)

            # Draw detections on frame
            if detections:
                detection_count += len(detections)

                # Print detected objects
                for det in detections:
                    color = (0, 255, 0)  # Green
                    # Highlight target classes in different color
                    if det.class_name in settings.OBJECT_CLASSES:
                        color = (0, 0, 255)  # Red for target objects

                    x1, y1, x2, y2 = det.bbox

                    # Draw bounding box
                    cv2.rectangle(img, (x1, y1), (x2, y2), color, 2)

                    # Draw label with confidence
                    label = f"{det.class_name}: {det.confidence:.2f}"
                    label_size, _ = cv2.getTextSize(label, cv2.FONT_HERSHEY_SIMPLEX, 0.6, 2)

                    # Draw label background
                    cv2.rectangle(
                        img,
                        (x1, y1 - label_size[1] - 10),
                        (x1 + label_size[0], y1),
                        color,
                        -1
                    )

                    # Draw label text
                    cv2.putText(
                        img,
                        label,
                        (x1, y1 - 5),
                        cv2.FONT_HERSHEY_SIMPLEX,
                        0.6,
                        (255, 255, 255),
                        2
                    )

            # Add info overlay
            elapsed_time = time.time() - start_time
            fps = frame_count / elapsed_time if elapsed_time > 0 else 0

            info_text = [
                f"FPS: {fps:.1f}",
                f"Frame: {frame_count}",
                f"Detections: {len(detections) if detections else 0}",
                f"Total: {detection_count}"
            ]

            y_offset = 30
            for i, text in enumerate(info_text):
                cv2.putText(
                    img,
                    text,
                    (10, y_offset + i * 30),
                    cv2.FONT_HERSHEY_SIMPLEX,
                    0.7,
                    (0, 255, 0),
                    2
                )

            # Add target classes info
            target_text = f"Target: {', '.join(settings.OBJECT_CLASSES)}"
            cv2.putText(
                img,
                target_text,
                (10, img.shape[0] - 20),
                cv2.FONT_HERSHEY_SIMPLEX,
                0.6,
                (0, 0, 255),
                2
            )

            # Show frame
            cv2.imshow("YOLO Detection - RoboMaster EP", img)

            # Check for quit
            if cv2.waitKey(1) & 0xFF == ord('q'):
                print("\nQuitting...")
                break

    except KeyboardInterrupt:
        print("\nInterrupted by user")

    finally:
        # Cleanup
        print("\nCleaning up...")
        cv2.destroyAllWindows()
        ep_camera.stop_video_stream()
        ep_robot.close()

        # Statistics
        print("\n" + "=" * 60)
        print("Session Statistics:")
        print("=" * 60)
        print(f"Total Frames: {frame_count}")
        print(f"Total Detections: {detection_count}")
        print(f"Average FPS: {fps:.1f}")
        print(f"Duration: {elapsed_time:.1f}s")
        print("=" * 60)


if __name__ == '__main__':
    main()
