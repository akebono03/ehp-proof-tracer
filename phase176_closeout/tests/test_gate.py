"""Gate helper contracts; never execute a real full suite in these tests."""
import pytest

from phase176_closeout import gate
from phase176_closeout.documents import DOCUMENT_BLOBS, HISTORICAL_HEADINGS, MARKER, render_full, sections


def evidence():
    return {'full_pytest_exit':0,'passed':3546,'summary':'3546 passed in 40.00s',
            'head':gate.HEAD,'stdout_sha256':'0'*64,'stderr_sha256':'1'*64}


def test_active_scope_and_summary():
    assert gate.ACTIVE_COMMAND == ('-B','-m','pytest','-q','--tb=short','--disable-warnings','-p','no:cacheprovider','tests')
    assert gate.parse_summary('3546 passed in 40.00s\n',0) == (3546,'3546 passed in 40.00s')


@pytest.mark.parametrize('output,code', [
    ('3546 passed, 1 failed in 40.00s',1), ('3546 passed, 1 skipped in 40.00s',0),
    ('3546 passed, 1 deselected in 40.00s',0), ('3545 passed in 40.00s',0),
    ('3546 passed in 40.00s\n3546 passed in 41.00s',0), ('collection error',0),
])
def test_invalid_summary(output,code):
    with pytest.raises(RuntimeError):
        gate.parse_summary(output,code)


def test_full_documents_preserve_history_and_current_heading():
    additions = sections(evidence())
    assert set(additions) == set(DOCUMENT_BLOBS)
    for name, section in additions.items():
        for eol in (b'\n',b'\r\n'):
            heading = HISTORICAL_HEADINGS.get(name, ('## Historical','## Historical'))[0].encode()
            raw = b'# Title'+eol+eol+heading+eol+b'Old record'+eol
            updated = render_full(name,raw,section)
            assert updated.count(MARKER.encode()) == 1
            if name in HISTORICAL_HEADINGS:
                old,new = (s.encode() for s in HISTORICAL_HEADINGS[name])
                assert old not in updated and new in updated and b'Old record'+eol in updated
                assert updated.endswith(raw[raw.index(b'\n')+1:].replace(old,new,1))
            else:
                assert updated.startswith(raw)
            with pytest.raises(ValueError):
                render_full(name,updated,section)
    assert 'formally closed' in additions['README.md']
    assert all('正式終了' in text or '終了監査' in text or '完成証明' in text for name,text in additions.items() if name != 'README.md')


def test_unverified_evidence_refuses_documents():
    report = evidence(); report['full_pytest_exit'] = 1
    with pytest.raises(ValueError):
        sections(report)


def test_dryrun_and_attempt_guard(monkeypatch,tmp_path):
    monkeypatch.setattr(gate,'evidence_dir',lambda:tmp_path)
    monkeypatch.setattr(gate,'preflight',lambda:{'head':gate.HEAD})
    def refuse(*args,**kwargs):
        raise AssertionError('MUST_NOT_START_PROCESS')
    monkeypatch.setattr(gate.subprocess,'run',refuse)
    assert gate.run(True) == 0
    assert not (tmp_path/'attempt.json').exists()
    (tmp_path/'attempt.json').write_text('{}',encoding='utf-8')
    assert gate.run(False) == 1
