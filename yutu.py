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
version = "2015-02-09T2111Z"

import sys
import math
import csv
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

def clamp(x): 
    return(max(0, min(x, 255)))

def RGB_to_HEX(RGB_tuple):
    # This function returns a HEX string given an RGB tuple.
    r = RGB_tuple[0]
    g = RGB_tuple[1]
    b = RGB_tuple[2]
    return("#{0:02x}{1:02x}{2:02x}".format(clamp(r), clamp(g), clamp(b)))

def HEX_to_RGB(HEX_string):
    # This function returns an RGB tuple given a HEX string.
    HEX = HEX_string.lstrip('#')
    HEX_length = len(HEX)
    return(
        tuple(
            int(HEX[i:i + HEX_length // 3], 16) for i in range(
                0,
                HEX_length,
                HEX_length // 3
            )
        )
    )

class P:

    def __init__(
        self,
        x           = 0,
        y           = 0,
        z           = 0,
        color       = "#ffffff",
        sizeX       = None,
        sizeY       = None,
        size        = 1
        ):
        self.x      = float(x)
        self.y      = float(y)
        self.z      = float(z)
        self._color = color
        if sizeX is None and sizeY is None:
            self._sizeX = size
            self._sizeY = size
        else:
            self._sizeX = sizeX
            self._sizeY = sizeY
 
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
        return(P(xzyx, yzyx, zzyx))
 
    def translate(
        self,
        displacementX = 0,
        displacementY = 0,
        displacementZ = 0
        ):
        x = self.x + displacementX
        y = self.y + displacementY
        z = self.z + displacementZ
        return(P(x, y, z))
 
    def project(
        self,
        window_width    = None,
        window_height   = None,
        field_of_view   = None,
        viewer_distance = None
        ):
        # convert viewer distance to float
        viewer_distance = float(viewer_distance)
        # generate 2D perspective projection of point
        if viewer_distance != -self.z:
            factor = field_of_view / (viewer_distance + self.z)
        else:
            factor = 50000000
        x =  self.x * factor + window_width / 2
        y = -self.y * factor + window_height / 2
        return(P(x, y, 1))

    def colorHEX(
        self
        ):
        return(self._color)

    def colorRGB(
        self
        ):
        return(HEX_to_RGB(self._color))

    def sizeX(
        self
        ):
        return(self._sizeX)

    def sizeY(
        self
        ):
        return(self._sizeY)

def load_yutu_file(
    fileName   = None,
    percentage = 100
    ):
    points = []
    nmation = int(100.0/percentage)
    lineNumber = 1
    for line in csv.reader(
        open(fileName),
        delimiter = " ",
        skipinitialspace = True
        ):
        if line and lineNumber % nmation == 0:
            x = line[0]
            y = line[1]
            z = line[2]
            r = int(line[3])
            g = int(line[4])
            b = int(line[5])
            point = P(x, y, z, color = RGB_to_HEX((r, g, b)), size = 1)
            points.append(point)
        lineNumber += 1
    return(points)

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
                self.display.fill(
                    point.colorRGB(),
                    (x, y, point.sizeX(), point.sizeY())
                )
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
                self.display.fill(
                    point.colorRGB(),
                    (x, y, point.sizeX(), point.sizeY())
                )
            pygame.display.flip()
