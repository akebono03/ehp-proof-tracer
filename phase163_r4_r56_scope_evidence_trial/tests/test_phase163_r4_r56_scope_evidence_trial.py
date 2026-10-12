import copy
import json
from pathlib import Path

import pytest

from phase163_r4_r56_scope_evidence_trial import build_scope_report, write_report

ROOT = Path.cwd()


def inputs():
    catalog = json.loads((ROOT/'phase163_r4_r47_output'/'catalog.json').read_text(encoding='utf-8'))
    trial = json.loads((ROOT/'phase163_r4_r55_output'/'trial.json').read_text(encoding='utf-8'))
    return catalog, trial


def test_three_source_grounded_scope_records():
    report = build_scope_report(*inputs())
    assert report['scope_record_count'] == 3
    assert {x['locator'] for x in report['scope_items']} == {'(2.9)', '(2.10)', '(4.3)'}


def test_domain_codomain_are_explicit():
    report = build_scope_report(*inputs())
    assert report['domain_codomain_record_count'] == 2
    assert all(x['domain_tex'] and x['codomain_tex'] for x in report['scope_items'][:2])


def test_three_cases_preserved_without_global_range_inference():
    report = build_scope_report(*inputs())
    item = report['scope_items'][2]
    assert item['domain_tex'] is None and item['codomain_tex'] is None
    assert len(item['cases']) == 3
    assert report['conditions_inferred_count'] == 0


def test_variables_do_not_claim_implicit_quantification():
    report = build_scope_report(*inputs())
    assert [x['variables'] for x in report['scope_items']] == [['m','i'],['m','i'],['i','n']]
    assert report['formal_mathematical_ast_count'] == 0


def test_unrelated_context_does_not_become_map_condition():
    report = build_scope_report(*inputs())
    assert report['scope_items'][0]['condition_status'] == 'NONE_EXPLICIT_IN_DEFINITION_EQUATION'
    assert 'denominator' in report['scope_items'][0]['context_boundary_note']


def test_rejects_source_checksum_tampering():
    catalog, trial = inputs()
    catalog = copy.deepcopy(catalog)
    next(x for x in catalog['items'] if x['locator']=='(2.9)')['tex_body'] += 'NOT_IN_SOURCE'
    with pytest.raises(ValueError, match='checksum'):
        build_scope_report(catalog,trial)


def test_rejects_trial_source_mismatch():
    catalog, trial = inputs()
    trial = copy.deepcopy(trial)
    next(x for x in trial['trial_items'] if x['locator']=='(2.10)')['source_unit_id'] = 'wrong'
    with pytest.raises(ValueError,match='mismatch'):
        build_scope_report(catalog,trial)


def test_retains_read_only_and_unreviewed_boundaries():
    report = build_scope_report(*inputs())
    assert report['untouched_candidate_count'] == 16
    assert report['pending_other_candidates_count'] == 237
    assert report['production_registry_modified'] is False
    assert report['production_ids_allocated'] is False


def test_writes_expected_artifacts(tmp_path):
    report = build_scope_report(*inputs())
    write_report(report,tmp_path)
    assert {p.name for p in tmp_path.iterdir()} == {'scope.json','scope.csv','report.md'}
