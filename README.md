# einstein-tiling

Generate aperiodic tilings by the hat monotile as SVG images, using the clusters
and matching rules of Smith, Myers, Kaplan and Goodman-Strauss,
[An aperiodic monotile](https://arxiv.org/abs/2303.10798).

It has no dependencies, and uses exact integer coordinates throughout.

## Command line

```console
$ einstein-tiling tiling --level 4 -o tiling.svg
$ einstein-tiling tiling --level 3 --metatiles --no-crop -o patch.svg
$ einstein-tiling clusters -o clusters.svg
$ einstein-tiling check --level 5
```

## Python

```python
import einstein_tiling as et

tiles = et.supertile("H", level=4)
assert not et.label_violations(tiles)

with open("tiling.svg", "w") as f:
    f.write(et.tiling_svg(tiles, width=1200))

for cluster, reflected, vertices in et.hat_polygons(tiles):
    ...  # Each hat's (x, y) vertices, for use with any plotting library.
```

## Licence

BSD-3-Clause. The substitution rules are adapted from
[hatviz](https://github.com/isohedral/hatviz) by Craig S. Kaplan: see
`LICENSES/hatviz-BSD-3-Clause.txt`.
