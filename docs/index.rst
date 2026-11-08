***************
einstein-tiling
***************

The einstein-tiling package draws aperiodic tilings by the *hat*, the
"einstein" found by David Smith, Joseph Samuel Myers, Craig S. Kaplan and
Chaim Goodman-Strauss: a single shape that covers the plane with no gaps or
overlaps, but never in a repeating pattern.

.. image:: _generated/tiling.svg
   :alt: A patch of the hat tiling. Each hat is coloured by the kind of
         cluster it belongs to, and the reflected hats are dark blue.

It builds the tilings from the four clusters of hats and the matching rules of
their paper, `An aperiodic monotile <https://doi.org/10.5070/C64163843>`_, and
draws them as SVG images, from the command line:

.. code-block:: console

   $ einstein-tiling tiling --level 4 -o tiling.svg

or from Python:

>>> import einstein_tiling as et
>>> tiles = et.supertile("H", level=3)
>>> len(tiles)
442
>>> et.label_violations(tiles)
[]
>>> svg = et.tiling_svg(tiles, width=800)

The einstein-tiling package is pure Python, with no dependencies, and needs
Python 3.10 or later:

.. code-block:: console

   $ pip install einstein-tiling

.. toctree::
   :maxdepth: 2
   :caption: Contents

   guide
   how-it-works
   api
