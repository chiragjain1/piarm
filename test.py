import os
import sys
import cv2
import math
import time
import datetime
import threading
import numpy as np
import HiwonderSDK.Board as Board
import HiwonderSDK.Misc as Misc
from HiwonderSDK.PID import PID
 
 
def Videodetact():
    servo1_pid = PID(P=0.4, I=0.2, D=0.04)  # pid初始化 #上下
    servo2_pid = PID(P=0.4, I=0.2, D=0.04)  # pid初始化 #左右
    servo1_pulse = 1850
    servo2_pulse = 1500
    img_center_x = 320
    img_center_y = 240
    while True:
        ret, frame = cap.read()
        gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
        faces = face_cascade.detectMultiScale(gray, scaleFactor=1.3, minNeighbors=3)
 
        faceNum = len(faces)
        print("人脸数量: %s" % faceNum)
 
        if len(faces) == 1:
            for faceRect in faces:
                x, y, w, h = faceRect
                cv2.rectangle(frame, (x, y), (x + w, y + h), (255, 255, 0), 2)
                # TODO PID控制舵机
                center_X = x
                center_Y = y
                err = abs(img_center_y - center_Y)  # Y轴误差
                if err < 15:
                    servo1_pid.SetPoint = center_Y
                else:
                    servo1_pid.SetPoint = img_center_y
                servo1_pid.update(center_Y)
                tmp = int(servo1_pulse + servo1_pid.output)
                tmp = 1000 if tmp < 1000 else tmp  # 舵机角度限幅
                servo1_pulse = 2500 if tmp > 2500 else tmp
 
                err = abs(img_center_x - center_X)  # x轴偏差计算
                if err < 20:
                    servo2_pid.SetPoint = 2 * img_center_x - center_X
                else:
                    servo2_pid.SetPoint = img_center_x
                servo2_pid.update(2 * img_center_x - center_X)  # pid计算
                tmp = int(servo2_pulse - servo2_pid.output)
                tmp = 500 if tmp < 500 else tmp
                servo2_pulse = 2500 if tmp > 2500 else tmp
                Board.setPWMServoPulse(1, servo1_pulse, 20)  # 设置舵机角度
                Board.setPWMServoPulse(2, servo2_pulse, 20)
 
        cv2.imshow('Output', frame)
 
        if cv2.waitKey(1) & 0xff == ord('q'):
            break
    cv2.destroyAllWindows()
    cap.release()
 
 
if __name__ == '__main__':
    face_cascade = cv2.CascadeClassifier(
        '/home/pi/ArmPi/haarcascade_frontalface_default.xml')
    # 打开内置摄像头
    cap = cv2.VideoCapture(0)
 
    # 设置视频窗口大小
    cap.set(3, 640)
    cap.set(4, 480)
    faceNum = 0
    Videodetact()
