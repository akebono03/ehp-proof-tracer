def format_complete_proof_sentences(lines: list[str], model) -> list[str]:
    """Keep the original tree/citations; alter only completed narrative prose."""
    from phase174_r3_r7_r70_verified_narrative_projection.projection import (
        project_verified_general_narrative,
    )
    return split_completed_proof_sentences(
        project_verified_general_narrative(
            combine_adjacent_verified_eta_sentences(lines, model), model,
        )
    )
