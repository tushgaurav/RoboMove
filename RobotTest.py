from owl_client import OwlClient, Joint
import random

# Initialize the client with the robot's IP address
owl_robot_ip = "10.42.0.54"  # Replace with your robot's actual IP address
client = OwlClient(owl_robot_ip)

# Ensure the robot is running before sending commands
if client.is_running():
    # Generate random joint angles within the robot's range
    # Note: Replace these ranges with your robot's actual joint limits
    random_joint_values = [
        random.uniform(-1.57, 1.57),  # Base
        random.uniform(-1.57, 1.57),  # Shoulder
        random.uniform(-1.57, 1.57),  # Elbow
        random.uniform(-1.57, 1.57),  # Wrist1
        random.uniform(-1.57, 1.57),  # Wrist2
        random.uniform(-1.57, 1.57)   # Wrist3
    ]

    # Create a Joint object with the random values
    random_joint_position = Joint(*random_joint_values)

    # Move the robot to the random joint position
    jointSpeed = 20  # Define the joint speed (degrees/sec)
    client.move_to_joint(random_joint_position, jointSpeed)

    print("Moved to random joint position:", random_joint_values)
else:
    print("Robot is not running. Please check the robot's status.")

# Remember to close the connection when done
client.close()
