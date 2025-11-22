# -*-coding:utf-8-*-
"""
Optimized YOLO Object Detection Test
Fixed slow camera synchronization with:
- Low resolution (360P)
- Frame skipping
- Buffer flushing
"""

import sys
import cv2
import time
from pathlib import Path

# Add project root to path
project_root = Path(__file__).parent.parent.parent.parent
sys.path.insert(0, str(project_root))
sys.path.insert(0, str(project_root / "src"))

from robomaster import robot, camera
from src.vision.detection import ObjectDetector


def main():
    print("=" * 60)
    print("Optimized YOLO Detection - Fast Camera Mode")
    print("=" * 60)
    print("\nOptimizations:")
    print("  ✓ Low resolution (360P)")
    print("  ✓ Frame skipping")
    print("  ✓ Buffer flushing")
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

    # Start camera with LOW RESOLUTION for better performance
    print("Starting camera stream (360P for speed)...")
    ep_camera.start_video_stream(display=False, resolution=camera.STREAM_360P)

    # Wait longer for stream to stabilize
    time.sleep(3)

    # Flush initial frames
    print("Flushing initial frames...")
    for _ in range(10):
        ep_camera.read_cv2_image()
        time.sleep(0.1)

    print("✓ Camera ready!\n")
    print("Running detection...\n")

    frame_count = 0
    detection_count = 0
    start_time = time.time()
    last_detection_time = time.time()

    # Performance settings
    SKIP_FRAMES = 2  # Process every 3rd frame for speed
    DETECTION_COOLDOWN = 0.5  # Min time between detections in seconds

    try:
        while True:
            # Get frame
            img = ep_camera.read_cv2_image()

            if img is None:
                continue

            frame_count += 1

            # Skip frames for better performance
            if frame_count % SKIP_FRAMES != 0:
                # Just show the frame without detection
                cv2.imshow("YOLO Detection (Optimized)", img)
                if cv2.waitKey(1) & 0xFF == ord('q'):
                    break
                continue

            # Cooldown between detections
            current_time = time.time()
            if current_time - last_detection_time < DETECTION_COOLDOWN:
                cv2.imshow("YOLO Detection (Optimized)", img)
                if cv2.waitKey(1) & 0xFF == ord('q'):
                    break
                continue

            # Run detection
            detections = detector.detect_objects(img)
            last_detection_time = current_time

            # Draw detections
            if detections:
                detection_count += len(detections)

                for det in detections:
                    x1, y1, x2, y2 = det.bbox

                    # Draw box
                    cv2.rectangle(img, (x1, y1), (x2, y2), (0, 255, 0), 2)

                    # Draw label
                    label = f"{det.class_name}: {det.confidence:.2f}"
                    cv2.putText(
                        img,
                        label,
                        (x1, y1 - 10),
                        cv2.FONT_HERSHEY_SIMPLEX,
                        0.6,
                        (0, 255, 0),
                        2
                    )

                # Print to console
                print(f"Frame {frame_count}: Found {len(detections)} objects")
                for det in detections:
                    print(f"  - {det.class_name}: {det.confidence:.2f}")

            # Calculate and show FPS
            elapsed = time.time() - start_time
            fps = frame_count / elapsed if elapsed > 0 else 0

            cv2.putText(
                img,
                f"FPS: {fps:.1f}",
                (10, 30),
                cv2.FONT_HERSHEY_SIMPLEX,
                0.7,
                (0, 255, 0),
                2
            )

            # Show frame
            cv2.imshow("YOLO Detection (Optimized)", img)

            # Minimal wait time
            if cv2.waitKey(1) & 0xFF == ord('q'):
                break

    except KeyboardInterrupt:
        print("\nInterrupted")

    finally:
        # Cleanup
        print("\nCleaning up...")
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


if __name__ == '__main__':
    main()
