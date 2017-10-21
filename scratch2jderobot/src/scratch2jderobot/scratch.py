#!/usr/bin/env python
# -*- coding: utf-8 -*-

import time

def execute(robot):
    try:
        while True:
            laser_data = (robot.get_laser_distance())
            if ((laser_data) < 1.5):
                robot.turn("left")
            else:
                robot.move("forward")
            
        
    except KeyboardInterrupt:
        raise
