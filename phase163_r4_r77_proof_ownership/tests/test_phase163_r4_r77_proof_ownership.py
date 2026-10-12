import hashlib
import json
from pathlib import Path

import pytest

from phase163_r4_r77_proof_ownership import audit, describe_owner, write_reports


TEX = r'''\begin{proposition}\label{prop:1-5}
Some theorem.
\end{proposition}
\noindent (要するに)
\[ A=B \]
\begin{proposition}\label{prop:1-6}
Some other theorem.
\end{proposition}
Proof.\
We will show the following.
\[C=D\]
\qed
\begin{lemma}\label{lem:1-7}
Statement
\end{lemma}
'''


def row(index, line):
    return {'r48_index': index, 'source_line': line}


def test_post_proposition_paraphrase():
    result = describe_owner(row(66, 5), TEX)
    assert result['structural_attachment'] == 'EXPLICIT_POST_STATEMENT_PARAPHRASE'
    assert result['source_owner_label'] == 'prop:1-5'
    assert result['post_statement_summary_line'] == 4


def test_proof_segment_attachment():
    result = describe_owner(row(67, 11), TEX)
    assert result['structural_attachment'] == 'WITHIN_EXPLICIT_PROOF_SEGMENT'
    assert result['proof_start_line'] == 9
    assert result['source_owner_label'] == 'prop:1-6'


def test_finished_proof_no_registration():
    result = describe_owner(row(99, 13), TEX.replace('\\qed\n\\begin{lemma}', '\\qed\nPost proof.\n\\begin{lemma}'))
    assert result['structural_attachment'] == 'AFTER_PROOF_END_NEEDS_REVIEW'


def test_no_preceding_statement():
    assert describe_owner(row(1, 1), TEX)['structural_attachment'] == 'NO_PRECEDING_NUMBERED_STATEMENT'


def test_rejects_invalid_line():
    with pytest.raises(ValueError):
        describe_owner(row(1, 10000), TEX)


def test_audit_checks_hash_and_preserves_candidates(tmp_path):
    source = tmp_path / 'text.tex'
    source.write_text(TEX, encoding='utf-8')
    digest = hashlib.sha256(source.read_bytes()).hexdigest()
    records = [dict(r48_index=66 if index == 0 else index + 100,
                    chapter=1, source_file='text.tex', source_line=5 if index == 0 else 11,
                    proposed_ownership='UNNUMBERED_ASSERTION_CASE', owner_relation='UNRESOLVED')
               for index in range(11)]
    data = {'phase': '163 R4-R76', 'records': records, 'source_sha256': {'text.tex': digest}}
    result = audit(data, tmp_path)
    assert result['candidate_count'] == 11
    assert result['structural_attachment_counts']['WITHIN_EXPLICIT_PROOF_SEGMENT'] == 10
    assert result['production_registry_modified'] is False
    write_reports(result, tmp_path / 'out')
    assert len(json.loads((tmp_path / 'out/proof_ownership.json').read_text(encoding='utf-8'))['records']) == 11
    assert (tmp_path / 'out/proof_ownership.csv').exists()
    assert (tmp_path / 'out/report.md').exists()


def test_rejects_wrong_input_phase(tmp_path):
    with pytest.raises(ValueError):
        audit({'phase': '163 R4-R75'}, tmp_path)


def test_rejects_repeated_index(tmp_path):
    with pytest.raises(ValueError):
        audit({'phase': '163 R4-R76', 'records': [{'r48_index': 3}] * 11}, tmp_path)


def test_rejects_changed_source_hash(tmp_path):
    (tmp_path / 'text.tex').write_text(TEX, encoding='utf-8')
    rows = [dict(r48_index=i, source_file='text.tex', source_line=5,
                 chapter=1, proposed_ownership='X', owner_relation='X') for i in range(11)]
    with pytest.raises(ValueError, match='Source hash mismatch'):
        audit({'phase': '163 R4-R76', 'records': rows, 'source_sha256': {'text.tex': 'wrong'}}, tmp_path)
