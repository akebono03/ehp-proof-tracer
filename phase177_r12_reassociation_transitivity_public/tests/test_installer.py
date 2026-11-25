import pytest

from phase177_r12_reassociation_transitivity_public.installer import (
    ANCHOR, PATCH, R11_PATCH, full_review_source, proposed_source,
)


def baseline():
    return ('import os\n\ndef shared_expansion_provider():\n'
            '    def expand(goal):\n' + R11_PATCH + ANCHOR + '    return expand\n\n'
            'def unrelated():\n    return None\n')


def test_exact_insertion_and_full_review():
    original = baseline()
    revised = proposed_source(original)
    assert revised.replace(PATCH, '', 1) == original
    review = full_review_source(revised)
    assert 'import os' in review and R11_PATCH in review and PATCH in review
    assert 'def unrelated' not in review


def test_refuse_missing_anchor_or_duplicate():
    original = baseline()
    for source in (original.replace(R11_PATCH, ''), original.replace(ANCHOR, '        return None\n'), proposed_source(original)):
        with pytest.raises(ValueError):
            proposed_source(source)
