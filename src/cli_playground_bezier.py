# -*- coding: utf-8 -*-
"""
quick demo to generate a smoothed bezier curve through a number of given points (here: randomly selected)
"""

import sys

import click
import numpy as np
import svgwrite

from array_tools import get_neighbors
from bezier import get_bezier_control_points


def get_random_points(n=10):
    return [(50 + x * 25, 100 + np.random.random() * 150) for x in range(n)]


@click.command()
@click.option('--out', default='output.svg', help='Output image name')
@click.option('--image-w', default=600, help='Width of the output image in pixels')
@click.option('--image-h', default=300, help='Height of the output image in pixels')
@click.option('--bg-color', default='#0563a5', help='Background color')
def main(out, image_w, image_h, bg_color):

    dwg = svgwrite.Drawing(out, (image_w, image_h), debug=True)
    dwg.add(dwg.rect(insert=(0, 0), size=('100%', '100%'), fill=bg_color))

    # points = [(x, 100 + 100 * (i % 2)) for i, x in enumerate(range(0, 350, 50))]
    points = get_random_points(20)

    cps = get_bezier_control_points(points, .2)

    for p1, p2 in get_neighbors(points, False):
        dwg.add(dwg.line(p1, p2, stroke="gray", stroke_width=1, stroke_dasharray="2,2"))

    ps = ' '.join(["{:.1f},{:.1f}".format(*p) for p in cps])
    ps = "M {:.1f},{:.1f}".format(*points[0]) + " C " + ps

    dwg.add(dwg.path(d=ps,
                     stroke="black",
                     fill="none",
                     stroke_width=2.5)
            )

    t = cps[1:-2]
    for cp1, p, cp2 in zip(t[::3], t[1::3], t[2::3]):
        dwg.add(dwg.line(p, cp1, stroke="orange", stroke_width=1))
        dwg.add(dwg.circle(cp1, 1.5, stroke="orange", fill="orange"))

        dwg.add(dwg.line(p, cp2, stroke="lightblue", stroke_width=1))
        dwg.add(dwg.circle(cp2, 1.5, stroke="lightblue", fill="lightblue"))

    for p in points:
        dwg.add(dwg.circle(p, 3, fill="white"))

    dwg.save(pretty=True)
    click.echo("Saved generated background image to file %s" % out)


if __name__ == "__main__":
    sys.exit(main())
