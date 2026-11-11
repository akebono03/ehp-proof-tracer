"""R67 focused proof-safe arrow contracts and negative source-guard tests."""
from __future__ import annotations

from pathlib import Path

import pytest

from phase174_r3_r7_r67_zero_map_tex_arrow_fix.install import (
    NEW_LINE, OLD_LINE, REVIEWED_BLOB, TARGET, git_blob_sha,
    normalized_contents, review_patch, verified_function,
)


def sample_source() -> bytes:
    return (
        "def typed_sentence(statement, step):\n"
        "    if True:\n"
        + OLD_LINE + "\n"
        + "    return None\n"
    ).encode("utf-8")


def test_reviewed_target_patched_exactly_once() -> None:
    root = Path(__file__).resolve().parents[2]
    raw = (root / TARGET).read_bytes()
    status, output = review_patch(raw)
    assert status == "ALREADY_APPLIED"
    normalized, _ = normalized_contents(output)
    assert normalized.count(NEW_LINE) == 1
    assert OLD_LINE not in normalized
    before = normalized.replace(NEW_LINE, OLD_LINE, 1)
    assert REVIEWED_BLOB in {
        git_blob_sha(before.encode("utf-8")),
        git_blob_sha(before.replace("\n", "\r\n").encode("utf-8")),
    }
    assert verified_function(output).count(NEW_LINE) == 1


@pytest.mark.parametrize("n,k", [(5, 5), (6, 5), (8, 5)])
def test_general_typed_zero_map_arrow(n: int, k: int) -> None:
    from homotopy_groups import TodaPrimaryGroup, TodaSuspensionMap
    from map_property_rules import ImageZeroStatement
    from phase168_r3_27_typed_statement_projection import typed_sentence

    source = TodaPrimaryGroup(n + k, n)
    target = TodaPrimaryGroup(n + k + 1, n + 1)
    sentence = typed_sentence(ImageZeroStatement(TodaSuspensionMap(source, target)), None)
    assert sentence == rf"$E:\pi_{{{n + k}}}^{{{n}}}\to \pi_{{{n + k + 1}}}^{{{n + 1}}}$ は零写像."
    assert r"\\to" not in sentence


def test_patch_accepts_lf_and_crlf_without_duplication(monkeypatch: pytest.MonkeyPatch) -> None:
    import phase174_r3_r7_r67_zero_map_tex_arrow_fix.install as module
    text = sample_source()
    monkeypatch.setattr(module, "REVIEWED_BLOB", git_blob_sha(text))
    for content in (text, text.replace(b"\n", b"\r\n")):
        status, new_bytes = module.review_patch(content)
        assert status == "PATCH_REQUIRED"
        assert new_bytes.count(b"\r\n") == content.count(b"\r\n")
        assert b"\r\r\n" not in new_bytes
        repeat_status, repeat_bytes = module.review_patch(new_bytes)
        assert repeat_status == "ALREADY_APPLIED"
        assert repeat_bytes == new_bytes


def test_unreviewed_source_is_refused(monkeypatch: pytest.MonkeyPatch) -> None:
    import phase174_r3_r7_r67_zero_map_tex_arrow_fix.install as module
    valid = sample_source()
    monkeypatch.setattr(module, "REVIEWED_BLOB", git_blob_sha(valid))
    altered = valid + b"# altered\n"
    with pytest.raises(RuntimeError, match="R67_SOURCE_GUARD_FAILED"):
        module.review_patch(altered)


def test_reject_mixed_line_endings_and_carriage_return_only() -> None:
    with pytest.raises(RuntimeError, match="R67_MIXED_LINE_ENDINGS"):
        normalized_contents(b"one\r\ntwo\n")
    with pytest.raises(RuntimeError, match="R67_UNEXPECTED_CR_ONLY"):
        normalized_contents(b"one\rtwo\n")


def test_reject_unknown_anchor(monkeypatch: pytest.MonkeyPatch) -> None:
    import phase174_r3_r7_r67_zero_map_tex_arrow_fix.install as module
    text = b"def unrelated():\n    return True\n"
    monkeypatch.setattr(module, "REVIEWED_BLOB", git_blob_sha(text))
    with pytest.raises(RuntimeError, match="R67_SOURCE_GUARD_FAILED"):
        module.review_patch(text)


def test_mathjax_arrow_in_other_map_format_unchanged() -> None:
    from homotopy_groups import TodaPrimaryGroup, TodaSuspensionMap
    from phase165_r14_r6_generic_iso import MapSurjective
    from phase168_r3_27_typed_statement_projection import typed_sentence
    source = TodaPrimaryGroup(11, 6)
    target = TodaPrimaryGroup(12, 7)
    sentence = typed_sentence(MapSurjective(TodaSuspensionMap(source, target)), None)
    assert sentence is not None
    assert r"\to" in sentence
    assert r"\\to" not in sentence
