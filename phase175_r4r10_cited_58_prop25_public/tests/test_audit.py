"""Prior-report and source-first audit boundary checks."""
from __future__ import annotations

from copy import deepcopy
from pathlib import Path

import pytest

from phase175_r4r10_cited_58_prop25_public import audit, source


def passed_report() -> dict[str, object]:
    return {
        'phase': '175-R4R8', 'gate': audit.PRIOR_GATE, 'dry_run': False,
        'new_given': 0, 'new_mathematical_rules': 0,
        'production_changes': [], 'rule_connected_to_public': False,
        'pi95_proof_complete': False, 'full_pytest_executed': False,
        'prior_proof_search_executed': False,
        'groups': {
            'prior_presentations_identified': 2,
            'group_presentations_do_not_certify_E_actions': True,
        },
        'unresolved_obligations': [{'index': k} for k in range(1, 7)],
    }


def test_prior_report_is_audit_not_proof() -> None:
    result = audit.validate_prior(passed_report())
    assert result['prior_unresolved_obligations'] == 6
    assert result['prior_math_proofs_not_adopted'] is True


@pytest.mark.parametrize('key,value', (
    ('phase', '175-R4R7'), ('gate', audit.DRY_GATE), ('dry_run', True),
    ('new_given', 1), ('new_mathematical_rules', 1),
    ('production_changes', ['proof.py']), ('rule_connected_to_public', True),
    ('pi95_proof_complete', True), ('full_pytest_executed', True),
    ('prior_proof_search_executed', True),
))
def test_bad_prior_report_rejected(key: str, value: object) -> None:
    bad = passed_report()
    bad[key] = value
    with pytest.raises(RuntimeError, match='REPORT_SCOPE_INVALID'):
        audit.validate_prior(bad)


@pytest.mark.parametrize('change', ('groups', 'obligations', 'missing_groups'))
def test_missing_prior_math_boundary_rejected(change: str) -> None:
    data = passed_report()
    if change == 'groups':
        data['groups']['group_presentations_do_not_certify_E_actions'] = False
    elif change == 'obligations':
        data['unresolved_obligations'] = []
    else:
        data.pop('groups')
    with pytest.raises(RuntimeError, match='REPORT_EVIDENCE_INVALID'):
        audit.validate_prior(data)


def test_sample_is_only_a_typed_goal() -> None:
    from toda_rules import TodaDeltaImageUpToSignStatement
    from phase175_r4r7_prop25_typed_composition.rule import typed_endpoints
    goal = audit.sample_delta_eta9()
    assert isinstance(goal, TodaDeltaImageUpToSignStatement)
    assert typed_endpoints(goal.element) == (10, 9)
    assert typed_endpoints(goal.positive_value) == (8, 4)


def test_source_integrity_rejects_unknown_file(tmp_path: Path) -> None:
    candidate = tmp_path / 'Toda.tex'
    candidate.write_text('fabricated source\n', encoding='utf-8')
    with pytest.raises(ValueError, match='SOURCE_BLOB_DRIFT'):
        source.vetted_source(candidate, source.CHAPTER_5_BLOB)


def test_source_identity_has_no_direct_group_claim() -> None:
    eq = source.CitedToda58SignedDelta(source.canonical_toda58())
    prop = source.CitedTodaProp25()
    assert eq.locator == '(5.8)'
    assert prop.locator == 'Proposition 2.5'
    assert eq.statement.element.dimension == 9


def test_source_bound_chain_replays_without_group_conclusion(
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    """Independent source GIVEN parents must produce a signed INFERENCE chain."""
    monkeypatch.setattr(source, 'source_positions', lambda root=source.ROOT,
                        manifest=source.DEFAULT_MANIFEST: {
                            source.EQUATION_REFERENCE_ID: 8500,
                            source.PROPOSITION_REFERENCE_ID: 2500,
                        })
    result = audit.replay_cited_prop25()
    assert result['conclusion_is_signed'] is True
    assert result['equation_5_8_citation_present'] is True
    assert result['proposition_2_5_citation_present'] is True
    assert result['eta_family_citation_present'] is True
    assert result['root_group_conclusion_inferred'] is False
    assert result['full_search_performed'] is False
