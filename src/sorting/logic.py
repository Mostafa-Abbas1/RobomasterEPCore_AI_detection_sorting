"""
Sorting Logic Module
Main controller for object sorting operations
"""

from typing import List, Optional
from ..vision.detection import DetectedObject
from .strategy import SortingStrategy
from .zones import ZoneManager
import logging

logger = logging.getLogger(__name__)


class SortingController:
    """
    Main controller for sorting detected objects
    """

    def __init__(self, robot, strategy: Optional[SortingStrategy] = None):
        """
        Initialize the sorting controller

        Args:
            robot: Connected robot instance
            strategy: Sorting strategy to use
        """
        self.robot = robot
        self.strategy = strategy
        self.zone_manager = ZoneManager()
        self.sorted_objects_count = 0

    def set_strategy(self, strategy: SortingStrategy):
        """
        Set the sorting strategy

        Args:
            strategy: New sorting strategy to use
        """
        self.strategy = strategy
        logger.info(f"Set sorting strategy to {strategy.__class__.__name__}")

    def sort_object(self, detected_object: DetectedObject) -> bool:
        """
        Sort a single detected object

        Args:
            detected_object: Object to sort

        Returns:
            bool: True if sorting successful
        """
        if not self.strategy:
            logger.error("No sorting strategy set")
            return False

        try:
            logger.info(f"Sorting object: {detected_object}")

            # 1. Determine target zone using strategy
            zone_name = self.strategy.determine_zone(detected_object)
            zone = self.zone_manager.get_zone(zone_name)

            if not zone:
                logger.error(f"Zone '{zone_name}' not found")
                return False

            logger.info(f"Target zone: {zone_name}")

            # 2. Navigate to object
            if not self.navigate_to_object(detected_object):
                logger.error("Failed to navigate to object")
                return False

            # 3. Pick up object
            if not self.pick_up_object():
                logger.error("Failed to pick up object")
                return False

            # 4. Navigate to target zone
            zone_position = zone.position
            from ..robot_control import RobotMovement
            movement = RobotMovement(self.robot)
            if not movement.move_to_position(zone_position[0], zone_position[1]):
                logger.error("Failed to navigate to zone")
                return False

            # 5. Place object in zone
            if not self.place_object_in_zone(zone_name):
                logger.error("Failed to place object")
                return False

            self.sorted_objects_count += 1
            logger.info(f"Successfully sorted object to {zone_name}")
            return True

        except Exception as e:
            logger.error(f"Error sorting object: {e}")
            return False

    def sort_objects_batch(self, detected_objects: List[DetectedObject]) -> int:
        """
        Sort multiple detected objects

        Args:
            detected_objects: List of objects to sort

        Returns:
            int: Number of successfully sorted objects
        """
        # TODO: Implement batch sorting
        logger.info(f"Sorting batch of {len(detected_objects)} objects")
        sorted_count = 0

        for obj in detected_objects:
            if self.sort_object(obj):
                sorted_count += 1

        return sorted_count

    def get_sorting_statistics(self) -> dict:
        """
        Get statistics about sorting operations

        Returns:
            dict: Sorting statistics
        """
        # TODO: Implement statistics tracking
        return {
            "total_sorted": self.sorted_objects_count,
            "strategy": self.strategy.__class__.__name__ if self.strategy else None,
            "zones": len(self.zone_manager.zones)
        }

    def reset_statistics(self):
        """
        Reset sorting statistics
        """
        self.sorted_objects_count = 0
        logger.info("Reset sorting statistics")

    def navigate_to_object(self, detected_object: DetectedObject) -> bool:
        """
        Navigate robot to detected object

        Args:
            detected_object: Object to navigate to

        Returns:
            bool: True if navigation successful
        """
        try:
            logger.info(f"Navigating to object at {detected_object.bbox}")

            # Get object center position in image
            center_x, center_y = detected_object.center

            # For now, use simple approach: move forward a fixed distance
            # In production, you would calculate distance based on object size
            # or use depth sensors

            from ..robot_control import RobotMovement
            movement = RobotMovement(self.robot)

            # Simple approach: move forward 0.3m
            # You should adjust this based on actual distance measurement
            success = movement.move_forward(distance=0.3, speed=0.3)

            if success:
                logger.info("Reached object position")
                return True
            else:
                logger.error("Failed to reach object")
                return False

        except Exception as e:
            logger.error(f"Error navigating to object: {e}")
            return False

    def pick_up_object(self) -> bool:
        """
        Pick up object at current position

        Returns:
            bool: True if pickup successful
        """
        try:
            logger.info("Picking up object")

            from ..robot_control import RobotGripper
            gripper = RobotGripper(self.robot)

            # Open gripper
            if not gripper.open(power=50):
                logger.error("Failed to open gripper")
                return False

            # Wait a moment
            import time
            time.sleep(0.5)

            # Close gripper to grab object
            if not gripper.grab_object(power=50):
                logger.error("Failed to grab object")
                return False

            logger.info("Object picked up successfully")
            return True

        except Exception as e:
            logger.error(f"Error picking up object: {e}")
            return False

    def place_object_in_zone(self, zone_name: str) -> bool:
        """
        Place currently held object in specified zone

        Args:
            zone_name: Name of the target zone

        Returns:
            bool: True if placement successful
        """
        try:
            logger.info(f"Placing object in zone '{zone_name}'")

            from ..robot_control import RobotGripper
            gripper = RobotGripper(self.robot)

            # Release object
            if not gripper.release_object(power=50):
                logger.error("Failed to release object")
                return False

            # Update zone count
            zone = self.zone_manager.get_zone(zone_name)
            if zone:
                zone.add_object()

            logger.info("Object placed successfully")
            return True

        except Exception as e:
            logger.error(f"Error placing object: {e}")
            return False
