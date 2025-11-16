"""
RoboMaster Movement Module
Handles all robot movement operations (driving, rotating, etc.)
"""

from typing import Tuple
import logging

logger = logging.getLogger(__name__)


class RobotMovement:
    """
    Controls all movement operations of the RoboMaster robot
    """

    def __init__(self, robot):
        """
        Initialize the movement controller

        Args:
            robot: Connected robot instance
        """
        self.robot = robot
        self.chassis = robot.chassis if robot else None

    def move_forward(self, distance: float, speed: float = 0.5) -> bool:
        """
        Move robot forward by specified distance

        Args:
            distance: Distance to move in meters
            speed: Movement speed (0.0 to 1.0)

        Returns:
            bool: True if movement successful
        """
        try:
            if not self.chassis:
                logger.error("Chassis not available - robot not connected")
                return False

            logger.info(f"Moving forward {distance}m at speed {speed}")
            self.chassis.move(x=distance, y=0, z=0, xy_speed=speed).wait_for_completed()
            logger.info("Forward movement completed")
            return True

        except Exception as e:
            logger.error(f"Failed to move forward: {e}")
            return False

    def move_backward(self, distance: float, speed: float = 0.5) -> bool:
        """
        Move robot backward by specified distance

        Args:
            distance: Distance to move in meters
            speed: Movement speed (0.0 to 1.0)

        Returns:
            bool: True if movement successful
        """
        try:
            if not self.chassis:
                logger.error("Chassis not available - robot not connected")
                return False

            logger.info(f"Moving backward {distance}m at speed {speed}")
            self.chassis.move(x=-distance, y=0, z=0, xy_speed=speed).wait_for_completed()
            logger.info("Backward movement completed")
            return True

        except Exception as e:
            logger.error(f"Failed to move backward: {e}")
            return False

    def move_left(self, distance: float, speed: float = 0.5) -> bool:
        """
        Move robot left by specified distance

        Args:
            distance: Distance to move in meters
            speed: Movement speed (0.0 to 1.0)

        Returns:
            bool: True if movement successful
        """
        try:
            if not self.chassis:
                logger.error("Chassis not available - robot not connected")
                return False

            logger.info(f"Moving left {distance}m at speed {speed}")
            self.chassis.move(x=0, y=-distance, z=0, xy_speed=speed).wait_for_completed()
            logger.info("Left movement completed")
            return True

        except Exception as e:
            logger.error(f"Failed to move left: {e}")
            return False

    def move_right(self, distance: float, speed: float = 0.5) -> bool:
        """
        Move robot right by specified distance

        Args:
            distance: Distance to move in meters
            speed: Movement speed (0.0 to 1.0)

        Returns:
            bool: True if movement successful
        """
        try:
            if not self.chassis:
                logger.error("Chassis not available - robot not connected")
                return False

            logger.info(f"Moving right {distance}m at speed {speed}")
            self.chassis.move(x=0, y=distance, z=0, xy_speed=speed).wait_for_completed()
            logger.info("Right movement completed")
            return True

        except Exception as e:
            logger.error(f"Failed to move right: {e}")
            return False

    def rotate(self, angle: float, speed: float = 45.0) -> bool:
        """
        Rotate robot by specified angle

        Args:
            angle: Angle to rotate in degrees (positive = counter-clockwise, negative = clockwise)
            speed: Rotation speed in degrees per second

        Returns:
            bool: True if rotation successful
        """
        try:
            if not self.chassis:
                logger.error("Chassis not available - robot not connected")
                return False

            logger.info(f"Rotating {angle} degrees at speed {speed} deg/s")
            self.chassis.move(x=0, y=0, z=angle, z_speed=speed).wait_for_completed()
            logger.info("Rotation completed")
            return True

        except Exception as e:
            logger.error(f"Failed to rotate: {e}")
            return False

    def move_to_position(self, x: float, y: float, speed: float = 0.5) -> bool:
        """
        Move robot to specific position

        Args:
            x: X coordinate in meters
            y: Y coordinate in meters
            speed: Movement speed (0.0 to 1.0)

        Returns:
            bool: True if movement successful
        """
        try:
            if not self.chassis:
                logger.error("Chassis not available - robot not connected")
                return False

            logger.info(f"Moving to position ({x}, {y}) at speed {speed}")
            self.chassis.move(x=x, y=y, z=0, xy_speed=speed).wait_for_completed()
            logger.info("Position movement completed")
            return True

        except Exception as e:
            logger.error(f"Failed to move to position: {e}")
            return False

    def stop(self) -> bool:
        """
        Stop all robot movement immediately

        Returns:
            bool: True if stop successful
        """
        try:
            if not self.chassis:
                logger.error("Chassis not available - robot not connected")
                return False

            logger.info("Stopping robot movement")
            self.chassis.drive_speed(x=0, y=0, z=0)
            logger.info("Robot stopped")
            return True

        except Exception as e:
            logger.error(f"Failed to stop robot: {e}")
            return False

    def get_current_position(self) -> Tuple[float, float, float]:
        """
        Get current robot position and orientation

        Returns:
            Tuple[float, float, float]: (x, y, angle) position
        """
        try:
            if not self.chassis:
                logger.error("Chassis not available - robot not connected")
                return (0.0, 0.0, 0.0)

            # Note: This requires subscription to chassis position
            # For now, return placeholder
            logger.warning("Position tracking requires chassis subscription - not yet implemented")
            return (0.0, 0.0, 0.0)

        except Exception as e:
            logger.error(f"Failed to get position: {e}")
            return (0.0, 0.0, 0.0)
