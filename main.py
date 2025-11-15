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

    detector = ObjectDetector(
        model_path=settings.DETECTION_MODEL_PATH,
        confidence_threshold=settings.DETECTION_CONFIDENCE_THRESHOLD
    )

    # Load detection model
    if not detector.load_model():
        logger.warning("Failed to load detection model (will use placeholder)")

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

        # TODO: Implement main application loop
        logger.info("System initialized and ready")
        logger.info("Main loop not yet implemented - this is the base project structure")

        # Example of what the main loop would look like:
        # while True:
        #     # 1. Get frame from camera
        #     frame = camera.get_frame()
        #
        #     # 2. Preprocess image
        #     processed = preprocessor.preprocess_for_detection(frame)
        #
        #     # 3. Detect objects
        #     detections = detector.detect_objects(processed)
        #
        #     # 4. Track objects
        #     tracked = tracker.update(detections)
        #
        #     # 5. Sort objects
        #     for obj in detections:
        #         sorting_controller.sort_object(obj)

        # Cleanup
        logger.info("Shutting down...")
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
