#!/usr/bin/env python
# -*- coding: utf-8 -*-

import time

def execute(robot):
    try:
        robot.take_off()
        while True:
            robot.stop()
            size = (robot.get_size_object())
            if ((size) > 0):
                centre_x = (robot.get_x_position())
                centre_y = (robot.get_y_position())
                if ((size) > 670):
                    robot.move("back")
                else:
                    robot.move("forward")
                
                if ((centre_x) > 165):
                    robot.turn("right")
                else:
                    robot.turn("right")
                
                if ((centre_y) > 110):
                    robot.move("down")
                else:
                    robot.move("up")
                
            else:
                robot.turn("left")
            
        
    except KeyboardInterrupt:
        raise
