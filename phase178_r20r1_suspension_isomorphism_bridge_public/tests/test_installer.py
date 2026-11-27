"""Pure installer contract: no repository mutations."""
import pytest
from phase178_r20r1_suspension_isomorphism_bridge_public import installer


def test_append_anchor():
    source = 'def expand():\n    def inner():\n' + installer.RETURN_ANCHOR
    updated = installer.proposed_source(source)
    assert updated == source.replace(installer.RETURN_ANCHOR, installer.RETURN_INSERT + installer.RETURN_ANCHOR)
    assert updated.count(installer.RETURN_INSERT) == 1
    with pytest.raises(RuntimeError):
        installer.proposed_source(updated)


@pytest.mark.parametrize('source', ['def other(): pass\n', installer.RETURN_ANCHOR * 2])
def test_bad_anchor_refused(source):
    with pytest.raises(RuntimeError):
        installer.proposed_source(source)
