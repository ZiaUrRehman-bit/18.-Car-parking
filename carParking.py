
import cv2 as cv
import pickle
import numpy as np

# video feed
cap = cv.VideoCapture("carPark.mp4")

# import the position list
with open("CarParkPos", "rb") as f:
    posList = pickle.load(f)

width, height = 107, 48

def checkParkingSpace(imgPro):
    spaceCounter = 0

     # this will create reactangle
    for pos in posList:
        # now we crop the each image and find out the insdie there is car or not
        x, y = pos

        imgCrop = imgPro[y:y+height, x:x+width]

        # cv.imshow(str(x*y), imgCrop)
        # now we count none zero pixels 
        count = cv.countNonZero(imgCrop)
        # now we write this count no infront of box
        cv.putText(frame, str(count), (x, y+height-10), cv.FONT_HERSHEY_COMPLEX_SMALL,
                    1, (0,0,255), 1)

        # now check the count, as if there is no car then the
        # count value is smaller as compare to when there is car
        if count < 900:
            color = (0,255,0) # we change the color of box to green
            thickness = 4
            spaceCounter +=1
        else:
            color = (0,0,255)
            thickness = 2
        
        cv.rectangle(frame, pos, (pos[0]+width, pos[1]+height), color,thickness)

    cv.putText(frame, f"Empty Spaces are {spaceCounter}", (20,40),
                cv.FONT_HERSHEY_PLAIN, 2, (255, 0 ,255), 3)


kernel = np.ones((3,3), "uint8")
while True:

    # check if running frames is equal to total num of frames then makes running frames = 0 so 
    # that we can replay the video agian and again
    if cap.get(cv.CAP_PROP_POS_FRAMES) == cap.get(cv.CAP_PROP_FRAME_COUNT):
        cap.set(cv.CAP_PROP_POS_FRAMES,0)

    Success, frame = cap.read()

    imgGray = cv.cvtColor(frame, cv.COLOR_BGR2GRAY)
    imgBlur = cv.GaussianBlur(imgGray, (3,3), 1)

    imgThres = cv.adaptiveThreshold(imgBlur, 255, cv.ADAPTIVE_THRESH_GAUSSIAN_C, cv.THRESH_BINARY_INV, 25, 16)

    imgMedian = cv.medianBlur(imgThres, 5)
    imgDilate = cv.dilate(imgMedian, kernel, iterations=1)
   

    # so first thing is that we have to import all positon we have
    checkParkingSpace(imgDilate)
    
    # draw the reactangle
    # for pos in posList:
        # cv.rectangle(frame, pos, (pos[0]+width, pos[1]+height), (0,255,255),2)

    cv.imshow("frame", frame)
    # cv.imshow("frame2", imgThres)
    # cv.imshow("frame3", imgMedian)
    # cv.imshow("frame4", imgDilate)
    k = cv.waitKey(10)

    if k == ord("q"):
        cv.destroyAllWindows()
        break