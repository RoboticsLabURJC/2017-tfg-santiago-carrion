#!/usr/bin/env python
# -*- coding: utf-8 -*-

import time

def execute(robot):
    try:
        robot.take_off()
        time.sleep(1)
        robot.turn("left")
        time.sleep(3)
        robot.stop()
        time.sleep(1)
        robot.turn("right")
        time.sleep(3)
        robot.stop()
        time.sleep(1)
        robot.land()
        time.sleep(1)
    except KeyboardInterrupt:
        raise
