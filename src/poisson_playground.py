#!/usr/bin/python3
# -*- coding: utf-8 -*-
import numpy as np
from PIL import Image
from matplotlib.image import imsave
from matplotlib.pyplot import imread

from poisson import read_potential_from_png, do_poisson_solve_step
import matplotlib.pyplot as plt


def scale_array(array, factor):
    shape = array.shape
    scaled_shape = int(shape[0] * factor), int(shape[1] * factor)
    scaled_array = np.array(Image.fromarray(array.T).resize(scaled_shape)).T
    return scaled_array


def solve_poisson(start_potential, fixed_potential_map, target=1.e-6):
    current_r = np.array(start_potential)

    for i in range(25000):
        last_r = np.array(current_r)
        current_r = do_poisson_solve_step(current_r)
        current_r[fixed_potential_map] = start_potential[fixed_potential_map]
        if i % 1000 == 0:
            delta = ((last_r - current_r)**2).sum()
            print("Iteration %7i. Total delta %.2e" % (i, delta))
            np.save("tmppotential", current_r)
            imsave("output_potentials.png", current_r)
            ax.matshow(current_r.T, cmap="RdBu")
            plt.pause(.01)
            if delta < target:
                print("good enough")
                break
    return current_r


if __name__ == "__main__":
    potentials = read_potential_from_png("input_potentials.png")
    p_map_unscaled = potentials != 0

    ax = plt.gca()
    ax.cla()

    ax.add_artist(plt.Circle((200//2, 100//2), 5, color='#ff7800'))
    ax.add_artist(plt.Circle((400//2, 300//2), 5, color='#58aef8'))

    cax = ax.matshow(potentials.T, cmap="RdBu")
    plt.colorbar(cax, ticks=[-100, 0, 100])

    print("orig size: %s" % str(potentials.shape))

    p = scale_array(potentials, 1/4)
    p_map = p != 0
    print("scaled size: %s" % str(p.shape))
    r = solve_poisson(p, p_map)

    p = scale_array(r, 4)
    p_map = p != 0
    print("re scaled size: %s" % str(p.shape))

    r = solve_poisson(p, p_map_unscaled, target=1e-4)
    cax = ax.matshow(r.T, cmap="RdBu")
    imsave("output_potentials.png", r.T)
