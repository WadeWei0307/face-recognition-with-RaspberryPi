from picamera.array import PiRGBArray
from picamera import PiCamera
import cv2
import time
import numpy as np
import sys
sys.path.append("/usr/local/lib/python2.7/dist-packages/")
from firebase import firebase

camera = PiCamera()
camera.resolution = (448, 448)
camera.framerate = 40
rawCapture = PiRGBArray(camera, size=(448, 448))
detected = False                                                                     #whether detected
counter = 0                                                                          #image counter
face = []                                                                            #face array
url = "https://project-33535.firebaseio.com/"
fb = firebase.FirebaseApplication(url,None)

display_window = cv2.namedWindow("Faces")
face_cascade = cv2.CascadeClassifier('/home/pi/opencv/data/haarcascades/haarcascade_frontalface_alt2.xml')

for frame in camera.capture_continuous(rawCapture, format="bgr", use_video_port=True):
    
    image = frame.array
    cv2.rectangle(image,(60,30),(388,430),(127,127,0),5)                            #put face in the rectangle
    
    #FACE DETECTION STUFF
    gray = cv2.cvtColor(image,cv2.COLOR_BGR2GRAY)
    faces = face_cascade.detectMultiScale(gray, 1.2, 1)                             #1.2 is search rate(can be modified)
    if (len(faces) != 0):                                                           #detected
        detected = True
        
    if detected:    
        for (x,y,w,h) in faces:
            cv2.rectangle(image,(x,y),(x+w,y+h),(255,0,0),2)
            if( (x>60) & (x+w<388) & (y>30) & (y+h<430)):
                face.append(image[y:y+h,x:x+w])                                     #put face's range into array
                face = np.array(face).reshape(h,w,3)                                #reshape face array
                face = np.array(face, dtype=np.uint8)                               #轉換data type讓imread能夠讀取
                cv2.imshow('My face', face)                                         #show出照片
                
                counterTemp = []                                                    #counter's temp array
                counter = fb.get("/counter",None)                                   #fetch counter's data from database
                for key, value in counter.items():
                    counterTemp.append(key)
                    counterTemp.append(value)
                counterTemp[1] = counterTemp[1] + 1                                 #increase image number
                fb.put('/counter/',counterTemp[0],counterTemp[1])                   #upload image number
                
                cv2.waitKey(1000)                                                   #wait 1 sec to prevent blurring
                #cv2.imwrite("/home/pi/Desktop/faces/face-" + str(counterTemp[1]) + ".jpg", face)    #write pic to particular dir
                        
                temp = []
                for i in range(0,w):                                                #upload firebase function
                    for j in range(0,h):
                        temp.append(face[i][j].tolist())
                fb.post("/FACE/face-" + str(counterTemp[1]),temp)                   #post data to database
                face = []
        
    #DISPLAY TO WINDOW
    cv2.imshow("Faces", image)
    key = cv2.waitKey(1)

    rawCapture.truncate(0)

    if key == 27: #press esc to terminate
        camera.close()
        cv2.destroyAllWindows()
        break