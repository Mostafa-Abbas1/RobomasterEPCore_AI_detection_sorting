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

## Project Status

- ✅ Detect at least 3 different object types (YOLOv8 integrated)
- ✅ Sort objects autonomously (implemented)
- ✅ Navigate to objects and sorting zones (implemented)
- ✅ Pick and place objects using gripper (implemented)
- ✅ Real-time object tracking (basic implementation)
- ✅ RoboMaster SDK fully integrated
- ✅ Camera streaming and frame capture
- ✅ Main program loop complete

## Quick Start

### 1. Installation

```bash
# Install dependencies
pip install -r requirements.txt
```

This will install:
- RoboMaster SDK
- YOLOv8 (Ultralytics)
- OpenCV
- All other required packages

### 2. Robot Setup

1. Connect your RoboMaster EP Core to your WiFi network using the DJI app
2. Note the robot's IP address (or use auto-discovery)

### 3. Test the System

Before running the full program, test individual components:

```bash
python test_system.py
```

This will test:
- ✓ Robot connection
- ✓ Camera stream
- ✓ YOLO object detection

### 4. Run the Main Program

```bash
python main.py
```

The program will:
1. Connect to the robot
2. Start camera stream
3. Load YOLOv8 model (downloads automatically on first run)
4. Detect objects (bottle, cup, book by default)
5. Sort detected objects into designated zones

## Configuration

Edit `config/settings.py` to customize:

### Object Classes

Currently configured for COCO dataset classes:
```python
OBJECT_CLASSES = [
    "bottle",   # Zone A
    "cup",      # Zone B
    "book"      # Zone C
]
```

You can use any COCO classes: "cell phone", "mouse", "keyboard", "banana", "apple", etc.

### Training Custom Model

To detect custom objects (cube, sphere, cylinder):
1. Collect and label training data
2. Train YOLOv8 model
3. Update `DETECTION_MODEL_PATH` in `config/settings.py`

### Sorting Zones

Adjust zone positions in meters:
```python
SORTING_ZONES = {
    "zone_a": {"position": (1.0, 0.5), "capacity": 10},
    "zone_b": {"position": (1.0, 1.5), "capacity": 10},
    "zone_c": {"position": (1.0, 2.5), "capacity": 10},
}
```

## How It Works

### Detection Pipeline

1. **Camera Stream**: Captures live video from robot camera
2. **YOLO Detection**: YOLOv8 detects objects in each frame
3. **Filtering**: Only target classes are processed
4. **Sorting Decision**: Strategy determines target zone

### Sorting Process

For each detected object:
1. Navigate to object position
2. Open gripper
3. Close gripper to grab object
4. Navigate to target zone
5. Open gripper to release object
6. Update statistics

## Project Goals



## Acknowledgments

- DJI RoboMaster SDK
- OpenCV community
- YOLO object detection framework
