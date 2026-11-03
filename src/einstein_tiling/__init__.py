"""Generate aperiodic hat tilings from the clusters of arXiv:2303.10798.

    import einstein_tiling as et

    tiles = et.supertile("H", level=4)
    assert not et.label_violations(tiles)
    svg = et.tiling_svg(tiles, width=1200)
"""

from importlib.metadata import version

from .hat_data import CLUSTERS
from .substitute import supertile
from .svg import clusters_svg, hat_polygons, metatile_polygons, tiling_svg
from .validate import hat_edges, label_violations, rim

__all__ = [
    "CLUSTERS",
    "clusters_svg",
    "hat_edges",
    "hat_polygons",
    "label_violations",
    "metatile_polygons",
    "rim",
    "supertile",
    "tiling_svg",
]
__version__ = version("einstein-tiling")
