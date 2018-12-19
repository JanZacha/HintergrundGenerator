# -*- coding: utf-8 -*-

"""Console script for hintergrundgenerator."""
import sys

import click
import numpy as np
import svgwrite

from array_tools import get_neighbors


def get_random_points(n=10):
    return [(50 + x * 25, 100 + np.random.random() * 100) for x in range(n)]


def calc_neighbors_tangent(points):
    """
    """
    neighs = get_neighbors(points, False)
    vs = np.array([neigh[1] - neigh[0] for neigh in neighs])
    return vs


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

    points = get_random_points(20)

    tangents = calc_neighbors_tangent(points)

    result = []
    for p, t in zip(points, tangents):
        v = t / np.linalg.norm(t)
        control_p = p - v*10
        control_p2 = p + v*10

        dwg.add(dwg.line(p, control_p, stroke="orange", stroke_width=1))
        dwg.add(dwg.circle(control_p, 1, stroke="orange", fill="orange"))

        dwg.add(dwg.line(p, control_p2, stroke="lightblue", stroke_width=1))
        dwg.add(dwg.circle(control_p2, 1, stroke="lightblue", fill="lightblue"))

        result.append(control_p)
        result.append(p)
        result.append(control_p2)

    result = [points[0]] + result
    result.append(points[-1])
    result.append(points[-1])

    ps = ' '.join(["{:.1f},{:.1f}".format(*p) for p in points])

    dwg.add(dwg.path(d="M" + ps,
                     stroke="gray",
                     fill="none", stroke_dasharray="2,2",
                     stroke_width=2)
            )

    ps = ' '.join(["{:.1f},{:.1f}".format(*p) for p in result[:]])
    ps = "M {:.1f},{:.1f}".format(*points[0]) + " C " + ps

    dwg.add(dwg.path(d=ps,
                     stroke="black",
                     fill="none",
                     stroke_width=2)
            )

    for p in points:
        dwg.add(dwg.circle(p, 4, fill="white"))

    dwg.save(pretty=True)
    click.echo("Saved generated background image to file %s" % out)


if __name__ == "__main__":
    #sys.exit(main())
    main()
