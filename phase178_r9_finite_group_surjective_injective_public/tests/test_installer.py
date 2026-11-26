"""Check the single insertion and fail-closed source boundary."""
import pytest

from phase178_r9_finite_group_surjective_injective_public.installer import ANCHOR, HOOK, proposed_source, full_review_source


def test_single_hook_and_full_function_export():
    original = 'from __future__ import annotations\n\ndef shared_expansion_provider(bridge, extra_providers=()):\n' + ANCHOR + '    return extra_providers\n'
    revised = proposed_source(original)
    assert revised.replace(HOOK, '', 1) == original
    assert revised.count(HOOK) == 1
    review = full_review_source(revised)
    assert 'from __future__ import annotations' in review
    assert HOOK in review
    assert '    return extra_providers' in review


def test_reject_missing_duplicate_and_outside_anchor():
    for source in ('def shared_expansion_provider():\n    return ()\n', 'def shared_expansion_provider():\n' + ANCHOR + ANCHOR + '    return ()\n', 'def shared_expansion_provider():\n    return ()\n\ndef other():\n' + ANCHOR + '    return ()\n', 'def shared_expansion_provider():\n' + HOOK + ANCHOR + '    return ()\n'):
        with pytest.raises(RuntimeError):
            proposed_source(source)
