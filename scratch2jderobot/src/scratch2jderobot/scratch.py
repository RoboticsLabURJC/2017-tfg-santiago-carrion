#!/usr/bin/env python
# -*- coding: utf-8 -*-

import time

def execute(robot):
    try:
        while True:
            size = (robot.get_size_object())
            if ((size) > 20):
                robot.stop()
            else:
                robot.move("forward", 1)
            
        
    except KeyboardInterrupt:
        raise
