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
        angleX                   = -84,
        angleY                   = 28,
        angleZ                   = -90,
        displacementX            = 0,
        displacementY            = 0,
        displacementZ            = 300
    )

if __name__ == "__main__":

    main()
