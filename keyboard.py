#!/usr/bin/env python3
# encoding: utf-8
import os
import time
import json
import pygame
import requests

url = "http://127.0.0.1:9030/jsonrpc"
cmd = {
    "method":"SetBusServoPulse",
    "params": [],
    "jsonrpc": "2.0",
    "id": 0,
    }

step_width = 10

os.environ["SDL_VIDEODRIVER"] = "dummy"
pygame.init()
pygame.display.init()
win = pygame.display.set_mode((500,250))

pygame.font.init()
font = pygame.font.SysFont("Arial", 20)
text_surface = font.render("Click to enable.", False, (220,0,0))
win.fill((255,255,255))
win.blit(text_surface, (40,100))
keys = pygame.key.get_pressed()
msg = {}

change = [500,500,136,931,795,500]
while True:
    pygame.event.pump()
    keys = pygame.key.get_pressed()
    print(keys)
    try:
        if keys[pygame.K_a] :
            print("hi")
            change[0] -= step_width
            change[0] = 0 if change[0] < 0 else change[0]
            cmd["params"] = [20, 1, 1, change[0]]
            r = requests.post(url, json = cmd).json()
        if keys[pygame.K_RIGHT] :
            change[0] += step_width
            change[0] = 1000 if change[0] > 1000 else change[0]
            cmd["params"] = [20, 1, 1, change[0]]
            r = requests.post(url, json = cmd).json()
        if keys[pygame.K_UP] :
            change[1] -= step_width
            change[1] = 0 if change[1] < 0 else change[1]
            cmd["params"] = [20, 1, 2, change[1]]
            r = requests.post(url, json = cmd).json()
        if keys[pygame.K_DOWN] :
            change[1] += step_width
            change[1] = 1000 if change[1] > 1000 else change[1]
            cmd["params"] = [20, 1, 2, change[1]]
            r = requests.post(url, json = cmd).json()
        # if js.get_button(key_map["PSB_R2"]) :
        #     change[2] += step_width
            #     change[2] = 1000 if change[2] > 1000 else change[2]
            #     cmd["params"] = [20, 1, 3, change[2]]
            #     r = requests.post(url, json = cmd).json() 
            # if js.get_button(key_map["PSB_L2"]) :
            #     change[2] -= step_width
            #     change[2] = 0 if change[2] < 0 else change[2]
            #     cmd["params"] = [20, 1, 3, change[2]]
            #     r = requests.post(url, json = cmd).json() 
            # if js.get_button(key_map["PSB_TRIANGLE"]) :
            #     change[3] += step_width
            #     change[3] = 1000 if change[3] > 1000 else change[3]
            #     cmd["params"] = [20, 1, 4, change[3]]
            #     r = requests.post(url, json = cmd).json()
            # if js.get_button(key_map["PSB_CROSS"]) :
            #     change[3] -= step_width
            #     change[3] = 0 if change[3] < 0 else change[3]
            #     cmd["params"] = [20, 1, 4, change[3]]
            #     r = requests.post(url, json = cmd).json()
            # hat = js.get_hat(0)
            # if hat[0] > 0 :
            #     change[5] -= step_width
            #     change[5] = 0 if change[5] < 0 else change[5]
            #     cmd["params"] = [20, 1, 6, change[5]]
            #     r = requests.post(url, json = cmd).json()
            # elif hat[0] < 0:
            #     change[5] += step_width
            #     change[5] = 1000 if change[5] > 1000 else change[5]
            #     cmd["params"] = [20, 1, 6, change[5]]
            #     r = requests.post(url, json = cmd).json()
            # if hat[1] > 0 :
            #     change[4] -= step_width
            #     change[4] = 0 if change[4] < 0 else change[4]
            #     cmd["params"] = [20, 1, 5, change[4]]
            #     r = requests.post(url, json = cmd).json()
            # elif hat[1] < 0:
            #     change[4] += step_width
            #     change[4] = 0 if change[4] > 1000 else change[4]
            #     cmd["params"] = [20, 1, 5, change[4]]
            #     r = requests.post(url, json = cmd).json()

            # lx = js.get_axis(0)
            # ly = js.get_axis(1)
            # rx = js.get_axis(2)
            # ry = js.get_axis(3)
            # if lx < -0.5 :
            #     change[5] += step_width
            #     change[5] = 1000 if change[5] > 1000 else change[5]
            #     cmd["params"] = [20, 1, 6, change[5]]
            #     r = requests.post(url, json = cmd).json()
            # elif lx > 0.5:             
            #     change[5] -= step_width
            #     change[5] = 0 if change[5] < 0 else change[5]
            #     cmd["params"] = [20, 1, 6, change[5]]
            #     r = requests.post(url, json = cmd).json()

            # l3_state = js.get_button(key_map["PSB_L3"])
            # if ly < -0.5 :
            #     if not l3_state:
            #         change[4] -= step_width
            #         change[4] = 0 if change[4] < 0 else change[4]
            #         cmd["params"] = [20, 1, 5, change[4]]
            #         r = requests.post(url, json = cmd).json()
            #     else:
            #         change[3] += step_width
            #         change[3] = 1000 if change[3] > 1000 else change[3]
            #         cmd["params"] = [20, 1, 4, change[3]]
            #         r = requests.post(url, json = cmd).json()
            # elif ly > 0.5:
            #     if not l3_state:
            #         change[4] += step_width
            #         change[4] = 1000 if change[4] > 1000 else change[4]
            #         cmd["params"] = [20, 1, 5, change[4]]
            #         r = requests.post(url, json = cmd).json()
            #     else:
            #         change[3] -= step_width
            #         change[3] = 0 if change[3] < 0 else change[3]
            #         cmd["params"] = [20, 1, 4, change[3]]
            #         r = requests.post(url, json = cmd).json()
            # if rx > 0.5 :
            #     change[1] += step_width
            #     change[1] = 1000 if change[1] > 1000 else change[1]
            #     cmd["params"] = [20, 1, 2, change[1]]
            #     r = requests.post(url, json = cmd).json()
            # elif rx < -0.5:
            #     change[1] -= step_width
            #     change[1] = 0 if change[1] < 0 else change[1]
            #     cmd["params"] = [20, 1, 2, change[1]]
            #     r = requests.post(url, json = cmd).json()
            # if ry > 0.5 :
            #     change[3] -= step_width
            #     change[3] = 0 if change[3] < 0 else change[3]
            #     cmd["params"] = [20, 1, 4, change[3]]
            #     r = requests.post(url, json = cmd).json() 
            # elif ry < -0.5:
            #     change[3] += step_width
            #     change[3] = 1000 if change[3] > 1000 else change[3]
            #     cmd["params"] = [20, 1, 4, change[3]]
            #     r = requests.post(url, json = cmd).json()                  
            # if js.get_button(key_map["PSB_START"]):
            #     change = [500,500,136,931,795,500]
            #     cmd["params"] =  [1000, 6, 1, 500, 2, 500, 3, 136, 4, 931, 5, 795, 6, 500]
            #     r = requests.post(url, json = cmd).json()                
    except Exception as e:
        print(e)         
    time.sleep(0.06)
    pygame.display.flip()
