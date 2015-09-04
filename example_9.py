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

    points = yutu.load_yutu_file(
        "scan000.3d",
        percentage = 100
    )

    # Create a scatter object and set the data.
    scatter = visuals.Markers()
    scatter.set_data(
        yutu.P_to_NumPyArray(points),
        edge_color = None,
        face_color = (1, 1, 1, .5),
        size = 5
    )

    view.add(scatter)

    view.camera = "fly"

    # Add a 3D color axis for orientation.
    axis = visuals.XYZAxis(
        parent = view.scene
    )

    print("flying camera:")
    print("- move:  WASD or arrows")
    print("- brake: space")
    print("- up:    F")
    print("- down:  C")
    print("- look:  IJKL")

    vispy.app.run()

if __name__ == "__main__":

    main()
