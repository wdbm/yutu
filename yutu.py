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
version = "2017-01-16T1603Z"

import sys
import math
import numpy
import csv
import pygame
from   pygame.locals import *

def radians(degrees):
    return(degrees * math.pi / 180)

def Cos(angle_in_degrees):
    return(math.cos(radians(angle_in_degrees)))

def Sin(angle_in_degrees):
    return(math.sin(radians(angle_in_degrees)))

def list_percentage(
    list_full  = None,
    percentage = None
    ):
    # This function returns a list that is a percentage of evenly-distributed
    # elements of an input list.
    return list_full[::int(100.0/percentage)]

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

class TextRectException:
    def __init__(self, message = None):
        self.message = message
    def __str__(self):
        return self.message

def text_box(
    text             = None,
    font             = None,            # pygame.Font
    rect             = None,            # pygame.Rect
    text_color       = (255, 255, 255), # RGB tuple
    background_color = (0, 0, 0),       # RGB tuple
    justification    = 0                # 0 (default): left, 1: center, 2: right
    ):
    # This function returns a surface containing specified text, anti-aliased
    # and reformatted to fit within the rectangle, word-wrapping as necessary.
    final_lines = []
    requested_lines = text.splitlines()
    # Create a series of lines to fit in the provided rectangle.
    for requested_line in requested_lines:
        if font.size(requested_line)[0] > rect.width:
            words = requested_line.split(' ')
            # If any of the words are too long to fit, return.
            for word in words:
                if font.size(word)[0] >= rect.width:
                    # word too long to fit in rect specified
                    raise(Exception)
            # Start a new line.
            accumulated_line = ""
            for word in words:
                test_line = accumulated_line + word + " "
                # Build the line while the words fit.    
                if font.size(test_line)[0] < rect.width:
                    accumulated_line = test_line
                else:
                    final_lines.append(accumulated_line)
                    accumulated_line = word + " "
            final_lines.append(accumulated_line)
        else:
            final_lines.append(requested_line)
    # Attempt to write the text to the surface.
    surface = pygame.Surface(rect.size)
    surface.fill(background_color)
    accumulated_height = 0
    for line in final_lines:
        if accumulated_height + font.size(line)[1] >= rect.height:
            # once word-wrapped, text too tall to fit in rect specified
            raise(Exception)
        if line != "":
            temporary_surface = font.render(line, 1, text_color)
            if justification == 0:
                surface.blit(
                    temporary_surface,
                    (0, accumulated_height)
                )
            elif justification == 1:
                surface.blit(
                    temporary_surface,
                    ((rect.width - temporary_surface.get_width()) / 2,
                    accumulated_height)
                )
            elif justification == 2:
                surface.blit(
                    temporary_surface,
                    (rect.width - temporary_surface.get_width(),
                    accumulated_height)
                )
            else:
                # invalid justification specified
                raise(Excepton)
        accumulated_height += font.size(line)[1]
    return(surface)

def geometry_status_text_box(
    angle_x        = None,
    angle_y        = None,
    angle_z        = None,
    displacement_x = None,
    displacement_y = None,
    displacement_z = None,
    font           = None,
    x1             = 0,
    y1             = 0,
    x2             = 300,
    y2             = 127
    ):
    _geometry_status = "angles:         x: {angle_x}\n"        + \
                       "                y: {angle_y}\n"        + \
                       "                z: {angle_z}\n\n"      + \
                       "displacement:   x: {displacement_x}\n" + \
                       "                y: {displacement_y}\n" + \
                       "                z: {displacement_z}\n"
    geometry_status = _geometry_status.format(
        angle_x            = angle_x,
        angle_y            = angle_y,
        angle_z            = angle_z,
        displacement_x     = displacement_x,
        displacement_y     = displacement_y,
        displacement_z     = displacement_z
    )
    rect = pygame.Rect((x1, y1, x2, y2))
    geometry_status_text_box = text_box(
        text             = geometry_status,
        font             = font,
        rect             = rect,
        text_color       = (255, 255, 255),
        background_color = (0, 85, 160),
        justification    = 0
        )
    return(geometry_status_text_box)

class P:

    def __init__(
        self,
        x           = 0,
        y           = 0,
        z           = 0,
        color       = "#ffffff",
        size_x      = None,
        size_y      = None,
        size        = 1
        ):
        self.x      = float(x)
        self.y      = float(y)
        self.z      = float(z)
        self._color = color
        if size_x is None and size_y is None:
            self._size_x = size
            self._size_y = size
        else:
            self._size_x = size_x
            self._size_y = size_y
 
    def rotate(
        self,
        angle_x = 0,
        angle_y = 0,
        angle_z = 0
        ):
        # rotation around x-axis
        xx = self.x
        yx = self.y * Cos(angle_x) - self.z * Sin(angle_x)
        zx = self.y * Sin(angle_x) + self.z * Cos(angle_x)
        # rotation around y-axis
        xyx = zx    * Sin(angle_y) + xx     * Cos(angle_y)
        yyx = yx
        zyx = zx    * Cos(angle_y) - xx     * Sin(angle_y)
        # rotation around z-axis
        xzyx = xyx  * Cos(angle_z) - yyx    * Sin(angle_z)
        yzyx = xyx  * Sin(angle_z) + yyx    * Cos(angle_z)
        zzyx = zyx
        return(P(xzyx, yzyx, zzyx))
 
    def translate(
        self,
        displacement_x = 0,
        displacement_y = 0,
        displacement_z = 0
        ):
        x = self.x + displacement_x
        y = self.y + displacement_y
        z = self.z + displacement_z
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

    def color_HEX(
        self
        ):
        return(self._color)

    def color_RGB(
        self
        ):
        return(HEX_to_RGB(self._color))

    def size_x(
        self
        ):
        return(self._size_x)

    def size_y(
        self
        ):
        return(self._size_y)

def load_yutu_file(
    filename   = None,
    percentage = 100
    ):
    points = []
    nmation = int(100.0/percentage)
    line_number = 1
    for line in csv.reader(
        open(filename),
        delimiter = " ",
        skipinitialspace = True
        ):
        if line and line_number % nmation == 0:
            x = line[0]
            y = line[1]
            z = line[2]
            r = int(line[3])
            g = int(line[4])
            b = int(line[5])
            point = P(x, y, z, color = RGB_to_HEX((r, g, b)), size = 1)
            points.append(point)
        line_number += 1
    return(points)

def P_to_NumPyArray(
    points = None
    ):
    number_of_points = len(points)
    array = numpy.zeros(shape = (number_of_points, 3))
    for index, point in enumerate(points):
        array[index] = [point.x, point.y, point.z]
    return array

class Visualisation3D:

    def __init__(
        self,
        window_width   = 1280,
        window_height  = 960,
        caption        = "points visualisation",
        points         = None,
        percentage     = 100
        ):
        if percentage is not 100:
            self.points = list_percentage(
                list_full  = points,
                percentage = percentage
            )
        else:
            self.points = points
        pygame.init()
        self.display = pygame.display.set_mode((window_width, window_height))
        pygame.display.set_caption(caption)
        self.clock = pygame.time.Clock()
        pygame.key.set_repeat(10, 10)
        self.font = pygame.font.SysFont("monospace", 15)
 
    def run_rotation(
        self,
        viewer_distance     = 4,
        angle_change_rate   = 1,
        frame_rate          = 50,
        angle_x             = 0,
        angle_y             = 0,
        angle_z             = 0,
        displacement_x      = 0,
        displacement_y      = 0,
        displacement_z      = 0,
        geometry_status     = True
        ):
        self.angle_x        = angle_x
        self.angle_y        = angle_y
        self.angle_z        = angle_z
        self.displacement_x = displacement_x
        self.displacement_y = displacement_y
        self.displacement_z = displacement_z
        while True:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    sys.exit()
                elif event.type == KEYDOWN and event.key == K_ESCAPE:
                    sys.exit()
            keys = pygame.key.get_pressed()
            if keys[K_F11]:
                pygame.display.toggle_fullscreen()
            self.clock.tick(frame_rate)
            self.display.fill((0, 0, 0))
            # Move all points.
            for point in self.points:
                # Rotate the point around the x-axis, the y-axis and the z-axis.
                p_prime = point.rotate(
                    angle_x = self.angle_x,
                    angle_y = self.angle_y,
                    angle_z = self.angle_z
                )
                # Project the 3D point to 2D.
                point_2D = p_prime.project(
                    window_width    = self.display.get_width(),
                    window_height   = self.display.get_height(),
                    field_of_view   = 256,
                    viewer_distance = viewer_distance
                )
                # Round the 2D point for display.
                x = int(point_2D.x)
                y = int(point_2D.y)
                self.display.fill(
                    point.color_RGB(),
                    (x, y, point.size_x(), point.size_y())
                )
            self.angle_x += angle_change_rate
            self.angle_y += angle_change_rate
            self.angle_z += angle_change_rate
            if geometry_status is True:
                self.display.blit(
                    geometry_status_text_box(
                        angle_x            = self.angle_x,
                        angle_y            = self.angle_y,
                        angle_z            = self.angle_z,
                        displacement_x     = self.displacement_x,
                        displacement_y     = self.displacement_y,
                        displacement_z     = self.displacement_z,
                        font              = self.font
                    ),
                    (0, 0)
                )
            pygame.display.flip()

    def run_control_rigid_body_motions(
        self,
        viewer_distance          = 4,
        angle_change_rate        = 2,
        displacement_change_rate = 0.2,
        frame_rate               = 50,
        angle_x                  = 0,
        angle_y                  = 0,
        angle_z                  = 0,
        displacement_x           = 0,
        displacement_y           = 0,
        displacement_z           = 0,
        geometry_status          = True
        ):
        self.angle_x             = angle_x
        self.angle_y             = angle_y
        self.angle_z             = angle_z
        self.displacement_x      = displacement_x
        self.displacement_y      = displacement_y
        self.displacement_z      = displacement_z
        while True:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    sys.exit()
                elif event.type == KEYDOWN and event.key == K_ESCAPE:
                    sys.exit()
            keys = pygame.key.get_pressed()
            if keys[K_w]:
                self.angle_x        += angle_change_rate
            if keys[K_s]:
                self.angle_x        += -angle_change_rate
            if keys[K_d]:
                self.angle_y        += -angle_change_rate
            if keys[K_a]:
                self.angle_y        += angle_change_rate
            if keys[K_q]:
                self.angle_z        += angle_change_rate
            if keys[K_e]:
                self.angle_z        += -angle_change_rate
            if keys[K_UP]:
                self.displacement_z += displacement_change_rate
            if keys[K_DOWN]:
                self.displacement_z += -displacement_change_rate
            if keys[K_RIGHT]:
                self.displacement_x += displacement_change_rate
            if keys[K_LEFT]:
                self.displacement_x += -displacement_change_rate
            if keys[K_o]:
                self.displacement_y += displacement_change_rate
            if keys[K_l]:
                self.displacement_y += -displacement_change_rate
            if keys[K_F11]:
                pygame.display.toggle_fullscreen()
            self.clock.tick(frame_rate)
            self.display.fill((0, 0, 0))
            # Move all points.
            for point in self.points:
                # Rotate the point around the x-axis, the y-axis and the z-axis.
                p_prime = point.rotate(
                    angle_x = self.angle_x,
                    angle_y = self.angle_y,
                    angle_z = self.angle_z
                )
                # Translate the point.
                p_prime_prime = p_prime.translate(
                    displacement_x = self.displacement_x,
                    displacement_y = self.displacement_y,
                    displacement_z = self.displacement_z
                )
                # Project the 3D point to 2D.
                point_2D = p_prime_prime.project(
                    window_width    = self.display.get_width(),
                    window_height   = self.display.get_height(),
                    field_of_view   = 256,
                    viewer_distance = viewer_distance
                )
                # Round the 2D point for display.
                x = int(point_2D.x)
                y = int(point_2D.y)
                self.display.fill(
                    point.color_RGB(),
                    (x, y, point.size_x(), point.size_y())
                )
            if geometry_status is True:
                self.display.blit(
                    geometry_status_text_box(
                        angle_x        = self.angle_x,
                        angle_y        = self.angle_y,
                        angle_z        = self.angle_z,
                        displacement_x = self.displacement_x,
                        displacement_y = self.displacement_y,
                        displacement_z = self.displacement_z,
                        font           = self.font
                    ),
                    (0, 0)
                )
            pygame.display.flip()
