#!/usr/bin/env python
# -*- coding: utf-8 -*-

# commands:Array
commands_extra = [
    # manually added
    ['set %m.var to %s', ' ', 9, 'setVar:to:'],
    ['change %m.var by %n', ' ', 9, 'changeVar:by:'],
]

# extension:Array
extras = []

# robotics:ScratchExtension
extras += [
    # add extensions code if not auto-generated
    [' ', 'stop robot-drone', 'Scratch2JdeRobot/stop'],
    [' ', 'move robot %m.robotDirections', 'Scratch2JdeRobot/robot/move', 'forward'],
    [' ', 'move drone %m.direction speed %n', 'Scratch2JdeRobot/robot/move/speed', 'forward', 1],
    [' ', 'move robot %m.direction speed %n', 'Scratch2JdeRobot/robot/move/speed', 'forward', 1],
    [' ', 'turn drone %m.turnDirections speed %n', 'Scratch2JdeRobot/turn/speed', 'left', 1],
    [' ', 'turn robot %m.turnDirections speed %n', 'Scratch2JdeRobot/turn/speed', 'left', 1],
    [' ', 'take off drone', 'Scratch2JdeRobot/drone/takeoff'],
    [' ', 'land drone', 'Scratch2JdeRobot/drone/land'],
    [' ', 'move robot %m.robotDirections meters %n', 'Scratch2JdeRobot/robot/move/meters', 'forward', 1],

    #perceptive blocks
    ['r', 'frontal laser distance', 'Scratch2JdeRobot/laser/frontal'],
    ['r', 'size of object', 'Scratch2JdeRobot/camera/size'],
    ['r', 'x position of object', 'Scratch2JdeRobot/camera/x_pos'],
    ['r', 'y position of object', 'Scratch2JdeRobot/camera/y_pos'],
    ['r', 'drone size object', 'Scratch2JdeRobot/camera/size'],
    ['r', 'drone x centro object', 'Scratch2JdeRobot/camera/x_pos'],
    ['r', 'drone y centro object', 'Scratch2JdeRobot/camera/y_pos'],
    ['r', 'Pose3D x', 'Scratch2JdeRobot/camera/pose3D/x'],
    ['r', 'Pose3D y', 'Scratch2JdeRobot/camera/pose3D/y'],
    ['r', 'Pose3D z', 'Scratch2JdeRobot/camera/pose3D/z'],
]
