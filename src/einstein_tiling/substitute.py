"""Build patches of metatiles by substitution (Figure 2.6 of arXiv:2303.10798).

Adapted from constructPatch() and constructMetatiles() in hat.js from
https://github.com/isohedral/hatviz, Copyright (c) 2023 Craig S. Kaplan,
BSD-3-Clause.

At each level, 29 copies of the current supertiles are fitted together edge to
edge. Some of those copies are kept as the children of the next level's four
supertiles; the rest only position the others.

A placed metatile is (name, k, t): a cluster from hat_data, rotated by k * 60
degrees and translated by t. Metatiles are never reflected.
"""

from fractions import Fraction

from .geometry import add, rotate

# Each metatile's corners in its hat_data frame, in the order RULES refers to.
OUTLINES = {
    "H": [(10, 0), (2, 8), (0, 8), (0, 0), (2, -2), (10, -2)],
    "T": [(0, 0), (6, 0), (0, 6)],
    "P": [(4, -4), (12, -4), (8, 0), (0, 0)],
    "F": [(4, -4), (10, -4), (10, -2), (8, 0), (0, 0)],
}

# ["H"] starts the patch. [i, e, name, f] places a new tile with its edge f
# against edge e of tile i. [i, a, j, b, name, f] places it with its edge f
# against the line from corner a of tile i to corner b of tile j.
RULES = [
    ["H"], [0, 0, "P", 2], [1, 0, "H", 2], [2, 0, "P", 2], [3, 0, "H", 2],
    [4, 4, "P", 2], [0, 4, "F", 3], [2, 4, "F", 3], [4, 1, 3, 2, "F", 0],
    [8, 3, "H", 0], [9, 2, "P", 0], [10, 2, "H", 0], [11, 4, "P", 2],
    [12, 0, "H", 2], [13, 0, "F", 3], [14, 2, "F", 1], [15, 3, "H", 4],
    [8, 2, "F", 1], [17, 3, "H", 0], [18, 2, "P", 0], [19, 2, "H", 2],
    [20, 4, "F", 3], [20, 0, "P", 2], [22, 0, "H", 2], [23, 4, "F", 3],
    [23, 0, "F", 3], [16, 0, "P", 2], [9, 4, 0, 2, "T", 2], [4, 0, "F", 3],
]

# The patch tiles kept as the children of each new supertile.
KEPT = {
    "H": [0, 9, 16, 27, 26, 6, 1, 8, 10, 15],
    "T": [11],
    "P": [7, 2, 3, 4, 28],
    "F": [21, 20, 22, 23, 24, 25],
}


def sub(p, q):
    return p[0] - q[0], p[1] - q[1]


def intersect(p1, q1, p2, q2):
    """Return where the line p1-q1 meets the line p2-q2."""
    (x1, y1), (x2, y2), (x3, y3), (x4, y4) = p1, q1, p2, q2
    denominator = (x1 - x2) * (y3 - y4) - (y1 - y2) * (x3 - x4)
    u = ((x1 - x3) * (y3 - y4) - (y1 - y3) * (x3 - x4)) / denominator
    return x1 + u * (x2 - x1), y1 + u * (y2 - y1)


class Supertile:
    """A metatile (level 0) or a larger tile built from them."""

    def __init__(self, outline, tiles):
        self.outline = outline      # Corners, as exact fractions.
        self.tiles = tiles          # The placed metatiles inside it.


def align(tile, edge, p, q):
    """Return (k, t) putting a tile's edge on the line from p to q."""
    n = len(tile.outline)
    start, end = tile.outline[edge], tile.outline[(edge + 1) % n]
    for k in range(6):
        if rotate(sub(end, start), k) == sub(q, p):
            return k, sub(p, rotate(start, k))
    raise ValueError("no rotation aligns these edges")


def build_patch(tiles):
    """Fit copies of the four supertiles together, following RULES."""
    patch = []

    def corner(i, c):
        k, t, tile = patch[i]
        return add(rotate(tile.outline[c % len(tile.outline)], k), t)

    for rule in RULES:
        if len(rule) == 1:
            patch.append((0, (Fraction(0), Fraction(0)), tiles[rule[0]]))
            continue
        if len(rule) == 4:
            i, e, name, f = rule
            p, q = corner(i, e + 1), corner(i, e)
        else:
            i, a, j, b, name, f = rule
            p, q = corner(j, b), corner(i, a)
        patch.append((*align(tiles[name], f, p, q), tiles[name]))
    return patch, corner


def children(patch, indices):
    """Flatten some of the patch's tiles into a list of placed metatiles."""
    placed = []
    for i in indices:
        k, t, tile = patch[i]
        placed += [(name, (k + k2) % 6, add(rotate(t2, k), t))
                   for name, k2, t2 in tile.tiles]
    return placed


def inflate(tiles):
    """Return the next level's four supertiles."""
    patch, corner = build_patch(tiles)

    # The new outlines are fixed by a few key points, as in Figure 2.6, plus
    # the rule that the hexagons have interior angles of 120 degrees.
    b1, b2 = corner(8, 2), corner(21, 2)
    p7, p25, f6 = corner(7, 2), corner(25, 2), corner(6, 2)
    rotated_b2 = add(b1, rotate(sub(b2, b1), 4))
    low = intersect(b1, rotated_b2, f6, p7)

    w = rotate(sub(f6, low), 5)
    h3 = corner(14, 2)
    v = rotate(w, 5)
    h = [low, b1, add(b1, w), h3, sub(h3, v), f6]
    p = [p7, add(p7, sub(b1, low)), b1, low]
    f = [b2, corner(24, 2), corner(25, 0), p25, add(p25, sub(low, b1))]
    t_start = add(h[1], sub(h[4], h[5]))
    t = [t_start, add(t_start, rotate(sub(h[2], t_start), 5)), h[2]]

    outlines = {"H": h, "T": t, "P": p, "F": f}
    return {name: Supertile(outlines[name], children(patch, KEPT[name]))
            for name in outlines}


def metatiles():
    """Return the four level 0 tiles."""
    origin = (Fraction(0), Fraction(0))
    return {name: Supertile([(Fraction(a), Fraction(b)) for a, b in corners],
                            [(name, 0, origin)])
            for name, corners in OUTLINES.items()}


def supertile(name, level):
    """Return the metatiles of a supertile, placed with integer coordinates.

    `name` is one of "H", "T", "P" or "F", and `level` is the number of
    substitution steps: level 0 is a single metatile, and each level
    multiplies the number of tiles by about 6.85.

    Each placed metatile is a tuple (name, k, t): the cluster of that name in
    CLUSTERS, rotated anticlockwise by k * 60 degrees about its origin, then
    moved by t. A point (a, b) stands for a + b w, where w = exp(i pi / 3), in
    units of the hat's short edge. Metatiles are never reflected.

    Raises ValueError for an unknown name or a negative level.
    """
    if name not in OUTLINES:
        raise ValueError(f"unknown supertile {name!r}: use H, T, P or F")
    if level < 0:
        raise ValueError(f"level must not be negative: {level}")
    tiles = metatiles()
    for _ in range(level):
        tiles = inflate(tiles)
    placed = []
    for tile_name, k, (a, b) in tiles[name].tiles:
        assert a.denominator == 1 and b.denominator == 1
        placed.append((tile_name, k, (int(a), int(b))))
    return placed
