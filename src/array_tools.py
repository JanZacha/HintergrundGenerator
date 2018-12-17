#!/usr/bin/python3
# -*- coding: utf-8 -*-
import numpy as np


def get_neighbors(items, closed=True):
    """
    Given an array of 2d points, return the array containing the preceding and subsequent element for every point.

    >>> get_neighbors([[1, -1], [2, -2], [3, -3]])
    array([[[ 3, -3],
            [ 2, -2]],
    <BLANKLINE>
           [[ 1, -1],
            [ 3, -3]],
    <BLANKLINE>
           [[ 2, -2],
            [ 1, -1]]])


    >>> get_neighbors([[1, -1], [2, -2], [3, -3]], closed=False)
    array([[[ 1, -1],
            [ 3, -3]]])

    """
    items = np.asarray(items)
    a = np.vstack((items[-1][None], items[:-1]))
    b = np.vstack((items[1:], items[0][None]))

    ret = np.stack((a, b), 1)
    if closed:
        return ret
    else:
        return ret[1:-1]


def merge(array1, array2):
    """
    Create the array that consists of all elements from array1 and array2 alternately. Starting with the first element
    from array1.

    >>> merge([1, 2, 3], [4, 5, 6])
    array([ 1.,  4.,  2.,  5.,  3.,  6.])

    """
    array1 = np.asarray(array1)
    array2 = np.asarray(array2)
    assert len(array1) == len(array2)
    shape = list(array1.shape)
    shape[0] *= 2
    r = np.zeros(shape)
    r[::2] = array1
    r[1::2] = array2
    return r


if __name__ == "__main__":
    import doctest
    doctest.testmod()
