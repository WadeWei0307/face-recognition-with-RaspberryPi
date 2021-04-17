import cv2
import numpy as np
import sys
sys.path.append("/usr/local/lib/python2.7/dist-packages/")
from firebase import firebase

url = "https://project-33535.firebaseio.com/"
fb = firebase.FirebaseApplication(url,None)

#fb.delete('counter', None)                                              #delete selected data
fb.delete('face-1', None)

#counter = 0
#fb.post("/counter",counter)

'''
tmp = []
counter = fb.get("/counter",None)                                    #fetch the newset counter
for key, value in counter.items():
    tmp.append(key)
    tmp.append(value)
face = fb.get("/FACE/face-" + str(tmp[1]),None)                      #get the newset data from database

list = []                                                            #empty list
for key, value in face.items(): 
    list.append(value)
image = np.array(list)
image = np.array(list).reshape(46,46,3)
#print(image)
#print((img == image).all())                                         #檢查抓下來之陣列是否跟原陣列一樣


image = np.array(image, dtype=np.uint8)                              #轉換data type讓imread能夠讀取
cv2.imshow('My Image', image)                                        #show出照片
cv2.waitKey(0)
cv2.destroyAllWindows()
'''