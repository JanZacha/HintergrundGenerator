# -*- coding: utf-8 -*-

"""Console script for creating a scalable droplet."""
import os

import matplotlib.patches as mpatches
import matplotlib.path as mpath
import matplotlib.pyplot as plt
import numpy as np

Path = mpath.Path


def add_bezier(ax, p0, p1, p2, p3):
    pp1 = mpatches.PathPatch(
        Path([p0, p1, p2, p3],
             [Path.MOVETO, Path.CURVE4, Path.CURVE4, Path.CURVE4]),
        fc="none", transform=ax.transData)
    ax.add_patch(pp1)
    return ax


def add_bezier2(ax, p0, p1, p2):
    pp1 = mpatches.PathPatch(
        Path([p0, p1, p2],
             [Path.MOVETO, Path.CURVE3, Path.CURVE3]),
        fc="none", transform=ax.transData)
    ax.add_patch(pp1)
    return ax


def _b(t, p0, p1, p2, p3):
    return (
        (1 - t) ** 3 * p0 +
        3 * (1 - t) ** 2 * t * p1 +
        3 * (1 - t) * t ** 2 * p2 +
        t ** 3 * p3
    )


def b(t, p0, p1, p2, p3):
    return (
        _b(t, p0[0], p1[0], p2[0], p3[0]),
        _b(t, p0[1], p1[1], p2[1], p3[1])
    )


def b2(t, p0, p1, p3):
    return (
        (1 - t)**2 * p0 +
        2 * (1 - t) * t * p1 +
        t ** 2 * p3
    )


def b2s(t, p0, p1, p3):
    return 2*(1-t)*(p1-p0) + 2*t*(p2-p1)


if __name__ == "__main__":

    r = 3

    pi = np.array([(0., 0), (5, 8), (10, 10)])
    p0, p1, p2 = pi

    ax = plt.gca()
    ax.cla()
    ax.set_aspect('1')

    ax.plot(np.array(pi)[..., 0],
            np.array(pi)[..., 1],
            "go", color="orange"
    )

    ps = np.array([b2(t, p0, p1, p2) for t in np.linspace(0, 1, 10)])

    for t in np.linspace(0, 1, 10):
        x = b2(t, *pi)
        ax.add_patch(plt.Circle(x, r * t, color="lightgray"))
    ax.add_patch(plt.Circle(p2, r, color="gray"))

    xs, ys = ps[..., 0], ps[..., 1]
    ax.plot(xs, ys, "go", color="black")

    bs_4 = 3. * (p2 - p1)
    bs_4 = bs_4 / np.linalg.norm(bs_4)
    bn_4 = np.array([bs_4[1], -bs_4[0]])

    bsx = np.array([p2 + t * bs_4 for t in np.linspace(0, 3, 10)])

    ax.plot(bsx[...,0], bsx[...,1], "go", color="darkgray")

    c1 = p2 - bn_4 * r
    c2 = p2 + bn_4 * r

    ax.add_patch(plt.Circle(c1, .1, color="blue"))
    ax.add_patch(plt.Circle(c2, .1, color="red"))

    add_bezier2(ax, p0, p1, p2)

    f = .5
    bs_f = b2s(f, *pi)
    bs_f = bs_f / np.linalg.norm(bs_f)
    bn_f = np.array([bs_f[1], -bs_f[0]])

    d1 = b2(f, *pi) - bn_f * r * f
    d0 = b2(f, *pi)
    d2 = b2(f, *pi) + bn_f * r * f

    ax.add_patch(plt.Circle(d1, .1, color="blue"))
    ax.add_patch(plt.Circle(d0, .1, color="black"))
    ax.add_patch(plt.Circle(d2, .1, color="red"))

    control_point_above = 2*d1 - p0/2 - c1/2
    control_point_below = 2*d2 - p0/2 - c2/2

    add_bezier2(ax, p0, control_point_above, c1)

    add_bezier2(ax, p0, control_point_below, c2)


    plt.show()

    plt.savefig(os.path.expanduser("~/curve.svg"))


