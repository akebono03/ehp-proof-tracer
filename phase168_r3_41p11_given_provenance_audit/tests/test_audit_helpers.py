"""Tests of audit-only matching and reporting; no app runtime required."""
from dataclasses import dataclass
from types import SimpleNamespace

from phase168_r3_41p11_given_provenance_audit.audit import (
    markdown_report,
    matching_step_links,
    same_content,
)


def test_same_content_normalizes_windows_line_endings():
    assert same_content('a\r\nb\r', 'a\nb\n')
    assert not same_content('a', 'b')


def test_step_link_same_identity_or_value():
    @dataclass(frozen=True)
    class FakeStep:
        conclusion: str
    step = FakeStep('x')
    a = SimpleNamespace(step=step)
    b = SimpleNamespace(step=FakeStep('x'))
    c = SimpleNamespace(step=FakeStep('y'))
    d = SimpleNamespace(step=None)
    bridge = SimpleNamespace(proof_links=(a, b, c, d))
    assert matching_step_links(bridge, step) == (a, b)


def test_markdown_report_distinguishes_source_and_proof():
    report = {'status': 'PASS', 'cases': {'pi3_2': {
        'given_audit': {'given_count': 5, 'linked_count': 4, 'fixed_cited_count': 4},
        'fulltext_equal': True,
    }}, 'counterfeit': {'model_accepts_fake_given': True, 'screened_source_gate_rejects': True}}
    text = markdown_report(report)
    assert 'FIXEDかつCitation対応' in text
    assert '文献順' in text
    assert 'FULL_PYTEST_NOT_RUN' in text


def test_error_visible_in_report():
    text = markdown_report({'status': 'ERROR', 'error': 'probe failed'})
    assert 'probe failed' in text
    assert 'AUDIT_STATUS**: ERROR' in text


def test_provenance_requires_fixed_matching_link_and_model_citation(monkeypatch):
    import sys
    from enum import Enum
    from types import ModuleType

    from phase168_r3_41p11_given_provenance_audit.audit import audit_given_provenance

    class ProofRule(Enum):
        GIVEN = 1
        INFERENCE = 2

    class Origin(Enum):
        FIXED_STATEMENT = 'fixed_statement'
        SOURCE_ARCHIVE = 'source_archive'

    proof = ModuleType('proof')
    proof.ProofRule = ProofRule
    registry_module = ModuleType('unified_statement_registry')
    registry_module.AssertionOrigin = Origin
    monkeypatch.setitem(sys.modules, 'proof', proof)
    monkeypatch.setitem(sys.modules, 'unified_statement_registry', registry_module)

    source = SimpleNamespace(conclusion='known', rule=ProofRule.GIVEN)
    assertion = SimpleNamespace(
        assertion_id='a', reference_id='r', origin=Origin.FIXED_STATEMENT,
        content='known', component_position=100,
    )
    ref = SimpleNamespace(locator='(5.1)', publication_position=7700)
    registry = SimpleNamespace(assertion=lambda _: assertion, reference=lambda _: ref)
    bridge = SimpleNamespace(registry=registry, proof_links=(SimpleNamespace(assertion_id='a', step=source),))
    cite = SimpleNamespace(number=1, reference_ids=('r',), step_indices=(0,))
    model = SimpleNamespace(steps=(source,), citations=(cite,), step_citation_numbers=((1,),))
    accepted = audit_given_provenance(model, bridge)
    assert accepted['given_count'] == 1
    assert accepted['fixed_cited_count'] == 1
    assert accepted['publication_order_reverified'] is False

    fake = SimpleNamespace(conclusion='false', rule=ProofRule.GIVEN)
    forged_model = SimpleNamespace(steps=(fake,), citations=(), step_citation_numbers=((),))
    rejected = audit_given_provenance(forged_model, bridge)
    assert rejected['given_count'] == 1
    assert rejected['fixed_cited_count'] == 0
    assert rejected['missing_link_indices'] == [0]


def test_source_archive_is_not_fixed_evidence(monkeypatch):
    import sys
    from enum import Enum
    from types import ModuleType
    from phase168_r3_41p11_given_provenance_audit.audit import audit_given_provenance

    class ProofRule(Enum):
        GIVEN = 1

    class Origin(Enum):
        FIXED_STATEMENT = 'fixed_statement'
        SOURCE_ARCHIVE = 'source_archive'

    proof = ModuleType('proof')
    proof.ProofRule = ProofRule
    module = ModuleType('unified_statement_registry')
    module.AssertionOrigin = Origin
    monkeypatch.setitem(sys.modules, 'proof', proof)
    monkeypatch.setitem(sys.modules, 'unified_statement_registry', module)

    given = SimpleNamespace(conclusion='claim', rule=ProofRule.GIVEN)
    assertion = SimpleNamespace(assertion_id='archive', reference_id='ref',
                                origin=Origin.SOURCE_ARCHIVE, content='claim', component_position=None)
    ref = SimpleNamespace(locator='(5.1)', publication_position=7700)
    bridge = SimpleNamespace(proof_links=(SimpleNamespace(assertion_id='archive', step=given),),
                             registry=SimpleNamespace(assertion=lambda _: assertion, reference=lambda _: ref))
    model = SimpleNamespace(steps=(given,), citations=(SimpleNamespace(number=1,reference_ids=('ref',),step_indices=(0,)),),
                            step_citation_numbers=((1,),))
    outcome = audit_given_provenance(model, bridge)
    assert outcome['linked_count'] == 1
    assert outcome['fixed_cited_count'] == 0
