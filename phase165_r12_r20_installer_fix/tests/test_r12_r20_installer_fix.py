"""Regression test for shared source tuple installation syntax."""
from __future__ import annotations

import ast
from pathlib import Path


def test_eta_source_injection_preserves_balanced_parentheses():
    original = (
        "        sources = (production, build_adopted_typed_reference_registry(adopted_tex),\n"
        "                   build_adopted_toda51_zero_reference(adopted_tex))\n"
    )
    needle = "build_adopted_toda51_zero_reference(adopted_tex))"
    replacement = (
        needle[:-1]
        + ", build_cited_eta_family_definition(Path(__file__).resolve().parent "
        + "/ 'sources' / 'toda' / 'Toda_05_2.tex'))"
    )
    modified = original.replace(needle, replacement, 1)
    ast.parse("from pathlib import Path\n" + "def f():\n" + modified)
    assert modified.count("build_cited_eta_family_definition(") == 1


def test_installer_source_contains_corrected_replacement():
    source = (Path(__file__).resolve().parents[1] / "install.py").read_text(encoding="utf8")
    ast.parse(source)
    assert 'needle2[:-1] + ", build_cited_eta_family_definition(Path(__file__).resolve().parent / \'sources\' / \'toda\' / \'Toda_05_2.tex\'))"' in source
