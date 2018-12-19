#!/usr/bin/python3
# -*- coding: utf-8 -*-

import matplotlib.pyplot as plt
import numpy as np


if __name__ == "__main__":
    height = 480
    width = 600
    d = np.zeros((width, height), dtype=np.float)

    artists = [
        plt.Circle((x, y), 2, color='orange')
        for y in np.linspace(5, height-5, 100)
        for x in [0, 5, 10, 15]
    ]

    ax = plt.gca()
    ax.cla()
    for a in artists:
        ax.add_artist(a)

    f_base = (1.0, 0)

    xs = np.array([a.center for a in artists])
    vs = np.array([(2., 0) for _ in artists])
    fs = np.zeros(xs.shape, dtype=float) + f_base

    potential = np.load("tmppotential.npy")

    density = np.zeros(potential.shape, dtype=np.float)

    e_force = np.array(np.gradient(potential))
    ax.matshow(potential.T, cmap="RdBu")

    dtime = 20
    for i in range(300):
        print("iteration %5i" % i)

        xs_indices = np.array(xs, dtype=int)

        force_x = []
        force_y = []
        still_in_game = 0
        for xi, yi in xs_indices:
            if 0 <= xi < width and 0 <= yi < height:
                force_x.append(e_force[0][xi][yi])
                force_y.append(e_force[1][xi][yi])
                density[xi][yi] += 1

                still_in_game += 1
            else:
                force_x.append(0)
                force_y.append(0)

        fs = np.vstack([force_x, force_y]).T + f_base
        vs += fs
        xs += vs / dtime
        for a, x in zip(artists, xs):
            a.center = x

        if still_in_game == 0:
            print("done")
            break

        plt.pause(0.01)

    ax.imshow(np.log(1 + density.T), cmap="gray_r")
