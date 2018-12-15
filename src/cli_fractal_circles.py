# -*- coding: utf-8 -*-

"""Console script for hintergrundgenerator."""
import sys
from random import random, gauss

import click
import svgwrite
from svgwrite import Drawing

from circle_intersections import get_linear_interpolation_of_circle, subdivide_and_distort
from geomerics import disturb_points_by_neighbors_normals, subdivide
from src.hintergrundgenerator import get_coords_random, map_opacity_to_layer


def create_blur_filter(dwg: Drawing, i):
    """Create simple Filters to blur"""
    blur_filter = dwg.filter()
    blur_filter.feGaussianBlur(in_='SourceGraphic', stdDeviation=i * .9)

    return blur_filter


def create_circle(dwg: Drawing, x, y, radius, opacity):
    return dwg.circle((x, y), radius, fill='white', fill_opacity=opacity)


def create_fractal_circle(dwg: Drawing, x, y, radius, opacity):
    c = get_linear_interpolation_of_circle(x, y, radius, n=10)

    n_steps = 6
    for _ in range(n_steps):
        c = subdivide_and_distort(c)

    return dwg.add(dwg.polygon(c, fill='white', fill_opacity=opacity))


def create_disturbed_circle(dwg: Drawing, x, y, radius, opacity):
    c = get_linear_interpolation_of_circle(x, y, radius, n=4)
    c = disturb_points_by_neighbors_normals(c)
    return dwg.add(dwg.polygon(c, fill='white', fill_opacity=opacity))


def create_disturbed_circle2(dwg: Drawing, x, y, radius, opacity):
    c = get_linear_interpolation_of_circle(x, y, radius, 100)

    n_steps = 3

    for i in range(n_steps):
        c = disturb_points_by_neighbors_normals(c, 5)
        c = subdivide(c)

    return dwg.add(dwg.polygon(c, fill='white', fill_opacity=opacity))


@click.command()
@click.option('--out', default='output.svg', help='Output image name')
@click.option('--layers', default=10, help='Number of layers.')
@click.option('--max-size', default=10)
@click.option('--image-w', default=800, help='Width of the output image in pixels')
@click.option('--image-h', default=600, help='Height of the output image in pixels')
@click.option('--bg-color', default='#0563a5', help='Background color')
def main(out, layers, max_size, image_w, image_h, bg_color):
    """Console script for hintergrundgenerator."""

    dwg = svgwrite.Drawing(out, (image_w, image_h), debug=True)
    dwg.add(dwg.rect(insert=(0, 0), size=('100%', '100%'), fill=bg_color))

    filters = [create_blur_filter(dwg, i) for i in range(layers)]

    for f in filters:
        dwg.defs.add(f)

    groups = [dwg.add(dwg.g(filter=f.get_funciri())) for f in filters]

    # This is a hack to ensure the groups (aka layers) have the same size as the image
    # if we do not do this, we get rendering artifacts when the blurred circles extend the group dimensions
    for g in groups:
        g.add(dwg.rect(insert=(0, 0), size=('100%', '100%'), fill="#ff0000", fill_opacity=0))

    for x, y in get_coords_random(image_w):
        opacity = random()
        radius = gauss(max_size, 40)
        group_index = map_opacity_to_layer(layers, opacity)
        groups[group_index].add(create_disturbed_circle2(dwg, x, y, radius, opacity))

    dwg.save(pretty=True)
    click.echo("Saved generated background image to file %s" % out)
    # sad. cairo ignores the blurring effect completely!
    # for now, converting to png has to be done externally.
    # cairosvg.svg2png(bytestring=dwg.tostring(), write_to='random_circles.png')


if __name__ == "__main__":
    sys.exit(main())  # pragma: no cover
