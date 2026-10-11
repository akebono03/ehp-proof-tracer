from pathlib import Path

from phase163_r4_r41_tex_inventory import inspect_sources


def test_missing_source_explicit(tmp_path: Path) -> None:
    result = inspect_sources(tmp_path)
    assert len(result) == 5
    assert all(item["status"] == "MISSING" for item in result)


def test_tex_is_unchanged_and_duplicate_labels_reported(tmp_path: Path) -> None:
    path = tmp_path / "Toda_01.tex"
    original = "\\section{開始}\n\\label{a}\n\\label{a}\n\\label{b}\n"
    path.write_text(original, encoding="utf-8")
    item = inspect_sources(tmp_path)[0]
    assert item["status"] == "READABLE"
    assert item["labels"] == ["a", "a", "b"]
    assert item["duplicate_labels"] == ["a"]
    assert path.read_text(encoding="utf-8") == original


def test_unreadable_encoding_is_reported(tmp_path: Path) -> None:
    (tmp_path / "Toda_02.tex").write_bytes(b"\xff\xfe")
    assert inspect_sources(tmp_path)[1]["status"] == "ENCODING_UNRESOLVED"
