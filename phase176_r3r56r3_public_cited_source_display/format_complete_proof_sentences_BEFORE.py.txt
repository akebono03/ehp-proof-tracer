def format_complete_proof_sentences(lines: list[str], model) -> list[str]:
    """Keep the original tree/citations; alter only completed narrative prose."""
    from phase174_r3_r7_r70_verified_narrative_projection.projection import (
        project_verified_general_narrative,
    )
    from phase175_r3r11_cited_hopf_narrative.projection import (
        project_verified_source_and_hopf_summary,
    )
    combined = project_verified_general_narrative(
        combine_adjacent_verified_eta_sentences(lines, model), model,
    )
    cited = project_verified_source_and_hopf_summary(combined, model)
    return split_completed_proof_sentences(cited)
