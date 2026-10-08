from toda_literature_statement_boundary import (
    get_toda_fixed_statement_component,
    get_toda_fixed_statement_components,
)


def test_phase161_equation52_reference_range_is_general_form():
    component = get_toda_fixed_statement_component(
        '(5.2)', 'eta2_composition_isomorphism'
    )
    assert component.range_text == 'i >= 3'
    assert component.range_is_explicit_in_current_aggregate is True


def test_phase161_proposition51_higher_eta_reference_range_is_general_form():
    component = get_toda_fixed_statement_component(
        'Proposition 5.1', 'higher_eta_group_relation'
    )
    assert component.range_text == 'n >= 3'
    assert component.range_is_explicit_in_current_aggregate is False
    assert tuple(c.range_text for c in get_toda_fixed_statement_components('Proposition 5.1')) == (
        None, None, None, 'n >= 3'
    )
