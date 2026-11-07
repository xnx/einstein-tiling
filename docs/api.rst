*************
API reference
*************

These names can be imported from ``einstein_tiling``.

.. currentmodule:: einstein_tiling

Building patches
================

.. autofunction:: supertile

.. data:: CLUSTERS

   The four clusters of Figure 4.1, as a dict from ``"H"``, ``"T"``, ``"P"``
   and ``"F"`` to :class:`~einstein_tiling.hat_data.Cluster` objects.

.. autoclass:: einstein_tiling.hat_data.Cluster
   :members: hat_outlines, segments

Checking patches
================

.. autofunction:: label_violations

.. autofunction:: hat_edges

.. autofunction:: rim

Drawing
=======

.. autofunction:: tiling_svg

.. data:: COLOURS

   The default colours of :func:`tiling_svg`, as a dict from each name to an
   SVG colour:

   .. include:: _generated/colours.inc

.. autofunction:: clusters_svg

.. autofunction:: hat_polygons

.. autofunction:: metatile_polygons
