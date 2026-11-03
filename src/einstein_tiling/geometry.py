"""Exact geometry on the triangular lattice.

A point (a, b) stands for a + b*w, where w = e^(i*pi/3), so coordinates stay
exact integers. Convert to Cartesian coordinates with to_xy() only for output.

A placement (k, reflected, t) is a rigid motion: reflect in the x-axis if
`reflected`, rotate anticlockwise by k * 60 degrees, then translate by t.
"""

import math


def add(p, q):
    """Return the sum of two points."""
    return p[0] + q[0], p[1] + q[1]


def rotate(p, k=1):
    """Rotate p anticlockwise about the origin by k * 60 degrees."""
    a, b = p
    for _ in range(k % 6):
        a, b = -b, a + b
    return a, b


def reflect(p):
    """Reflect p in the x-axis."""
    a, b = p
    return a + b, -b


def place(p, placement):
    """Apply a placement to the point p."""
    k, reflected, t = placement
    return add(rotate(reflect(p) if reflected else p, k), t)


def to_xy(p):
    """Return the Cartesian coordinates of p."""
    a, b = p
    return a + b / 2, b * math.sqrt(3) / 2
