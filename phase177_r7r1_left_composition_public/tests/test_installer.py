import pytest

from phase177_r7r1_left_composition_public.installer import ANCHOR, PATCH, R6_PATCH, proposed_source, full_review_source


def baseline():
    return ('import os\n\ndef shared_expansion_provider():\n'
            '    def expand(goal):\n' + R6_PATCH + ANCHOR + '    return expand\n\n'
            'def unrelated():\n    return None\n')


def test_exact_insertion_and_review():
    original = baseline()
    revised = proposed_source(original)
    assert revised.replace(PATCH, '', 1) == original
    review = full_review_source(revised)
    assert 'import os' in review and R6_PATCH in review and PATCH in review
    assert 'def unrelated' not in review


def test_fail_closed_on_wrong_anchor_or_duplicate():
    original = baseline()
    for source in (original.replace(R6_PATCH, ''), original.replace(ANCHOR, '        return None\n'), proposed_source(original)):
        with pytest.raises(ValueError):
            proposed_source(source)
