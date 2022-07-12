from unittest import result
import cv2
import mediapipe as mp
import time # To check the frame-rate.


class handDetector():
    def __init__(self, mode = False, maxHands = 2):
        self.mode = mode
        self.maxHands = maxHands

        self.mpHands = mp.solutions.hands
        self.hands = self.mpHands.Hands(self.mode, self.maxHands)
        self.mpDraw = mp.solutions.drawing_utils

        self.color_hand_connection = self.mpDraw.DrawingSpec()
        self.color_hand_connection.color = (57, 255, 20)
        self.color_hand_connection.thickness = 1

        self.color_Lms = self.mpDraw.DrawingSpec()
        self.color_Lms.color = (0, 0, 255)
        self.color_Lms.circle_radius = 2

    def findHands(self, img, draw = True):
        imgRGB = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
        results = self.hands.process(imgRGB)
        if draw:
            if results.multi_hand_landmarks :
                for handLms in results.multi_hand_landmarks :
                    self.mpDraw.draw_landmarks(img, handLms, self.mpHands.HAND_CONNECTIONS, self.color_Lms , self.color_hand_connection)
        return img

    def findPosition(self, img, handNo = 0, draw = True):
        lmList = []
        imgRGB = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
        results = self.hands.process(imgRGB)

        if results.multi_hand_landmarks :
            myHand = results.multi_hand_landmarks[handNo]
            for id, lm in enumerate(myHand.landmark):
                h, w, c = img.shape
                cx, cy = int(lm.x*w), int(lm.y*h)
                lmList.append([id, cx, cy])
                if draw :
                    cv2.circle(img, (cx, cy), 7, (255, 100, 200), cv2.FILLED)
        return lmList

def main():
    pTime = 0
    cTime = 0

    cap = cv2.VideoCapture(0)

    while True :
        success, img = cap.read()

        cTime = time.time()
        fps = 1/(cTime - pTime)
        pTime = cTime

        detector = handDetector()
        img = detector.findHands(img, True)

        cv2.putText(img, f"FPS : {(int(fps))}", (10,70), cv2.FONT_HERSHEY_PLAIN, 3, (255, 100, 0), 2)

        cv2.imshow("Image", img)
        cv2.waitKey(1)
    

if __name__ == "__main__" :
    main()