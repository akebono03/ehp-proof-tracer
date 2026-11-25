"""Test the exact historical assertion update; keep all unrelated bytes."""
import pytest

from phase176_r3r53r1_historical_kernel_test.apply import TARGET, OLD, NEW, updated_source


def test_historical_test_patch_idempotent_and_fail_closed():
    raw = TARGET.read_bytes()
    assert updated_source(raw) == raw
    source = raw.decode('utf-8').replace('\r\n','\n')
    assert source.count(NEW) == 1 and OLD not in source
    base = source.replace(NEW,OLD,1)
    for eol in ('\n','\r\n'):
        before = base.replace('\n',eol).encode('utf-8')
        after = source.replace('\n',eol).encode('utf-8')
        assert updated_source(before) == after
        assert updated_source(after) == after
    with pytest.raises(ValueError):
        updated_source(raw+b'\n# unknown edit\n')
