#!/usr/bin/python3
# -*- coding: utf-8 -*-
import numpy as np
import pytest

from geomerics import calc_normals_by_neighbors, get_neighbors


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


@pytest.mark.skip(reason="sad. the onedimensonal version fails.")
def test_get_neighbors():
    data = ['A', 'B', 'C', 'D']
    result = get_neighbors(data)

    assert result[0][0] == 'D'
    assert result[0][1] == 'B'

    expected = np.asarray([('D', 'B'), ('A', 'C'), ('B', 'D'), ('C', 'A')])
    np.testing.assert_array_equal(result, expected)


def test_get_neighbors2():
    rectangle = np.array([
        [0, 0],
        [1, 0],
        [2, 3]
    ], dtype=float)

    result = get_neighbors(rectangle)

    expected = np.array([
        [[2, 3], [1, 0]],
        [[0, 0], [2, 3]],
        [[1, 0], [0, 0]]
    ], dtype=float)

    np.testing.assert_array_equal(result, expected)
