from __future__ import annotations

import json
from pathlib import Path

from phase165_r27_r14.audit import collect, source_bucket


def test_backup_is_not_live_production():
    assert source_bucket('repository_operation_query_facade.phase164_backup.py') == 'BACKUP_ROOT_FALSE_POSITIVE'


def test_operation_and_generator_categories():
    assert source_bucket('repository_operation_query_facade.py') == 'OPERATION_CONSUMER_REVIEW'
    assert source_bucket('repository_generator_applicability_facade.py') == 'GENERATOR_CONSUMER_REVIEW'


def test_report_preserves_non_deletion_boundary(tmp_path):
    r = tmp_path / 'phase165_r27_r13'
    r.mkdir()
    (r / 'audit_report.json').write_text(json.dumps({'phase':'165 R27-R13','mode':'READ_ONLY_CLASSIFY_DEPENDENCY_EDGES','entries':[{'path':'repository_operation_query_facade.py','scope':'ROOT_PRODUCTION_OR_UNCLASSIFIED','symbol':'ProofRepository','kind':'import','line':1},{'path':'archive/x.py','scope':'HISTORICAL_OR_PACKAGE_REFERENCE','symbol':'ProofRepository','kind':'import','line':1}]}),encoding='utf-8')
    (tmp_path / 'repository_operation_query_facade.py').write_text('from proof_repository import ProofRepository\n\ndef consumer():\n    return ProofRepository()\n',encoding='utf-8')
    result = collect(tmp_path)
    assert result['candidate_root_files'] == 1
    assert result['upstream_reference_events'] == 1
    assert result['review_rows'][0]['exists']
    assert result['review_rows'][0]['parses']
    assert not result['deletion_authorized']
    assert not result['reachable_from_public_entry_certified']
