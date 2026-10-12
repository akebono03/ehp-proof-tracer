import copy
import json
from pathlib import Path

import pytest

from phase163_r4_r55_structured_definition_trial import (SAMPLES, SourceGroundedDefinition,
                                                         build_trial, write_report)
from unified_statement_registry import AssertionKind, AssertionOrigin, ReferenceKind


ROOT = Path.cwd()


def inputs():
    # Source files live in the user's Windows project, not in the test package.
    catalog = json.loads((ROOT / 'phase163_r4_r47_output' / 'catalog.json').read_text(encoding='utf-8'))
    overlap = json.loads((ROOT / 'phase163_r4_r53_output' / 'overlap_audit.json').read_text(encoding='utf-8'))
    return catalog, overlap


def test_three_scoped_samples():
    report, _ = build_trial(*inputs())
    assert report['trial_definition_count'] == 3
    assert {r['locator'] for r in report['trial_items']} == set(SAMPLES)


def test_typed_definition_and_source_kind():
    report, registry = build_trial(*inputs())
    for row in report['trial_items']:
        assertion = registry.assertion(row['trial_assertion_id'])
        assert assertion.kind is AssertionKind.DEFINITION
        assert assertion.origin is AssertionOrigin.FIXED_STATEMENT
        assert registry.reference(row['trial_reference_id']).kind is ReferenceKind.EQUATION
        assert isinstance(assertion.content, SourceGroundedDefinition)


def test_trial_not_mathematical_ast():
    report, registry = build_trial(*inputs())
    assert report['formal_mathematical_ast_count'] == 0
    assert all(registry.assertion(r['trial_assertion_id']).content.scope_text for r in report['trial_items'])


def test_preserves_remaining_candidates_and_boundaries():
    report, _ = build_trial(*inputs())
    assert report['untouched_candidate_count'] == 16
    assert report['pending_other_candidates_count'] == 237
    assert report['production_registry_modified'] is False
    assert report['production_ids_allocated'] is False


def test_rejects_mismatched_source_unit():
    catalog, overlap = inputs()
    overlap = copy.deepcopy(overlap)
    next(x for x in overlap['candidates'] if x['editorial_key'] == 'delta_homomorphism')['matched_source_unit_id'] = 'wrong'
    with pytest.raises(ValueError, match='mismatch'):
        build_trial(catalog, overlap)


def test_rejects_mutated_formula_checksum():
    catalog, overlap = inputs()
    catalog = copy.deepcopy(catalog)
    next(x for x in catalog['items'] if x['locator'] == '(2.9)')['tex_body'] += 'BAD'
    with pytest.raises(ValueError, match='checksum'):
        build_trial(catalog, overlap)


def test_rejects_mutating_input():
    catalog, overlap = inputs()
    overlap = copy.deepcopy(overlap)
    overlap['registration_applied'] = True
    with pytest.raises(ValueError, match='mutation'):
        build_trial(catalog, overlap)


def test_ids_disjoint_from_existing():
    catalog, overlap = inputs()
    report, _ = build_trial(catalog, overlap)
    old = set(catalog['existing_assertion_ids']) | set(catalog['existing_reference_ids'])
    assert all(r['trial_reference_id'] not in old and r['trial_assertion_id'] not in old for r in report['trial_items'])


def test_writes_three_outputs(tmp_path):
    report, _ = build_trial(*inputs())
    write_report(report, tmp_path)
    assert {p.name for p in tmp_path.iterdir()} == {'trial.json', 'trial.csv', 'report.md'}
