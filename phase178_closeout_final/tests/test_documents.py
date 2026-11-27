from __future__ import annotations

from copy import deepcopy

import pytest

from phase178_closeout_final.documents import DOCUMENTS, HEADINGS, MARKER, render_full, sections
from phase178_closeout_final.gate import (MEASUREMENT_GATE, MEASURED_HEAD, EXPECTED_TOTALS,
                                           validate_headline, validate_narrative)


def measurement():
    return dict(gate=MEASUREMENT_GATE, head=MEASURED_HEAD, dry_run=False,
                phase178_formally_closed=False, full_pytest='PASS', full_pytest_exit=0,
                passed=3546, summary='3546 passed in 54.95s', repository_unchanged=True,
                historical_guard='RESOLVED_6_OF_6_PASS',
                stable_boundary_status='DEFERRED_PHASE179_PARTIAL', k6_totals=EXPECTED_TOTALS.copy(),
                focused=dict(passed=189,exit_code=0),stdout_sha256='a'*64,stderr_sha256='b'*64,
                full_pytest_evidence={'xml_sha256':'c'*64},
                k6_groups=[dict(n=n,proven_step_count=s,given_count=g,inference_count=i,model_citation_count=c)
                           for n,s,g,i,c in [(2,3,2,1,2),(3,20,5,15,5),(4,6,4,2,4),
                                             (5,18,6,12,6),(6,18,5,13,5),(7,18,5,13,5)]])


def test_measurement_headline():
    validate_headline(measurement())


@pytest.mark.parametrize('key,value', [('gate','FAIL'),('head','wrong'),('dry_run',True),
    ('full_pytest','NOT_RUN'),('full_pytest_exit',1),('passed',3545),('summary','wrong'),
    ('repository_unchanged',False),('historical_guard','OPEN'),('stable_boundary_status','complete'),
    ('phase178_formally_closed',True),('k6_totals',{}),('focused',dict(passed=188,exit_code=0))])
def test_reject_wrong_measurement(key,value):
    row = measurement()
    row[key] = value
    with pytest.raises(RuntimeError):
        validate_headline(row)


@pytest.mark.parametrize('name', DOCUMENTS)
@pytest.mark.parametrize('eol', ['\n','\r\n'])
def test_render_full_preserves_history(name,eol):
    text = '# Original title\n\n' + (HEADINGS[name][0]+'\n\n' if name in HEADINGS else '')
    text += 'Historical record and formula $x=0$.\n不安定\n' if name!='README.md' else 'Historical record.\n'
    raw = text.replace('\n',eol).encode()
    addition = '<!-- '+MARKER+' -->\n\nNew section.\n'
    result = render_full(name,raw,addition).decode()
    assert result.count(MARKER)==1
    assert 'Historical record' in result
    if name in HEADINGS:
        assert HEADINGS[name][1] in result and HEADINGS[name][0] not in result
        assert result.index(MARKER)<result.index(HEADINGS[name][1])
    else:
        assert result.index(MARKER)>result.index('Historical record')
    if name!='README.md':
        assert '非安定' in result and '不安定' not in result
    if eol=='\r\n':
        assert '\n' not in result.replace('\r\n','')


def test_reject_duplicate_marker():
    with pytest.raises(ValueError):
        render_full('docs/proof_records.md',MARKER.encode(),'<!-- '+MARKER+' -->')


def test_reject_missing_heading():
    with pytest.raises(ValueError):
        render_full('README.md',b'# Old\n','<!-- '+MARKER+' -->')


def test_sections_record_all_narratives():
    narratives = {n:f'**[R1] Source.**\n\nResult {n}.\n\n□\n' for n in range(2,8)}
    additions = sections(measurement(),'d'*64,narratives)
    assert set(additions)==set(DOCUMENTS)
    for name,section in additions.items():
        assert section.count(MARKER)==1
        assert '3546 passed in 54.95s' in section
        assert '497' in section and '313' in section
        assert '189' in section
        assert 'd'*64 in section
    for text in narratives.values():
        assert text.strip() in additions['docs/proof_records.md']
    assert 'Phase 179' in additions['docs/roadmap.md']
    assert '不安定' not in additions['docs/design.md']


def test_narrative_contract():
    validate_narrative(2,'**[R1] A.**\n\n**[R2] B.**\n\n□\n',2)


@pytest.mark.parametrize('text',['**[R1] A.**\n□','**[R2] B.**\n**[R1] A.**\n□',
    '**[R1] A.**\n**[R2] B.**','**[R1] A.**\n**[R2] B.**\n'+MARKER+'\n□'])
def test_bad_narrative_rejected(text):
    with pytest.raises(RuntimeError):
        validate_narrative(2,text,2)
