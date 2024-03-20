from owl_client import OwlClient, Joint
import os
import json
import math
class robotMove():

    def __init__(self):
        self.joint_index = 0
        self.DISABLE_ROBOT = False
        self.jointSpeed = 50
        self.owl_robot_ip = "10.42.0.53"
        self.client = None
        self.joint_path =  os.path.join(os.getcwd(),"config/joint.json")

        if not self.DISABLE_ROBOT:
            self.client = OwlClient(self.owl_robot_ip)

    def joint_poses(self,angle_list):
        joint_pose = Joint()
        for i in range(len(angle_list)):
            angle_list[i] = angle_list[i] * math.pi / 180
        joint_pose.Base = angle_list[0]
        joint_pose.Shoulder =angle_list[1]
        joint_pose.Elbow = angle_list[2]
        joint_pose.Wrist3 = angle_list[3]
        joint_pose.Wrist2 = angle_list[4]
        joint_pose.Wrist1 = angle_list[5]

        return joint_pose


    def move_bot(self,joint_index):
        with open("/home/ow-labs/workspaces/symphony/RoboMove/config/joint.json", 'r') as file:
            data = json.load(file)
        
        joint_angles = data[str(joint_index)]
        print(joint_angles)
        poses = self.joint_poses(joint_angles)

        self.client.move_to_joint(poses,self.jointSpeed)
        
        
# if __name__ == "__main__":
#     Move = robotMove()
#     Move.move_bot(1)


        
    

