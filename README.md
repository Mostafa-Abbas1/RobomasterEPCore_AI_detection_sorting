# RoboMaster EP Core - AI Object Detection and Sorting

A project for the RoboMaster EP Core robot that uses AI-based object detection to identify and sort at least 3 different types of objects.

## Project Overview

This project enables the RoboMaster EP Core to:
- Detect objects using AI/computer vision (YOLO or similar)
- Track objects across video frames
- Sort objects into designated zones based on their class
- Autonomously navigate and manipulate objects using the gripper

## Project Structure

```
RobomasterEPCore_AI_detection_sorting/
│
├── src/
│   ├── robot_control/          # Robot control and communication
│   │   ├── connection.py       # Connect/disconnect from robot
│   │   ├── movement.py         # Movement control (drive, rotate)
│   │   ├── camera.py           # Camera streaming and capture
│   │   └── gripper.py          # Gripper control for object manipulation
│   │
│   ├── vision/                 # Computer vision and AI
│   │   ├── detection.py        # Object detection (YOLO/AI models)
│   │   ├── preprocessing.py    # Image preprocessing and enhancement
│   │   └── tracking.py         # Object tracking across frames
│   │
│   └── sorting/                # Sorting logic
│       ├── logic.py            # Main sorting controller
│       ├── strategy.py         # Sorting strategies (class-based, size-based, etc.)
│       └── zones.py            # Sorting zone management
│
├── config/
│   └── settings.py             # Project configuration
│
├── tests/                      # Unit and integration tests
│
├── data/                       # Data directory (created at runtime)
├── models/                     # AI model files (created at runtime)
├── logs/                       # Log files (created at runtime)
│
├── main.py                     # Main entry point
├── requirements.txt            # Python dependencies
└── README.md                   # This file
```

## Features

### Robot Control
- **Connection Management**: Connect/disconnect from RoboMaster EP Core
- **Movement Control**: Forward/backward movement, rotation, position-based navigation
- **Camera Control**: Video streaming, frame capture, resolution settings
- **Gripper Control**: Open/close gripper, pick and place objects

### Vision System
- **Object Detection**: AI-based object detection using deep learning models
- **Image Preprocessing**: Image enhancement, normalization, noise reduction
- **Object Tracking**: Track objects across multiple frames
- **Multi-class Support**: Detect and classify at least 3 object types (cube, sphere, cylinder)

### Sorting System
- **Multiple Strategies**: Class-based, size-based, and confidence-based sorting
- **Zone Management**: Define and manage multiple sorting zones
- **Sorting Logic**: Autonomous navigation and object placement

## Requirements

- Python 3.6-3.8
- RoboMaster EP Core robot
- RoboMaster SDK
- Computer vision libraries (OpenCV, PyTorch/TensorFlow)
- Pre-trained object detection model (YOLO recommended)

- Read this for detailed installation: https://robomaster-dev.readthedocs.io/en/latest/introduction.html

## Installation

1. Clone the repository:
```bash
git clone <repository-url>
cd RobomasterEPCore_AI_detection_sorting
```

2. Create a virtual environment (recommended):
```bash
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```

3. Install dependencies:
```bash
pip install -r requirements.txt
```

4. Download or train an object detection model and place it in the `models/` directory.

## Configuration

Edit `config/settings.py` to customize:
- Robot connection settings
- Camera resolution and FPS
- Detection confidence threshold
- Object classes to detect
- Sorting zones and their positions
- Movement speeds and tolerances

### Minimum Required Configuration

The project requires at least 3 object classes to be detected:
```python
OBJECT_CLASSES = [
    "cube",
    "sphere",
    "cylinder"
]
```

## Usage

### Basic Usage

Run the main application:
```bash
python main.py
```

### Step-by-Step Implementation Guide

This base project provides the structure. To complete the implementation:

1. **Setup Robot Connection**:
   - Implement the RoboMaster SDK integration in `src/robot_control/connection.py`
   - Test connection to your robot

2. **Implement Camera Streaming**:
   - Complete the camera streaming logic in `src/robot_control/camera.py`
   - Verify you can capture frames

3. **Setup Object Detection**:
   - Choose and train/download a detection model (YOLOv5/v8 recommended)
   - Implement detection in `src/vision/detection.py`
   - Test detection on sample images

4. **Implement Movement**:
   - Complete movement control in `src/robot_control/movement.py`
   - Test basic navigation

5. **Implement Sorting Logic**:
   - Complete the sorting workflow in `src/sorting/logic.py`
   - Define sorting zones based on your environment
   - Integrate gripper control

6. **Test and Refine**:
   - Test individual components
   - Run integration tests
   - Adjust parameters for optimal performance

## Project Goals

- ✅ Detect at least 3 different object types
- ⏳ Sort objects autonomously
- ⏳ Navigate to objects and sorting zones
- ⏳ Pick and place objects using gripper
- ⏳ Real-time object tracking



## Acknowledgments

- DJI RoboMaster SDK
- OpenCV community
- YOLO object detection framework
