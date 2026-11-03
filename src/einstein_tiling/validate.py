"""Check a patch of placed metatiles against the rules of Figure 4.1."""

from .geometry import place
from .hat_data import CLUSTERS

COMPLEMENT = {"A+": "A-", "A-": "A+", "B+": "B-", "B-": "B+", "X+": "X-",
              "X-": "X+", "F+": "F-", "F-": "F+", "L": "L"}


def unit_edges(start, end, unit):
    """Split a lattice segment into steps of the given length."""
    da, db = end[0] - start[0], end[1] - start[1]
    n = max(abs(da), abs(db), abs(da + db)) // unit
    return [((start[0] + da * i // n, start[1] + db * i // n),
             (start[0] + da * (i + 1) // n, start[1] + db * (i + 1) // n), i, n)
            for i in range(n)]


def label_violations(tiles):
    """Return the shared unit edges that break the matching rules."""
    edges = {}
    for name, k, t in tiles:
        move = (k, False, t)
        for start, end, label in CLUSTERS[name].segments():
            for p, q, i, n in unit_edges(start, end, 2):
                edge = place(p, move), place(q, move)
                if edge in edges:
                    raise ValueError(f"two tiles overlap on edge {edge}")
                edges[edge] = label, i, n
    bad = []
    for (p, q), (label, i, n) in edges.items():
        other = edges.get((q, p))
        if other and other != (COMPLEMENT[label], n - 1 - i, n):
            bad.append((p, q, label, other))
    return bad


def hat_edges(tiles):
    """Return every directed hat edge, raising if any is used twice."""
    edges = set()
    outlines = {name: [v for _, _, v in c.hat_outlines()]
                for name, c in CLUSTERS.items()}
    for name, k, t in tiles:
        move = (k, False, t)
        for vertices in outlines[name]:
            points = [place(v, move) for v in vertices]
            for p, q in zip(points, points[1:] + points[:1]):
                da, db = q[0] - p[0], q[1] - p[1]
                is_long = max(abs(da), abs(db), abs(da + db)) == 2 and (
                    da == 0 or db == 0 or da + db == 0)
                pieces = (unit_edges(p, q, 1) if is_long else [(p, q, 0, 1)])
                for a, b, _, _ in pieces:
                    if (a, b) in edges:
                        raise ValueError(f"hats overlap on edge {(a, b)}")
                    edges.add((a, b))
    return edges


def rim(edges):
    """Return the edges with no partner: the outside of a gap-free patch."""
    return [(p, q) for p, q in edges if (q, p) not in edges]
