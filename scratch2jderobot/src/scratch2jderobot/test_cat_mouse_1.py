#!/usr/bin/env python
# -*- coding: utf-8 -*-

import time
import config
import sys
import comm
import os
import yaml

from drone import Drone
from robot import Robot

def execute(robot):
    try:
        robot.take_off()
        while True:
            size = robot.get_size_object()
            if size > 0:
                x = robot.get_x_position()
                y = robot.get_y_position()
                if x >   165:
                    robot.turn("right", 2)
                else:
                    robot.turn("left", 2)
                
                if y >  110 :
                    robot.move("down", 1)
                else:
                    robot.move("up", 1)
                
                if size > 700:
                    robot.move("back", 2)
                else:
                    robot.move("forward", 2)
                
            else:
                robot.stop()
                robot.turn("left", 2)
            
        
    except KeyboardInterrupt:
        raise

if __name__ == '__main__':
    if len(sys.argv) == 2:
        path = os.getcwd()
        open_path = path[:path.rfind('src')] + 'cfg/'
        filename = sys.argv[1]

    else:
        sys.exit("ERROR: Example:python my_generated_script.py cfgfile.yml")

    # loading the ICE and ROS parameters
    cfg = config.load(open_path + filename)
    stream = open(open_path + filename, "r")
    yml_file = yaml.load(stream)

    for section in yml_file:
        if section == 'drone':
            #starting comm
            jdrc = comm.init(cfg,'drone')

            # creating the object
            robot = Drone(jdrc)

            break
        elif section == 'robot':
            #starting comm
            jdrc = comm.init(cfg,'robot')

            # creating the object
            robot = Robot(jdrc)

            break
    # executing the scratch program
    execute(robot)

