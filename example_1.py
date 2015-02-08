import yutu

def main():

    cube = [
        yutu.Point3D(-1,     1,   -1), # vertex
        yutu.Point3D( 1,     1,   -1), # vertex
        yutu.Point3D( 1,    -1,   -1), # vertex
        yutu.Point3D(-1,    -1,   -1), # vertex
        yutu.Point3D(-1,     1,    1), # vertex
        yutu.Point3D( 1,     1,    1), # vertex
        yutu.Point3D( 1,    -1,    1), # vertex
        yutu.Point3D(-1,    -1,    1), # vertex
        yutu.Point3D( 0,     1,    1), # midpoint
        yutu.Point3D(-1,     1,    0), # midpoint
        yutu.Point3D( 0,     1,   -1), # midpoint
        yutu.Point3D( 1,     1,    0), # midpoint
        yutu.Point3D(-1,     0,   -1), # midpoint
        yutu.Point3D( 1,     0,   -1), # midpoint
        yutu.Point3D( 1,     0,    1), # midpoint
        yutu.Point3D(-1,     0,    1), # midpoint
        yutu.Point3D( 0,    -1,   -1), # midpoint
        yutu.Point3D( 1,    -1,    0), # midpoint
        yutu.Point3D( 0,    -1,    1), # midpoint
        yutu.Point3D(-1,    -1,    0), # midpoint
        yutu.Point3D(-0.5,   1,    1), # midmidpoint
        yutu.Point3D(-1,     1,  0.5), # midmidpoint
        yutu.Point3D(-0.5,   1,   -1), # midmidpoint
        yutu.Point3D(1,      1, -0.5), # midmidpoint
        yutu.Point3D(-1,   0.5,   -1), # midmidpoint
        yutu.Point3D(1,    0.5,   -1), # midmidpoint
        yutu.Point3D(1,    0.5,    1), # midmidpoint
        yutu.Point3D(-1,   0.5,    1), # midmidpoint
        yutu.Point3D(-0.5,  -1,   -1), # midmidpoint
        yutu.Point3D(1,     -1, -0.5), # midmidpoint
        yutu.Point3D(-0.5,  -1,    1), # midmidpoint
        yutu.Point3D(-1,    -1,  0.5), # midmidpoint
        yutu.Point3D(0.5,    1,    1), # midmidpoint
        yutu.Point3D(-1,     1, -0.5), # midmidpoint
        yutu.Point3D(0.5,    1,   -1), # midmidpoint
        yutu.Point3D(1,      1,  0.5), # midmidpoint
        yutu.Point3D(-1,  -0.5,   -1), # midmidpoint
        yutu.Point3D(1,   -0.5,   -1), # midmidpoint
        yutu.Point3D(1,   -0.5,    1), # midmidpoint
        yutu.Point3D(-1,  -0.5,    1), # midmidpoint
        yutu.Point3D(0.5,   -1,   -1), # midmidpoint
        yutu.Point3D(1,     -1,  0.5), # midmidpoint
        yutu.Point3D(0.5,   -1,    1), # midmidpoint
        yutu.Point3D(-1,    -1, -0.5)  # midmidpoint
    ]

    #yutu.Visualisation3D(
    #    points = cube
    #).run_rotation()

    yutu.Visualisation3D(
        points = cube
    ).run_control_rigid_body_motions()

if __name__ == "__main__":

    main()
