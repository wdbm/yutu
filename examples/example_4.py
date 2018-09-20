#!/usr/bin/env python

from yutu import *
import csv

def main():

    points = load_yutu_file(
        "scan000.3d",
        percentage = 1
    )

    Visualisation3D(points = points).run_control_rigid_body_motions(
        viewer_distance          = 100,
        displacement_change_rate = 20,
    )

if __name__ == "__main__":

    main()
