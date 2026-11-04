"""Pure DryRun previews of reviewed presentation changes, no repository edits."""
from __future__ import annotations

import pytest

from phase173_r4_r15r16_verified_progress_punctuation.projection_patch import (
    LAYOUT_APPEND,
    LAYOUT_OLD,
    PROJECTION_NEW,
    PROJECTION_OLD,
    patch_layout,
    patch_projection,
)


def test_projection_patch_is_single_replacement() -> None:
    proposed = patch_projection(PROJECTION_OLD)
    assert proposed.count("def _verified_abstract_progress_lines(") == 1
    assert proposed.count("def _render_abstract_claim(") == 1
    assert "## 検証済みの途中経過" in proposed
    assert "## 証明済みの抽象群構造" in proposed
    compile(proposed, "reviewed-projection.py", "exec")


def test_layout_patch_has_one_shared_formatter() -> None:
    proposed = patch_layout(LAYOUT_OLD)
    assert proposed.count("def _normalize_narrative_punctuation(") == 1
    assert proposed.count("_normalize_narrative_punctuation(normalized)") == 1
    compile("def example(markdown, normalized):\n" + LAYOUT_OLD, "preview.py", "exec")


def test_prose_punctuation_preview_and_math_protection() -> None:
    namespace: dict[str, object] = {}
    exec(compile(LAYOUT_APPEND, "reviewed-punctuation.py", "exec"), namespace)
    normalize = namespace["_normalize_narrative_punctuation"]
    result = normalize([
        "確認した。次に、証明する。",
        "**[R1] Proposition 4.4.**",
        r"$H(\nu_4)=\iota_7$ と $\pi_{12}^{4}$ を使う。",
    ])
    assert result[0] == "確認した."
    assert result[1] == "次に, 証明する."
    assert result[2] == "**[R1] Proposition 4.4.**"
    assert r"$H(\nu_4)=\iota_7$" in result[3]


def test_conflicting_source_is_rejected() -> None:
    with pytest.raises(RuntimeError):
        patch_layout("unrelated text")
    with pytest.raises(RuntimeError):
        patch_projection("unrelated text")
    assert "No new proof step" in PROJECTION_NEW
