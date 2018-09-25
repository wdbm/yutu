#!/usr/bin/env python

import yutu

def main():

    df = yutu.load_yutu_file(filepath = "cube.3d", percentage = 100)
    #df = yutu.load_yutu_file(filepath = "scan000.3d", percentage = 0.1)

    _p = yutu.Projection(df = df)
    p = yutu.Projection_Pygame(projection = _p)
    p.run()

if __name__ == "__main__":
    main()
