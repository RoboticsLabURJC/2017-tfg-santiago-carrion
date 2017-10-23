#!/usr/bin/env python
# -*- coding: utf-8 -*-

__author__ = "Raul Perula-Martinez"
__copyright__ = "JdeRobot project"
__credits__ = ["Raul Perula-Martinez"]
__license__ = "GPL v3"
__version__ = "0.0.0"
__maintainer__ = "Raul Perula-Martinez"
__email__ = "raules@gmail.com"
__status__ = "Development"


import comm
import time
import math

from jderobotTypes import CMDVel
from jderobotTypes import Pose3d

class Robot():

    """
    Robot class.
    """

    def __init__(self, jdrc):
        """
        Init method.

        @param jdrc:
        """

        # variables

        self.__vel = CMDVel()
        self.__pose3d = Pose3d()

        # get clients
        self.__motors_client = jdrc.getMotorsClient("robot.Motors")
        self.__laser_client = jdrc.getLaserClient("robot.Laser")
        self.__pose3d_client = jdrc.getPose3dClient("robot.Pose3D")

    def __publish(self, vel):
        """
        .

        @param vel:
        """

        self.__motors_client.sendVelocities(vel)
        time.sleep(1)

    def __reset(self):
        """
        Reset the values to zero.
        """

        # reset velocities (m/s)
        self.__vel.vx = 0.0
        self.__vel.vy = 0.0
        self.__vel.vz = 0.0
        self.__vel.ax = 0.0
        self.__vel.ay = 0.0
        self.__vel.az = 0.0


    def get_distance_traveled(self, initialPose3d):
        """
        Set the straight movement of the robot.

        @param initialPose3d: place from which we calculate the distance

        @return: the distance traveled
        """
        actualPose3d = self.__pose3d_client.getPose3d()

        distance = math.hypot(actualPose3d.x - initialPose3d.x, actualPose3d.y - initialPose3d.y)

        return abs(distance)

    def move_meters(self,direction, meters=None):
        """
        Set the straight movement of the robot.

        @param direction: direction of the move. Options: forward (default), back.
        @param vel: a number with the distance in m. Default: 1 m.
        """
        # reset values
        self.__reset()

        # get initial pose3d
        initialPose3d = self.__pose3d_client.getPose3d()

        # set default velocity (m/s)
        self.__vel.vx = 0.2

        # set different direction
        if direction == "back":
            self.__vel.vx = -self.__vel.vx

        # publish movement
        self.__publish(self.__vel)

        # compare initial pose3d with actual pose3d
        while True:

            # get distance traveled
            distance = self.get_distance_traveled(initialPose3d)
            if distance >= meters:
                break;

        # reset values
        self.__reset()

        # publish movement
        self.__publish(self.__vel)

    def get_laser_distance(self):
        """
        Get the average value for the values of the frontal laser.

        @return: the average measure of the frontal laser data.
        """

        # get laser values
        laser = self.__laser_client.getLaserData()

        # clean data (unranged values, e.g. nan)
        l = [x for x in laser.values if str(x) != 'nan' and x < 10]

        try:
            avg = sum(l) / len(l)
        except ZeroDivisionError:
            avg = 0

        return avg

    def move(self, direction, vel=None):
        """
        Set the straight movement of the robot.

        @param direction: direction of the move. Options: forward (default), back.
        @param vel: a number with the velocity in m/s. Default: 0.2 m/s.
        """

        # reset values
        self.__reset()

        # set default velocity (m/s)
        self.__vel.vx = 0.2

        # set different velocity than default
        if vel != None:
            self.__vel.vx = vel

        # set different direction
        if direction == "back":
            self.__vel.vx = -self.__vel.vx

        # publish movement
        self.__publish(self.__vel)

    def turn(self, direction, vel=None):
        """
        Set the angular movement of the robot.

        @param direction: direction of the move. Options: left (default), right.
        @param vel: a number with the velocity in m/s. Default: 0.2 m/s.
        """

        # reset values
        self.__reset()

        # set default velocity (m/s)
        self.__vel.az = 0.2

        # set different velocity
        if vel != None:
            self.__vel.az = vel

        # set different direction
        if direction == "right":
            self.__vel.az = -self.__vel.az

        # publish movement
        self.__publish(self.__vel)

    def stop(self):
        """
        Set all velocities to zero in order to stop any move.
        """

        # reset values
        self.__reset()

        # publish movement
        self.__publish(self.__vel)
