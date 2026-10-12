import csv
import json
from pathlib import Path

import pytest

from phase163_r4_r76_tex_boundary_link import audit, locate_candidate, scan_tex, write_reports


@pytest.fixture
def sample(tmp_path):
    tex = r'''\begin{proposition}\label{prop:1.1}
Statement.
\end{proposition}
\noindent\textbf{Proof.}
text
\[
a=b
\]
\qed
\begin{lemma}\label{lem:1.2}
result
\end{lemma}
'''
    source = tmp_path / 'Toda_01_corrected.tex'
    source.write_text(tex, encoding='utf-8')
    base = {'chapter': 1, 'source_file': source.name, 'source_line': 6,
            'proposed_ownership': 'PROOF_COSET_EXPRESSION',
            'provisional_group': 'sample', 'excerpt_sha256': 'dummy'}
    data = {'focused_proposals': [dict(base, r48_index=i) for i in range(1, 12)]}
    return tex, tmp_path, data


def test_scan_theorem_and_labels(sample):
    tex, _, _ = sample
    events = scan_tex(tex)
    assert len(events) == 2
    assert events[0]['labels'] == ['prop:1.1']
    assert events[0]['end_line'] == 3


def test_proof_relation(sample):
    tex, _, data = sample
    row = locate_candidate(data['focused_proposals'][0], tex)
    assert row['owner_relation'] == 'POSSIBLE_PROOF_OF_PRECEDING'
    assert row['nearest_numbered_owner'] == 'prop:1.1'


def test_inside_statement(sample):
    tex, _, data = sample
    row = locate_candidate(dict(data['focused_proposals'][0], source_line=2), tex)
    assert row['owner_relation'] == 'INSIDE_NUMBERED_BODY'


def test_after_qed_not_assigned(sample):
    tex, _, data = sample
    row = locate_candidate(dict(data['focused_proposals'][0], source_line=9), tex)
    assert row['owner_relation'] == 'AFTER_QED_UNOWNED'


def test_out_of_range(sample):
    tex, _, data = sample
    row = locate_candidate(dict(data['focused_proposals'][0], source_line=999), tex)
    assert row['position_status'] == 'LINE_OUT_OF_RANGE'


def test_audit_count_and_no_registration(sample):
    _, folder, data = sample
    result = audit(data, folder)
    assert result['candidate_count'] == 11
    assert result['line_located_count'] == 11
    assert result['production_registry_modified'] is False
    assert result['formal_source_boundary_verified_count'] == 0


def test_missing_source_is_not_fabricated(sample):
    _, folder, data = sample
    data['focused_proposals'][0]['source_file'] = 'missing.tex'
    result = audit(data, folder)
    assert result['line_located_count'] == 10
    assert result['records'][0]['position_status'] == 'SOURCE_MISSING'


def test_duplicate_index_rejected(sample):
    _, folder, data = sample
    data['focused_proposals'][1]['r48_index'] = 1
    with pytest.raises(ValueError):
        audit(data, folder)


def test_reports_parse_csv(sample):
    _, folder, data = sample
    result = audit(data, folder)
    out = folder / 'output'
    write_reports(result, out)
    with (out / 'numbered_boundary_crosswalk.csv').open(encoding='utf-8-sig', newline='') as f:
        assert len(list(csv.DictReader(f))) == 11
    assert len(json.loads((out / 'numbered_boundary_crosswalk.json').read_text(encoding='utf-8'))['records']) == 11
