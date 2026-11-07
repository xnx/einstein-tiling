# conf.py
# Configuration for the Sphinx documentation of einstein-tiling.
#
# SPDX-License-Identifier: BSD-3-Clause

import contextlib
import io
import os
from pathlib import Path

import einstein_tiling as et
from einstein_tiling.cli import main

project = "einstein-tiling"
author = "Christian Hill"
copyright = "2026, Christian Hill"
release = et.__version__
version = ".".join(release.split(".")[:2])

extensions = ["sphinx.ext.autodoc"]
autodoc_member_order = "bysource"
default_role = "py:obj"
exclude_patterns = ["_build"]

html_theme = "furo"
html_title = f"einstein-tiling {release}"

# The pictures, the table of default colours and the command-line help are
# made by the package itself whenever the documentation is built, so that
# they always match the code.
GENERATED = Path(__file__).parent / "_generated"
GENERATED.mkdir(exist_ok=True)


def _write(name, text):
    (GENERATED / name).write_text(text, encoding="utf-8")


def _help(command):
    output = io.StringIO()
    with contextlib.redirect_stdout(output), contextlib.suppress(SystemExit):
        main([command, "--help"])
    return output.getvalue()


_write("tiling.svg", et.tiling_svg(et.supertile("H", 3), width=900))
_write("clusters.svg", et.clusters_svg())
for _level in range(3):
    _write(f"level{_level}.svg",
           et.tiling_svg(et.supertile("H", _level), width=400, crop=False,
                         show_metatiles=True))
_write("colours.svg",
       et.tiling_svg(et.supertile("H", 3), width=900, colours={
           "H": "#f4d8cd", "T": "#ffffff", "P": "#ede4d3", "F": "#d9c6b0",
           "reflected": "#8c2f39", "outline": "#3b2f2f"}))

_COLOURED = {
    "H": "The unreflected hats in H clusters",
    "T": "The hat in each T cluster",
    "P": "The hats in P clusters",
    "F": "The hats in F clusters",
    "reflected": "The reflected hat in each H cluster",
    "outline": "The edges of the hats",
    "metatile": "Metatile outlines, when they are shown",
    "background": "The background",
}
_rows = [".. list-table::", "   :header-rows: 1", "",
         "   * - Name", "     - Default", "     - Colours"]
for _name, _value in et.COLOURS.items():
    _rows += [f"   * - ``{_name}``", f"     - ``{_value}``",
              f"     - {_COLOURED[_name]}"]
_write("colours.inc", "\n".join(_rows) + "\n")

os.environ["COLUMNS"] = "79"
os.environ["NO_COLOR"] = "1"
for _command in ("tiling", "clusters", "check"):
    _write(f"help-{_command}.txt", _help(_command))
