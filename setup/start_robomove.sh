#!/bin/bash

cd /home/aion/workspace/RoboMove
echo "Starting Owl Robo-Dance"

# Base directory
base_dir=$(pwd)

# Terminal 2: launch script
echo "Running map_human_pose.py script..."
gnome-terminal -- bash -c "python3 ${base_dir}/map_human_pose.py"

# Terminal 2: launch script
echo "Running the video feed script..."
gnome-terminal -- bash -c "python3 ${base_dir}/video.py"
