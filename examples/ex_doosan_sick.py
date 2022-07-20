# -*- coding: utf-8 -*-
"""
An example to get the location of each parts with two different methods with a SICK camera.
Copyright (C) 2022 HumaRobotics

Licensed under the Apache License, Version 2.0 (the "License");
you may not use this file except in compliance with the License.
You may obtain a copy of the License at

    http://www.apache.org/licenses/LICENSE-2.0

Unless required by applicable law or agreed to in writing, software
distributed under the License is distributed on an "AS IS" BASIS,
WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
See the License for the specific language governing permissions and
limitations under the License.

In your Task Writer/ Task Builder you need:
    - A 'CustomCode' with the 'DoosanSick' file
    - A 'CustomCode' with this file
    - Add Home point outside of the camera field of view
    - Change 'ip' variable if necessary
    - Change portIN if necessary

What does this example:
    1- Connection to the camera
    2- Take a capture to get the position of each part
    3- Move to the position of each part
    4- Move to the Home position
    5- Take a capture to know the number of parts in the camera field of view
    6- Repeat steps 3 and 4 by taking a capture for each part
"""

# Keep thoses lines in order to test the code without a Doosan:
import sys
import os
import time
sys.path.insert(1, os.path.join(sys.path[0], '..'))

from DoosanSick import DoosanSick
wait = time.sleep

def movejx(pos, ref, sol):
    movejx = print("pos:", pos, "ref:", ref, "sol:", sol)

def movej(pos):
    movej = print("pos:", pos)

def posx(x,y,z,r1,r2,r3):
    posx = [x,y,z,r1,r2,r3]

Global_home = [50,50,50,0,0,0]

# Remove lines above when you want to used this code on the robot

camera_ip = "192.168.0.5"
id_ref = 113
sick = DoosanSick(ip=camera_ip, portIN=14158)

movej(Global_home)

pos_all_parts = sick.locate_all_parts(1)
for i in range(len(pos_all_parts)):
    pos = posx(pos_all_parts[i][0], pos_all_parts[i][1], pos_all_parts[i][2]-50, pos_all_parts[i][3], pos_all_parts[i][4], pos_all_parts[i][5])
    movejx(pos, id_ref, sol=2)

movej(Global_home)

nb_parts = sick.get_nb_parts(1)
for j in range(nb_parts):
    (x, y, z, r1, r2, r3, scale, score, match_time, exposure, identified) = sick.locate_one_part(1, j+1)
    pos = posx(x, y, z-50, r1, r2, r3)
    movejx(pos, id_ref, sol =2)
    movej(Global_home)
