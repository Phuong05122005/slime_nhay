import cv2 
import mediapipe as mp
import time
import pyautogui

class Event:
    def __init__(self):
        self.mouse_down = False
        self.count = 0

    def spuat(self, distance1):
        if distance1 < 160 and not self.mouse_down:
            pyautogui.mouseDown() 
            print("đang giữ click chuột nè")
            self.mouse_down = True
        elif distance1 >= 170 and self.mouse_down:
            pyautogui.mouseUp()
            print("xy , xc")
            self.mouse_down = False
            self.count += 1
            print(f"Số lần click chuột: {self.count}")

# nhận diện pose
mpPose = mp.solutions.pose
pose = mpPose.Pose()
# vẽ các khớp nối ra
mpDraw = mp.solutions.drawing_utils

cap = cv2.VideoCapture(0)
pTime = 0

sukien = Event()

while True:
    success,img=cap.read()
    imgRGB = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
    results = pose.process(imgRGB)
    # ghi các điểm kết quả ra
    if results.pose_landmarks:
        mpDraw.draw_landmarks(img, results.pose_landmarks, mpPose.POSE_CONNECTIONS)
        for id, lm in enumerate(results.pose_landmarks.landmark):
            h , w, c = img.shape
            cx, cy = int(w * lm.x), int(h * lm.y)
            
            if id == 24:
                left_hip = [cx, cy]
            if id == 30:
                right_anke = [cx, cy]
        
        distance1 = ((left_hip[0] - right_anke[0]) ** 2 + (left_hip[1] - right_anke[1]) ** 2) ** 0.5
        sukien.spuat(distance1)
                
    #ghi thời gian thực
    cTime=time.time()
    fps = 1/(cTime-pTime)
    pTime = cTime
    cv2.putText(img,str(int(fps)),(10,70),cv2.FONT_HERSHEY_PLAIN,3,(255,255,0),3)
    # vẽ hình chữ nhật và ghi số lần click chuột
    cv2.rectangle(img, (10, h - 40), (200, h - 10), (0, 255, 0), -1)
    cv2.putText(img, f"Clicks: {sukien.count}", (20, h - 15), cv2.FONT_HERSHEY_PLAIN, 2, (255, 255, 255), 2)
    cv2.imshow("RealTime", img)
    # Thoát khỏi vòng lặp 
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

cap.release()
cv2.destroyAllWindows()
