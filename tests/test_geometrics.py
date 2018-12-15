#!/usr/bin/python3
# -*- coding: utf-8 -*-
import numpy as np

from geomerics import subdivide, calc_normals_by_neighbors, interpolate


def test_subdivide():
    rectangle = np.array([
        [0, 0],
        [1, 0],
        [1, 1],
        [0, 1]
    ], dtype=float)

    expected = np.array([
        [0, 0],
        [.5, 0],
        [1, 0],
        [1, .5],
        [1, 1],
        [.5, 1],
        [0, 1],
        [0, .5]
    ], dtype=float)

    result = subdivide(rectangle)
    np.testing.assert_allclose(result, expected)


def test_calc_normals_by_neighbors():
    rectangle = np.array([
        [0, 0],
        [1, 0],
        [1, 1],
        [0, 1]
    ], dtype=float)

    expected = np.array([
        [-1, -1],
        [+1, -1],
        [+1, +1],
        [-1, +1]
    ], dtype=float) / np.math.sqrt(2)

    result = calc_normals_by_neighbors(rectangle)
    np.testing.assert_allclose(result, expected)


def test_interpolate():
    triangle = np.array([
        [0, 0],
        [0, 1],
        [1, 1]
    ], dtype=float)

    scaled = 3 * triangle

    result = interpolate(triangle, scaled, 3)

    np.testing.assert_allclose(result[0], triangle)
    np.testing.assert_allclose(result[1], (triangle+scaled)/2)
    np.testing.assert_allclose(result[2], scaled)

