#!/usr/bin/env python

import yutu

def main():

    config = {
        "VisPy" : 1,
        "PyGame": 1,
        "tty"   : 1
    }

    df = yutu.load_yutu_file(filepath = "cube.3d", percentage = 100)
    #df = yutu.load_yutu_file(filepath = "scan000.3d", percentage = 0.01)

    if config["VisPy"]:
        print("\n VisPy \n"
        print("flying camera:")
        print("- move:  WASD or arrows")
        print("- brake: space")
        print("- up:    F")
        print("- down:  C")
        print("- look:  IJKL")
        p = yutu.Projection_VisPy(df = df)
        p.run()
    if config["PyGame"]:
        print("\n PyGame \n"
        _p = yutu.Projection(df = df)
        p = yutu.Projection_Pygame(projection = _p)
        p.run()
    if config["tty"]:
        print("\n tty \n"
        _p = yutu.Projection(df = df)
        p = yutu.Projection_tty(projection = _p)
        p.run()

if __name__ == "__main__":
    main()
