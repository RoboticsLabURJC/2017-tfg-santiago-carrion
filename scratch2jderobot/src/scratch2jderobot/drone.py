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


import math
import time
import imutils
import cv2
import comm

from jderobotTypes import CMDVel
from jderobotTypes import Pose3d
from jderobotTypes import Image

# define the lower and upper boundaries of the basic colors
GREEN_RANGE = ((29, 86, 6), (64, 255, 255))
RED_RANGE = ((139, 0, 0), (255, 160, 122))
BLUE_RANGE = ((0, 128, 128), (65, 105, 225))


class Drone():

    """
    Drone class.
    """

    def __init__(self, jdrc):
        """
        Init method.
        @param jdrc:
        """

    	#variables

    	#get clients
        self.__pose3d_client = jdrc.getPose3dClient("drone.Pose3D")
        self.__camera_client = jdrc.getCameraClient("drone.Camera1")
        self.__cmdvel_client = jdrc.getCMDVelClient("drone.CMDVel")
        self.__extra_client = jdrc.getArDroneExtraClient("drone.Extra")
        self.__navdata_client = jdrc.getNavdataClient("drone.Navdata")

    def close(self):
        """
        Close communications with servers.
        """

        self.__camera_client.stop()
        self.__navdata_client.stop()
        self.__pose3d_client.stop()

    def color_object_centroid(self):
        """
        Return the x,y centroid of a colorful object in the camera.

        @return: The (x,y) centroid of the object or None if not found.
        """

        # FIXME: set color (manual)
        color = BLUE_RANGE

        # get image from camera
        frame = self.__camera_client.getImage()

        # resize the frame
        frame = imutils.resize(frame, width=600)

        # convert to the HSV color space
        hsv = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)

        # construct a mask for the color specified
        # then perform a series of dilations and erosions
        # to remove any small blobs left in the mask
        mask = cv2.inRange(hsv, color[0], color[1])
        mask = cv2.erode(mask, None, iterations=2)
        mask = cv2.dilate(mask, None, iterations=2)

        # find contours in the mask and
        # initialize the current center
        cnts = cv2.findContours(
            mask.copy(), cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)[-2]
        center = None

        # only proceed if at least one contour was found
        if len(cnts) > 0:
            # find the largest contour in the mask, then use
            # it to compute the minimum enclosing circle and
            # centroid
            c = max(cnts, key=cv2.contourArea)
            ((x, y), radius) = cv2.minEnclosingCircle(c)
            M = cv2.moments(c)
            center = (int(M["m10"] / M["m00"]), int(M["m01"] / M["m00"]))

            # only proceed if the radius meets a minimum size
            if radius > 10:
                # draw the circle border
                cv2.circle(
                    frame, (int(x), int(y)), int(radius), (0, 255, 255), 2)

                # and the centroid
                cv2.circle(frame, center, 5, (0, 0, 255), -1)

        # show the frame to our screen
        cv2.imshow("Frame", frame)
        key = cv2.waitKey(1) & 0xFF

        return center

    def go_up_down(self, direction):
        """
        Set the vertical movement of the drone.

        @param direction: direction of the move. Options: forward (default), back.
        """

        # set default velocity (m/s)
        vz = 1.0

        if direction == "down":
            vz = -vz

        # assign velocity
        self.__cmdvel_client.setVZ(vz)

        # publish movement
        self.__cmdvel_client.sendVelocities()

    def move(self, direction):
        """
        Set the horizontal movement of the drone.

        @param direction: direction of the move. Options: forward (default), back.
        """

        # set default velocities (m/s)
        vx = 5.0
        vy = 0.0

        # set different direction
        if direction == "back":
            vx = -vx
        elif direction == "left":
            vy = float(vx)
            vx = 0.0
        elif direction == "right":
            vy = float(-vx)
            vx = 0.0

        # assign velocities
        self.__cmdvel_client.setVX(vx)
        self.__cmdvel_client.setVY(vy)

        # publish movement
        self.__cmdvel_client.sendVelocities()

    def turn(self, direction):
        """
        Set the angular velocity.

        @param direction: direction of the move. Options: left (default), right.
        """

        # set default velocity (m/s)
        yaw = 5.0 * math.pi

        if direction == "right":
            yaw = -yaw

        # assign velocity
        self.__cmdvel_client.setYaw(yaw)

        # publish movement
        self.__cmdvel_client.sendVelocities()

    def stop(self):
        """
        Set all velocities to zero.
        """

        self.__cmdvel_client.setVX(0)
        self.__cmdvel_client.setVY(0)
        self.__cmdvel_client.setVZ(0)
        self.__cmdvel_client.setYaw(0)

        self.__cmdvel_client.sendVelocities()

    def take_off(self):
        """
        Send the take off command.
        """

        self.__extra_client.takeoff()
        time.sleep(1)

    def land(self):
        """
        Send the land command.
        """

        self.__extra_client.land()
        time.sleep(1)
