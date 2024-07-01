import cv2 as cv
import imutils
import threading
import winsound

cap=cv.VideoCapture(0,cv.CAP_DSHOW)
cap.set(cv.CAP_PROP_FRAME_WIDTH,640)
cap.set(cv.CAP_PROP_FRAME_HEIGHT,480)

_,start_frame=cap.read()
start_frame=imutils.resize(start_frame,width=500)
start_frame=cv.cvtColor(start_frame,cv.COLOR_BGR2GRAY)
start_frame=cv.GaussianBlur(start_frame,(21,21),0)

alram=False
alram_mode=False
alram_counter=0

def beep_alert():
    global alram
    for _ in range(5):
        if not alram_mode:
            break
        print("ALERT ALERT 👮🚓")
        winsound.Beep(2500,1000)
    alarm=False

while True:
    _,frame=cap.read()
    frame=imutils.resize(frame,width=500)
    
    if alram_mode:
        frame_bw=cv.cvtColor(frame,cv.COLOR_BGR2GRAY)
        frame_bw=cv.GaussianBlur(frame_bw,(5,5),0)
        
        difference=cv.absdiff(frame_bw,start_frame)
        threshold=cv.threshold(difference,25,255,cv.THRESH_BINARY)[1]
        start_frame=frame_bw
        
        if threshold.sum()>420:
            alram_counter=+1
        else:
            if  alram_counter>0:
                alram_counter-=1
        cv.imshow("CAM",threshold)
    else:
        cv.imshow("CAM",frame)
    if alram_counter>20:
        if not alram:
            alram=True
            threading.Thread(target=beep_alert).start()
    key_pressed=cv.waitKey(30)
    if key_pressed==ord("g"):
        alram_mode=not alram_mode
        alram_counter=0
    if key_pressed==ord('x'):
        alram_mode=False
        break
    
    cap.release
    cv.destroyAllWindows()
    
            
        
