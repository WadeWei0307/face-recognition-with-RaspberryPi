import sys
import cv2
import numpy as np
import threading
sys.path.append("/usr/local/lib/python2.7/dist-packages/")
from firebase import firebase
import dlib

cap = cv2.VideoCapture(0)
detector = dlib.get_frontal_face_detector()# Dlib 的人臉偵測器


url = "https://project-33535.firebaseio.com/"
fb = firebase.FirebaseApplication(url,None)
counter = 0                                             #image counter

def upload(url,frame):
    #img = cv2.imread('C:\\Users\\a0926_000\\Desktop\\images.jpg')   #read image
    #img = cv2.resize(img,(160, 160))
    #print(img)
    #print('\n')
    
    '''                                           
    temp = []
    for i in range(0,160):                         #upload firebase function
        for j in range(0,160):
            temp.append(img[i][j].tolist())
    '''
    
    temp1 = []
    counter = fb.get("/counter",None)
    for key, value in counter.items():
        temp1.append(key)
        temp1.append(value)
        
    print('/counter/' + temp1[0])                           #upload image number
    fb.delete('/counter/' + temp1[0], None)                 #upload image number
    counter = temp1[1] + 1                                  #upload image number
            
    fb.post("/counter",counter)
    fb.post("FACE/face-" + str(counter),frame)                   #post data to database
    
while cap.isOpened():
    ret,frame = cap.read()
    kk = cv2.waitKey(1)
    frame = cv2.flip(frame, 1) #將顯示出來的畫面左右顛倒，不會有鏡像的感覺
    frame = cv2.cvtColor(frame, cv2.COLOR_RGB2GRAY)
    face_rects, scores, idx = detector.run(frame, 0)#偵測人臉   
    for i, d in enumerate(face_rects):    # 取出所有偵測的結果
        x1 = d.left()
        y1 = d.top()
        x2 = d.right()
        y2 = d.bottom()
        if(scores and x1 > 109 and x2 < 541 and y1 > 0 and y2 < 480): 
            #cv2.waitKey(500)
            upload(url,frame)
            #cv2.imwrite("output.jpg",frame)
            #print(frame)
            #print(type(frame))
            '''
            for j in range(x1,x2+1):
                for k in range(y1,y2+1):
                    print(type(frame[k][j]))
                   # frame[k][j]
                   # print(kao)
                   # value = tuple(kao)
                    url = "https://life-with-face.firebaseio.com/"
                    fb = firebase.FirebaseApplication(url,None)
                    fb.post("/identify",frame[k][j])
                 '''
                    
        text = "%2.2f(%d)" % (scores[i], idx[i])
        #cv2.line(frame,(0,0),(511,480),(255,0,0),5) #開始位置，結束位置，顏色，粗度(pixels)
        cv2.rectangle(frame, (x1, y1), (x2, y2), (0, 255, 0), 4, cv2.LINE_AA)# 以方框標示偵測的人臉
        cv2.putText(frame, text, (x1, y1), cv2.FONT_HERSHEY_DUPLEX,
        0.8, (255, 255, 255), 1, cv2.LINE_AA)# 標示分數
        cv2.imshow("Faces", frame)
        cv2.waitKey(1)
    if kk == ord('q'):
        break
cap.release()
cv2.destroyAllWindows()
