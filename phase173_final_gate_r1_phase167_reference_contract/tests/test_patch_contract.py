"""Offline checks for the Phase 167 historical Reference boundary fix."""
from __future__ import annotations

import ast
from pathlib import Path
from types import SimpleNamespace

import pytest

from phase173_final_gate_r1_phase167_reference_contract.patch import (
    BASE_BLOBS,
    TEST_FILES,
    normalized,
)


PACKAGE = Path(__file__).resolve().parents[1]


def _sources(name: str) -> tuple[str, str]:
    original = (PACKAGE / "expected" / name).read_text(encoding="utf-8")
    updated = (PACKAGE / "replacement" / name).read_text(encoding="utf-8")
    return original, updated


def _compiled_test_unit(name: str, unit: str):
    """Execute only the selected full function with a stand-in Web result."""
    source = (PACKAGE / "replacement" / name).read_text(encoding="utf-8")
    tree = ast.parse(source, filename=name)
    selected = next(
        node for node in tree.body
        if isinstance(node, ast.FunctionDef) and node.name == unit
    )
    module = ast.Module(body=[selected], type_ignores=[])
    ast.fix_missing_locations(module)
    namespace = {}
    exec(compile(module, name, "exec"), namespace)
    return namespace[unit], namespace


def _fake_line(kind: str, prefix: str, math: str | None = None):
    return SimpleNamespace(
        kind=kind, prefix=prefix, statement_latex=math, suffix="",
    )


@pytest.mark.parametrize("name", [Path(path).name for path in TEST_FILES])
def test_each_replacement_is_complete_python_and_preserves_other_functions(name: str) -> None:
    original, updated = _sources(name)
    a, b = ast.parse(original), ast.parse(updated)
    assert len(a.body) == len(b.body)
    changed = (
        "test_phase167_r2_pi43_reference_has_two_general_results"
        if name == "test_phase167_r2_shared_reference.py"
        else "_reference_text"
    )
    for before, after in zip(a.body, b.body):
        assert type(before) is type(after)
        if isinstance(before, ast.FunctionDef) and before.name == changed:
            assert ast.dump(before) != ast.dump(after)
        else:
            assert ast.dump(before) == ast.dump(after)
    assert 'and is_section(line, "証明")' in original
    assert 'and is_section(line, "証明")' not in updated
    assert 'line.kind == "separator"' in updated
    assert "assert len(separators) == 1" in updated


@pytest.mark.parametrize("name", (
    "test_phase167_r2_range_dedup.py",
    "test_phase167_r2_unified_reference.py",
))
def test_reference_helper_selects_one_separator_and_excludes_proof_body(name: str) -> None:
    helper, namespace = _compiled_test_unit(name, "_reference_text")
    lines = (
        _fake_line("heading", "使用する結果"),
        _fake_line("text", "Proposition 5.1"),
        _fake_line("text", "", r"\pi_{n}^{n}"),
        _fake_line("separator", ""),
        _fake_line("text", "should not be in Reference"),
    )
    namespace["build_standard_web_group_proof_view"] = (
        lambda *args: SimpleNamespace(key="generic-complete-proof", rendered_lines=lines)
    )
    value = helper(2, 1)
    assert "Proposition 5.1" in value
    assert r"\pi_{n}^{n}" in value
    assert "should not be in Reference" not in value


def test_reference_helper_rejects_duplicate_boundaries() -> None:
    helper, namespace = _compiled_test_unit(
        "test_phase167_r2_range_dedup.py", "_reference_text"
    )
    lines = (
        _fake_line("heading", "使用する結果"),
        _fake_line("separator", ""),
        _fake_line("separator", ""),
    )
    namespace["build_standard_web_group_proof_view"] = (
        lambda *args: SimpleNamespace(key="generic-complete-proof", rendered_lines=lines)
    )
    with pytest.raises(AssertionError):
        helper(2, 1)


def test_shared_reference_test_preserves_general_form_assertions() -> None:
    name = "test_phase167_r2_shared_reference.py"
    test, namespace = _compiled_test_unit(
        name, "test_phase167_r2_pi43_reference_has_two_general_results"
    )
    lines = (
        _fake_line("heading", "使用する結果"),
        _fake_line("text", "Proposition 5.1"),
        _fake_line("text", "", r"\pi_{n}^{n}"),
        _fake_line("text", "", r"\pi_i^n=0"),
        _fake_line("separator", ""),
        _fake_line("text", "proof follows"),
    )
    namespace["build_standard_web_group_proof_view"] = (
        lambda *args: SimpleNamespace(key="generic-complete-proof", rendered_lines=lines)
    )
    test()


def test_only_three_test_paths_and_reviewed_source_guards() -> None:
    assert len(TEST_FILES) == 3
    assert len(BASE_BLOBS) == 7
    assert "phase168_r3_5_model_renderer.py" in BASE_BLOBS
    assert "phase173_r4_r15r13_unified_presentation/layout.py" in BASE_BLOBS
    assert normalized("a\r\nb\r\n") == "a\nb\n"


def test_frozen_originals_match_reviewed_git_blobs() -> None:
    """The three complete original sources must match the reviewed Git blobs."""
    import hashlib

    for path in TEST_FILES:
        raw = (PACKAGE / "expected" / Path(path).name).read_bytes()
        possibilities = (raw, raw.replace(b"\n", b"\r\n"))
        hashes = {
            hashlib.sha1(
                b"blob " + str(len(candidate)).encode("ascii") + b"\x00" + candidate
            ).hexdigest()
            for candidate in possibilities
        }
        assert BASE_BLOBS[path] in hashes
