# yutu

![](https://raw.githubusercontent.com/wdbm/yutu/master/media/yutu_tty.gif)

This package can display and move point cloud data in color using VisPy, PyGame and the terminal.

# setup

```Bash
sudo apt install python-pygame
pip install yutu
```

# usage

See the `examples` directory for example scripts.

# data

![](https://raw.githubusercontent.com/wdbm/yutu/master/media/scan000_1.png)
![](https://raw.githubusercontent.com/wdbm/yutu/master/media/scan006_1.png)

Data by Dorit Borrmann and Hassan Afzal of Jacobs University Bremen gGmbH was provided by the [Robotic 3D Scan Repository](http://kos.informatik.uni-osnabrueck.de/3Dscans/). The data were recorded at the Automation Lab at Jacobs University Bremen using a Riegl VZ-400 laser scanner and an Optris PI infrared camera. Thermal data is encoded as colour.

# future

Under consideration are more vectorization, rigid body movement matrices and perspective projection data cuts.
