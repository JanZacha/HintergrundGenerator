#!/usr/bin/python3
# -*- coding: utf-8 -*-
import numpy as np
import scipy
from matplotlib.image import imsave
from matplotlib.pyplot import imread
from scipy import ndimage


def solve_poisson(potentials: np.array):
    init = np.array(potentials)

    field = np.array(potentials)

    return field


import matplotlib

matplotlib.rcParams['backend'] = 'ps'


k = np.array([[0, 1, 0],
              [1, 1, 1],
              [0, 1, 0]]) / 5


def read_potential_from_png(filename):
    input_r, input_g, input_b, _ = imread(filename).T
    p = np.zeros(input_r.shape, dtype=np.float32)
    p[input_r == 1] = -100
    p[input_b == 1] = 100
    return p


def do_poisson_solve_step(array):
    return ndimage.convolve(array, k, mode='constant', cval=0.0)


if __name__ == "__main__":

    potentials, potentials_map = read_potential_from_png("input_potentials.png")
    imsave("ref_potentials.png", potentials - potentials.min())

    try:
        current_r = np.load("tmppotential.npy")
    except FileNotFoundError:
        current_r = np.zeros((480, 640))

    for i in range(25000):
        last_r = np.array(current_r)
        current_r = do_poisson_solve_step(current_r)
        current_r[potentials_map] = potentials[potentials_map]
        if i % 1000 == 0:
            delta = ((last_r - current_r)**2).sum()
            print("Iteration %7i. Total delta %.2e" % (i, delta))
            np.save("tmppotential", current_r)
            if delta < 1.e-5:
                print("good enough")
                break

    current_r -= current_r.max()
    current_r /= (current_r.max() - current_r.min())
    imsave("output_potentials.png", current_r)
