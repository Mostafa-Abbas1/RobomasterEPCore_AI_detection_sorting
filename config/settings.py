"""
Configuration Settings
Project-wide configuration parameters
"""

import os

# Project paths
PROJECT_ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
SRC_DIR = os.path.join(PROJECT_ROOT, "src")
DATA_DIR = os.path.join(PROJECT_ROOT, "data")
MODELS_DIR = os.path.join(PROJECT_ROOT, "models")
LOGS_DIR = os.path.join(PROJECT_ROOT, "logs")

# Robot connection settings
ROBOT_IP = None  # None for auto-discovery
ROBOT_CONNECTION_TIMEOUT = 10  # seconds

# Camera settings
CAMERA_RESOLUTION = (1280, 720)
CAMERA_FPS = 30

# Vision settings
DETECTION_MODEL_PATH = os.path.join(MODELS_DIR, "yolo_model.pt")
DETECTION_CONFIDENCE_THRESHOLD = 0.5
DETECTION_IOU_THRESHOLD = 0.45

# Supported object classes (minimum 2 for project requirements)
# Note: Using COCO dataset classes from pre-trained YOLOv8
# Selected objects: Easy to find, good detection, grippable
OBJECT_CLASSES = [
    "bottle",      # Plastic bottle - Zone B (RIGHT)
    "cup"          # Cup/Mug - Zone A (LEFT)
]
# Why these objects?
# - Excellent YOLO detection accuracy (>90%)
# - Commonly available for testing
# - Different shapes (cylinder vs cup shape)
# - Easy to grip with RoboMaster gripper
# - Perfect for demonstration
# - Can use multiple bottles/cups for more complex sorting

# If you need a 3rd object class, good alternatives:
# "book", "mouse", "remote", "banana", "apple", "sports ball", etc.

# Tracking settings
MAX_DISAPPEARED_FRAMES = 10
TRACKING_ENABLED = True

# Sorting settings
SORTING_STRATEGY = "class_based"  # Options: class_based, size_based, confidence_based
DEFAULT_ZONE_CAPACITY = 10

# Sorting zones configuration (x, y positions in meters)
# Only 2 zones needed for 2 object types
SORTING_ZONES = {
    "zone_a": {"position": (1.0, 0.5), "capacity": 10},   # Left zone - Cups
    "zone_b": {"position": (1.0, 1.5), "capacity": 10},   # Right zone - Bottles
    "zone_default": {"position": (0.5, 1.5), "capacity": 20}
}

# Class to zone mapping for class-based sorting
CLASS_ZONE_MAPPING = {
    "bottle": "zone_b",      # Bottles go to RIGHT zone
    "cup": "zone_a"          # Cups go to LEFT zone
}

# Movement settings
MOVEMENT_SPEED = 0.5  # 0.0 to 1.0
ROTATION_SPEED = 0.5  # 0.0 to 1.0
NAVIGATION_TOLERANCE = 0.05  # meters

# Gripper settings
GRIPPER_CLOSE_DELAY = 0.5  # seconds
GRIPPER_OPEN_DELAY = 0.5  # seconds

# Logging settings
LOG_LEVEL = "INFO"  # DEBUG, INFO, WARNING, ERROR, CRITICAL
LOG_FORMAT = "%(asctime)s - %(name)s - %(levelname)s - %(message)s"
LOG_FILE = os.path.join(LOGS_DIR, "robomaster_sorting.log")

# Performance settings
ENABLE_GPU = True
IMAGE_PREPROCESSING = True
ENABLE_VISUALIZATION = False  # Show detection visualization

# Safety settings
EMERGENCY_STOP_ENABLED = True
MAX_OPERATION_TIME = 300  # seconds, 0 for unlimited

# Debug settings
DEBUG_MODE = False
SAVE_DEBUG_IMAGES = False
DEBUG_IMAGES_DIR = os.path.join(DATA_DIR, "debug")


def create_directories():
    """
    Create necessary project directories if they don't exist
    """
    dirs = [DATA_DIR, MODELS_DIR, LOGS_DIR]
    if SAVE_DEBUG_IMAGES:
        dirs.append(DEBUG_IMAGES_DIR)

    for directory in dirs:
        os.makedirs(directory, exist_ok=True)


def validate_settings():
    """
    Validate configuration settings

    Returns:
        bool: True if all settings are valid
    """
    # Check if at least 3 object classes are defined (project requirement)
    if len(OBJECT_CLASSES) < 3:
        raise ValueError("Project requires at least 3 object classes")

    # Validate confidence threshold
    if not 0.0 <= DETECTION_CONFIDENCE_THRESHOLD <= 1.0:
        raise ValueError("Detection confidence threshold must be between 0.0 and 1.0")

    # Validate speeds
    if not 0.0 <= MOVEMENT_SPEED <= 1.0:
        raise ValueError("Movement speed must be between 0.0 and 1.0")
    if not 0.0 <= ROTATION_SPEED <= 1.0:
        raise ValueError("Rotation speed must be between 0.0 and 1.0")

    return True


# Initialize on import
create_directories()
