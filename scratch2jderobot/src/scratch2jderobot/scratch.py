#!/usr/bin/env python
# -*- coding: utf-8 -*-

import time

def execute(robot):
    try:
        robot.take_off()
        while True:
            size = (robot.get_size_object())
            if ((size) > 0):
                x = (robot.get_x_position())
                y = (robot.get_y_position())
                if ((x) >   165):
                    robot.turn("right", 2)
                else:
                    robot.turn("left", 2)
                
                if ((y) >  110 ):
                    robot.move("down", 1)
                else:
                    robot.move("up", 1)
                
                if ((size) > 700):
                    robot.move("back", 2)
                else:
                    robot.move("forward", 2)
                
            else:
                robot.stop()
                robot.turn("left", 2)
            
        
    except KeyboardInterrupt:
        raise
