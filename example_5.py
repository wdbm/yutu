#!/usr/bin/env python

from yutu import *
import csv

def main():

    points = load_yutu_file(
        "scan000.3d",
        percentage = 100
    )

    Visualisation3D(points = points).run_control_rigid_body_motions(
        viewer_distance          = 100,
        displacement_change_rate = 20,
        angle_x                  = -84,
        angle_y                  = 28,
        angle_z                  = -90,
        displacement_x           = 0,
        displacement_y           = 0,
        displacement_z           = 300
    )

if __name__ == "__main__":

    main()
