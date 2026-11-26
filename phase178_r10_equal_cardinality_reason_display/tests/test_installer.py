import pytest
from phase178_r10_equal_cardinality_reason_display.installer import ANCHOR, HOOK, proposed_source, full_review_source


def test_single_function_and_export():
    original='from __future__ import annotations\n\ndef map_property_sentence(statement, step):\n'+ANCHOR+'    return premises\n\ndef other():\n    return None\n'
    revised=proposed_source(original)
    assert revised.replace(HOOK,'',1)==original
    assert revised.count(HOOK)==1
    review=full_review_source(revised)
    assert 'from __future__ import annotations' in review and HOOK in review and '    return premises' in review
    assert 'def other' not in review


def test_reject_missing_duplicate_or_preinstalled_hook():
    for source in ('def map_property_sentence():\n    return None\n',
                   'def map_property_sentence():\n'+ANCHOR+ANCHOR+'    return None\n',
                   'def map_property_sentence():\n'+HOOK+ANCHOR+'    return None\n'):
        with pytest.raises(RuntimeError):
            proposed_source(source)
