
from __future__ import annotations

import ast

import audit_phase155_r3_3d_r1 as audit


def test_split_test_id_normalizes_backslashes():
    assert audit._split_test_id(
        r"tests\test_a.py::test_x"
    ) == (
        "tests/test_a.py",
        "test_x",
    )


def test_normalized_ignores_source_locations():
    a = "def test_x():\n  assert True\n"
    b = "\n\n\ndef test_x():\n  assert True\n"

    assert audit._normalized(a) == audit._normalized(b)


def test_function_sources_returns_all_same_name_definitions(
    tmp_path,
):
    path = tmp_path / "test_x.py"
    path.write_text(
        "def test_x():\n"
        "  assert True\n"
        "\n"
        "def test_x():\n"
        "  assert True\n",
        encoding="utf-8",
    )

    sources = audit._function_sources(
        path,
        "test_x",
    )

    assert len(sources) == 2


def test_function_sources_can_detect_divergent_bodies(
    tmp_path,
):
    path = tmp_path / "test_x.py"
    path.write_text(
        "def test_x():\n"
        "  assert True\n"
        "\n"
        "def test_x():\n"
        "  assert False\n",
        encoding="utf-8",
    )

    sources = audit._function_sources(
        path,
        "test_x",
    )
    hashes = [
        audit._hash(
            audit._normalized(source)
        )
        for source in sources
    ]

    assert len(set(hashes)) == 2
