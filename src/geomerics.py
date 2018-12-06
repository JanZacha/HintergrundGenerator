#!/usr/bin/python3
# -*- coding: utf-8 -*-
import numpy as np


def get_neighbors(items):
    """
    Given an array of 2d points, return the array containing the pro and preceding element for every point.

    >>> get_neighbors([1, 2, 3])
    array([[3, 2],
           [1, 3],
           [2, 1]])
    """
    items = np.asarray(items)
    a = np.vstack((items[-1][None], items[:-1]))
    b = np.vstack((items[1:], items[0][None]))
    return np.stack((a, b), 1)


def calc_normals_by_neighbors(points):
    """
    Given an array of 2d points, calculate the normal vector for every point.
    The normal vector is orthogonal to the line connecting its two nearest neighbors.
    """
    neighs = get_neighbors(points)
    vs = np.array([neigh[0] - neigh[1] for neigh in neighs])
    ns = np.array([(-v[1], v[0]) for v in vs])
    return ns / np.linalg.norm(ns, axis=1)[None].T


def disturb_points_by_neighbors_normals(points):
    ns = calc_normals_by_neighbors(points)

    d = ns * (np.random.random_sample(len(points)) * 30)[None].T
    return points + d


if __name__ == "__main__":
    i = np.array([
        [0,0],
        [1,0],
        [1,1],
        [0,1]
    ], dtype=float)

    r = calc_normals_by_neighbors(i)
    print(repr(r))

