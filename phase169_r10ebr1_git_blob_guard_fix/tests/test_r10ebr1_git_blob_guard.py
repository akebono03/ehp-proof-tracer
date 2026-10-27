"""Focused tests of the Git-object CRLF fix; no repository changes."""
from __future__ import annotations

import pytest

from phase169_r10eb_typed_composition_power import patch as original
from phase169_r10ebr1_git_blob_guard_fix.patch import TARGETS, prepare_patch


def _source_fixtures(newline: str) -> dict[str, bytes]:
    """Construct full, syntactically valid function fixtures for both targets."""
    if newline not in ("LF", "CRLF"):
        raise ValueError("unexpected test newline")
    samples = {
        "phase168_r3_27_typed_statement_projection.py": (
            "def element_tex(value):\n"
            + original.NARRATIVE_ANCHOR
            + ":\n        return None\n    return None\n"
        ),
        "toda_human_readable_renderer.py": (
            "def render_toda_expression_latex(expression):\n"
            + original.PUBLIC_ANCHOR
            + "\n    return 'fallback'\n"
        ),
    }
    return {
        name: text.replace("\n", "\r\n").encode("utf-8")
        if newline == "CRLF" else text.encode("utf-8")
        for name, text in samples.items()
    }


@pytest.mark.parametrize("newline", ["LF", "CRLF"])
def test_r10ebr1_accepts_exact_reviewed_blob_and_preserves_newline(
    monkeypatch: pytest.MonkeyPatch, newline: str,
) -> None:
    samples = _source_fixtures(newline)
    monkeypatch.setattr(
        "phase169_r10ebr1_git_blob_guard_fix.patch.TARGETS",
        {path: original._git_blob(source) for path, source in samples.items()},
    )
    output = prepare_patch(samples)
    assert set(output) == set(samples)
    for path, (patched, function, style) in output.items():
        assert style == newline
        assert "typed_stable_composition_power_latex" in function
        assert b"typed_stable_composition_power_latex" in patched
        if newline == "CRLF":
            assert b"\r\n" in patched
            assert b"\n" not in patched.replace(b"\r\n", b"")
        else:
            assert b"\r" not in patched
        assert patched != samples[path]


def test_r10ebr1_allows_valid_lf_checkout_for_crlf_blob(
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    samples = _source_fixtures("LF")
    crlf_committed = _source_fixtures("CRLF")
    monkeypatch.setattr(
        "phase169_r10ebr1_git_blob_guard_fix.patch.TARGETS",
        {path: original._git_blob(raw) for path, raw in crlf_committed.items()},
    )
    result = prepare_patch(samples)
    assert all(style == "LF" for _, _, style in result.values())


def test_r10ebr1_refuses_changed_source_without_mutating_inputs(
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    samples = _source_fixtures("CRLF")
    monkeypatch.setattr(
        "phase169_r10ebr1_git_blob_guard_fix.patch.TARGETS",
        {path: original._git_blob(raw) for path, raw in samples.items()},
    )
    before = dict(samples)
    changed = dict(samples)
    first = next(iter(TARGETS))
    changed[first] += b"# unreviewed change\r\n"
    with pytest.raises(RuntimeError, match="source Git blob not reviewed"):
        prepare_patch(changed)
    assert samples == before


def test_r10ebr1_mixed_newlines_refused(
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    samples = _source_fixtures("LF")
    changed = dict(samples)
    first = next(iter(TARGETS))
    changed[first] = changed[first].replace(b"\n", b"\r\n", 1)
    monkeypatch.setattr(
        "phase169_r10ebr1_git_blob_guard_fix.patch.TARGETS",
        {path: original._git_blob(raw) for path, raw in changed.items()},
    )
    with pytest.raises(RuntimeError, match="mixed"):
        prepare_patch(changed)


def test_r10ebr1_second_patch_refused(
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    samples = _source_fixtures("CRLF")
    monkeypatch.setattr(
        "phase169_r10ebr1_git_blob_guard_fix.patch.TARGETS",
        {path: original._git_blob(raw) for path, raw in samples.items()},
    )
    patched = {path: payload for path, (payload, _, _) in prepare_patch(samples).items()}
    with pytest.raises(RuntimeError, match="source Git blob not reviewed"):
        prepare_patch(patched)


def test_r10ebr1_missing_file_refused() -> None:
    with pytest.raises(RuntimeError, match="requires both"):
        prepare_patch({})
