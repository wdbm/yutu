#!/usr/bin/env python

import pandas as pd
import yutu

def main():

    df = pd.DataFrame(
        [
            [-1,     1,   -1, 255, 255, 255, 1], # vertex
            [ 1,     1,   -1, 255, 255, 255, 1], # vertex
            [ 1,    -1,   -1, 255, 255, 255, 1], # vertex
            [-1,    -1,   -1, 255, 255, 255, 1], # vertex
            [-1,     1,    1, 255, 255, 255, 1], # vertex
            [ 1,     1,    1, 255, 255, 255, 1], # vertex
            [ 1,    -1,    1, 255, 255, 255, 1], # vertex
            [-1,    -1,    1, 255, 255, 255, 1], # vertex
            [ 0,     1,    1, 255, 255, 255, 1], # midpoint
            [-1,     1,    0, 255, 255, 255, 1], # midpoint
            [ 0,     1,   -1, 255, 255, 255, 1], # midpoint
            [ 1,     1,    0, 255, 255, 255, 1], # midpoint
            [-1,     0,   -1, 255, 255, 255, 1], # midpoint
            [ 1,     0,   -1, 255, 255, 255, 1], # midpoint
            [ 1,     0,    1, 255, 255, 255, 1], # midpoint
            [-1,     0,    1, 255, 255, 255, 1], # midpoint
            [ 0,    -1,   -1, 255, 255, 255, 1], # midpoint
            [ 1,    -1,    0, 255, 255, 255, 1], # midpoint
            [ 0,    -1,    1, 255, 255, 255, 1], # midpoint
            [-1,    -1,    0, 255, 255, 255, 1], # midpoint
            [-0.5,   1,    1, 255, 255, 255, 1], # midmidpoint
            [-1,     1,  0.5, 255, 255, 255, 1], # midmidpoint
            [-0.5,   1,   -1, 255, 255, 255, 1], # midmidpoint
            [1,      1, -0.5, 255, 255, 255, 1], # midmidpoint
            [-1,   0.5,   -1, 255, 255, 255, 1], # midmidpoint
            [1,    0.5,   -1, 255, 255, 255, 1], # midmidpoint
            [1,    0.5,    1, 255, 255, 255, 1], # midmidpoint
            [-1,   0.5,    1, 255, 255, 255, 1], # midmidpoint
            [-0.5,  -1,   -1, 255, 255, 255, 1], # midmidpoint
            [1,     -1, -0.5, 255, 255, 255, 1], # midmidpoint
            [-0.5,  -1,    1, 255, 255, 255, 1], # midmidpoint
            [-1,    -1,  0.5, 255, 255, 255, 1], # midmidpoint
            [0.5,    1,    1, 255, 255, 255, 1], # midmidpoint
            [-1,     1, -0.5, 255, 255, 255, 1], # midmidpoint
            [0.5,    1,   -1, 255, 255, 255, 1], # midmidpoint
            [1,      1,  0.5, 255, 255, 255, 1], # midmidpoint
            [-1,  -0.5,   -1, 255, 255, 255, 1], # midmidpoint
            [1,   -0.5,   -1, 255, 255, 255, 1], # midmidpoint
            [1,   -0.5,    1, 255, 255, 255, 1], # midmidpoint
            [-1,  -0.5,    1, 255, 255, 255, 1], # midmidpoint
            [0.5,   -1,   -1, 255, 255, 255, 1], # midmidpoint
            [1,     -1,  0.5, 255, 255, 255, 1], # midmidpoint
            [0.5,   -1,    1, 255, 255, 255, 1], # midmidpoint
            [-1,    -1, -0.5, 255, 255, 255, 1]  # midmidpoint
        ],
        columns = ["x", "y", "z", "r", "g", "b", "s"]
    )

    _p = yutu.Projection(df = df)
    p = yutu.Projection_Pygame(projection = _p)
    p.run()

if __name__ == "__main__":
    main()
