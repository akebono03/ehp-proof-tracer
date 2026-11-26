import pytest
from phase178_r11_hopf_zero_reason_display.installer import ANCHOR, HOOK, proposed_source


def test_scoped_hook():
    source = 'def map_property_sentence(statement, step):\n'+ANCHOR+'    return None\n'
    assert proposed_source(source)==source.replace(ANCHOR,HOOK+ANCHOR)


def test_refuse_missing_or_duplicate_hook():
    source = 'def map_property_sentence(statement, step):\n    return None\n'
    with pytest.raises(RuntimeError):
        proposed_source(source)
    source = 'def map_property_sentence(statement, step):\n'+HOOK+ANCHOR+'    return None\n'
    with pytest.raises(RuntimeError):
        proposed_source(source)
