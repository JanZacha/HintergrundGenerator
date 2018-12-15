#!/usr/bin/python3
# -*- coding: utf-8 -*-
import numpy as np

from array_tools import get_neighbors, merge


def calc_normals_by_neighbors(points):
    """
    Given an array of 2d points, calculate the normal vector for every point.
    The normal vector is orthogonal to the line connecting its two nearest neighbors.
    """
    neighs = get_neighbors(points)
    vs = np.array([neigh[0] - neigh[1] for neigh in neighs])
    ns = np.array([(-v[1], v[0]) for v in vs])
    return ns / np.linalg.norm(ns, axis=1)[None].T


def calc_normals_by_neighbors_with_norms_by_neighs(points):
    neighs = get_neighbors(points)
    vs = np.array([neigh[1] - neigh[0] for neigh in neighs])
    ns = np.array([(-v[1], v[0]) for v in vs])

    return ns, np.linalg.norm(ns, axis=1)[None].T


def disturb_points_by_neighbors_normals(points, scale=50):
    ns, ns_norms = calc_normals_by_neighbors_with_norms_by_neighs(points)
    ns /= ns_norms
    d = ns * (np.random.random_sample(len(points)) - .5)[None].T
    return points + d * scale


def subdivide(points):
    points2 = np.vstack((points[1:], points[0]))
    vs = (points + points2) / 2

    return merge(points, vs)


def interpolate(points0, points1, steps: int):
    assert points0.shape == points1.shape

    fs = np.linspace(0, 1, steps)
    return points0 + ((points1 - points0) * fs[:, np.newaxis, np.newaxis])


if __name__ == "__main__":
    pass
