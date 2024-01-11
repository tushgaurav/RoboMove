# RoboMove - Orangewood Robotic Arm Computer Vision Control

## Overview
This project is a computer vision control system for the Orangewood Robotic Arm. The system uses a USB cameras or sample videos from the video directory to control the movement of the robotic arm. The system is implemented in Python and uses OpenCV for computer vision, [Mediapipe](https://developers.google.com/mediapipe) for the models and [OwlRobot Client](https://owldoc.bitbucket.io/) for serial communication with the arm.

## Components
1. **RobotDance.py** - The main file for making the robot dance by detecting the users hand movements and poses.
2. **RobotControl.py** - The main file for controlling the robot using the users finger movements.
![RobotControl](/Images/Screenshots/RobotControl1.png)

## Installation
Make sure that you have Python 3.8 installed on your system. Note that other Python version are not compatible. You can install Python 3.8 from [here](https://www.python.org/downloads/release/python-380/).

Activate your virtual environment and install the required packages using the following command:
```
python -m venv env && source env/bin/activate
pip install -r requirements.txt
```

## Usage
To run the system, use the following command:
```
python RobotDance.py
python RobotMove.py
```

## Demo
![RobotDance](/Images/Screenshots/RobotControl2.png)