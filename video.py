import cv2 
import PoseModule as pm
import time
from utilities import Overlays
feed_path = "Videos/moves.mp4"
detection = pm.poseDetector()

cap = cv2.VideoCapture(feed_path)
pTime = 0

def draw_zones(poselist,frame):
    vert_x = poselist[0][1]
    vert_y = poselist[0][2]
    vert_Y = vert_y + 200

    hor_x = poselist[24][1] -100
    hor_y = poselist[24][2]
    hor_X = hor_x + 200

    img = cv2.line(frame,(vert_x,vert_y), ( vert_x,vert_Y),(255,0,0,), 1)
    img = cv2.line(frame,(hor_x,hor_y), (hor_X,hor_y),(255,0,0,), 1)

    return vert_x, hor_y ,img

while True:
    success, frame = cap.read()
    img = cv2.resize(frame,(1080,720))
    detection.findPose(img)
    lmList = detection.findPosition(img)
    if len(lmList)!= 0:
        thres_x, thres_y, img = draw_zones(lmList,img)
    cTime = time.time()
    fps = 1/(cTime-pTime)
    pTime = cTime
    img = Overlays.OverlayLogo('Images/owl_logo.png', img, 60, 10, 10)
    frame = Overlays.OverlayLogo('Images/owl_logo.png', frame, 60, 10, 10)
    cv2.imshow("Orangewood - Detection View", img)
    cv2.imshow("Orangewood - Normal View", frame)
            
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

# When everything done, release the capture and destroy all windows
cap.release()
cv2.destroyAllWindows()
    
