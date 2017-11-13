#!/usr/bin/env python
# -*- coding: utf-8 -*-

import time

def execute(robot):
    try:
        robot.take_off()
        while True:
            size = (robot.get_laser_distance())
            if ((size) > 0):
                x = (get x_position of object red)
                y = (get y_position of object red)
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
                robot.turn("left", 2)
                robot.stop()
            
        
    except KeyboardInterrupt:
        raise
