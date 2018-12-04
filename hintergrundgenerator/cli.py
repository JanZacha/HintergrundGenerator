# -*- coding: utf-8 -*-

"""Console script for hintergrundgenerator."""
import sys
from random import random, gauss

import click
import svgwrite

from hintergrundgenerator.hintergrundgenerator import get_coords_random, map_opacity_to_layer


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

    # create simple filters to blur
    def create_blur_filter(i):
        blur_filter = dwg.filter()
        blur_filter.feGaussianBlur(in_='SourceGraphic', stdDeviation=i * .9)
        return blur_filter

    filters = [create_blur_filter(i) for i in range(layers)]

    for f in filters:
        dwg.defs.add(f)

    groups = [dwg.add(dwg.g(filter=f.get_funciri())) for f in filters]

    # This is a hack to ensure the groups (aka layers) have the same size as the image
    # if we do not do this, we get artifacts when the blurred circles extend the group dimensions
    for g in groups:
        g.add(dwg.rect(insert=(0, 0), size=('100%', '100%'), fill="#ff0000", fill_opacity=0))

    for x, y in get_coords_random(image_w):
        opacity = random()
        size = gauss(max_size, 30)
        group_index = map_opacity_to_layer(layers, opacity)
        groups[group_index].add(dwg.circle((x, y), size, fill='white', fill_opacity=opacity))

    dwg.save(pretty=True)
    # sad. cairo ignores the blurring effect completely!
    # cairosvg.svg2png(bytestring=dwg.tostring(), write_to='random_circles.png')


if __name__ == "__main__":
    sys.exit(main())  # pragma: no cover
