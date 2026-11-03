"""The command-line interface: a thin layer over the public API."""

import argparse
import os
import sys

from . import (COLOURS, __version__, clusters_svg, hat_edges,
               label_violations, supertile, tiling_svg)
from .hat_data import CLUSTERS


def level(text):
    value = int(text)
    if value < 0:
        raise argparse.ArgumentTypeError("must not be negative")
    return value


def positive(kind):
    def convert(text):
        value = kind(text)
        if value <= 0:
            raise argparse.ArgumentTypeError("must be positive")
        return value
    convert.__name__ = kind.__name__
    return convert


def colour(text):
    """Parse NAME=COLOUR, as in H=#d0e4f5."""
    name, _, value = text.partition("=")
    if not value:
        raise argparse.ArgumentTypeError("use NAME=COLOUR, as in H=#d0e4f5")
    if name not in COLOURS:
        raise argparse.ArgumentTypeError(
            f"unknown name {name!r}: use {', '.join(COLOURS)}")
    return name, value


def write(document, path):
    """Write a document to a file, or to standard output for '-'."""
    if path == "-":
        sys.stdout.write(document)
        sys.stdout.flush()
    else:
        with open(path, "w", encoding="utf-8") as f:
            f.write(document)
        print(f"wrote {path}", file=sys.stderr)


def describe(tiles):
    hats = sum(len(CLUSTERS[name].hats) for name, _, _ in tiles)
    return f"{len(tiles)} metatiles, {hats} hats"


def run_tiling(args):
    tiles = supertile(args.supertile, args.level)
    if label_violations(tiles):
        print("error: the patch breaks the matching rules", file=sys.stderr)
        return 1
    write(tiling_svg(tiles, width=args.width, aspect=args.aspect,
                     crop=not args.no_crop, show_metatiles=args.metatiles,
                     colours=dict(args.colours)),
          args.output)
    return 0


def run_clusters(args):
    write(clusters_svg(show_vertex_numbers=args.vertex_numbers), args.output)
    return 0


def run_check(args):
    tiles = supertile(args.supertile, args.level)
    violations = label_violations(tiles)
    hat_edges(tiles)
    print(f"{args.supertile} at level {args.level}: {describe(tiles)}, "
          f"{len(violations)} rule violations")
    return 1 if violations else 0


def add_patch_options(parser):
    parser.add_argument("-l", "--level", type=level, default=4,
                        help="substitution level; each one multiplies the "
                             "tiles by about 6.85 (default: 4)")
    parser.add_argument("-s", "--supertile", choices="HTPF", default="H",
                        help="which supertile to build (default: H)")


def build_parser():
    parser = argparse.ArgumentParser(
        prog="einstein-tiling",
        description="Generate aperiodic hat tilings as SVG images.")
    parser.add_argument("--version", action="version",
                        version=f"%(prog)s {__version__}")
    commands = parser.add_subparsers(dest="command", required=True)

    tiling = commands.add_parser("tiling", help="draw a tiling")
    add_patch_options(tiling)
    tiling.add_argument("-o", "--output", default="tiling.svg",
                        help="output file, or - for standard output "
                             "(default: tiling.svg)")
    tiling.add_argument("--width", type=positive(int), default=1200,
                        help="picture width in pixels (default: 1200)")
    tiling.add_argument("--aspect", type=positive(float), default=1.5,
                        help="width / height of the crop (default: 1.5)")
    tiling.add_argument("--no-crop", action="store_true",
                        help="draw the whole patch, with its ragged edge")
    tiling.add_argument("--metatiles", action="store_true",
                        help="outline each metatile")
    tiling.add_argument("--colour", "--color", dest="colours", type=colour,
                        action="append", default=[], metavar="NAME=COLOUR",
                        help="set a colour, and repeat for more; NAME is "
                             f"one of {', '.join(COLOURS)}")
    tiling.set_defaults(run=run_tiling)

    clusters = commands.add_parser("clusters",
                                   help="draw the clusters of Figure 4.1")
    clusters.add_argument("-o", "--output", default="clusters.svg",
                          help="output file, or - for standard output "
                               "(default: clusters.svg)")
    clusters.add_argument("--vertex-numbers", action="store_true",
                          help="number each hat's vertices")
    clusters.set_defaults(run=run_clusters)

    check = commands.add_parser("check",
                                help="check a patch against the rules")
    add_patch_options(check)
    check.set_defaults(run=run_check)
    return parser


def main(argv=None):
    """Run the command line, returning the process's exit status."""
    args = build_parser().parse_args(argv)
    try:
        return args.run(args)
    except BrokenPipeError:
        # The reader went away, as with `| head`. Stop quietly, and stop
        # Python reporting the same error when it flushes stdout on exit.
        os.dup2(os.open(os.devnull, os.O_WRONLY), sys.stdout.fileno())
        return 1
    except (OSError, ValueError) as error:
        print(f"error: {error}", file=sys.stderr)
        return 1
