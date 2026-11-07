**********
User guide
**********

Installing
==========

einstein-tiling is on PyPI, and has no dependencies:

.. code-block:: console

   $ pip install einstein-tiling

To use the command without installing anything, `uv <https://docs.astral.sh/uv/>`_
can fetch and run it:

.. code-block:: console

   $ uvx einstein-tiling tiling -o tiling.svg

Drawing a tiling
================

.. code-block:: console

   $ einstein-tiling tiling --level 4 -o tiling.svg

A tiling is built up in *levels*: level 0 is a single cluster of hats, and
each level groups the tiles of the one before into larger *supertiles* (see
:doc:`how-it-works`). Each level has about 6.85 times as many tiles as the one
before:

.. list-table::
   :header-rows: 1

   * - Level
     - Metatiles
     - Hats
   * - 3
     - 442
     - 1,156
   * - 4
     - 3,025
     - 7,921
   * - 5
     - 20,737
     - 54,289
   * - 6
     - 142,129
     - 372,100

These are the numbers in the H supertile, the default; ``--supertile`` (or
``-s``) chooses T, P or F instead. Levels 4 and 5 make the most useful
pictures: a level 6 picture is around 30 MB, and slow to open.

A supertile has a ragged edge, so the picture is cropped to the largest
rectangle, centred on the patch, that has no gaps. ``--aspect`` sets its shape
(width / height, 1.5 by default), and ``--width`` its width in pixels. At low
levels, that rectangle holds only a few hats: ``--no-crop`` draws the whole
patch instead. ``--metatiles`` outlines each cluster's *metatile*, as in
Figure 4.1 of the paper:

.. code-block:: console

   $ einstein-tiling tiling --level 2 --no-crop --metatiles -o patch.svg

``-o -`` writes the SVG to standard output, for use in a pipeline.

Colours
-------

``--colour NAME=COLOUR`` sets a colour, and can be repeated (``--color`` works
too). Any SVG colour will do, including ``none``. Put a colour such as
``#d0e4f5`` in quotes, because some shells treat ``#`` specially:

.. code-block:: console

   $ einstein-tiling tiling --colour 'H=#f4d8cd' --colour reflected=navy \
       --colour outline=none -o tiling.svg

.. image:: _generated/colours.svg
   :alt: The tiling in shades of brown and cream, with the reflected hats in
         dark red.

These are the names, and their default colours:

.. include:: _generated/colours.inc

Drawing the clusters
====================

.. code-block:: console

   $ einstein-tiling clusters -o clusters.svg

draws Figure 4.1 of the paper: the four clusters of hats, with their metatiles
and the labels of the matching rules. ``--vertex-numbers`` numbers each hat's
corners.

Checking a patch
================

.. code-block:: console

   $ einstein-tiling check --level 5
   H at level 5: 20737 metatiles, 54289 hats, 0 rule violations

checks every edge that two metatiles share against the matching rules, and
checks that no two hats overlap along an edge. It exits with status 1 if
either check fails. The patches that einstein-tiling builds always pass; the
checks are there for patches made in other ways, and as a test of the
package.

The checks do not yet notice a *missing* tile: a hole in the middle of a
patch passes.

Using einstein-tiling from Python
=================================

:func:`~einstein_tiling.supertile` returns a supertile as a list of placed
metatiles:

>>> import einstein_tiling as et
>>> tiles = et.supertile("H", level=3)
>>> tiles[:2]
[('H', 0, (0, 0)), ('H', 0, (-8, 10))]

Each is a tuple ``(name, k, t)``: the cluster of that name, turned
anticlockwise by ``k`` × 60° and then moved by ``t``. The coordinates are exact
integers (see :ref:`exact-coordinates`). The clusters themselves are in
:data:`~einstein_tiling.CLUSTERS`.

:func:`~einstein_tiling.label_violations` checks a patch against the matching
rules, returning an empty list if it obeys them:

>>> et.label_violations(tiles)
[]

:func:`~einstein_tiling.tiling_svg` returns an SVG document as a string, and
takes the same options as the command line:

>>> svg = et.tiling_svg(tiles, width=800, colours={"reflected": "navy"})
>>> svg[:58]
'<svg xmlns="http://www.w3.org/2000/svg" width="800" height'

Write it to a file to view it::

    with open("tiling.svg", "w") as f:
        f.write(svg)

Using the coordinates
---------------------

:func:`~einstein_tiling.hat_polygons` gives each hat's corners as ordinary
``(x, y)`` coordinates, in units of the hat's short edge, for use with any other
software:

>>> name, reflected, vertices = next(et.hat_polygons(tiles))
>>> name, reflected, len(vertices)
('H', True, 13)

For example, to draw a patch with `Matplotlib <https://matplotlib.org>`_::

    import matplotlib.pyplot as plt

    fig, ax = plt.subplots()
    for name, reflected, vertices in et.hat_polygons(tiles):
        ax.fill(*zip(*vertices), "navy" if reflected else "lightblue",
                edgecolor="black", linewidth=0.3)
    ax.set_aspect("equal")
    ax.axis("off")
    plt.show()

Or to count the hats in a large patch. There are about 6.854 unreflected hats
for each reflected one, very close to φ⁴ ≈ 6.854, the factor by which the
tiles' area grows at each level:

>>> tiles = et.supertile("H", level=5)
>>> hats = [reflected for _, reflected, _ in et.hat_polygons(tiles)]
>>> len(hats), sum(hats)
(54289, 6912)
>>> round((len(hats) - sum(hats)) / sum(hats), 3)
6.854

Command-line reference
======================

The command exits with status 0 on success, 1 on an error (such as a file that
cannot be written, or a patch that breaks the rules) and 2 if its arguments
are wrong.

.. literalinclude:: _generated/help-tiling.txt
   :language: text

.. literalinclude:: _generated/help-clusters.txt
   :language: text

.. literalinclude:: _generated/help-check.txt
   :language: text
