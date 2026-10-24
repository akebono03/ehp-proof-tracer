def test_pi32_three_windows_project_one_chain():
    result, model = _case(2, 1)
    chains = project_exactness_chains(model)
    assert len(chains) == 1
    assert len(chains[0].arrows) == 4
    assert len(chains[0].step_indices) == 3
    rendered = render_model_backed_narrative_markdown(result, model)
    assert rendered.count("次の完全列を考える") == 1
    # The Reference may contain the same general EHP arrow.
    # Count the concrete displayed arrow only in the proof section.
    reference, proof = rendered.split("\n証明\n", 1)
    assert proof.count(r"\xrightarrow{\Delta}") == 1
