import imp
import cv2
import time 
import os 
import HandTrackingModule as htm

print('download ok')

wCam,hCam=640,480
#stream = "rtsp://root:80661707@192.168.33.169:554/axis-media/media.amp?"
#stream = 0
cap=cv2.VideoCapture(0)   # 選擇第一隻攝影機 
cap.set(3,wCam)
cap.set(4,wCam)

cwd = os.getcwd()
print(cwd)   #C:\Users\elisa\Documents\python\H\v  #路徑這個東西很容易看錯請善用ctrl c ctrl v 

folderPath=r"C:\Users\elisa\Documents\python\HandTrackingProject\FingerImages"     
myList=os.listdir(folderPath)
print(myList)

overlayList=[]
for imPath in myList:
    image=cv2.imread(f'{folderPath}/{imPath}')
    print(f'{folderPath}/{imPath}')     #C:\Users\elisa\Documents\python\H\F/one.png
    overlayList.append(image)

print(len(overlayList))
pTime=0

detector =htm.handDetector(detectionCon=0.75) #呼叫另外一隻

tipIds=[4,8,12,16,20]   #大拇指的頂是4 食指頂是8 中指的頂是12......


while True:
    success,img =cap.read()   # 從攝影機擷取一張影像
    img=detector.findHands(img)  #呼叫另外一隻
    lmList=detector.findPosition(img, draw=False)
    #print(lmList)  #should show parameter in terminal

    




    if len(lmList) !=0:
        fingers=[]
        
        #thumb 
        if lmList[tipIds[0]][1]>lmList[tipIds[0]-1][1]:
            fingers.append(1)
        else:
            fingers.append(0)

        # 4 fingers
        for id in range(1,5):   #大拇指很難識別
            if lmList[tipIds[id]][2]<lmList[tipIds[id]-2][2]:
                fingers.append(1)
            else:
                fingers.append(0)

        totalFingers=fingers.count(1)
        print(totalFingers)




        h,w,c=overlayList[totalFingers - 1].shape
        #img[0:h,0:w]=overlayList[0]  #完全沒有調整空間 必須剛剛好一樣
        img[0:h,0:w]=overlayList[totalFingers-1]

    cTime=time.time()
    fps=1/(cTime-pTime)
    pTime=cTime

    cv2.putText(img, f'FPS:{int(fps)}',(400,70),cv2.FONT_HERSHEY_PLAIN,3,(255,0,0),3)  

    cv2.imshow('Image',img)   # 開新視窗顯示圖片
    #print ('new windows')    # 因為是一直更新所以不能寫print 不然會被log 寫滿
    
    if cv2.waitKey(1) & 0xFF == ord('q'):  #cv2.waitkey是OpenCV內置的函式，用途是在給定的時間內(單位毫秒)等待使用者的按鍵(q)觸發，否則持續循環 0xFF是十六進制常數不必深入理解，此處是為了防止BUG 
        break
cap.release()   #彈出視窗一併關掉
