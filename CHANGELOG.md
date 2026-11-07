# Changelog

## 0.2.0 (unreleased)

### Added

- Colours for every part of a tiling: `tiling_svg()` now also takes
  `reflected`, `outline`, `metatile` and `background` in `colours`, and the
  `tiling` command has `--colour NAME=COLOUR` (or `--color`). The defaults are
  in `COLOURS`. The default output is unchanged.
- `CITATION.cff`, for GitHub's "Cite this repository".
- Documentation at https://einstein-tiling.readthedocs.io: a user guide, an
  explanation of how the tilings are made, and an API reference. Its examples
  are tested with the rest of the code.

## 0.1.0 (3 November 2026)

The first release: hat tilings built by substitution, checked against the
matching rules of Figure 4.1 of the paper, and drawn as SVG, from Python or
the command line.
