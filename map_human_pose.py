import cv2 
import PoseModule as pm
import time
from utilities import Overlays
from movements import robotMove
from collections import Counter
import base64
class posemapping():

    def __init__(self):
        self.detection = pm.poseDetector()
        self.move_dict = {}
        self.feed_path = "Videos/moves.mp4"
        self.imgLogo = cv2.imread('Images/owl_logo.png', cv2.IMREAD_UNCHANGED)



    def map(self,poselist):
        for i in range (len(poselist)):
            # Map left arm points
            if poselist[i][0] in [14, 16, 20]:
                self.append_to_dict('left arm', poselist[i])

            # Map right arm points
            if poselist[i][0] in [13, 15, 19]:
                self.append_to_dict('right arm', poselist[i])   

            # Map left leg points
            if poselist[i][0] in [26, 28, 32]:
                self.append_to_dict('left leg', poselist[i])   
                
            # Map right leg points
            if poselist[i][0] in [25, 27, 31]:
                self.append_to_dict('right leg', poselist[i])   

        return self.move_dict
    

    def zones(self, limbs_dict, thres_x, thres_y):
        zones = [0,0,0,0]
        for point in limbs_dict['left arm']:
            x, y = point[1], point[2]  # Assuming point[2] is the y-coordinate
            if x < thres_x and y < thres_y:
                zone = 1
            elif x < thres_x and y > thres_y:
                zone = 2
            elif x > thres_x and y < thres_y:
                zone = 3
            elif x > thres_x and y > thres_y:
                zone = 4
            else:
                zone = None  # For cases that do not match any condition, if any
            zones[0] = zone
        
        for point in limbs_dict['right arm']:
            x, y = point[1], point[2]  # Assuming point[2] is the y-coordinate
            if x < thres_x and y < thres_y:
                zone = 1
            elif x < thres_x and y > thres_y:
                zone = 2
            elif x > thres_x and y < thres_y:
                zone = 3
            elif x > thres_x and y > thres_y:
                zone = 4
            else:
                zone = None  # For cases that do not match any condition, if any
            zones[1] = zone

        for point in limbs_dict['left leg']:
            x, y = point[1], point[2]  # Assuming point[2] is the y-coordinate
            if x < thres_x and y < thres_y:
                zone = 1
            elif x < thres_x and y > thres_y:
                zone = 2
            elif x > thres_x and y < thres_y:
                zone = 3
            elif x > thres_x and y > thres_y:
                zone = 4
            else:
                zone = None  # For cases that do not match any condition, if any
            zones[2] = zone

        for point in limbs_dict['right leg']:
            x, y = point[1], point[2]  # Assuming point[2] is the y-coordinate
            if x < thres_x and y < thres_y:
                zone = 1
            elif x < thres_x and y > thres_y:
                zone = 2
            elif x > thres_x and y < thres_y:
                zone = 3
            elif x > thres_x and y > thres_y:
                zone = 4
            else:
                zone = None  # For cases that do not match any condition, if any
            zones[3] = zone
        
        return zones
  
    def dance_moves(self,zone):
        if zone == [1,3,2,2]:
            robotMove().move_bot(1)
        if zone == [2, 4, 2, 4]:
            robotMove().move_bot(2)
        if zone == [1, 4, 2, 4]:
            robotMove().move_bot(3)
    
    
    def append_to_dict(self, key, data):
        # Check if key exists in the dictionary, create it if not
        if key not in self.move_dict:
            self.move_dict[key] = []
        # Now it's safe to append the data
        self.move_dict[key].append(data)

    def draw_zones(self,poselist,frame):
        vert_x = poselist[0][1]
        vert_y = poselist[0][2]
        vert_Y = vert_y + 200

        hor_x = poselist[24][1] -100
        hor_y = poselist[24][2]
        hor_X = hor_x + 200

        img = cv2.line(frame,(vert_x,vert_y), ( vert_x,vert_Y),(255,0,0,), 1)
        img = cv2.line(frame,(hor_x,hor_y), (hor_X,hor_y),(255,0,0,), 1)

        return vert_x, hor_y ,img
    
    def find_most_common_elements(self,list_of_lists):
        if not list_of_lists:
          return []
    
        # Assuming all lists have the same length, if lists have variable lengths, adjust accordingly.
        list_length = len(list_of_lists[0])
        most_common_elements = []
    
        for i in range(list_length):
            # Collect the ith element from each of the last six lists
            ith_elements = [lst[i] for lst in list_of_lists]
            # Find the most common element for this position
            most_common = Counter(ith_elements).most_common(1)[0][0]
            most_common_elements.append(most_common)
    
        return most_common_elements

    def camera_feed(self):
        cap = cv2.VideoCapture(0)
        pTime = 0

        while True:
            success, frame = cap.read()
            img = cv2.resize(frame, (1080,720))
            cTime = time.time()
            fps = 1/(cTime-pTime)
            pTime = cTime
            img = Overlays.OverlayLogo('Images/owl_logo.png', img, 60, 10, 10)
            cv2.imshow("Orangewood - Detection View", img)
            cv2.imshow("Orangewood - Normal View", frame)
            
            cv2.waitKey(20)


    def feed(self):
        cap = cv2.VideoCapture(self.feed_path)
        pTime = 0

        while True:
            success, frame = cap.read()
            img = cv2.resize(frame, (1080,720))
            frame = cv2.resize(frame, (1080,720))

            _,buffer = cv2.imencode('.jpg',img)
            jpg_to_text = base64.b64encode(buffer)

            self.detection.findPose(img)
            lmList = self.detection.findPosition(img)
            if len(lmList) != 0:
                move = self.map(lmList)
                thres_x, thres_y, img = self.draw_zones(lmList,img)
                all_generated_lists = []
                all_generated_lists.append(self.zones(move,thres_x=thres_x, thres_y=thres_y))
                last_six_lists = all_generated_lists[-6:]
                most_common_in_last_six = self.find_most_common_elements(last_six_lists)
                print(most_common_in_last_six)
                # break
                # self.dance_moves(most_common_in_last_six)
                

            # cTime = time.time()
            # fps = 1/(cTime-pTime)
            # pTime = cTime
            # img = Overlays.OverlayLogo('Images/owl_logo.png', img, 60, 10, 10)
            # # cv2.imshow("Orangewood - Detection View", img)
            # # cv2.imshow("Orangewood - Normal View", frame)
            
            cv2.waitKey(20)


def main():
    map = posemapping()
    map.feed()

if __name__ == "__main__":
    main()