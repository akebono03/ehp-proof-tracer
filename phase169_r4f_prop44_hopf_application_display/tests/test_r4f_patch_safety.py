"""R4F edit must be limited to one function under reviewed R4E anchor."""
from __future__ import annotations

import ast

import pytest

from phase169_r4f_prop44_hopf_application_display.patch import (
    _HOPF_APPLICABILITY,
    _INJECTION_ANCHOR,
    updated_hopf_application,
)


def test_r4f_only_one_rendering_function_is_modified():
    original = (
        "def helper():\n"
        "    return 5\n\n"
        "def render_model_backed_narrative_markdown():\n"
        "    if True:\n"
        + _INJECTION_ANCHOR
        + "    return 4\n"
    )
    # The anchor is nested in the actual source under conditional blocks;
    # this synthetic function is solely a parser-level change boundary test.
    updated = updated_hopf_application(original)
    before = ast.parse(original).body
    after = ast.parse(updated).body
    assert ast.dump(before[0], include_attributes=False) == ast.dump(after[0], include_attributes=False)
    assert "Hopf fibration" in updated
    assert "nu_4" in _HOPF_APPLICABILITY  # Never invoked, documented as forbidden


def test_r4f_missing_anchor_rejected():
    with pytest.raises(RuntimeError, match="baseline mismatch"):
        updated_hopf_application("def render_model_backed_narrative_markdown():\n    pass\n")


def test_r4f1_patch_keeps_the_original_r4e_injectivity_sentence():
    from phase169_r4f_prop44_hopf_application_display.patch import (
        _INJECTION_ANCHOR,
        updated_hopf_application,
    )
    original = (
        "def render_model_backed_narrative_markdown():\n"
        "    if True:\n"
        + _INJECTION_ANCHOR
        + "    return 4\n"
    )
    revised = updated_hopf_application(original)
    assert revised.count(_INJECTION_ANCHOR) == 1
    assert 'lines.extend((application, ""))' in revised
    assert revised.index('lines.extend((application, ""))') > revised.index(_INJECTION_ANCHOR)
    assert 'sentence = (' not in revised
