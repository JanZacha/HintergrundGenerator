#!/usr/bin/python3
# -*- coding: utf-8 -*-
from random import random

import matplotlib.pyplot as plt
import numpy as np


def create_base_artists(ax, radius=1, alpha=1.):
    n = 60
    artists = [
        plt.Circle((x, y), radius, color=str(.5)) # color=str(random())
        for y in np.linspace(5, height-5, n)
        for x in np.linspace(5, width-5, n)
    ]
    for a in artists:
        a.set_alpha(alpha)
        ax.add_artist(a)

    return artists


def copy_artists(artists, coords, radius, alpha):
    for _, coord in zip(artists, coords):
        a = plt.Circle(tuple(coord), radius, color=_.get_facecolor())
        a.set_alpha(alpha)
        ax.add_artist(a)


if __name__ == "__main__":
    height = 480
    width = 600
    d = np.zeros((width, height), dtype=np.float)
    r = 1
    a = .1
    ax = plt.gca()
    ax.cla()
    artists0 = create_base_artists(ax, r, a)

    xs = np.array([a.center for a in artists0])
    fs = np.zeros(xs.shape, dtype=float)

    potential = np.load("tmppotential.npy")

    density = np.zeros(potential.shape, dtype=np.float)

    e_force = np.array(np.gradient(potential))
    ax.matshow(potential.T, cmap="RdBu")

    dtime = 2
    for i in range(10):
        r += .1
        a += .05
        print("iteration %5i" % i)

        xs_indices = np.array(xs, dtype=int)

        force_x = []
        force_y = []
        for xi, yi in xs_indices:
            if 0 <= xi < width and 0 <= yi < height:
                force_x.append(e_force[0][xi][yi])
                force_y.append(e_force[1][xi][yi])
                density[xi][yi] += 1
            else:
                force_x.append(0)
                force_y.append(0)

        fs = np.vstack([force_x, force_y]).T
        xs += fs / dtime
        copy_artists(artists0, xs, r, a)

        plt.pause(0.01)
    d = np.zeros((height,width))
    d[0,0] = -100
    d[1,1] = 100
    ax.matshow(d, cmap="RdBu")
