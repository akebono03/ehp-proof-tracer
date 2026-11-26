from __future__ import annotations

import pytest

from phase178_r12_suspension_composition_audit.audit import (
    ancestor_indices, locate_sentence, preview_notation,
)


def test_ancestor_indices_tracks_identity_edges():
    assert ancestor_indices(((), (), (0,), (1, 2)), 3) == frozenset({0, 1, 2})
    assert ancestor_indices(((), (), (0,), (1, 2)), 2) == frozenset({0})


@pytest.mark.parametrize('parents', [((), (1,)), ((), (None,)), ((), (-1,)), ((), (True,))])
def test_invalid_edges_fail_closed(parents):
    with pytest.raises(ValueError):
        ancestor_indices(parents, 1)


def test_locate_sentence_requires_unique_body_anchor_and_actual_tag():
    lines = ['[R4]より, X.', '証明', '[R4]より, X.', '']
    assert locate_sentence(lines, 1, 'X.', [4]) == 2
    assert locate_sentence(lines, 1, 'X.', [5]) is None
    assert locate_sentence(lines + ['X.'], 1, 'X.', [4]) is None
    assert locate_sentence(lines, 1, None, [4]) is None


def test_preview_notation_preserves_citations_layout_and_input():
    lines = ['reference', '証明', '[R4]より, old.', '', 'last.']
    row = {'index': 3, 'body_line_index': 2, 'typed_sentence': 'old.',
           'canonical_sentence': 'new.', 'ancestor_citations': [4]}
    output, edits = preview_notation(lines, 1, [row])
    assert output == ['reference', '証明', '[R4]より, new.', '', 'last.']
    assert lines[2] == '[R4]より, old.'
    assert edits == [{'index': 3, 'line': 3, 'before': lines[2], 'after': output[2]}]
    assert preview_notation(lines, 1, [row, dict(row, index=4)]) == (lines, [])
    assert preview_notation(lines, 1, [dict(row, ancestor_citations=[5])]) == (lines, [])
    assert preview_notation(lines, 1, [dict(row, body_line_index=0)]) == (lines, [])
