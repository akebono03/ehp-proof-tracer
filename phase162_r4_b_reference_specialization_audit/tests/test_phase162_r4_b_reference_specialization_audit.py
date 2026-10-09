from phase162_r4_b_reference_specialization_audit.audit_phase162_r4_b_reference_specialization import audit_group, walk_steps
from tests.test_phase143_19_method_evidence import _method_evidence_data


def test_phase162_r4_b_audit_two_stable_targets_read_only():
    for n in (4, 5):
        presentation, _, _, _ = _method_evidence_data(n, 1)
        before = tuple((id(s), tuple(id(p) for p in s.premises)) for s, _ in walk_steps(presentation.root_step))
        result = audit_group(n)
        after = tuple((id(s), tuple(id(p) for p in s.premises)) for s, _ in walk_steps(presentation.root_step))
        assert before == after
        assert result['tree_step_count'] > 0
        assert result['target'] == f'pi_{n+1}^{n}'
        assert isinstance(result['presentation_references_before_filtering'], list)
        assert isinstance(result['canonical_toda45_comparison_only']['premises'], list)


def test_phase162_r4_b_reference_origin_not_conflated():
    result = audit_group(4)
    for record in result['steps']:
        if record['reference_origin'] == 'explicit':
            assert record['explicit_reference'] is not None
        if record['reference_origin'] == 'absent':
            assert record['selected_reference'] is None
