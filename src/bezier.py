#!/usr/bin/python3
# -*- coding: utf-8 -*-
import numpy as np

from geometrics import calc_neighbors_tangent


def get_bezier_control_points(points, scale=.25):
    """
    returns a list of bezier control points as needed for SVG's c-style beziers.

    """
    tangents = calc_neighbors_tangent(points)

    result = [points[0]]

    for p, t in zip(points[1:-1], tangents):
        v = np.asarray(t) * scale
        result.append(p - v)
        result.append(p)
        result.append(p + v)

    result.append(points[-1])
    result.append(points[-1])

    return result


if __name__ == "__main__":
    pass
