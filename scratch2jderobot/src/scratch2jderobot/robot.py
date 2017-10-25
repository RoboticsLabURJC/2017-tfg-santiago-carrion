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
import cv2

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
        self.__camera_client = jdrc.getCameraClient("robot.Camera1")

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


    def detect_object(self, position, color):
        """
        Detect an object using the camera.

        @param

        @return: True if there is an object detect and its size in pixels
        """
        # define the lower and upper boundaries of the basic colors
        GREEN_RANGE = ((29, 86, 6), (64, 255, 255))
        RED_RANGE = ((139, 0, 0), (255, 160, 122))
        BLUE_RANGE = ((0, 128, 128), (65, 105, 225))

        # initialize the values in case there is not object
        x_position = 0
        y_position = 0
        size = 0

        # chose the color to find
        if color == "red":
            color_range = RED_RANGE
        if color == "green":
            color_range = GREEN_RANGE
        if color == "blue":
            color_range = BLUE_RANGE

        # get images from camera
        image = self.__camera_client.getImage()

        # apply color filters to the image
        blur = cv2.GaussianBlur(image,(5,5), 2, 2)
        hsv = cv2.cvtColor(blur, cv2.COLOR_RGB2HSV)
        filtered_image = cv2.inRange(hsv, color_range[0], color_range[1])

        # Apply threshold to the masked image
        ret,thresh = cv2.threshold(filtered_image,127,255,0)
        im,contours,hierarchy = cv2.findContours(thresh,cv2.RETR_TREE,cv2.CHAIN_APPROX_SIMPLE)

        # Find the index of the largest contour
        for c in contours:
            if c.any != 0:
                cnt=contours[0]
                x,y,w,h = cv2.boundingRect(cnt)
                x_position = (w/2)+x
                y_position = (h/2)+y
                size = w*h

        if position == "x position":
            return x_position
        if position == "y position":
            return y_position
        else:
            return size

    def __get_distance_traveled(self, initialPose3d):
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
            distance = self.__get_distance_traveled(initialPose3d)
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
