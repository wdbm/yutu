#!/usr/bin/env python

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

    # Generate data.
    points = numpy.random.normal(
        size = (100000, 3),
        scale = 0.1
    )

    # Make the data appear more interesting.
    centers = numpy.random.normal(
        size=(50, 3)
    )
    indices = numpy.random.normal(
        size  = 100000,
        loc   = centers.shape[0]/2.,
        scale = centers.shape[0]/3.
    )
    indices = numpy.clip(indices, 0, centers.shape[0] - 1).astype(int)
    scales = 10 ** (
        numpy.linspace(-2, 0.5, centers.shape[0])
    )[indices][:, numpy.newaxis]
    points *= scales
    points += centers[indices]
    
    # Create a scatter object and set the data.
    scatter = visuals.Markers()
    scatter.set_data(
        points,
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
