import pytest

import einstein_tiling as et

FIBONACCI = [1, 1, 2, 3, 5, 8, 13, 21, 34, 55, 89, 144, 233]


@pytest.mark.parametrize("level", range(5))
def test_hat_counts_are_fibonacci_squares(level):
    tiles = et.supertile("H", level)
    hats = sum(len(et.CLUSTERS[name].hats) for name, _, _ in tiles)
    assert hats == FIBONACCI[2 * level + 2] ** 2


@pytest.mark.parametrize("name", "HTPF")
@pytest.mark.parametrize("level", range(5))
def test_patches_obey_the_matching_rules(name, level):
    tiles = et.supertile(name, level)
    assert et.label_violations(tiles) == []
    et.hat_edges(tiles)


def test_coordinates_are_integers():
    for _, k, (a, b) in et.supertile("F", 3):
        assert (type(k), type(a), type(b)) == (int, int, int)


def test_rotated_tile_is_rejected():
    tiles = et.supertile("H", 3)
    name, k, t = tiles[100]
    tiles[100] = name, (k + 1) % 6, t
    with pytest.raises(ValueError):
        et.label_violations(tiles)


def test_duplicate_tile_is_rejected():
    tiles = et.supertile("H", 3)
    with pytest.raises(ValueError):
        et.label_violations(tiles + tiles[:1])


def test_removing_a_tile_lengthens_the_rim():
    tiles = et.supertile("H", 3)
    assert (len(et.rim(et.hat_edges(tiles[:100] + tiles[101:])))
            > len(et.rim(et.hat_edges(tiles))))


@pytest.mark.parametrize("name, level", [("X", 1), ("H", -1)])
def test_bad_arguments_are_rejected(name, level):
    with pytest.raises(ValueError):
        et.supertile(name, level)


def test_svg_documents_are_well_formed():
    from xml.dom.minidom import parseString
    parseString(et.clusters_svg())
    parseString(et.clusters_svg(show_vertex_numbers=True))
    tiles = et.supertile("H", 2)
    parseString(et.tiling_svg(tiles))
    parseString(et.tiling_svg(tiles, crop=False, show_metatiles=True))


def test_whole_patch_draws_every_hat():
    tiles = et.supertile("T", 2)
    hats = sum(1 for _ in et.hat_polygons(tiles))
    assert et.tiling_svg(tiles, crop=False).count("<polygon") == hats


def test_colours_can_be_overridden():
    svg = et.tiling_svg(et.supertile("H", 2), colours={"F": "#123456"})
    assert "#123456" in svg


def test_every_colour_can_be_set():
    colours = {name: f"#{i:06x}" for i, name in enumerate(et.COLOURS, 1)}
    svg = et.tiling_svg(et.supertile("H", 3), show_metatiles=True,
                        colours=colours)
    for value in colours.values():
        assert value in svg


def test_unknown_colour_name_is_rejected():
    with pytest.raises(ValueError, match="unknown colour name h"):
        et.tiling_svg(et.supertile("H", 1), colours={"h": "red"})


def test_colour_values_cannot_break_the_svg():
    from xml.dom.minidom import parseString
    svg = et.tiling_svg(et.supertile("H", 2),
                        colours={"H": 'red"/><script>alert(1)</script>'})
    assert "<script>" not in svg
    parseString(svg)
