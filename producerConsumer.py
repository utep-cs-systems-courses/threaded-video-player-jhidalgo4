#!/usr/bin/env python3
import cv2
import numpy as np
from threading import Thread
from queueFrame import Queue


#variables
fName = "clip.mp4"
capacity = 10


#takes in file name and queue to file with frames
def extractFrames(fName, fBuffer):
    fCount = 0  #frame count
    
    videoCap = cv2.VideoCapture(fName)
    success, img = videoCap.read()  #read from video file
    print("Reading frame {} {} ".format(fCount, success))
    
    while success:
        success, jpgImage = cv2.imencode('.jpg', img)  #encode img
        fBuffer.post(jpgImage)  #add frame to color queue
        success, img  =  videoCap.read()
        print('Reading frame {} {}'.format(fCount, success))
        fCount += 1  

    #EOF
    fBuffer.post(None)  #done adding to queue
    print("Frame extraction complete")

    
def convertToGrayFrame(colorBuffer, grayBuffer):
    fCount = 0
    
    while True:
        jpgImage = colorBuffer.get()

        #EOF
        if jpgImage is None:
            break
        fCount += 1 
        jpgImage = np.asarray(bytearray(jpgImage), dtype= np.uint8)  #make to np array
        img = cv2.imdecode(jpgImage, cv2.IMREAD_UNCHANGED)
        print("Converting frame {}".format(fCount))

        
        grayImage = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)  #convert gray
        success, jpgImage = cv2.imencode('.jpg', grayImage)
        grayBuffer.post(jpgImage) #add frame to gray queue

    #EOF
    grayBuffer.post(None) #done adding to gray queue
    print("Gray conversion is complete")


#take in a gray frame buffer to display
def displayFrames(fBuffer):
    fCount = 0

    #iter thru frames
    while True:
        jpgImage = fBuffer.get()

        #EOF
        if jpgImage is None:
            break
        fCount += 1
        
        #convert.jpg to np array
        jpgImage = np.asarray(bytearray(jpgImage), dtype = np.uint8)

        #decode .jpg frame encoded
        img = cv2.imdecode(jpgImage, cv2.IMREAD_UNCHANGED)
        print("Displaying frame {}".format(fCount))

        cv2.imshow("Video", img)

        #wait 42ms
        if cv2.waitKey(42) and 0xFF == ord("q"):
            break

    print("DONE displaying gray frames")
    cv2.destroyAllWindows()

    
#######################################################
#2 video-frame queues

colorQueue = Queue(capacity)
grayQueue = Queue(capacity)

extractFrameThread = Thread(target = extractFrames, args = (fName,colorQueue))
grayFrameThread = Thread(target = convertToGrayFrame, args = (colorQueue,grayQueue))
displayThread = Thread(target = displayFrames, args = (grayQueue,))

extractFrameThread.start()  
grayFrameThread.start()  
displayThread.start()
