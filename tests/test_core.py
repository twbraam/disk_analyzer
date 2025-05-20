import os
from disk_analyzer.core import get_size, find_largest_entries


def test_get_size_file_and_directory(tmp_path):
    file_path = tmp_path / "file.txt"
    file_path.write_bytes(b"x" * 123)

    subdir = tmp_path / "subdir"
    subdir.mkdir()
    (subdir / "inner.txt").write_bytes(b"y" * 10)

    # single file size
    assert get_size(str(file_path)) == 123
    # directory size should include contents
    expected = 123 + 10
    assert get_size(str(tmp_path)) == expected


def test_find_largest_entries(tmp_path):
    (tmp_path / "small.txt").write_bytes(b"a" * 10)

    d1 = tmp_path / "d1"
    d1.mkdir()
    (d1 / "big.txt").write_bytes(b"b" * 100)

    d2 = tmp_path / "d2"
    d2.mkdir()
    (d2 / "bigger.txt").write_bytes(b"c" * 150)

    results = find_largest_entries(str(tmp_path), top_n=3)
    names = [os.path.basename(e.path) for e in results]
    sizes = [e.size for e in results]

    assert names == ["d2", "d1", "small.txt"]
    assert sizes == [150, 100, 10]

