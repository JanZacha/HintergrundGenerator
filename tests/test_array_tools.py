#!/usr/bin/python3
# -*- coding: utf-8 -*-
import numpy as np
import pytest

from array_tools import get_neighbors, merge


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


def test_merge():
    array1 = np.array([1, 2, 3])
    array2 = np.array([-1, -2, -3])

    expected = np.array([
        1, -1, 2, -2, 3, -3
    ])

    result = merge(array1, array2)
    np.testing.assert_array_equal(result, expected)


def test_merge2():
    array1 = np.array([[1, 2], [3, 4], [5, 6]])
    array2 = np.array([[-1, -2], [-3, -4], [-5, -6]])

    expected = np.array([[1, 2], [-1, -2], [3, 4], [-3, -4], [5, 6], [-5, -6]])

    result = merge(array1, array2)
    np.testing.assert_array_equal(result, expected)
