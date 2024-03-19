import cv2
import mediapipe as mp
import time
import numpy as np
from mediapipe import solutions


class poseDetector():

    def __init__(self, mode=False, smooth=True, detectionCon=0.5, trackCon=0.5):
        self.mode = mode
        self.smooth = smooth
        self.detectionCon = detectionCon
        self.trackCon = trackCon

        self.mpDraw = mp.solutions.drawing_utils
        self.mpPose = mp.solutions.pose

        # # # # # #
        # Solution APIs
        # # # # # #
        # static_image_mode=False,
        # model_complexity=1,
        # smooth_landmarks=True,
        # enable_segmentation=False,
        # smooth_segmentation=True,
        # min_detection_confidence=0.5,
        # min_tracking_confidence=0.5,

        self.pose = self.mpPose.Pose(
            self.mode, 1, self.smooth, False, True, min_detection_confidence=self.detectionCon, min_tracking_confidence=self.trackCon)

    def findPose(self, img, draw=True):
        imgRGB = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
        self.results = self.pose.process(imgRGB)
        if self.results.pose_landmarks:
            if draw:
                self.mpDraw.draw_landmarks(img, self.results.pose_landmarks,
                                           self.mpPose.POSE_CONNECTIONS)
        return img

    def findPosition(self, img, draw=False):
        lmList = []
        if self.results.pose_landmarks:
            for id, lm in enumerate(self.results.pose_landmarks.landmark):
                h, w, c = img.shape
                # print(id, lm)
                cx, cy = int(lm.x*w), int(lm.y*h)
                lmList.append([id, cx, cy])
                if draw:
                    cv2.circle(img, (cx, cy), 5, (0, 255, 0), cv2.FILLED)

        return lmList
    

def main():
    cap = cv2.VideoCapture('/home/ow-labs/workspaces/symphony/RoboMove/test_videos/1.mp4')
    pTime = 0
    detector = poseDetector()

    while True:
        success, img = cap.read()
        img = cv2.resize(img, (640,480))

        detector.findPose(img)
        lmList = detector.findPosition(img)
        print(lmList)

        # cTime = time.time()
        # fps = 1/(cTime-pTime)
        # pTime = cTime

        # cv2.putText(img, str(int(fps)), (10, 70),
        #             cv2.FONT_HERSHEY_PLAIN, 5, (255, 0, 0), 5)

        cv2.imshow("Image", img)
        cv2.waitKey(20)


if __name__ == "__main__":
    main()
