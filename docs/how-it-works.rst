************
How it works
************

einstein-tiling follows Smith, Myers, Kaplan and Goodman-Strauss,
`An aperiodic monotile <https://doi.org/10.5070/C64163843>`_, *Combinatorial
Theory* 4(1) (2024), © the authors, released under the
`CC BY 4.0 <https://creativecommons.org/licenses/by/4.0/>`_ licence. The figure
numbers here are those of that paper. The picture of the four clusters below
is redrawn from its Figure 4.1.

The hat
=======

The hat is a *polykite*: eight kites of the [3.4.6.4] Laves tiling, the tiling
of the plane by kites that each make up one sixth of a hexagon. Its outline
has 13 edges, of lengths 1 and √3, apart from one edge of length 2. Every
tiling by hats uses some reflected hats as well as unreflected ones.

Clusters, metatiles and matching rules
======================================

The paper groups the hats of any hat tiling into four kinds of *cluster*
(Figure 4.1):

.. image:: _generated/clusters.svg
   :alt: Figure 4.1: the four clusters T, H, P and F, with their metatiles
         outlined in green and the edge labels of the matching rules.

- **H**: four hats, one of them reflected (H\ :sub:`1`, in the middle).
- **T**: a single hat.
- **P** and **F**: two hats each.

Each cluster is simplified to a *metatile*, outlined in green: a hexagon,
a triangle, a parallelogram and a pentagon. Marked points divide each
metatile's boundary into segments, and the labels on the segments are the
*matching rules*. Where two metatiles meet, A\ :sup:`+` must meet
A\ :sup:`−`, and likewise for B, X and F, while L meets L. The metatiles are
only ever rotated, never reflected.

Following the rules, the hats of neighbouring clusters fit together exactly,
so any tiling by the metatiles gives a tiling by hats.

Why substitution
================

The matching rules are local, but they are not enough to build a tiling one
tile at a time: a patch can obey every rule and still be impossible to
extend, so a tile placed early can turn out to be wrong much later.

So einstein-tiling builds tilings by *substitution* (Figure 2.6), and uses the
matching rules to check the result. At each level:

1. 29 copies of the four tiles are fitted together edge to edge, using the
   table of placements in `hatviz <https://github.com/isohedral/hatviz>`_.
2. 22 of them become the children of the next level's four *supertiles*: ten
   in H, one in T, five in P and six in F. The rest only position the others.
3. The supertiles' outlines are worked out from a few key points of the
   patch, and the rule that their interior angles are 120°. They are not
   scaled copies of the metatiles.

The supertiles have the same matching rules as the metatiles, so the
same steps build the next level, and so on. Here are levels 0, 1 and 2 of the
H supertile (not to scale):

.. list-table::
   :header-rows: 1

   * - Level 0
     - Level 1
     - Level 2
   * - .. image:: _generated/level0.svg
          :alt: Level 0: a single H cluster of four hats.
     - .. image:: _generated/level1.svg
          :alt: Level 1: ten metatiles.
     - .. image:: _generated/level2.svg
          :alt: Level 2: 64 metatiles.

The numbers of hats in the H supertile, 4, 25, 169, 1,156, 7,921, ..., are the
squares of every other Fibonacci number, and the area of the tiles grows by
the factor φ⁴ ≈ 6.854 at each level, where φ is the golden ratio.

.. _exact-coordinates:

Exact coordinates
=================

Every corner of every hat lies on a triangular lattice, so einstein-tiling
stores a point as two integers ``(a, b)``, standing for a + b ω, where
ω = e\ :sup:`iπ/3`, in units of the hat's short edge. Rotating by 60° is then
``(a, b) → (−b, a + b)``. The corners of the supertiles' outlines can be
fractions, so they are kept as exact :class:`fractions.Fraction` values, but
the metatiles' placements always come out as integers.

So floating-point numbers appear only when drawing, and in
:func:`~einstein_tiling.hat_polygons` and
:func:`~einstein_tiling.metatile_polygons`, and the checks compare coordinates
exactly.

How patches are checked
=======================

:func:`~einstein_tiling.label_violations` splits every metatile's boundary into
steps, and checks that wherever two metatiles share a step, their labels are
complementary and line up. :func:`~einstein_tiling.hat_edges` traces every
hat's outline anticlockwise, so that two hats that meet share each edge in
opposite directions: an edge used twice in the same direction means two hats
overlap.

The edges that have no partner, from :func:`~einstein_tiling.rim`, form the
patch's outer boundary. The cropped pictures use them to find the largest
rectangle with no gaps. A hole in the middle of a patch would also show up in
the rim, but the checks do not yet look for one.
