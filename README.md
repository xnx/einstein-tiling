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
$ einstein-tiling tiling --colour 'H=#d0e4f5' --colour reflected=navy -o tiling.svg
```

The colour names are `H`, `T`, `P` and `F` for the hats in each kind of
cluster, `reflected` for the reflected hats, `outline`, `metatile` and
`background`. Any SVG colour works, including `none`.

## Python

```python
import einstein_tiling as et

tiles = et.supertile("H", level=4)
assert not et.label_violations(tiles)

with open("tiling.svg", "w") as f:
    f.write(et.tiling_svg(tiles, width=1200, colours={"reflected": "navy"}))

for cluster, reflected, vertices in et.hat_polygons(tiles):
    ...  # Each hat's (x, y) vertices, for use with any plotting library.
```

## Citing

If you use this software, please cite it, and the papers it implements:
GitHub's "Cite this repository" button gives the details from `CITATION.cff`.

- David Smith, Joseph Samuel Myers, Craig S. Kaplan and Chaim Goodman-Strauss,
  "An aperiodic monotile", *Combinatorial Theory* 4(1) (2024),
  [doi:10.5070/C64163843](https://doi.org/10.5070/C64163843).

## Licence

BSD-3-Clause. The substitution rules are adapted from
[hatviz](https://github.com/isohedral/hatviz) by Craig S. Kaplan: see
`LICENSES/hatviz-BSD-3-Clause.txt`.
