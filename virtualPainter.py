import cv2
import numpy as np
import time
import os
import fingers as fin

folderPath = "TaskBar"
myList = os.listdir(folderPath)
# print(myList)

overlayList = []
for imPath in myList :
    image = cv2.imread(folderPath + "/" + imPath)
    overlayList.append(image)
# print(len(overlayList))

header = overlayList[0]

cap = cv2.VideoCapture(0)
cap.set(3, 1280)
cap.set(4, 720)

detector = fin.handDetector()
brushThickness = 15
xp, yp = 0, 0

imgCanvas = np.zeros((720, 1280, 3), np.uint8) # It has 3 channels, as we want colors, and uint8 means unsigned integer of values from 0 to 255.

def fingersUp(lmList_) :
        fingers = []
        tipIds = [4, 8, 12, 16, 20] # Thumb, index, middle, ring, pinky (tips)
        # For thumb.
        if (lmList_[5][1] < lmList_[17][1] and lmList_[4][1] < lmList_[3][1]):
            fingers.append(1)
        elif (lmList_[5][1] > lmList_[17][1] and lmList_[4][1] > lmList_[3][1]):
            fingers.append(1)
        else:
            fingers.append(0)

        # For fingers. (index, middle, ring, pinky)
        for id in range(1, 5):
            if (lmList_[tipIds[id]][2] < lmList_[tipIds[id]-2][2]):
                fingers.append(1) # If fingers are open
            else:
                fingers.append(0) # If fingers are closed
        return fingers

downloaded = False
drawColor = (255, 100, 100)

def drawOnImg (img) :
    imgGray = cv2.cvtColor(imgCanvas, cv2.COLOR_BGR2GRAY)
    _, imgInv = cv2.threshold(imgGray, 50, 255, cv2.THRESH_BINARY_INV)
    imgInv = cv2.cvtColor(imgInv, cv2.COLOR_GRAY2BGR)
    img = cv2.bitwise_and(img, imgInv)
    img = cv2.bitwise_or(img, imgCanvas)

    return img

while True:
    success, img = cap.read()
    # Flipping the image (mirrorring)
    img = cv2.flip(img, 1)
    mode = 0

    #1. Find hand-Landmarks (with handtracking module)
    img = detector.findHands(img)
    lmList= detector.findPosition(img, draw=False)

    if len(lmList) != 0:
        # print(lmList)
        # Tip of index and middle finger.
        x1, y1 = lmList[8][1:] # Tip of the index.
        x2, y2 = lmList[12][1:] # Tip of middle finger.
        # xp, yp = x1, y1

    #2. Check which fingers are up (we want to draw when only our single finger is up and select when 2 fingers are up.)

    if len(lmList) != 0 :
        fingers = fingersUp(lmList)
        # print(fingers)
        tot = 0
        for i in fingers :
            tot += i
        if tot == 2 and fingers[1] == 1 and fingers[2] == 1 :
            # print("selection mode")
            cv2.circle(img, (x1, y1), 7, (200, 200, 200), 7)
            cv2.circle(img, (x2, y2), 7, (200, 200, 200), 7)
            mode = 2

        elif tot == 1 and fingers[1] == 1:
            # print("Drawing mode")
            cv2.circle(img, (x1, y1), 7, drawColor, 7)
            mode = 1

        else :
            mode = 0
    #3. Import the image (header)

    # As our 'img' is a matrix, we can put the header easily at desired place by slicing the matrix.
    # Setting the header image.
    img[0:120, 0:1280] = header

    #4. If selection mode (If 2 fingers are up), we have to select and not draw, and also if it enters the header, change the header image.

    if (mode == 2) :
        if(y1 < 120) :
            # blue -> 245 - 345
            # red -> 400 - 470
            # yellow -> 500 - 620
            # green -> 650 - 720
            # white -> 760 - 870
            # eraser -> 990 - 1100
            # download -> 
            if (x1 > 245 and x1 < 345):
                header = overlayList[0]
                drawColor = (255, 100, 100)

            elif (x1 > 390 and x1 < 470):
                header = overlayList[1]
                drawColor = (100, 100, 255)

            elif (x1 > 500 and x1 < 610):
                header = overlayList[2]
                drawColor = (0, 215, 255)

            elif (x1 > 650 and x1 < 720):
                header = overlayList[3]
                drawColor = (50, 205, 50)

            elif (x1 > 760 and x1 < 870):
                header = overlayList[4]
                drawColor = (255, 255, 255)

            elif(x1 > 990 and x1 < 1100):
                header = overlayList[5]
                drawColor = (0, 0, 0)

            elif(x1 > 1150 and x1 < 1270):
                if(not downloaded):
                    img = drawOnImg(img)
                    name = "AI_Paint_"+str(time.time())+".png"
                    cv2.imwrite(name, img)
                downloaded = True
                cv2.putText(img, 'Downloaded ...', (500, 190), cv2.FONT_HERSHEY_PLAIN, 4, (0, 100, 0), 5)

            else:
                pass
        else :
            downloaded = False
    #5. Draw when index finger is up.
    if (mode == 1):
        if xp == 0 and yp == 0 :
            xp, yp = x1, y1
        if drawColor == (0, 0, 0) :
            brushThickness = 35
        else :
            brushThickness = 15
        cv2.line(img, (xp, yp), (x1, y1), drawColor, brushThickness)
        cv2.line(imgCanvas, (xp, yp), (x1, y1), drawColor, brushThickness)
        xp, yp = x1, y1

    else:
        xp, yp = 0, 0

    img = drawOnImg(img)

    # img = cv2.addWeighted(img, 0.5, imgCanvas, 0.5, 0)
    cv2.imshow("Image", img)
    # cv2.imshow("Canvas", imgCanvas)
    cv2.waitKey(1)