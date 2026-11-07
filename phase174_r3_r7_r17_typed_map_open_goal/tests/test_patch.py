"""R17 guarded exact one-function replacement tests."""
from __future__ import annotations

import pytest

from phase174_r3_r7_r17_typed_map_open_goal.patch import (
    EXPECTED_BLOB, NEW, OLD, blob_sha, matches_git_blob,
    normalize_and_style, transform_source, export_complete_function,
)


def source_fixture() -> str:
    return (
        "def _group_proof_statement_latex(statement):\n"
        "  from expression import Expression\n"
        "  from homotopy_groups import TodaPrimaryGroup\n"
        "  from phase165_r12_r2_quotient_rules import CyclicStructureStatement\n"
        + OLD
        + "  ):\n"
        + "    return None, None\n"
        + "  return None, 'unhandled'\n"
    )


def test_exact_single_common_formatter_replacement_preserves_public_name() -> None:
    patched = transform_source(source_fixture())
    assert patched.count(NEW) == 1
    assert "def _group_proof_statement_latex(statement):" in patched
    assert "isinstance(statement, (MapInjective, MapSurjective, MapIsomorphism))" in patched
    assert "return (f'{symbol}: {source} {arrow} {target}', None)" in patched
    assert "  return None, 'unhandled'" in patched


def test_patch_never_accepts_reapplication_or_unreviewed_anchor() -> None:
    source = source_fixture()
    with pytest.raises(RuntimeError):
        transform_source(transform_source(source))
    with pytest.raises(RuntimeError):
        transform_source(source.replace("_group_proof_statement_latex", "other_formatter"))
    with pytest.raises(RuntimeError):
        transform_source(source + OLD)


@pytest.mark.parametrize("malformed", (
    b"one\r\ntwo\n", b"one\rtwo\r", b"\xef\xbb\xbfone\n",
))
def test_reject_unsafe_end_of_line_or_bom(malformed: bytes) -> None:
    with pytest.raises(RuntimeError):
        normalize_and_style(malformed)


def test_preserve_uniform_line_endings_and_strict_sha() -> None:
    assert normalize_and_style(b"one\ntwo\n") == ("one\ntwo\n", b"\n")
    assert normalize_and_style(b"one\r\ntwo\r\n") == ("one\ntwo\n", b"\r\n")
    assert len(EXPECTED_BLOB) == 40
    sha = blob_sha(b"one\ntwo\n")
    assert matches_git_blob(b"one\ntwo\n", sha)
    assert matches_git_blob(b"one\r\ntwo\r\n", sha)
    assert not matches_git_blob(b"one changed\ntwo\n", sha)
    assert not matches_git_blob(b"one\r\ntwo\n", sha)


def test_complete_replacement_function_is_exported(tmp_path) -> None:
    path = tmp_path / "MODIFIED_FUNCTION_FULL_JA.md"
    export_complete_function(transform_source(source_fixture()), path)
    content = path.read_text(encoding="utf-8")
    assert "def _group_proof_statement_latex(statement):" in content
    assert "from proof import Relation, RelationType" in content
    assert "from phase165_r14_r6_generic_iso import MapInjective, MapIsomorphism, MapSurjective" in content
    assert "  return None, 'unhandled'" in content
    assert "```python" in content


def test_replacement_contains_no_group_specific_dimension_or_generator() -> None:
    # The only map-specific distinction is the *type*, not a chosen n or k.
    patched = transform_source(source_fixture())
    addition = patched.split("  # A display projection", 1)[1].split("  if (\n    isinstance(statement, CyclicStructureStatement)", 1)[0]
    assert "sphere_dimension ==" not in addition
    assert "group_dimension ==" not in addition
    assert "nu_" not in addition
    assert "eta_" not in addition
