#!/usr/bin/env python

"""
################################################################################
#                                                                              #
# yutu                                                                         #
#                                                                              #
################################################################################
#                                                                              #
# LICENCE INFORMATION                                                          #
#                                                                              #
# This program provides point manipulation procedures.                         #
#                                                                              #
# copyright (C) 2015 William Breaden Madden                                    #
#                                                                              #
# This software is released under the terms of the GNU General Public License  #
# version 3 (GPLv3).                                                           #
#                                                                              #
# This program is free software: you can redistribute it and/or modify it      #
# under the terms of the GNU General Public License as published by the Free   #
# Software Foundation, either version 3 of the License, or (at your option)    #
# any later version.                                                           #
#                                                                              #
# This program is distributed in the hope that it will be useful, but WITHOUT  #
# ANY WARRANTY; without even the implied warranty of MERCHANTABILITY or        #
# FITNESS FOR A PARTICULAR PURPOSE. See the GNU General Public License for     #
# more details.                                                                #
#                                                                              #
# For a copy of the GNU General Public License, see                            #
# <http://www.gnu.org/licenses/>.                                              #
#                                                                              #
################################################################################
"""

name    = "yutu"
version = "2015-02-09T1118Z"

import sys
import math
import pygame
from   pygame.locals import *

def radians(degrees):
    return(degrees * math.pi / 180)

def Cos(angleInDegrees):
    return(math.cos(radians(angleInDegrees)))

def Sin(angleInDegrees):
    return(math.sin(radians(angleInDegrees)))

def listPercentage(
    listFull   = None,
    percentage = None
    ):
    # This function returns a list that is a percentage of evenly-distributed
    # elements of an input list.
    return listFull[::int(100.0/percentage)]

class Point3D:

    def __init__(
        self,
        x = 0,
        y = 0,
        z = 0
        ):
        self.x = float(x)
        self.y = float(y)
        self.z = float(z)
 
    def rotate(
        self,
        angleX = 0,
        angleY = 0,
        angleZ = 0
        ):
        # rotation around x-axis
        xx = self.x
        yx = self.y * Cos(angleX) - self.z * Sin(angleX)
        zx = self.y * Sin(angleX) + self.z * Cos(angleX)
        # rotation around y-axis
        xyx = zx    * Sin(angleY) + xx     * Cos(angleY)
        yyx = yx
        zyx = zx    * Cos(angleY) - xx     * Sin(angleY)
        # rotation around z-axis
        xzyx = xyx  * Cos(angleZ) - yyx    * Sin(angleZ)
        yzyx = xyx  * Sin(angleZ) + yyx    * Cos(angleZ)
        zzyx = zyx
        return(Point3D(xzyx, yzyx, zzyx))
 
    def translate(
        self,
        displacementX = 0,
        displacementY = 0,
        displacementZ = 0
        ):
        x = self.x + displacementX
        y = self.y + displacementY
        z = self.z + displacementZ
        return(Point3D(x, y, z))
 
    def project(
        self,
        window_width    = None,
        window_height   = None,
        field_of_view   = None,
        viewer_distance = None
        ):
        # generate 2D perspective projection of point
        factor = field_of_view / (viewer_distance + self.z)
        x      =  self.x * factor + window_width / 2
        y      = -self.y * factor + window_height / 2
        return(Point3D(x, y, 1))

class Visualisation3D:

    def __init__(
        self,
        window_width  = 1280,
        window_height = 960,
        caption       = "points visualisation",
        points        = None,
        percentage    = 100
        ):
        if percentage is not 100:
            self.points = listPercentage(
                listFull   = points,
                percentage = percentage
            )
        else:
            self.points = points
        pygame.init()
        self.display = pygame.display.set_mode((window_width, window_height))
        pygame.display.set_caption(caption)
        self.clock = pygame.time.Clock()
        pygame.key.set_repeat(10, 10)
 
    def run_rotation(
        self,
        viewer_distance   = 4,
        angle_change_rate = 1,
        frame_rate        = 50
        ):
        self.angleX       = 0
        self.angleY       = 0
        self.angleZ       = 0
        while True:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    sys.exit()
                elif event.type == KEYDOWN and event.key == K_ESCAPE:
                    sys.exit()
            self.clock.tick(frame_rate)
            self.display.fill((0, 0, 0))
            # Move all points.
            for point in self.points:
                # Rotate the point around the x-axis, the y-axis and the z-axis.
                p_prime = point.rotate(
                    angleX = self.angleX,
                    angleY = self.angleY,
                    angleZ = self.angleZ
                )
                # Project the 3D point to 2D.
                point2D = p_prime.project(
                    window_width    = self.display.get_width(),
                    window_height   = self.display.get_height(),
                    field_of_view   = 256,
                    viewer_distance = viewer_distance
                )
                # Round the 2D point for display.
                x = int(point2D.x)
                y = int(point2D.y)
                self.display.fill((255, 255, 255), (x, y, 1, 1))
            self.angleX += angle_change_rate
            self.angleY += angle_change_rate
            self.angleZ += angle_change_rate
            pygame.display.flip()

    def run_control_rigid_body_motions(
        self,
        viewer_distance          = 4,
        angle_change_rate        = 2,
        displacement_change_rate = 0.2,
        frame_rate               = 50
        ):
        self.angleX              = 0
        self.angleY              = 0
        self.angleZ              = 0
        self.displacementX       = 0
        self.displacementY       = 0
        self.displacementZ       = 0
        while True:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    sys.exit()
                elif event.type == KEYDOWN and event.key == K_ESCAPE:
                    sys.exit()
            keys = pygame.key.get_pressed()
            if keys[K_w]:
                self.angleX        += angle_change_rate
            if keys[K_s]:
                self.angleX        += -angle_change_rate
            if keys[K_d]:
                self.angleY        += -angle_change_rate
            if keys[K_a]:
                self.angleY        += angle_change_rate
            if keys[K_q]:
                self.angleZ        += angle_change_rate
            if keys[K_e]:
                self.angleZ        += -angle_change_rate
            if keys[K_UP]:
                self.displacementZ += displacement_change_rate
            if keys[K_DOWN]:
                self.displacementZ += -displacement_change_rate
            if keys[K_RIGHT]:
                self.displacementX += displacement_change_rate
            if keys[K_LEFT]:
                self.displacementX += -displacement_change_rate
            if keys[K_o]:
                self.displacementY += displacement_change_rate
            if keys[K_l]:
                self.displacementY += -displacement_change_rate
            self.clock.tick(frame_rate)
            self.display.fill((0, 0, 0))
            # Move all points.
            k = 60
            count = 0
            count1 = 0
            for point in self.points:
                # Rotate the point around the x-axis, the y-axis and the z-axis.
                p_prime = point.rotate(
                    angleX = self.angleX,
                    angleY = self.angleY,
                    angleZ = self.angleZ
                )
                # Translate the point.
                p_prime_prime = p_prime.translate(
                    displacementX = self.displacementX,
                    displacementY = self.displacementY,
                    displacementZ = self.displacementZ
                )
                # Project the 3D point to 2D.
                point2D = p_prime_prime.project(
                    window_width    = self.display.get_width(),
                    window_height   = self.display.get_height(),
                    field_of_view   = 256,
                    viewer_distance = viewer_distance
                )
                # Round the 2D point for display.
                x = int(point2D.x)
                y = int(point2D.y)
                self.display.fill((255, 255, 255), (x, y, 1, 1))
            pygame.display.flip()
