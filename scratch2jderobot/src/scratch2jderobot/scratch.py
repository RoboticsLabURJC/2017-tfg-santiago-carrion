#!/usr/bin/env python
# -*- coding: utf-8 -*-

import time

def execute(robot):
    try:
        robot.move_meters("forward", 1)
        robot.turn("left")
        robot.move_meters("back", 2)
        robot.turn("right", 1)
        robot.move_meters("forward", 3)
    except KeyboardInterrupt:
        raise
