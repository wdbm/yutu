#!/usr/bin/env python

import yutu

def main():

    df = yutu.load_yutu_file(filepath = "cube.3d", percentage = 100)
    #df = yutu.load_yutu_file(filepath = "scan000.3d", percentage = 0.1)

    print("flying camera:")
    print("- move:  WASD or arrows")
    print("- brake: space")
    print("- up:    F")
    print("- down:  C")
    print("- look:  IJKL")
    p = yutu.Projection_VisPy(df = df)
    p.run()

if __name__ == "__main__":
    main()
