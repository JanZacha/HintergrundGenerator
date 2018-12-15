#!/usr/bin/python3
# -*- coding: utf-8 -*-
import math
from random import random


def get_linear_interpolation_of_circle(x: float, y: float, r: float, n: int, starting_angle=None):
    """Returns a list of n points on a circle of radius r with the same distance.
    Orientation is picket randomly."""
    if starting_angle is None:
        starting_angle = random() * 2 * math.pi

    alpha = 2 * math.pi / n

    xs = [math.cos(starting_angle + i * alpha) * r for i in range(n)]
    ys = [math.sin(starting_angle + i * alpha) * r for i in range(n)]

    return [(x + xs[i], y + ys[i]) for i in range(n)]


def length(vector):
    return math.sqrt(vector[0] * vector[0] + vector[1] * vector[1])


def subdivide_and_distort_pair(a, b):
    m = (b[0] + a[0]) / 2, (b[1] + a[1]) / 2
    r_ab = b[0] - a[0], b[1] - a[1]
    n = [-r_ab[1], r_ab[0]]
    d_n = length(n)
    d_ab = length(r_ab)

    n[0] /= d_n
    n[1] /= d_n
    f = (random()-.5) * d_ab * .75
    return m[0] + n[0] * f, m[1] + n[1] * f


def subdivide_and_distort(points):
    p_a = points[0]
    r = [p_a]
    for p in points[1:]:
        p_n = subdivide_and_distort_pair(p_a, p)
        r.append(p_n)
        r.append(p)
        p_a = p
    r.append(subdivide_and_distort_pair(points[0], points[-1]))
    return r


if __name__ == "__main__":
    init_points = get_linear_interpolation_of_circle(0, 0, 50, 50)
    print(init_points)
    p1 = subdivide_and_distort(init_points)
    p2 = subdivide_and_distort(p1)
