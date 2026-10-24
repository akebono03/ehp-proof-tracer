def test_eta_suspension_cites_only_proved_eta_definition_ancestor(cases, name, source, target):
    result, model, markdown = cases[name]
    cited = _reference_number(model, 'Chapter V, i)')
    eta_witnesses = [step for step in model.steps
                     if isinstance(step.conclusion, GeneratorSuspension)
                     and _eta_pair(step.conclusion) is not None]
    assert eta_witnesses
    assert any(_has_typed_source_ancestor(step, TodaEtaFamilyGeneralDefinition)
               for step in eta_witnesses)
    expected = f'[R{cited}]より, $E(\\eta_{{{source}}})=\\eta_{{{target}}}$.'
    assert expected in markdown

