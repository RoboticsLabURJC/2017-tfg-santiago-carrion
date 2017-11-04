#!/usr/bin/env python
# -*- coding: utf-8 -*-

import time

def execute(robot):
    try:
        robot.take_off()
        while True:
            robot.move("up", 1)
            robot.turn("left", 1)
            time.sleep(2)
            robot.move("down", 1)
            robot.turn("right", 5)
            time.sleep(2)
        
    except KeyboardInterrupt:
        raise
