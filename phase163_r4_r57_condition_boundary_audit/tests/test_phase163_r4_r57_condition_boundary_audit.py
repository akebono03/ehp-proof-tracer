import copy
import json
from pathlib import Path

import pytest

from phase163_r4_r57_condition_boundary_audit import build_boundary_report, write_report

ROOT=Path.cwd()


def inputs():
    scope=json.loads((ROOT/'phase163_r4_r56_output'/'scope.json').read_text(encoding='utf-8'))
    source_dir=ROOT/'phase163_r4_r42_tex_extract'/'inputs'
    files={name:(source_dir/name).read_text(encoding='utf-8') for name in ('Toda_02_2(2).tex','Toda_04_2(2).tex')}
    return scope,files


def test_three_definition_boundaries():
    result=build_boundary_report(*inputs())
    assert result['definition_count']==3
    assert {e['locator'] for e in result['items']}=={'(2.9)','(2.10)','(4.3)'}


def test_three_cases_remain_explicit_only():
    result=build_boundary_report(*inputs())
    assert result['explicit_case_count']==3
    assert len(result['items'][2]['explicit_cases'])==3


def test_contextual_source_lines_are_grounded():
    result=build_boundary_report(*inputs())
    assert result['contextual_evidence_count']==3
    assert all(e['contextual_evidence'][0]['source_line']>0 for e in result['items'])


def test_no_context_as_global_precondition():
    result=build_boundary_report(*inputs())
    assert result['global_preconditions_verified_count']==0
    assert all(e['global_preconditions_verified'] is False for e in result['items'])


def test_unverified_inverse_and_quantification():
    result=build_boundary_report(*inputs())
    assert result['unverified_assumption_count']==9
    assert any('逆写像' in s for s in result['items'][1]['unverified_assumptions'])


def test_rejects_missing_context_evidence():
    scope,sources=inputs()
    sources['Toda_02_2(2).tex']=sources['Toda_02_2(2).tex'].replace('の kernel','の UNKNOWN')
    with pytest.raises(ValueError,match='missing source evidence'):
        build_boundary_report(scope,sources)


def test_rejects_mismatched_source_line():
    scope,sources=inputs()
    scope=copy.deepcopy(scope)
    scope['scope_items'][0]['equation_source_line']=100
    with pytest.raises(ValueError,match='equation line mismatch'):
        build_boundary_report(scope,sources)


def test_retains_read_only_boundaries():
    result=build_boundary_report(*inputs())
    assert result['untouched_definition_candidate_count']==16
    assert result['pending_other_candidates_count']==237
    assert result['production_registry_modified'] is False
    assert result['production_ids_allocated'] is False


def test_writes_three_report_files(tmp_path):
    result=build_boundary_report(*inputs())
    write_report(result,tmp_path)
    assert {x.name for x in tmp_path.iterdir()}=={'boundary.json','boundary.csv','report.md'}
