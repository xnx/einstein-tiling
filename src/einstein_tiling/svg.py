"""Draw clusters and tilings as SVG documents, returned as strings."""

import html
import math

from .geometry import place, to_xy
from .hat_data import CLUSTERS
from .validate import hat_edges, rim

# Cluster figure.
ROWS = ("TH", "PF")         # The arrangement used in Figure 4.1.
FIGURE_ROTATION = 30        # Degrees, to match the figure's orientation.
SCALE = 22                  # Pixels per hat short edge.
PADDING = 50                # Pixels around the drawing.
GAP = 70                    # Pixels between clusters.
CAPTION_HEIGHT = 45         # Pixels below each cluster.
LABEL_DISTANCE = 1.7        # Edge label distance from the boundary, in units.
FONT = 'font-family="serif" font-style="italic"'
HAT_FILL = "#e8eef3"
REFLECTED_HAT_FILL = "#8fc1e8"

METATILE_COLOUR = "#a3d900"

# Tilings: the default colour of each part of the picture.
COLOURS = {
    "H": "#8fc1e8",             # Unreflected hats, by cluster.
    "T": "#f2c14e",
    "P": "#e8eef3",
    "F": "#b7d99a",
    "reflected": "#1f6fb2",     # The reflected hat in each H cluster.
    "outline": "#222",          # The edges of the hats.
    "metatile": METATILE_COLOUR,  # Metatile outlines, with show_metatiles.
    "background": "white",
}


def _to_figure(p):
    """Return the Cartesian coordinates of p, turned to match the figure."""
    x, y = to_xy(p)
    angle = math.radians(FIGURE_ROTATION)
    c, s = math.cos(angle), math.sin(angle)
    return x * c - y * s, x * s + y * c


def _to_screen(xy, offset):
    """Convert figure coordinates to pixels: SVG's y-axis points down."""
    return offset[0] + SCALE * xy[0], offset[1] - SCALE * xy[1]


def _bounds(cluster):
    """Return (xmin, xmax, ymin, ymax) of a cluster in figure coordinates."""
    points = [point for point, _ in cluster.boundary]
    for _, _, vertices in cluster.hat_outlines():
        points += vertices
    xs, ys = zip(*map(_to_figure, points))
    return min(xs), max(xs), min(ys), max(ys)


def _layout():
    """Return each cluster's pixel offset, and the width and height needed."""
    offsets = {}
    width = 0
    top = PADDING
    for row in ROWS:
        boxes = {name: _bounds(CLUSTERS[name]) for name in row}
        row_height = max(SCALE * (b[3] - b[2]) for b in boxes.values())
        left = PADDING
        for name, (xmin, xmax, ymin, ymax) in boxes.items():
            # Centre each cluster vertically in its row.
            centre = top + row_height / 2
            offsets[name] = (left - SCALE * xmin,
                             centre + SCALE * (ymin + ymax) / 2)
            left += SCALE * (xmax - xmin) + GAP
        width = max(width, left - GAP + PADDING)
        top += row_height + CAPTION_HEIGHT + GAP
    return offsets, width, top - GAP + PADDING


def _polygon(points, attributes):
    coordinates = " ".join(f"{x:.2f},{y:.2f}" for x, y in points)
    return f'<polygon points="{coordinates}" {attributes}/>'


def _text(x, y, content, size, attributes=FONT):
    # There is no reliable vertical centring in SVG, so shift by hand.
    return (f'<text x="{x:.2f}" y="{y + 0.35 * size:.2f}" font-size="{size}" '
            f'text-anchor="middle" {attributes}>{content}</text>')


def _edge_label(label):
    """Format an edge label such as 'X+' with a raised, true minus sign."""
    if len(label) == 1:
        return label
    sign = label[1].replace("-", "\N{MINUS SIGN}")
    return f'{label[0]}<tspan dx="2" dy="-7" font-size="13">{sign}</tspan>'


def _hat_label(label):
    """Format a hat label such as 'H1' with a lowered subscript."""
    return f'{label[0]}<tspan dy="4" font-size="12">{label[1:]}</tspan>'


def _centroid(points):
    """Return the centroid of a polygon."""
    area = cx = cy = 0
    for (x1, y1), (x2, y2) in zip(points, points[1:] + points[:1]):
        cross = x1 * y2 - x2 * y1
        area += cross
        cx += (x1 + x2) * cross
        cy += (y1 + y2) * cross
    return cx / (3 * area), cy / (3 * area)


def _svg_hats(cluster, offset, show_vertex_numbers):
    shapes, labels = [], []
    for label, reflected, vertices in cluster.hat_outlines():
        corners = [_to_figure(v) for v in vertices]
        points = [_to_screen(corner, offset) for corner in corners]
        fill = REFLECTED_HAT_FILL if reflected else HAT_FILL
        shapes.append(_polygon(points, f'fill="{fill}" stroke="black"'))
        labels.append(_text(*_to_screen(_centroid(corners), offset),
                            _hat_label(label), 18))
        if show_vertex_numbers:
            labels += [_text(x, y, i, 9, 'fill="#b00020"')
                       for i, (x, y) in enumerate(points)]
    return shapes + labels


def _svg_boundary(cluster, offset):
    points = [_to_screen(_to_figure(p), offset) for p, _ in cluster.boundary]
    parts = [_polygon(points, f'fill="none" stroke="{METATILE_COLOUR}" '
                              'stroke-width="3"')]
    parts += [f'<circle cx="{x:.2f}" cy="{y:.2f}" r="4"/>' for x, y in points]
    for start, end, label in cluster.segments():
        (x1, y1), (x2, y2) = _to_figure(start), _to_figure(end)
        length = math.hypot(x2 - x1, y2 - y1)
        # The boundary is anticlockwise, so outwards is to the right.
        middle = ((x1 + x2) / 2 + LABEL_DISTANCE * (y2 - y1) / length,
                  (y1 + y2) / 2 - LABEL_DISTANCE * (x2 - x1) / length)
        parts.append(_text(*_to_screen(middle, offset),
                           _edge_label(label), 19))
    return parts


def _svg_caption(cluster, offset):
    xmin, xmax, ymin, _ = _bounds(cluster)
    x, y = _to_screen(((xmin + xmax) / 2, ymin), offset)
    return _text(x, y + CAPTION_HEIGHT, f"Cluster {cluster.name}", 18,
                 'font-family="serif"')


def clusters_svg(*, show_vertex_numbers=False):
    """Return an SVG document reproducing Figure 4.1 of the paper.

    It shows the four clusters with their metatile outlines, marked points
    and edge labels. With `show_vertex_numbers`, each hat's vertices are
    numbered.
    """
    offsets, width, height = _layout()
    parts = [f'<svg xmlns="http://www.w3.org/2000/svg" width="{width:.0f}" '
             f'height="{height:.0f}" viewBox="0 0 {width:.0f} {height:.0f}">',
             '<rect width="100%" height="100%" fill="white"/>']
    for name, offset in offsets.items():
        cluster = CLUSTERS[name]
        parts += _svg_hats(cluster, offset, show_vertex_numbers)
        parts += _svg_boundary(cluster, offset)
        parts.append(_svg_caption(cluster, offset))
    parts.append("</svg>")
    return "\n".join(parts) + "\n"


def hat_polygons(tiles):
    """Yield (name, reflected, vertices) for each hat in a patch.

    `name` is the hat's cluster, `reflected` is True for the one reflected
    hat in each H cluster, and `vertices` lists the hat's 13 corners as
    Cartesian (x, y) pairs, anticlockwise, in units of its short edge.
    """
    outlines = {name: list(cluster.hat_outlines())
                for name, cluster in CLUSTERS.items()}
    for name, k, t in tiles:
        for _, reflected, vertices in outlines[name]:
            yield name, reflected, [to_xy(place(v, (k, False, t)))
                                    for v in vertices]


def metatile_polygons(tiles):
    """Yield (name, vertices) for each metatile in a patch.

    `vertices` are the marked points on the metatile's outline, including its
    corners, as Cartesian (x, y) pairs, anticlockwise.
    """
    for name, k, t in tiles:
        yield name, [to_xy(place(p, (k, False, t)))
                     for p, _ in CLUSTERS[name].boundary]


def _clear_rectangle(edges, aspect):
    """Return the largest centred rectangle free of the patch's rim."""
    points = [to_xy(p) for p, _ in edges]
    cx = sum(x for x, _ in points) / len(points)
    cy = sum(y for _, y in points) / len(points)
    half_height = min(max(abs(x - cx) / aspect, abs(y - cy))
                      for x, y in map(to_xy, (p for p, _ in rim(edges))))
    return cx, cy, aspect * half_height, half_height


def _whole_patch(edges):
    """Return a rectangle around the whole patch, with a small margin."""
    xs, ys = zip(*(to_xy(p) for p, _ in edges))
    half_width = (max(xs) - min(xs)) / 2 + 1
    half_height = (max(ys) - min(ys)) / 2 + 1
    return (min(xs) + max(xs)) / 2, (min(ys) + max(ys)) / 2, half_width, \
        half_height


def _colours(overrides):
    """Merge colour overrides into COLOURS, escaped for use in SVG."""
    overrides = overrides or {}
    unknown = sorted(set(overrides) - set(COLOURS))
    if unknown:
        raise ValueError(f"unknown colour name {', '.join(unknown)}: use "
                         f"{', '.join(COLOURS)}")
    return {name: html.escape(value) for name, value in
            {**COLOURS, **overrides}.items()}


def tiling_svg(tiles, *, width=1200, aspect=1.5, crop=True,
               show_metatiles=False, colours=None):
    """Return an SVG document showing a patch of placed metatiles.

    `tiles` is a list of placed metatiles, as from supertile(), and `width`
    is the picture's width in pixels. With `crop`, the picture is the largest
    centred rectangle of the given aspect ratio (width / height) that has no
    gaps: a supertile's edge is ragged. That rectangle can be small at low
    levels. Without `crop`, the whole patch is drawn and `aspect` is ignored.
    With `show_metatiles`, each metatile is outlined.

    `colours` maps any of the names in COLOURS to an SVG colour, such as
    "#d0e4f5", "navy" or "none". Raises ValueError for an unknown name, or
    when no gap-free rectangle can be cropped.
    """
    fills = _colours(colours)
    edges = hat_edges(tiles)
    if crop:
        cx, cy, half_width, half_height = _clear_rectangle(edges, aspect)
    else:
        cx, cy, half_width, half_height = _whole_patch(edges)
    if half_width == 0 or half_height == 0:
        raise ValueError("no gap-free rectangle: use crop=False")
    scale = width / (2 * half_width)
    height = 2 * half_height * scale

    def svg_polygon(points, style):
        coordinates = " ".join(f"{(x - cx + half_width) * scale:.1f},"
                               f"{(cy + half_height - y) * scale:.1f}"
                               for x, y in points)
        return f'<polygon points="{coordinates}" {style}/>'

    def off_picture(points):
        return all(abs(x - cx) > half_width + 8
                   or abs(y - cy) > half_height + 8 for x, y in points)

    parts = [f'<svg xmlns="http://www.w3.org/2000/svg" width="{width}" '
             f'height="{height:.0f}" viewBox="0 0 {width} {height:.0f}">',
             f'<rect width="100%" height="100%" fill="{fills["background"]}"/>']
    for name, reflected, points in hat_polygons(tiles):
        if not off_picture(points):
            fill = fills["reflected"] if reflected else fills[name]
            parts.append(svg_polygon(
                points, f'fill="{fill}" stroke="{fills["outline"]}" '
                        'stroke-width="0.6"'))
    if show_metatiles:
        for _, points in metatile_polygons(tiles):
            if not off_picture(points):
                parts.append(svg_polygon(
                    points, f'fill="none" stroke="{fills["metatile"]}" '
                            'stroke-width="2.5"'))
    parts.append("</svg>")
    return "\n".join(parts) + "\n"
