"""
RoboMaster EP Core - AI Object Detection and Sorting
Main entry point for the application
"""

import sys
import logging
from pathlib import Path

# Add src to path
sys.path.insert(0, str(Path(__file__).parent / "src"))

from config import settings
from src.robot_control import RobotConnection, RobotMovement, RobotCamera, RobotGripper
from src.vision import ObjectDetector, ImagePreprocessor, ObjectTracker
from src.sorting import SortingController, ClassBasedStrategy, ZoneManager


def setup_logging():
    """
    Configure logging for the application
    """
    logging.basicConfig(
        level=getattr(logging, settings.LOG_LEVEL),
        format=settings.LOG_FORMAT,
        handlers=[
            logging.FileHandler(settings.LOG_FILE),
            logging.StreamHandler(sys.stdout)
        ]
    )
    return logging.getLogger(__name__)


def initialize_robot():
    """
    Initialize robot connection and components

    Returns:
        tuple: (connection, movement, camera, gripper) instances
    """
    logger = logging.getLogger(__name__)
    logger.info("Initializing robot connection...")

    # Connect to robot
    connection = RobotConnection()
    if not connection.connect(settings.ROBOT_IP):
        logger.error("Failed to connect to robot")
        return None, None, None, None

    # Initialize robot components
    movement = RobotMovement(connection.robot)
    camera = RobotCamera(connection.robot)
    gripper = RobotGripper(connection.robot)

    logger.info("Robot initialized successfully")
    return connection, movement, camera, gripper


def initialize_vision():
    """
    Initialize vision components

    Returns:
        tuple: (detector, preprocessor, tracker) instances
    """
    logger = logging.getLogger(__name__)
    logger.info("Initializing vision system...")

    # Use pre-trained YOLOv8n model (model_path=None)
    # If you have a custom model, set DETECTION_MODEL_PATH in settings.py
    import os
    model_path = None if not os.path.exists(settings.DETECTION_MODEL_PATH) else settings.DETECTION_MODEL_PATH

    detector = ObjectDetector(
        model_path=model_path,
        confidence_threshold=settings.DETECTION_CONFIDENCE_THRESHOLD
    )

    # Load detection model
    if not detector.load_model():
        logger.error("Failed to load detection model! Make sure ultralytics is installed.")
        raise RuntimeError("Cannot initialize vision system - model loading failed")

    preprocessor = ImagePreprocessor()
    tracker = ObjectTracker(max_disappeared=settings.MAX_DISAPPEARED_FRAMES)

    logger.info("Vision system initialized successfully")
    return detector, preprocessor, tracker


def initialize_sorting(robot):
    """
    Initialize sorting system

    Args:
        robot: Connected robot instance

    Returns:
        SortingController: Initialized sorting controller
    """
    logger = logging.getLogger(__name__)
    logger.info("Initializing sorting system...")

    # Create sorting strategy
    strategy = ClassBasedStrategy(settings.CLASS_ZONE_MAPPING)

    # Initialize sorting controller
    controller = SortingController(robot, strategy)

    # Setup sorting zones
    for zone_name, zone_config in settings.SORTING_ZONES.items():
        controller.zone_manager.create_zone(
            name=zone_name,
            position=zone_config["position"],
            capacity=zone_config["capacity"]
        )

    logger.info("Sorting system initialized successfully")
    return controller


def main():
    """
    Main application loop
    """
    logger = setup_logging()
    logger.info("=" * 50)
    logger.info("RoboMaster EP Core - AI Object Detection and Sorting")
    logger.info("=" * 50)

    try:
        # Validate settings
        settings.validate_settings()
        logger.info(f"Configuration validated. Target objects: {settings.OBJECT_CLASSES}")

        # Initialize robot
        connection, movement, camera, gripper = initialize_robot()
        if not connection:
            logger.error("Failed to initialize robot. Exiting.")
            return 1

        # Initialize vision system
        detector, preprocessor, tracker = initialize_vision()

        # Initialize sorting system
        sorting_controller = initialize_sorting(connection.robot)

        # Start camera stream
        logger.info("Starting camera stream...")
        if not camera.start_stream(display=False):
            logger.error("Failed to start camera stream")
            return 1

        # Main application loop
        logger.info("=" * 50)
        logger.info("Starting main detection and sorting loop")
        logger.info("Press Ctrl+C to stop")
        logger.info("=" * 50)

        import cv2
        import time

        frame_count = 0
        detection_interval = 30  # Detect every 30 frames to reduce processing load

        try:
            while True:
                # 1. Get frame from camera
                frame = camera.get_frame()
                if frame is None:
                    logger.warning("No frame received, retrying...")
                    time.sleep(0.1)
                    continue

                frame_count += 1

                # Only run detection every N frames
                if frame_count % detection_interval == 0:
                    logger.info(f"Processing frame {frame_count}...")

                    # 2. Preprocess image (optional - can improve detection)
                    processed = preprocessor.preprocess_for_detection(frame)

                    # 3. Detect objects
                    detections = detector.detect_objects(processed)

                    if detections:
                        logger.info(f"Found {len(detections)} objects")

                        # Filter for target classes only
                        target_detections = [
                            obj for obj in detections
                            if obj.class_name in settings.OBJECT_CLASSES
                        ]

                        if target_detections:
                            logger.info(f"Found {len(target_detections)} target objects")

                            # Sort the first detected target object
                            # (In production, you might want to sort all or prioritize)
                            obj_to_sort = target_detections[0]
                            logger.info(f"Attempting to sort: {obj_to_sort}")

                            if sorting_controller.sort_object(obj_to_sort):
                                logger.info("Object sorted successfully!")
                            else:
                                logger.warning("Failed to sort object")

                            # Show statistics
                            stats = sorting_controller.get_sorting_statistics()
                            logger.info(f"Statistics: {stats}")

                # Optional: Display frame with detections (for debugging)
                if settings.ENABLE_VISUALIZATION and frame_count % detection_interval == 0:
                    if detections:
                        vis_frame = detector.draw_detections(frame, detections)
                        cv2.imshow("Detection", vis_frame)
                        cv2.waitKey(1)

                # Small delay to prevent overload
                time.sleep(0.033)  # ~30 FPS

        except KeyboardInterrupt:
            logger.info("\nStopping main loop...")

        finally:
            # Cleanup
            logger.info("Shutting down...")
            if settings.ENABLE_VISUALIZATION:
                cv2.destroyAllWindows()
            camera.stop_stream()
            connection.disconnect()
            logger.info("Shutdown complete")

        return 0

    except KeyboardInterrupt:
        logger.info("\nInterrupted by user")
        return 0
    except Exception as e:
        logger.error(f"Fatal error: {e}", exc_info=True)
        return 1


if __name__ == "__main__":
    sys.exit(main())
