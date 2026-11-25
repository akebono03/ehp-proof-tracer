import pytest

from phase177_r8_unsigned_delta_public.installer import (
    ANCHOR, PATCH, R7R1_PATCH, SETUP, SETUP_ANCHOR, full_review_source, proposed_source,
)


def baseline():
    return ('import os\n\ndef shared_expansion_provider():\n'
            + SETUP_ANCHOR + '    )\n    def expand(goal):\n'
            + R7R1_PATCH + ANCHOR + '    return expand\n\ndef unrelated():\n    return None\n')


def test_exact_insertion_and_full_review():
    old = baseline()
    revised = proposed_source(old)
    assert revised.replace(SETUP, '', 1).replace(PATCH, '', 1) == old
    review = full_review_source(revised)
    assert 'import os' in review and SETUP in review and PATCH in review
    assert 'def unrelated' not in review


def test_refuse_missing_anchor_or_duplicate():
    old = baseline()
    for bad in (old.replace(R7R1_PATCH, ''), old.replace(SETUP_ANCHOR, '    other = dict(\n'), proposed_source(old)):
        with pytest.raises(ValueError):
            proposed_source(bad)
