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
# This program provides point cloud visualisations and manipulations.          #
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

from collections import defaultdict
import csv
import curses
import math
import math
import os
import subprocess
import sys

import pandas as pd
from   pygame.locals import *
import numpy
import pygame
import vispy.scene
from vispy.scene import visuals

name        = "yutu"
__version__ = "2018-09-25T2034Z"

def radians(degrees):
    return(degrees * math.pi / 180)

def Cos(angle_in_degrees):
    return(math.cos(radians(angle_in_degrees)))

def Sin(angle_in_degrees):
    return(math.sin(radians(angle_in_degrees)))

def clamp(x): 
    return(max(0, min(x, 255)))

def RGB_to_HEX(RGB_tuple):
    """
    Return a HEX string given an RGB tuple.
    """
    r = RGB_tuple[0]
    g = RGB_tuple[1]
    b = RGB_tuple[2]
    return("#{0:02x}{1:02x}{2:02x}".format(int(clamp(r)), int(clamp(g)), int(clamp(b))))

def HEX_to_RGB(HEX_string):
    """
    Return an RGB tuple given a HEX string.
    """
    HEX = HEX_string.lstrip('#')
    HEX_length = len(HEX)
    return tuple(
               int(HEX[i:i + int(HEX_length / 3)], 16) for i in range(
                   0,
                   HEX_length,
                   int(HEX_length / 3)
               )
           )

def terminal_dimensions():
    rows, columns = subprocess.check_output(["stty", "size"]).split()
    return (int(columns), int(rows))

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
    """
    Return a surface containing specified text, anti-aliased and reformatted to
    fit within the specified rectangle, wrapping as necessary.
    """
    final_lines = []
    requested_lines = text.splitlines()
    # Create a series of lines to fit in the specified rectangle.
    for requested_line in requested_lines:
        if font.size(requested_line)[0] > rect.width:
            words = requested_line.split(' ')
            # If any of the words are too long to fit, return.
            for word in words:
                if font.size(word)[0] >= rect.width:
                    # Raise an exception if the word is too long to fit in the
                    # specified rectangle.
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
            # Raise an exception if the wrapped text is too tall to fit in the
            # specified rectangle.
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
                # Raise an exception if there is invalid justification
                # specified.
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
    _geometry_status = "angles:         x: {angle_x}\n"        +\
                       "                y: {angle_y}\n"        +\
                       "                z: {angle_z}\n\n"      +\
                       "displacement:   x: {displacement_x}\n" +\
                       "                y: {displacement_y}\n" +\
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

def load_yutu_file(
    filepath   = None,
    percentage = None,
    s          = 1
    ):
    """
    Load from a plaintext delimited file with fields x, y, z, r, g, b, s. The
    coordinates (x, y, z) are required and the colors (r, g, b) and the sizes
    (s) are optional. Return the data as a pandas DataFrame.
    """
    df = pd.read_csv(filepath, sep = "\s*,\s*", engine = "python")
    if percentage: df = df[::int(100 / percentage)]
    df = tidy(df, s = s)
    return df

def tidy(
    df,
    s = 1
    ):
    df["s"]             = df["s"].fillna(s)
    df[["r", "g", "b"]] = df[["r", "g", "b"]].fillna(255)
    df["hexcolor"]      = df.apply(lambda row: RGB_to_HEX((row["r"], row["g"], row["b"])), axis = 1)
    return df

def rotate_point(
    x       = 0,
    y       = 0,
    z       = 0,
    angle_x = 0,
    angle_y = 0,
    angle_z = 0
    ):
    # rotation around x-axis
    xx  = x
    yx  = y    * Cos(angle_x) - z   * Sin(angle_x)
    zx  = y    * Sin(angle_x) + z   * Cos(angle_x)
    # rotation around y-axis
    xyx = zx   * Sin(angle_y) + xx  * Cos(angle_y)
    yyx = yx
    zyx = zx   * Cos(angle_y) - xx  * Sin(angle_y)
    # rotation around z-axis
    xzyx = xyx * Cos(angle_z) - yyx * Sin(angle_z)
    yzyx = xyx * Sin(angle_z) + yyx * Cos(angle_z)
    zzyx = zyx
    return (xzyx, yzyx, zzyx)

def project_point(
    x               = 0,
    y               = 0,
    z               = 0,
    window_width    = None,
    window_height   = None,
    field_of_view   = None,
    viewer_distance = None
    ):
    viewer_distance = float(viewer_distance)
    # generate 2D perspective projection of point
    if viewer_distance != -z:
        factor = field_of_view / (viewer_distance + z)
    else:
        factor = 50000000 # infinity
    x =  x * factor + window_width / 2
    y = -y * factor + window_height / 2
    return (x, y, 1)

class Canvas_TTY(object):
    """
    Create a terminal pixel surface in which Unicode Braille characters are used
    to draw pixels. Unicode Braille characters are a 4 by 2 matrix that can be
    used as a sub-matrix for each character in a terminal, so assuming the
    initial resolution of the terminal to be defined by one pixel corresponding
    to one character, using Unicode Braille characters effectively raises the
    resolution of a terminal by a factor of 8.

    Braille pattern dots:
       ,___,
       |1 4|
       |2 5|
       |3 6|
       |7 8|
       `````
    """
    def __init__(self, carriage_return = os.linesep):
        super(Canvas_TTY, self).__init__()
        self.clear()
        self.carriage_return = carriage_return
        self.pixel_map = ((0x01, 0x08),
                          (0x02, 0x10),
                          (0x04, 0x20),
                          (0x40, 0x80))
        # Braille Unicode characters start at 0x2800.
        self.braille_character_offset = 0x2800

    def Braille_coordinates(self, x, y):
        """
        Convert coordinates (x, y) to Unicode Braille (columns, rows).
        """
        return int(round(x) / 2), int(round(y) / 4)

    def clear(self):
        """
        Clear all pixels.
        """
        self.characters = defaultdict(lambda: defaultdict(int))

    def set(self, x, y):
        """
        Set a pixel at coordinate (x, y).
        """
        column, row = self.Braille_coordinates(x, y)
        self.characters[row][column] |= self.pixel_map[y % 4][x % 2]

    def unset(self, x, y):
        """
        Unset a pixel at coordinate (x, y).
        """
        column, row = self.Braille_coordinates(x, y)
        self.characters[row][column] &= ~self.pixel_map[y % 4][x % 2]

    def toggle(self, x, y):
        """
        Toggle a pixel at coordinate (x, y).
        """
        column, row = self.Braille_coordinates(x, y)
        if self.characters[row][column] & self.pixel_map[y % 4][x % 2]:
            self.unset(x, y)
        else:
            self.set(x, y)

    def set_text(self, x, y, text):
        """
        Set text at coordinate (x, y).
        """
        column, row = self.Braille_coordinates(x, y)
        for index, character in enumerate(text):
            self.characters[row][column + index] = character

    def get(self, x, y):
        """
        Get the state of a pixel at coordinate (x, y).
        """
        dot_index = self.pixel_map[y % 4][x % 2]
        column, row = self.Braille_coordinates(x, y)
        character = self.characters.get(row, {}).get(column)
        if not character:
            return False
        if type(character) != int:
            return True
        return bool(character & dot_index)

    def rows(
        self,
        min_x = None, # minimum x coordinate of canvas
        min_y = None, # minimum y coordinate of canvas
        max_x = None, # maximum x coordinate of canvas
        max_y = None  # maximum y coordinate of canvas
        ):
        """
        Return a list of the current canvas object rows.
        """
        if not self.characters.keys():
            return []
        min_row    = int(min_y       / 4) if min_y != None else min(self.characters.keys())
        max_row    = int((max_y - 1) / 4) if max_y != None else max(self.characters.keys())
        min_column = int(min_x       / 2) if min_x != None else min(min(x.keys()) for x in self.characters.values())
        max_column = int((max_x - 1) / 2) if max_x != None else max(max(x.keys()) for x in self.characters.values())
        result = []
        for row_number in range(min_row, max_row + 1):
            if not row_number in self.characters:
                result.append("")
                continue
            max_column = int((max_x - 1) / 2) if max_x != None else max(self.characters[row_number].keys())
            row = []
            for x in range(min_column, max_column + 1):
                character = self.characters[row_number].get(x)
                if not character:
                    row.append(chr(self.braille_character_offset))
                elif type(character) != int:
                    row.append(character)
                else:
                    row.append(chr(self.braille_character_offset + character))
            result.append("".join(row))
        return result

    def frame(
        self,
        min_x = None, # minimum x coordinate of canvas
        min_y = None, # minimum y coordinate of canvas
        max_x = None, # maximum x coordinate of canvas
        max_y = None  # maximum y coordinate of canvas
        ):
        """
        Return a string representation of canvas pixels.
        """
        ret = self.carriage_return.join(self.rows(min_x, min_y, max_x, max_y))
        return ret

    def line(x1, y1, x2, y2):
        """
        Yield the coordinates of the line from (x1, x2) to (x2, y2).
        """
        x1 = round(x1)
        y1 = round(y1)
        x2 = round(x2)
        y2 = round(y2)
        x_difference = max(x1, x2) - min(x1, x2)
        y_difference = max(y1, y2) - min(y1, y2)
        x_direction  = 1 if x1 <= x2 else -1
        y_direction  = 1 if y1 <= y2 else -1
        r = max(x_difference, y_difference)
        for n in range(r + 1):
            x = x1
            y = y1
            if y_difference: y += (float(n) * y_difference) / r * y_direction
            if x_difference: x += (float(n) * x_difference) / r * x_direction
            yield (x, y)
    
    def polygon(
        center_x = 0,
        center_y = 0,
        sides    = 4,
        radius   = 4
        ):
        """
        Yield the coordinates of the lines of a polygon with specified center
        coordinates, number of sides and radius.
        """
        degree = float(360) / sides
        for n in range(sides):
            a  = n * degree
            b  = (n + 1) * degree
            x1 = (center_x + math.cos(math.radians(a))) * (radius + 1) / 2
            y1 = (center_y + math.sin(math.radians(a))) * (radius + 1) / 2
            x2 = (center_x + math.cos(math.radians(b))) * (radius + 1) / 2
            y2 = (center_y + math.sin(math.radians(b))) * (radius + 1) / 2
            for x, y in line(x1, y1, x2, y2):
                yield x, y

class Projection(object):
    def __init__(
        self,
        df = None,
        s  = 1
        ):
        self.df = tidy(df, s = s)
        self.configure()
    def configure(self, **kwargs):
        defaults = {
            "mode"                    : "rotate",
            #"mode"                    : "control_rigid_body_motions",
            "window_width"            : 1280,
            "window_height"           : 960,
            "field_of_view"           : 256,
            "viewer_distance"         : 4,
            "angle_change_rate"       : 2,
            "displacement_change_rate": 0.2,
            "angle_x"                 : 0,
            "angle_y"                 : 0,
            "angle_z"                 : 0,
            "displacement_x"          : 0,
            "displacement_y"          : 0,
            "displacement_z"          : 0
        }
        self.__dict__.update(defaults)
        self.__dict__.update(kwargs)
        self._project()
    def _project(self):
        self.df["prime"] = self.df.apply(lambda row: rotate_point(
            x               = row["x"],
            y               = row["y"],
            z               = row["z"],
            angle_x         = self.angle_x,
            angle_y         = self.angle_y,
            angle_z         = self.angle_z
        ), axis = 1)
        self.df["prime"] = self.df.apply(lambda row: (
            row["prime"][0] + self.displacement_x,
            row["prime"][1] + self.displacement_y,
            row["prime"][2] + self.displacement_z,
        ), axis = 1)
        self.df["project"] = self.df.apply(lambda row: project_point(
            x               = row["prime"][0],
            y               = row["prime"][1],
            z               = row["prime"][2],
            window_width    = self.window_width,
            window_height   = self.window_height,
            field_of_view   = self.field_of_view,
            viewer_distance = self.viewer_distance
        ), axis=1)
    def update(self):
        if self.mode == "rotate":
            self.angle_x += self.angle_change_rate
            self.angle_y += self.angle_change_rate
            self.angle_z += self.angle_change_rate
        self._project()

class Projection_Pygame(object):
    def __init__(
        self,
        projection           = None,
        caption              = "PyGame canvas",
        geometry_status      = False
        ):
        self.projection      = projection
        self.caption         = caption
        self.geometry_status = geometry_status
        self.projection.configure(
            window_width    = 1280,
            window_height   = 960,
            field_of_view   = 256,
            viewer_distance = 4
        )
        pygame.init()
        self.display         = pygame.display.set_mode((projection.window_width, projection.window_height))
        self.frame_rate      = 50
        self.clock           = pygame.time.Clock()
        self.font            = pygame.font.SysFont("monospace", 15)
        pygame.display.set_caption(self.caption)
        pygame.key.set_repeat(10, 10)
    def run(self):
        while True:
            self.clock.tick(self.frame_rate)
            self.display.fill((0, 0, 0))
            for event in pygame.event.get():
                if event.type == pygame.QUIT or event.type == KEYDOWN and event.key == K_ESCAPE:
                    sys.exit()
            if self.projection.mode == "control_rigid_body_motions":
                keys = pygame.key.get_pressed()
                if keys[K_w]:     self.projection.angle_x        +=  self.projection.angle_change_rate
                if keys[K_s]:     self.projection.angle_x        += -self.projection.angle_change_rate
                if keys[K_d]:     self.projection.angle_y        += -self.projection.angle_change_rate
                if keys[K_a]:     self.projection.angle_y        +=  self.projection.angle_change_rate
                if keys[K_q]:     self.projection.angle_z        +=  self.projection.angle_change_rate
                if keys[K_e]:     self.projection.angle_z        += -self.projection.angle_change_rate
                if keys[K_UP]:    self.projection.displacement_z +=  self.projection.displacement_change_rate
                if keys[K_DOWN]:  self.projection.displacement_z += -self.projection.displacement_change_rate
                if keys[K_RIGHT]: self.projection.displacement_x +=  self.projection.displacement_change_rate
                if keys[K_LEFT]:  self.projection.displacement_x += -self.projection.displacement_change_rate
                if keys[K_o]:     self.projection.displacement_y +=  self.projection.displacement_change_rate
                if keys[K_l]:     self.projection.displacement_y += -self.projection.displacement_change_rate
                if keys[K_F11]:   pygame.display.toggle_fullscreen()
            for p in self.projection.df[["project", "hexcolor", "s"]].values:
                self.display.fill(
                    HEX_to_RGB(p[1]),
                    (
                        int(p[0][0]), # x
                        int(p[0][1]), # y
                        p[2],         # s
                        p[2]          # s
                    )
                )
                #self.display.set_at(
                #    (
                #        int(p[0][0]), # x
                #        int(p[0][1])  # y
                #
                #    ),
                #    HEX_to_RGB(p[1]),
                #)
            if self.geometry_status is True:
                self.display.blit(
                    geometry_status_text_box(
                        angle_x        = self.projection.angle_x,
                        angle_y        = self.projection.angle_y,
                        angle_z        = self.projection.angle_z,
                        displacement_x = self.projection.displacement_x,
                        displacement_y = self.projection.displacement_y,
                        displacement_z = self.projection.displacement_z,
                        font           = self.font
                    ),
                    (0, 0)
                )
            pygame.display.flip()
            self.projection.update()

class Projection_TTY(object):
    def __init__(
        self,
        projection      = None
        ):
        self.projection = projection
        window_width    = (terminal_dimensions()[0] - 1) * 2
        window_height   = (terminal_dimensions()[1] - 1) * 4
        self.projection.configure(
            window_width    = window_width,
            window_height   = window_height,
            field_of_view   = 40,
            viewer_distance = 3
        )
        self.frame_rate = 50
        self.clock      = pygame.time.Clock()
        self.stdscr     = curses.initscr()
        self.stdscr.refresh()
        self.canvas     = Canvas_TTY()
        self.canvas.set(0, 0)
        self.canvas.set(window_width, window_height)
    def run(self):
        while True:
            for p in self.projection.df[["project", "hexcolor", "s"]].values:
                x = int(p[0][0])
                y = int(p[0][1])
                self.canvas.set(x, y)
            f = self.canvas.frame(
                0,                                 # min x
                0,                                 # min y
                int(self.projection.window_width), # max x
                int(self.projection.window_height) # max y
            )
            self.stdscr.addstr(0, 0, "{0}\n".format(f))
            self.stdscr.refresh()
            self.clock.tick(self.frame_rate)
            self.canvas.clear()
            self.projection.update()

class Projection_VisPy(object):
    def __init__(
        self,
        df          = None,
        s_factor    = 3,
        camera_type = "fly"
        ):
        self.df       = df
        self.s_factor = s_factor
        self.canvas   = vispy.scene.SceneCanvas(
            keys = "interactive",
            show = True
        )
        self.view = self.canvas.central_widget.add_view()
        #self.axis = visuals.XYZAxis(parent = self.view.scene)
        self.scatter = visuals.Markers()
        self.scatter.set_data(
            self.df[["x", "y", "z"]].as_matrix(),
            edge_color = None,
            face_color = (df[["r", "g", "b"]] / 255).as_matrix(),
            size       = self.df["s"].values * self.s_factor
        )
        self.view.add(self.scatter)
        self.view.camera = camera_type
    def run(self):
        vispy.app.run()
