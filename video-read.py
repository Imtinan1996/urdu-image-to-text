import cv2
import numpy as np
import os
from rectangle import Rectangle

videoDirectory='video-library/'
videoName='testvideo1'
extension='.mp4'
imgextension='.jpg'

video=cv2.VideoCapture(videoDirectory+videoName+extension)
videoRunning=True

cropVideo=True

imgCounter=1

if not os.path.exists(videoDirectory+videoName+'images/'):
    os.makedirs(videoDirectory+videoName+'images/')

while videoRunning:

    videoRunning,frame=video.read()
    original=frame.copy()
    if videoRunning is False:
            cv2.destroyAllWindows()
            video.release()
            break
    if cv2.waitKey(25) & 0xFF == ord('q'):
        cv2.destroyAllWindows()
        video.release()
        break
    cv2.imshow('original-video',frame)
    grayframe=cv2.cvtColor(frame,cv2.COLOR_BGR2GRAY)
    
    mser=cv2.MSER_create()
    regions,_=mser.detectRegions(grayframe)
    hulls = [cv2.convexHull(region.reshape(-1, 1, 2)) for region in regions]
    rectangles=[]
    
    for contour in hulls:
        x,y,width,height=cv2.boundingRect(contour)
        temp=Rectangle((x,y,width,height))
        rectangles.append(temp)
    
    stack=[]
    boundingRectangles=[]
    while rectangles:
        newRect=rectangles.pop()
        newRect.pad(3)
        while rectangles:
            tempRect=rectangles.pop()
            copyRect=tempRect
            copyRect.pad(3)
            if newRect.intersects(copyRect):
                newx=min(newRect.x,copyRect.x)
                newy=min(newRect.y,copyRect.y)
                neww=max(copyRect.bottomRight.x,newRect.bottomRight.x)-newx
                newh=max(copyRect.topLeft.y,newRect.topLeft.y)-newy
                newRect=Rectangle((newx,newy,neww,newh))
            else:
                stack.append(tempRect)
        rectangles=stack
        stack=[]
        newRect.unpad(3)
        boundingRectangles.append(newRect)
    #------------------------------
    
    finalRectangles=[]
    stack=[]
    while boundingRectangles:
        newRect=boundingRectangles.pop()
        while boundingRectangles:
            copyRect=boundingRectangles.pop()
            if newRect.intersects(copyRect):
                newx=min(newRect.x,copyRect.x)
                newy=min(newRect.y,copyRect.y)
                neww=max(copyRect.bottomRight.x,newRect.bottomRight.x)-newx
                newh=max(copyRect.topLeft.y,newRect.topLeft.y)-newy
                newRect=Rectangle((newx,newy,neww,newh))
            else:
                stack.append(copyRect)
        boundingRectangles=stack
        stack=[]
        finalRectangles.append(newRect)
    
    
    #------------------CROP CODE----------------------------------
    fh,fw,_=frame.shape
    for box in finalRectangles:
        if box.x<0:
            box.x=0
        if box.y<0:
            box.y=0
        if box.topRight.x>fw:
            box.topRight.x=fw
        if box.topRight.y>fh:
            box.topRight.y=fh
        cv2.rectangle(frame,(box.x,box.y),(box.topRight.x,box.topRight.y),(0,255,0),2)
        if cropVideo is True:
            cropped=original[box.y:box.topRight.y,box.x:box.topRight.x]
            cv2.imwrite(videoDirectory+videoName+'images/'+str(imgCounter)+imgextension,cropped)
            imgCounter+=1
    #videoRunning=False
    cv2.imshow('boxes', frame)
        
        
