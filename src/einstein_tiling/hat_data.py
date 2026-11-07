"""The hat and the four clusters of Figure 4.1 of arXiv:2303.10798.

Lengths are in units of the hat's short edge, so metatile corners and marked
points all have even coordinates. Each cluster has its own origin, and Figure
4.1 shows this data turned anticlockwise by 30 degrees.

See geometry.py for the meaning of points and placements.
"""

from .geometry import place

# The vertices of the hat, anticlockwise.
HAT = [(0, 0), (-1, -1), (0, -2), (2, -2), (2, -1), (4, -2), (5, -1),
       (4, 0), (3, 0), (2, 2), (0, 3), (0, 2), (-1, 2)]

# The placement of each hat, in the order of the figure's labels (H1, H2, ...).
# H1 is the only reflected hat. P and F contain the same hats: they differ only
# in their boundaries.
CLUSTER_HATS = {
    "T": [(0, False, (0, 2))],
    "H": [(4, True, (4, 4)), (0, False, (0, 6)), (0, False, (6, 0)),
          (4, False, (2, 2))],
    "P": [(5, False, (2, 0)), (0, False, (6, -2))],
    "F": [(5, False, (2, 0)), (0, False, (6, -2))],
}

# The metatile boundaries, anticlockwise: each marked point, followed by the
# label of the edge segment leaving it.
BOUNDARY = {
    "T": [((0, 0), "A-"), ((6, 0), "A-"), ((0, 6), "B+")],
    "H": [((0, 0), "X+"), ((2, -2), "B-"), ((8, -2), "X-"), ((10, -2), "X+"),
          ((10, 0), "B-"), ((4, 6), "X-"), ((2, 8), "X+"), ((0, 8), "A+"),
          ((0, 2), "X-")],
    "P": [((0, 0), "L"), ((2, -2), "X-"), ((4, -4), "X+"), ((6, -4), "A-"),
          ((12, -4), "L"), ((10, -2), "X-"), ((8, 0), "X+"), ((6, 0), "B+")],
    "F": [((0, 0), "L"), ((2, -2), "X-"), ((4, -4), "X+"), ((6, -4), "L"),
          ((8, -4), "X-"), ((10, -4), "F+"), ((10, -2), "F-"), ((8, 0), "X+"),
          ((6, 0), "B+")],
}


class Cluster:
    """A cluster of hats and the labelled boundary of its metatile.

    `name` is "H", "T", "P" or "F". `hats` lists each hat's placement
    (k, reflected, t), in the order of the paper's labels (H1, H2, ...).
    `boundary` lists the metatile's marked points anticlockwise, each with
    the label of the edge segment that leaves it.
    """

    def __init__(self, name):
        self.name = name
        self.hats = CLUSTER_HATS[name]
        self.boundary = BOUNDARY[name]

    def hat_outlines(self):
        """Yield (label, reflected, vertices) for each hat.

        The vertices always run anticlockwise, so a reflected hat has its
        order reversed, keeping vertex 0 first.
        """
        for i, hat in enumerate(self.hats, start=1):
            vertices = [place(v, hat) for v in HAT]
            reflected = hat[1]
            if reflected:
                vertices = vertices[:1] + vertices[:0:-1]
            yield f"{self.name}{i}", reflected, vertices

    def segments(self):
        """Yield (start, end, label) for each boundary segment, anticlockwise."""
        points = [point for point, _ in self.boundary]
        for i, (start, label) in enumerate(self.boundary):
            yield start, points[(i + 1) % len(points)], label


CLUSTERS = {name: Cluster(name) for name in CLUSTER_HATS}
