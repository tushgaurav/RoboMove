from owl_client import OwlClient, Joint
from utilities import Overlays
import cv2
import time
import numpy as np
import math
import HandTrackingModule as htm

# For testing unsafe code disable the robot (set true)
# Robot Configuration
DISABLE_ROBOT = False
jointSpeed = 50


owl_robot_ip = "10.42.0.54"
client = None

if not DISABLE_ROBOT:
    client = OwlClient(owl_robot_ip)


cap = cv2.VideoCapture(0)
# cap = cv2.VideoCapture('Videos/Hand3.mp4')
pTime = 0

# Owl logo
imgLogo = cv2.imread('Images/owl_logo.png', cv2.IMREAD_UNCHANGED)

detector = htm.handDetector()

prevWrist = 0
prevBase = 0

while True:
    success, img = cap.read()
    img = cv2.resize(img, (0, 0), fx=1.5, fy=1.5)
    # img = cv2.resize(img, (1280, 720))

    img = detector.findHands(img)
    lmList = detector.findPosition(img, draw=False)

    if lmList:
        thumbTip = lmList[4]
        indexTip = lmList[8]

        pinkyTip = lmList[20]
        pinkyMcp = lmList[17]

        middleTip = lmList[12]
        middleMcp = lmList[9]

        distanceThumbIndex = np.round(math.hypot(
            thumbTip[1] - indexTip[1], thumbTip[2] - indexTip[2]), 3)

        distancePinkyMcpPinkyTip = np.round(math.hypot(
            pinkyMcp[1] - pinkyTip[1], pinkyMcp[2] - pinkyTip[2]), 3)

        distanceMiddleMcpMiddleTip = np.round(math.hypot(
            middleMcp[1] - middleTip[1], middleMcp[2] - middleTip[2]), 3)

        print("ThumbIndex Distance: ", distanceThumbIndex)
        print("PinkyMcpPinkyTip Distance: ", distancePinkyMcpPinkyTip)
        print("MiddleMcpMiddleTip Distance: ", distanceMiddleMcpMiddleTip)

        # For wrist
        cv2.line(img, (thumbTip[1], thumbTip[2]),
                 (indexTip[1], indexTip[2]), (255, 0, 255), 3)
        cv2.circle(img, (thumbTip[1], thumbTip[2]),
                   10, (255, 0, 255), cv2.FILLED)
        cv2.putText(img, str(int(distanceThumbIndex)), (thumbTip[1] - 20, thumbTip[2] + 50),
                    cv2.FONT_HERSHEY_PLAIN, 2, (255, 0, 255), 2)
        cv2.putText(img, "Wrist", (indexTip[1] - 20, indexTip[2] + 50),
                    cv2.FONT_HERSHEY_PLAIN, 2, (255, 0, 255), 2)

        # For pinky
        cv2.line(img, (pinkyMcp[1], pinkyMcp[2]),
                 (pinkyTip[1], pinkyTip[2]), (255, 0, 255), 3)
        cv2.circle(img, (pinkyMcp[1], pinkyMcp[2]),
                   10, (255, 0, 255), cv2.FILLED)
        cv2.putText(img, str(int(distancePinkyMcpPinkyTip)), (pinkyMcp[1] - 20, pinkyMcp[2] + 50),
                    cv2.FONT_HERSHEY_PLAIN, 2, (255, 0, 255), 2)
        cv2.putText(img, "Pinky", (pinkyTip[1] - 20, pinkyTip[2] + 50),
                    cv2.FONT_HERSHEY_PLAIN, 2, (255, 0, 255), 2)

        # For middle
        cv2.line(img, (middleMcp[1], middleMcp[2]),
                 (middleTip[1], middleTip[2]), (255, 0, 255), 3)
        cv2.circle(img, (middleMcp[1], middleMcp[2]),
                   10, (255, 0, 255), cv2.FILLED)
        cv2.putText(img, str(int(distanceMiddleMcpMiddleTip)), (middleMcp[1] - 20, middleMcp[2] + 50),
                    cv2.FONT_HERSHEY_PLAIN, 2, (255, 0, 255), 2)
        cv2.putText(img, "Middle", (middleTip[1] - 20, middleTip[2] + 50),
                    cv2.FONT_HERSHEY_PLAIN, 2, (255, 0, 255), 2)

        if not DISABLE_ROBOT:
            wrist = np.round(np.interp(distanceThumbIndex, [
                0, 350], [-1.20, 1.20]), 3)

            base = np.round(np.interp(distancePinkyMcpPinkyTip, [
                0, 350], [-1.54, 1.54]), 3)

            elbow = np.round(np.interp(distanceMiddleMcpMiddleTip, [
                0, 350], [-1.14, 1.14]), 3)

            print("Robot Joint Values --")
            print("Wrist: ", wrist)
            print("Base: ", base)
            print("Elbow: ", elbow)

            print("****\n")

            jointPos = Joint(base, 0, elbow, wrist, 0, 0)
            client.move_to_joint(jointPos, jointSpeed, wait=False)

    # img = cv2.resize(img, (1280, 720))
    # lmg = detector.findPose(img)
    # lmList = detector.findPosition(img, draw=False)

    # if len(lmList) != 0:
    # origin = 0
    # oX, oY = lmList[origin][1], lmList[origin][2]
    # print("Origin: ", oX, oY)
    # markers = [12, 14, 16]

    # # Mapping points
    # rShoulder = [lmList[12][1], lmList[12][2]]
    # rElbow = [lmList[14][1], lmList[14][2]]
    # lElbow = [lmList[13][1], lmList[13][2]]
    # rWrist = [lmList[16][1], lmList[16][2]]

    # distance_rShoulderOrigin = math.hypot(
    #     rShoulder[0] - oX, rShoulder[1] - oY)
    # distance_rElbowOrigin = math.hypot(
    #     rElbow[0] - oX, rElbow[1] - oY)
    # distance_lElbowOrigin = math.hypot(
    #     lElbow[0] - oX, lElbow[1] - oY)
    # distance_rWristsOrigin = math.hypot(
    #     rWrist[0] - oX, rWrist[1] - oY)

    # print("Distance from origin to markers --")
    # print("Origin: ", oX, oY)
    # print("rShoulder: ", distance_rShoulderOrigin)
    # print("rElbow: ", distance_rElbowOrigin)
    # print("lElbow: ", distance_lElbowOrigin)
    # print("rWrist: ", distance_rWristsOrigin)

    # cv2.circle(img, (oX, oY), 15, (0, 100, 255), cv2.FILLED)
    # cv2.circle(img, (rShoulder[0], rShoulder[1]),
    #            10, (0, 0, 255), cv2.FILLED)
    # cv2.circle(img, (rElbow[0], rElbow[1]), 10, (0, 0, 255), cv2.FILLED)
    # cv2.circle(img, (lElbow[0], lElbow[1]), 10, (0, 0, 255), cv2.FILLED)
    # cv2.circle(img, (rWrist[0], rWrist[1]), 10, (0, 0, 255), cv2.FILLED)

    # cv2.line(img, (oX, oY), (rShoulder[0], rShoulder[1]),
    #          (255, 0, 255), 3)
    # cv2.line(img, (rShoulder[0], rShoulder[1]),
    #          (rElbow[0], rElbow[1]), (255, 0, 255), 3)
    # cv2.line(img, (rElbow[0], rElbow[1]),
    #          (rWrist[0], rWrist[1]), (255, 0, 255), 3)

    # cv2.line(img, (oX, oY), (lElbow[0], lElbow[1]), (55, 0, 255), 2)
    # cv2.line(img, (oX, oY), (rElbow[0], rElbow[1]), (55, 0, 255), 2)
    # cv2.line(img, (oX, oY), (rWrist[0], rWrist[1]), (55, 0, 255), 2)

    # if not DISABLE_ROBOT:
    #     base = np.interp(distance_rShoulderOrigin, [
    #         0, 300], [-1.54, 1.54])
    #     shoulder = np.interp(distance_lElbowOrigin, [
    #         0, 300], [-0.54, 0.24])
    #     elbow = np.interp(distance_rElbowOrigin, [
    #         0, 300], [-0.74, 0.74])
    #     wrist = np.interp(distance_rWristsOrigin,
    #                       [0, 300], [-0.54, 0.74])

    #     print("Robot Joint Values --")
    #     print("Base: ", base)
    #     print("Shoulder: ", shoulder)
    #     print("Elbow: ", elbow)
    #     print("Wrist: ", wrist)
    #     print("****\n")

    #     jointPos = Joint(base, shoulder, 0, wrist, elbow, 0)

    #     client.move_to_joint(jointPos, jointSpeed, wait=False)

    cTime = time.time()
    fps = 1 / (cTime - pTime)
    pTime = cTime
    img = Overlays.fpsOverlay(fps, img)
    # img = Overlays.fpsOverlayHighContrast(fps, img)

    img = Overlays.OverlayLogo('Images/owl_logo.png', img, 60, 10, 10)

    cv2.imshow("Orangewood - Realtime View", img)
    if cv2.waitKey(0) == ord('q'):
        break

client.close()
cap.release()
cv2.destroyAllWindows()
