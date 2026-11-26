from __future__ import annotations

import ast
import pytest

from phase178_r12r1_suspension_composition_display.installer import ANCHOR, HOOK, proposed_source, full_review_source
from phase178_r12r1_suspension_composition_display.projection import unique_body_anchor, project_owned_lines


def test_anchor_needs_unique_exact_body_line():
    lines = ['[R4]より, old.', '証明', '[R4]より, old.', '']
    assert unique_body_anchor(lines, 1, 'old.', [4]) == 2
    assert unique_body_anchor(lines, 1, 'old.', [5]) is None
    assert unique_body_anchor(lines + ['old.'], 1, 'old.', [4]) is None


def test_projection_preserves_all_lines_and_citations():
    lines = ['reference', '証明', '[R4]より, old.', '', 'old2.', '']
    rows = [(2, 2, 'old.', 'new.', [4]), (3, 4, 'old2.', 'new.', [])]
    assert project_owned_lines(lines, 1, rows) == ['reference', '証明', '[R4]より, new.', '', 'new.', '']
    assert lines[2] == '[R4]より, old.'


def test_shared_line_and_wrong_tag_not_changed():
    lines = ['reference', '証明', '[R4]より, old.']
    row = (2, 2, 'old.', 'new.', [4])
    assert project_owned_lines(lines, 1, [row, (3, *row[1:])]) == lines
    assert project_owned_lines(lines, 1, [(2, 2, 'old.', 'new.', [5])]) == lines
    assert project_owned_lines(lines, 1, [(2, 0, 'reference', 'new.', [])]) == lines


def test_installer_scopes_single_hook_and_exports_full_function():
    source = 'import os\n\ndef render_model_backed_narrative_markdown(result, model):\n    if True:\n' + ANCHOR + '    return lines\n\ndef untouched():\n    return 1\n'
    updated = proposed_source(source)
    assert updated == source.replace(ANCHOR, ANCHOR + HOOK)
    ast.parse(updated)
    review = full_review_source(updated)
    assert 'import os' in review and '    return lines' in review and HOOK in review
    assert 'def untouched' not in review
    with pytest.raises(RuntimeError):
        proposed_source(updated)
