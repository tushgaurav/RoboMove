from owl_client import OwlClient, Joint
import cv2
import time
import numpy as np
import math
import PoseModule as pm

# For testing unsafe code disable the robot (set true)
# Robot Configuration
DISABLE_ROBOT = False
jointSpeed = 50


owl_robot_ip = "10.42.0.54"
client = None

if not DISABLE_ROBOT:
    client = OwlClient(owl_robot_ip)


cap = cv2.VideoCapture(0)
# cap = cv2.VideoCapture('Videos/Dance 2.mp4')
pTime = 0

# Owl logo
imgLogo = cv2.imread('Images/owl_logo.png', -1)
imgLogo = cv2.cvtColor(imgLogo, cv2.COLOR_BGR2GRAY)
imgLogo = cv2.resize(imgLogo, (0, 0), fx=0.5, fy=0.5)
rows, cols = imgLogo.shape
x_offset = 100
y_offset = 100

detector = pm.poseDetector()

while True:
    success, img = cap.read()
    img = cv2.resize(img, (0, 0), fx=2.5, fy=2.5)
    # img = cv2.resize(img, (1280, 720))
    lmg = detector.findPose(img)
    lmList = detector.findPosition(img, draw=False)

    if len(lmList) != 0:
        origin = 0
        oX, oY = lmList[origin][1], lmList[origin][2]
        print("Origin: ", oX, oY)
        markers = [12, 14, 16]

        # Mapping points
        rShoulder = [lmList[12][1], lmList[12][2]]
        rElbow = [lmList[14][1], lmList[14][2]]
        lElbow = [lmList[13][1], lmList[13][2]]
        rWrist = [lmList[16][1], lmList[16][2]]

        distance_rShoulderOrigin = math.hypot(
            rShoulder[0] - oX, rShoulder[1] - oY)
        distance_rElbowOrigin = math.hypot(
            rElbow[0] - oX, rElbow[1] - oY)
        distance_lElbowOrigin = math.hypot(
            lElbow[0] - oX, lElbow[1] - oY)
        distance_rWristsOrigin = math.hypot(
            rWrist[0] - oX, rWrist[1] - oY)

        print("Distance from origin to markers --")
        print("Origin: ", oX, oY)
        print("rShoulder: ", distance_rShoulderOrigin)
        print("rElbow: ", distance_rElbowOrigin)
        print("lElbow: ", distance_lElbowOrigin)
        print("rWrist: ", distance_rWristsOrigin)

        cv2.circle(img, (oX, oY), 15, (0, 100, 255), cv2.FILLED)
        cv2.circle(img, (rShoulder[0], rShoulder[1]),
                   10, (0, 0, 255), cv2.FILLED)
        cv2.circle(img, (rElbow[0], rElbow[1]), 10, (0, 0, 255), cv2.FILLED)
        cv2.circle(img, (lElbow[0], lElbow[1]), 10, (0, 0, 255), cv2.FILLED)
        cv2.circle(img, (rWrist[0], rWrist[1]), 10, (0, 0, 255), cv2.FILLED)

        cv2.line(img, (oX, oY), (rShoulder[0], rShoulder[1]),
                 (255, 0, 255), 3)
        cv2.line(img, (rShoulder[0], rShoulder[1]),
                 (rElbow[0], rElbow[1]), (255, 0, 255), 3)
        cv2.line(img, (rElbow[0], rElbow[1]),
                 (rWrist[0], rWrist[1]), (255, 0, 255), 3)

        cv2.line(img, (oX, oY), (lElbow[0], lElbow[1]), (55, 0, 255), 2)
        cv2.line(img, (oX, oY), (rElbow[0], rElbow[1]), (55, 0, 255), 2)
        cv2.line(img, (oX, oY), (rWrist[0], rWrist[1]), (55, 0, 255), 2)

        if not DISABLE_ROBOT:
            base = np.interp(distance_rShoulderOrigin, [
                0, 300], [-1.14, 1.14])
            shoulder = np.interp(distance_lElbowOrigin, [
                0, 300], [-0.24, 0.24])
            elbow = np.interp(distance_rElbowOrigin, [
                0, 300], [-0.74, 0.74])
            wrist = np.interp(distance_rWristsOrigin,
                              [0, 300], [-0.54, 0.74])

            print("Robot Joint Values --")
            print("Base: ", base)
            print("Shoulder: ", shoulder)
            print("Elbow: ", elbow)
            print("Wrist: ", wrist)
            print("****\n")

            jointPos = Joint(base, shoulder, 0, wrist, elbow, 0)

            client.move_to_joint(jointPos, jointSpeed, wait=False)

    cTime = time.time()
    fps = 1 / (cTime - pTime)
    pTime = cTime
    cv2.putText(img, "FPS: " + str(int(fps)), (70, 50), cv2.FONT_HERSHEY_PLAIN, 1.8,
                (255, 0, 0), 3)

    roi = img[0:rows, 0:cols]
    retval, thresh = cv2.threshold(imgLogo, 125, 25, cv2.THRESH_BINARY)
    mask_Image = cv2.bitwise_not(roi, roi, mask=thresh)
    img[0:rows, 0:cols] = mask_Image

    cv2.imshow("Orangewood - Realtime View", img)
    if cv2.waitKey(40) == ord('q'):
        break

client.close()
cap.release()
cv2.destroyAllWindows()
