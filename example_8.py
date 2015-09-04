import yutu
import numpy
import vispy.scene
from vispy.scene import visuals

def main():

    # Create a canvas and add a simple view.
    canvas = vispy.scene.SceneCanvas(
        keys = "interactive",
        show = True
    )
    view = canvas.central_widget.add_view()

    cube = [
        yutu.P(-1,     1,   -1), # vertex
        yutu.P( 1,     1,   -1), # vertex
        yutu.P( 1,    -1,   -1), # vertex
        yutu.P(-1,    -1,   -1), # vertex
        yutu.P(-1,     1,    1), # vertex
        yutu.P( 1,     1,    1), # vertex
        yutu.P( 1,    -1,    1), # vertex
        yutu.P(-1,    -1,    1), # vertex
        yutu.P( 0,     1,    1), # midpoint
        yutu.P(-1,     1,    0), # midpoint
        yutu.P( 0,     1,   -1), # midpoint
        yutu.P( 1,     1,    0), # midpoint
        yutu.P(-1,     0,   -1), # midpoint
        yutu.P( 1,     0,   -1), # midpoint
        yutu.P( 1,     0,    1), # midpoint
        yutu.P(-1,     0,    1), # midpoint
        yutu.P( 0,    -1,   -1), # midpoint
        yutu.P( 1,    -1,    0), # midpoint
        yutu.P( 0,    -1,    1), # midpoint
        yutu.P(-1,    -1,    0), # midpoint
        yutu.P(-0.5,   1,    1), # midmidpoint
        yutu.P(-1,     1,  0.5), # midmidpoint
        yutu.P(-0.5,   1,   -1), # midmidpoint
        yutu.P(1,      1, -0.5), # midmidpoint
        yutu.P(-1,   0.5,   -1), # midmidpoint
        yutu.P(1,    0.5,   -1), # midmidpoint
        yutu.P(1,    0.5,    1), # midmidpoint
        yutu.P(-1,   0.5,    1), # midmidpoint
        yutu.P(-0.5,  -1,   -1), # midmidpoint
        yutu.P(1,     -1, -0.5), # midmidpoint
        yutu.P(-0.5,  -1,    1), # midmidpoint
        yutu.P(-1,    -1,  0.5), # midmidpoint
        yutu.P(0.5,    1,    1), # midmidpoint
        yutu.P(-1,     1, -0.5), # midmidpoint
        yutu.P(0.5,    1,   -1), # midmidpoint
        yutu.P(1,      1,  0.5), # midmidpoint
        yutu.P(-1,  -0.5,   -1), # midmidpoint
        yutu.P(1,   -0.5,   -1), # midmidpoint
        yutu.P(1,   -0.5,    1), # midmidpoint
        yutu.P(-1,  -0.5,    1), # midmidpoint
        yutu.P(0.5,   -1,   -1), # midmidpoint
        yutu.P(1,     -1,  0.5), # midmidpoint
        yutu.P(0.5,   -1,    1), # midmidpoint
        yutu.P(-1,    -1, -0.5)  # midmidpoint
    ]

    # Create a scatter object and set the data.
    scatter = visuals.Markers()
    scatter.set_data(
        yutu.P_to_NumPyArray(cube),
        edge_color = None,
        face_color = (1, 1, 1, .5),
        size = 5
    )

    view.add(scatter)

    view.camera = "turntable"  # "arcball"

    # Add a 3D color axis for orientation.
    axis = visuals.XYZAxis(
        parent = view.scene
    )

    vispy.app.run()

if __name__ == "__main__":

    main()
