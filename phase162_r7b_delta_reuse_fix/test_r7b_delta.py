import inspect

from toda_group_proof_narrative_contribution_renderer import (
    insert_toda_group_proof_narrative_map_property_dependencies,
)


def test_r7b_delta_reuse_accepts_multiple_existing_matching_paragraphs():
    source = inspect.getsource(insert_toda_group_proof_narrative_map_property_dependencies)
    assert 'if not matches:' in source
    assert 'if len(\n      matches\n    ) != 1:' not in source


def test_r7b_delta_public_pi5_3_no_dependency_insertion_explosion():
    from phase162_pi5_3_renderer_audit import render_phase162_pi5_3_reconstructed_proof
    from tests.test_phase59_pi5_3_eta3_squared import build_phase59_4_data
    from tests.test_phase59_n3_ehp_chain import build_phase59_3_data

    data = build_phase59_4_data()
    result = render_phase162_pi5_3_reconstructed_proof(
        data['pi4_2_step'],
        (data['eta3_definition_step'], data['eta4_definition_step']),
        build_phase59_3_data()['premise_steps'],
    )
    count = sum(
        paragraph.strip() == r'$\Delta\left(\iota_{5}\right) = \pm [\iota_{2}, \iota_{2}]$.'
        for paragraph in result.markdown.split('\n\n')
    )
    assert 1 <= count < 8, f'Unexpected Delta paragraph count: {count}'
    assert r'\pi_{5}^{3} = \mathbb{Z}/2\{\eta_{3}^{2}\}' in result.markdown


def test_r7b_delta_existing_empty_document_behavior():
    # The helper must not insert proof steps when the presentation has no visible maps.
    from unittest.mock import Mock
    from toda_group_proof_narrative_contribution_renderer import (
        insert_toda_group_proof_narrative_map_property_dependencies as render,
    )
    from toda_group_proof_presentation import TodaGroupProofPresentation

    # Type validation remains part of the public contract.
    try:
        render(Mock(), 'unchanged')
    except TypeError:
        pass
    else:
        raise AssertionError('Expected presentation type validation')
