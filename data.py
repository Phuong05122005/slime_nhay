import cv2 
import mediapipe as mp
import time
import pyautogui
import mysql.connector

mydb = mysql.connector.connect(
  host="localhost",
  user="yourusername",
  password="yourpassword",
  database="yourdatabase"
)

mycursor = mydb.cursor()

class Event:
    def __init__(self):
        self.mouse_down = False
        self.count = 0

    def spuat(self, distance1):
        if distance1 < 160 and not self.mouse_down:
            pyautogui.mouseDown() 
          
            self.mouse_down = True
        elif distance1 >= 170 and self.mouse_down:
            pyautogui.mouseUp()
          
            self.mouse_down = False
            self.count += 1
            # Lưu số lần count vào mysql
            sql = "INSERT INTO yourtable (count) VALUES (%s)"
            val = (self.count,)
            mycursor.execute(sql, val)
            mydb.commit()

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
                
    cTime=time.time()
    fps = 1/(cTime-pTime)
    pTime = cTime
    cv2.putText(img,str(int(fps)),(10,70),cv2.FONT_HERSHEY_PLAIN,3,(0,240,5),3)
    # Ghi lại số lần spuat
    cv2.rectangle(img, (10, h - 40), (200, h - 10), (55, 20, 255), -1)
    cv2.putText(img, f"Count: {sukien.count}", (20, h - 15), cv2.FONT_HERSHEY_PLAIN, 2, (255, 255, 255), 2)
    
    cv2.imshow("Train Spuat", img)
   
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

cap.release()
cv2.destroyAllWindows()
