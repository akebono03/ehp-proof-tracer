from dataclasses import dataclass
from types import SimpleNamespace
from phase166_r2_correspondence.audit import analyze


@dataclass(frozen=True)
class ExampleStatement:
    content: str


@dataclass(frozen=True)
class Reference:
    reference_id: str
    locator: str


@dataclass(frozen=True)
class Assertion:
    assertion_id: str
    content: object
    origin: object


class Registry:
    def __init__(self, assertions):
        self._references = {'r1': Reference('r1', '(5.3)')}
        self.assertions = assertions

    def assertions_for(self, reference_id):
        return tuple(self.assertions) if reference_id == 'r1' else ()


def test_unmatched_source_cannot_grant_permission():
    bridge = SimpleNamespace(registry=Registry([]))
    details, summary = analyze([{'reference': '(9.9)', 'composition': 'a', 'rep_linear': 'b'}], bridge)
    assert details[0]['correspondence_status'] == 'NO_LOCATOR_MATCH'
    assert details[0]['proof_permission_granted'] is False
    assert summary['mathematical_identity_confirmed'] == 0


def test_typed_candidate_still_not_a_proof():
    assertion = Assertion('a1', ExampleStatement('x'), SimpleNamespace(value='fixed_statement'))
    bridge = SimpleNamespace(registry=Registry([assertion]))
    details, summary = analyze([{'reference': '(5.3), equation', 'composition': 'x', 'rep_linear': 'y'}], bridge)
    assert details[0]['correspondence_status'] == 'TYPED_ASSERTION_CANDIDATE'
    assert details[0]['typed_assertion_ids'] == ['a1']
    assert details[0]['mathematical_identity_confirmed'] is False
    assert summary['proof_permission_granted'] == 0


def test_reference_only_is_not_an_assertion_match():
    bridge = SimpleNamespace(registry=Registry([]))
    details, summary = analyze([{'reference': '(5.3)'}], bridge)
    assert details[0]['correspondence_status'] == 'REFERENCE_ONLY'
    assert summary['assertion_candidate_rows'] == 0


def test_untyped_assertion_not_upgraded():
    assertion = Assertion('a2', 'raw text', SimpleNamespace(value='fixed_statement'))
    bridge = SimpleNamespace(registry=Registry([assertion]))
    details, summary = analyze([{'reference': '(5.3)'}], bridge)
    assert details[0]['correspondence_status'] == 'ASSERTION_NOT_STRUCTURED'
    assert summary['typed_assertion_candidate_rows'] == 0
