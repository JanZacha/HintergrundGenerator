# -*- coding: utf-8 -*-

"""Main module."""
from random import random, gauss


def map_opacity_to_layer(num_layers, opacity):
    assert 0 <= opacity <= 1, "Opacity %s not in range 0..1" % opacity
    return int((1 - opacity) * num_layers)


def get_coords_random(width, num_points=100):
    for i in range(num_points):
        x = random() * width
        y = gauss(200, 70)
        yield x, y
