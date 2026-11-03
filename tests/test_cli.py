import subprocess
import sys

import pytest

import einstein_tiling as et
from einstein_tiling.cli import main


def test_a_closed_pipe_is_silent():
    process = subprocess.Popen(
        [sys.executable, "-m", "einstein_tiling", "tiling", "-l", "4", "-o", "-"],
        stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    process.stdout.readline()
    process.stdout.close()
    assert process.stderr.read() == b""
    process.stderr.close()
    process.wait()


def test_tiling_matches_the_api(tmp_path):
    path = tmp_path / "out.svg"
    assert main(["tiling", "-l", "2", "-o", str(path)]) == 0
    assert path.read_text() == et.tiling_svg(et.supertile("H", 2))


def test_clusters_to_standard_output(capsys):
    assert main(["clusters", "-o", "-"]) == 0
    assert capsys.readouterr().out == et.clusters_svg()


def test_check_reports_a_good_patch(capsys):
    assert main(["check", "-l", "2", "-s", "P"]) == 0
    assert "0 rule violations" in capsys.readouterr().out


def test_unwritable_output_is_an_error(tmp_path, capsys):
    assert main(["tiling", "-l", "1", "-o", str(tmp_path / "no/dir.svg")]) == 1
    assert capsys.readouterr().err.startswith("error:")


@pytest.mark.parametrize("arguments", [
    ["tiling", "--level", "-1"], ["tiling", "--width", "0"],
    ["tiling", "-s", "X"], ["unknown"], [],
])
def test_bad_usage_exits_with_status_2(arguments):
    with pytest.raises(SystemExit) as stop:
        main(arguments)
    assert stop.value.code == 2


def test_version(capsys):
    with pytest.raises(SystemExit) as stop:
        main(["--version"])
    assert stop.value.code == 0
    assert et.__version__ in capsys.readouterr().out

def test_width_and_aspect_options(tmp_path):
    path = tmp_path / "out.svg"
    assert main(["tiling", "-l", "2", "--width", "800", "--aspect", "2",
                 "-o", str(path)]) == 0
    assert path.read_text().startswith(
        '<svg xmlns="http://www.w3.org/2000/svg" width="800" height="400"')


def test_wrong_cluster_breaks_the_rules():
    tiles = et.supertile("H", 3)
    i = next(i for i, (name, _, _) in enumerate(tiles) if name == "P")
    _, k, t = tiles[i]
    tiles[i] = "F", k, t           # Same hats, different boundary.
    assert et.label_violations(tiles)
