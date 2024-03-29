#!/usr/bin/python3
# coding=utf8
import sys
sys.path.append('/home/pi/ArmPi/')
import cv2
import time
import Camera
import threading
from LABConfig import *
from ArmIK.Transform import *
from ArmIK.ArmMoveIK import *
import HiwonderSDK.Board as Board
from CameraCalibration.CalibrationConfig import *
from perception import Perception
import math 
import time 


class Motion():
    def __init__(self):
        self.AK = ArmIK()
        self.perception = Perception()
        self.detected_object = False
        self.count_second = 0
        self.first_move = True
        self.action_finish = True
        self.start_pick_up = False
        self.servo_1 = 500
        self.rotation_angle = 0 
        self.coordinate = {
        'red':   (-15 + 0.5, 12 - 0.5, 1.5),
        'green': (-15 + 0.5, 6 - 0.5,  1.5),
        'blue':  (-15 + 0.5, 0 - 0.5,  1.5),
        }

    def go_to_location (self,coordinates,alpha, alpha1, alpha2, movetime = None ):
            result = self.AK.setPitchRangeMoving(coordinates, alpha, alpha1, alpha2, movetime)
            return result
    
    def detect_object(self, color, my_camera):
        world_x, world_y = self.perception.get_coordinates(color, my_camera)
        return (world_x, world_y)

    def first_to_object (self, color, my_camera):
        #put in full code to run this if its the first move 
        while not self.detected_object: 
            self.world_x, self.world_y = self.detect_object(color, my_camera)
            self.detected_object = True 
        result = self.go_to_location((self.world_x, self.world_y-2, 12), -90, -90, 0)
        if result == False:
            self.unreachable = True  
        else: 
            self.unreachable = False
        time.sleep(result[2]/1000) #wait a little while 
        self.start_pick_up = False 
        self.first_move = False
        self.action_finished = True 
    
    def second_to_object(self, color, my_camera):
        #if not first_move and not unreachable
        #do this while self.start_pick_up is true
        self.action_finished = False 
        world_x, world_y = self.detect_object(color, my_camera)
        if self.count_second < 3:
            if math.isclose(world_x, self.world_x, rel_tol = 1) and math.isclose(world_y, self.world_y, rel_tol =1):
                self.start_pick_up = True
            else: 
                self.count_second = self.count_second +1 
            
        else: 
            self.world_x, self.world_y = self.detect_object(color, my_camera)
            self.count_second = 0 
        
    def grippers(self, open):
        if open:
            Board.setBusServoPulse(1, self.servo_1 - 280, 500) #open gripper 
            time.sleep(1)
        else: 
            Board.setBusServoPulse(1, self.servo_1, 500)  #close gripper 
            time.sleep(1)
    
    def rotate_gripper(self, color = None):
        if color == None:
            servo2_angle = getAngle(self.world_x, self.world_y, self.rotation_angle) # get roation angle 
        else: 
            servo2_angle = getAngle(self.coordinate[color][0], self.coordinate[color][1], -90)
        
        Board.setBusServoPulse(2, servo2_angle, 500)
        time.sleep(1) 
    
    def lower_block(self, color=None):
        if color == None:
            self.go_to_location((self.world_x, self.world_y, 2), -90. -90, 0, 1000)    
        else: 
            self.go_to_location((self.coordinate[color][0], self.coordinate[color][1], self.coordinate[color][2] + 3), -90, -90, 0)
            time.sleep(0.5)
            self.go_to_location((self.coordinate[color]), -90, -90, 0, 1000)

        time.sleep(2)

    def raise_block(self, color = None):
        if color == None:
            Board.setBusServoPulse(2, 500, 500)
            self.go_to_location((self.world_x, self.world_y, 12 ), -90, -90, 0, 1000)
        else:
            self.go_to_location((self.coordinate[color][0], self.coordinate[color][1], 12), -90, -90, 0)
        time.sleep(1)
    
    def starting_position(self):
        Board.setBusServoPulse(1, self.servo_1 - 50, 300)
        Board.setBusServoPulse(2, 500, 500)
        self.go_to_location((0, 10, 10), -30, -30, -90, 1500)
    
    def reset(self):
        self.detected_object = False
        self.count_second = 0
        self.first_move = True
        self.action_finish = True
        self.start_pick_up = False
    

    def run (self, color, my_camera):
        self.starting_position()
        self.perception.run(color,5,my_camera)
        if self.first_move:
            self.first_to_object(color, my_camera) # Go close to the location of the found block 
        if not self.first_move and not self.unreachable:
            while(self.start_pick_up ==False): 
                self.second_to_object(color, my_camera) # make sure the object hasn't moved in a while
            self.grippers(True) # open grippers 
            self.rotate_gripper() #calculate needed angle of the gripper and rotate to that angle 
            self.fix_offset()
            self.lower_block() #move directly to block location and lower 
            self.grippers(False) #close grippers 
            self.raise_block() # raise block up 
            self.raise_block(color) # go close to predetermined location of block drop off 
            self.rotate_gripper(color) #calculate needed angle of gripper and rotate to that angle 
            self.lower_block(color) #slowly lower the block 
            self.grippers(True) #open grippers and drop block 
            self.starting_position() # go to starting position 
            self.reset()
            return True 
        elif self.unreachable: 
            print("Unreachable")
            self.reset()
            return False 
        else: 
            self.reset()
            return False 
        
    def fix_offset(self):
        self.world_x= self.world_x 
        self.world_y = self.world_y 

if __name__ == '__main__':
    my_camera = Camera.Camera()
    motion = Motion()
    color = 'red'
    result= motion.run(color, my_camera)
    color = 'blue'
    result= motion.run(color, my_camera)
    color = 'green'
    result= motion.run(color, my_camera)






    





        
        
        
             
        
        
              
