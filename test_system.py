"""
Test Script for RoboMaster EP Core Object Detection System
Tests individual components before running the full sorting system
"""

import sys
import logging
from pathlib import Path

# Add src to path
sys.path.insert(0, str(Path(__file__).parent / "src"))

from config import settings
from src.robot_control import RobotConnection, RobotCamera
from src.vision import ObjectDetector

# Setup logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)


def test_robot_connection():
    """Test robot connection"""
    logger.info("=" * 50)
    logger.info("Testing Robot Connection")
    logger.info("=" * 50)

    connection = RobotConnection()

    # Try to connect (sta mode - WiFi router)
    if connection.connect(conn_type="sta"):
        logger.info("✓ Robot connection successful!")

        # Get robot info
        info = connection.get_robot_info()
        logger.info(f"Robot Info: {info}")

        # Disconnect
        connection.disconnect()
        return True
    else:
        logger.error("✗ Robot connection failed!")
        return False


def test_camera():
    """Test camera stream"""
    logger.info("=" * 50)
    logger.info("Testing Camera Stream")
    logger.info("=" * 50)

    connection = RobotConnection()

    if not connection.connect(conn_type="sta"):
        logger.error("Cannot test camera - robot not connected")
        return False

    camera = RobotCamera(connection.robot)

    # Start stream
    if camera.start_stream(display=False):
        logger.info("✓ Camera stream started!")

        # Get a frame
        import time
        time.sleep(2)  # Wait for stream to stabilize

        frame = camera.get_frame()
        if frame is not None:
            logger.info(f"✓ Frame captured! Shape: {frame.shape}")

            # Save test image
            import cv2
            test_path = "test_frame.jpg"
            cv2.imwrite(test_path, frame)
            logger.info(f"✓ Test frame saved to {test_path}")

            camera.stop_stream()
            connection.disconnect()
            return True
        else:
            logger.error("✗ Failed to capture frame")
            camera.stop_stream()
            connection.disconnect()
            return False
    else:
        logger.error("✗ Failed to start camera stream")
        connection.disconnect()
        return False


def test_yolo_detection():
    """Test YOLO object detection"""
    logger.info("=" * 50)
    logger.info("Testing YOLO Object Detection")
    logger.info("=" * 50)

    detector = ObjectDetector(confidence_threshold=0.5)

    # Load model
    if detector.load_model():
        logger.info("✓ YOLO model loaded successfully!")
        logger.info(f"Available classes: {len(detector.get_supported_classes())}")
        logger.info(f"Target classes: {settings.OBJECT_CLASSES}")

        # Test with camera if available
        connection = RobotConnection()
        if connection.connect(conn_type="sta"):
            camera = RobotCamera(connection.robot)

            if camera.start_stream(display=False):
                import time
                import cv2

                time.sleep(2)
                frame = camera.get_frame()

                if frame is not None:
                    logger.info("Running detection on live frame...")
                    detections = detector.detect_objects(frame)

                    logger.info(f"✓ Detected {len(detections)} objects")
                    for det in detections:
                        logger.info(f"  - {det}")

                    # Draw and save
                    if detections:
                        vis_frame = detector.draw_detections(frame, detections)
                        cv2.imwrite("test_detection.jpg", vis_frame)
                        logger.info("✓ Detection visualization saved to test_detection.jpg")

                camera.stop_stream()

            connection.disconnect()

        return True
    else:
        logger.error("✗ Failed to load YOLO model")
        logger.info("Make sure to install: pip install ultralytics")
        return False


def main():
    """Run all tests"""
    logger.info("\n" + "=" * 50)
    logger.info("RoboMaster EP Core - System Test")
    logger.info("=" * 50 + "\n")

    results = {
        "Robot Connection": False,
        "Camera Stream": False,
        "YOLO Detection": False
    }

    # Test 1: Robot Connection
    try:
        results["Robot Connection"] = test_robot_connection()
    except Exception as e:
        logger.error(f"Robot connection test failed with error: {e}")

    print()

    # Test 2: Camera
    try:
        results["Camera Stream"] = test_camera()
    except Exception as e:
        logger.error(f"Camera test failed with error: {e}")

    print()

    # Test 3: YOLO Detection
    try:
        results["YOLO Detection"] = test_yolo_detection()
    except Exception as e:
        logger.error(f"YOLO detection test failed with error: {e}")

    # Summary
    print("\n" + "=" * 50)
    print("Test Summary")
    print("=" * 50)
    for test_name, passed in results.items():
        status = "✓ PASSED" if passed else "✗ FAILED"
        print(f"{test_name}: {status}")

    print("=" * 50 + "\n")

    all_passed = all(results.values())
    if all_passed:
        logger.info("🎉 All tests passed! System is ready.")
        logger.info("You can now run: python main.py")
    else:
        logger.warning("⚠ Some tests failed. Please check the errors above.")

    return 0 if all_passed else 1


if __name__ == "__main__":
    sys.exit(main())
