import yutu

def main():

    cube = [
        yutu.P(-1,     1,   -1, color = "ff0000", size = 7), # vertex
        yutu.P( 1,     1,   -1, color = "ff0000", size = 7), # vertex
        yutu.P( 1,    -1,   -1, color = "ff0000", size = 7), # vertex
        yutu.P(-1,    -1,   -1, color = "ff0000", size = 7), # vertex
        yutu.P(-1,     1,    1, color = "ff0000", size = 7), # vertex
        yutu.P( 1,     1,    1, color = "ff0000", size = 7), # vertex
        yutu.P( 1,    -1,    1, color = "ff0000", size = 7), # vertex
        yutu.P(-1,    -1,    1, color = "ff0000", size = 7), # vertex
        yutu.P( 0,     1,    1, color = "00ff00", size = 5), # midpoint
        yutu.P(-1,     1,    0, color = "00ff00", size = 5), # midpoint
        yutu.P( 0,     1,   -1, color = "00ff00", size = 5), # midpoint
        yutu.P( 1,     1,    0, color = "00ff00", size = 5), # midpoint
        yutu.P(-1,     0,   -1, color = "00ff00", size = 5), # midpoint
        yutu.P( 1,     0,   -1, color = "00ff00", size = 5), # midpoint
        yutu.P( 1,     0,    1, color = "00ff00", size = 5), # midpoint
        yutu.P(-1,     0,    1, color = "00ff00", size = 5), # midpoint
        yutu.P( 0,    -1,   -1, color = "00ff00", size = 5), # midpoint
        yutu.P( 1,    -1,    0, color = "00ff00", size = 5), # midpoint
        yutu.P( 0,    -1,    1, color = "00ff00", size = 5), # midpoint
        yutu.P(-1,    -1,    0, color = "00ff00", size = 5), # midpoint
        yutu.P(-0.5,   1,    1, color = "00ff00", size = 5), # midmidpoint
        yutu.P(-1,     1,  0.5, color = "00ff00", size = 5), # midmidpoint
        yutu.P(-0.5,   1,   -1, color = "00ff00", size = 5), # midmidpoint
        yutu.P(1,      1, -0.5, color = "00ff00", size = 5), # midmidpoint
        yutu.P(-1,   0.5,   -1, color = "00ff00", size = 5), # midmidpoint
        yutu.P(1,    0.5,   -1, color = "00ff00", size = 5), # midmidpoint
        yutu.P(1,    0.5,    1, color = "00ff00", size = 5), # midmidpoint
        yutu.P(-1,   0.5,    1, color = "00ff00", size = 5), # midmidpoint
        yutu.P(-0.5,  -1,   -1, color = "00ff00", size = 5), # midmidpoint
        yutu.P(1,     -1, -0.5, color = "00ff00", size = 5), # midmidpoint
        yutu.P(-0.5,  -1,    1, color = "00ff00", size = 5), # midmidpoint
        yutu.P(-1,    -1,  0.5, color = "00ff00", size = 5), # midmidpoint
        yutu.P(0.5,    1,    1, color = "00ff00", size = 5), # midmidpoint
        yutu.P(-1,     1, -0.5, color = "00ff00", size = 5), # midmidpoint
        yutu.P(0.5,    1,   -1, color = "00ff00", size = 5), # midmidpoint
        yutu.P(1,      1,  0.5, color = "00ff00", size = 5), # midmidpoint
        yutu.P(-1,  -0.5,   -1, color = "00ff00", size = 5), # midmidpoint
        yutu.P(1,   -0.5,   -1, color = "00ff00", size = 5), # midmidpoint
        yutu.P(1,   -0.5,    1, color = "00ff00", size = 5), # midmidpoint
        yutu.P(-1,  -0.5,    1, color = "00ff00", size = 5), # midmidpoint
        yutu.P(0.5,   -1,   -1, color = "00ff00", size = 5), # midmidpoint
        yutu.P(1,     -1,  0.5, color = "00ff00", size = 5), # midmidpoint
        yutu.P(0.5,   -1,    1, color = "00ff00", size = 5), # midmidpoint
        yutu.P(-1,    -1, -0.5, color = "00ff00", size = 5)  # midmidpoint
    ]

    #yutu.Visualisation3D(
    #    points = cube
    #).run_rotation()

    yutu.Visualisation3D(
        points = cube
    ).run_control_rigid_body_motions()

if __name__ == "__main__":

    main()
