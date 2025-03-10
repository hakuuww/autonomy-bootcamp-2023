"""
BOOTCAMPERS TO COMPLETE.

Travel to designated waypoint.
"""
# Disable for bootcamp use
# pylint: disable=unused-import


from .. import commands
from .. import drone_report
from .. import drone_status
from .. import location
from ..private.decision import base_decision


# Disable for bootcamp use
# pylint: disable=unused-argument,line-too-long


# All logic around the run() method
# pylint: disable-next=too-few-public-methods
class DecisionSimpleWaypoint(base_decision.BaseDecision):
    """
    Travel to the designed waypoint.
    """
    def __init__(self, waypoint: location.Location, acceptance_radius: float):
        """
        Initialize all persistent variables here with self.
        """
        self.waypoint = waypoint
        print("Waypoint: " + str(waypoint))

        self.acceptance_radius = acceptance_radius

        # ============
        # ↓ BOOTCAMPERS MODIFY BELOW THIS COMMENT ↓
        # ============

        # Helper function for determining relative distance to travel
    def get_set_relative_distance_command(waypoint_position: location.Location, 
                                          report_position: location.Location) -> commands.Command:     
            
        x_distance = waypoint_position.location_x - report_position.location_x
        y_distance = waypoint_position.location_y - report_position.location_y

        set_relative_destination_command = commands.Command.create_set_relative_destination_command(x_distance, y_distance)

        return set_relative_destination_command
        
    def validate_arrival_at_destination(flight_position: location.Location, 
                                        destination_position: location.Location):
        if abs(flight_position.location_x - destination_position.location_x) > 0.01:
            return False
        if abs(flight_position.location_y - destination_position.location_y) > 0.01:
            return False
        return True

        # ============
        # ↑ BOOTCAMPERS MODIFY ABOVE THIS COMMENT ↑
        # ============

    def run(self,
            report: drone_report.DroneReport,
            landing_pad_locations: "list[location.Location]") -> commands.Command:
        """
        Make the drone fly to the waypoint.

        You are allowed to create as many helper methods as you want,
        as long as you do not change the __init__() and run() signatures.

        This method will be called in an infinite loop, something like this:

        ```py
        while True:
            report, landing_pad_locations = get_input()
            command = Decision.run(report, landing_pad_locations)
            put_output(command)
        ```
        """
        # Default command
        command = commands.Command.create_null_command()

        # ============
        # ↓ BOOTCAMPERS MODIFY BELOW THIS COMMENT ↓
        # ============

        # Do something based on the report and the state of this class...

        """
        a function to calculate the relative distance that we need to travel based on the difference between current position and the destination
        
        if the status = moving
                if reached destination
                    return a halt command
            return a null comand
    
        if the status is halted
            the drone might have reached the destination 
            see if there is a new destination
            calculate whether the drone has arrived at the destination
            if yes then 
                return a land command (the simulator will end)
            if not then pass in the new destination
            
        The difference between the coordinates of the drone position and waypoint under the text file in log/ should be less than 0.1
        
        """
        default_null_command = commands.Command.create_null_command()
        halt_command = commands.Command.create_halt_command()
        land_command = commands.Command.create_land_command()

        if report.status == drone_status.DroneStatus.MOVING:
            if self.validate_arrival_at_destination(report.position, self.waypoint):
                return halt_command
            else:
                return default_null_command

        if report.status == drone_status.DroneStatus.HALTED:
            if self.validate_arrival_at_destination(report.position, self.waypoint):
                return land_command
            else:
                set_relative_destination_command_result = self.get_set_relative_distance_command(
                    self.waypoint, 
                    report.position,
                )
                return set_relative_destination_command_result

        if report.status == drone_status.DroneStatus.LANDED:
            return default_null_command

        # Detection: Detects landing pad on camera image.

        # Geolocation: Converts bounding boxes to locations.

        # Display: Displays the camera image and drone information.

        #   DroneReport
        #       -  status
        #       -  destination
        #       -  position

        # ============
        # ↑ BOOTCAMPERS MODIFY ABOVE THIS COMMENT ↑
        # ============

        return command
