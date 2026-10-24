def test_unknown_citation_number_is_rejected():
    result, model = _case()
    wrong = replace(model, citations=(), step_citation_numbers=((2,),))
    with pytest.raises(ValueError, match="missing or unrelated"):
        build_narrative_body_lines(result, wrong)
