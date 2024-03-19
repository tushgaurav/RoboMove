import cv2 
import PoseModule as pm
import time
from utilities import Overlays

class posemapping():

    def __init__(self):
        self.detection = pm.poseDetector()
        self.move_dict = {}
        self.feed_path = "/home/ow-labs/workspaces/symphony/RoboMove/Videos/moves.MP4"
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


    def feed(self):
        cap = cv2.VideoCapture(self.feed_path)
        pTime = 0

        while True:
            success, img = cap.read()
            img = cv2.resize(img, (1240,720))

            self.detection.findPose(img)
            lmList = self.detection.findPosition(img)
            if len(lmList) != 0:
                move = self.map(lmList)
                # print(type(leftarm))
                # print(*move['left leg'], sep="\n")
                thres_x, thres_y, img = self.draw_zones(lmList,img)
                print(self.zones(move,thres_x=thres_x, thres_y=thres_y))
            cTime = time.time()
            fps = 1/(cTime-pTime)
            pTime = cTime

            # cv2.putText(img, str(int(fps)), (10, 70),
            #             cv2.FONT_HERSHEY_PLAIN, 5, (255, 0, 0), 5)
             # img = Overlays.fpsOverlayHighContrast(fps, img)
            img = Overlays.OverlayLogo('/home/ow-labs/workspaces/symphony/RoboMove/Images/owl_logo.png', img, 60, 10, 10)
            cv2.imshow("Orangewood - Realtime View", img)
            cv2.waitKey(20)


def main():
    map = posemapping()
    map.feed()

if __name__ == "__main__":
    main()