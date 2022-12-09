

# we need to mark our region of interst
# we need to write a program to select or deselect area from image

import cv2 as cv
import pickle

img = cv.imread("carParkImg.png")

width, height = 107, 48

try:    
    with open("CarParkPos", "rb") as f:
        posList = pickle.load(f)
except:
    posList = []

def mouseClick(events, x, y, flags, params):
    # if event is left click button then get the x and y pos 
    if events == cv.EVENT_LBUTTONDOWN:
        posList.append((x,y))
    # if event is right click button 
    if events == cv.EVENT_RBUTTONDOWN:
        
        for i, pos in enumerate(posList):
            
            x1,y1 = pos
            
            if x1 < x < x1 + width and y1 < y< y1 + height:
                posList.pop(i)

    # we are going to add the pos in pickle object
    with open("CarParkPos", "wb") as f:
        pickle.dump(posList, f)

while True:
    img = cv.imread("carParkImg.png") 

    # this will create reactangle
    for pos in posList:
        cv.rectangle(img, pos, (pos[0]+width, pos[1]+height), (0,255,255),2)
    # we need to create a reactangle to find the slot
    # cv.rectangle(img, (50,192), (157, 240), (0,255,255),2)

    cv.imshow("image", img)
    # now we need to detect mouse click
    cv.setMouseCallback("image", mouseClick)

    k = cv.waitKey(1)

    if k == ord("q"):
        cv.destroyAllWindows()
        break
