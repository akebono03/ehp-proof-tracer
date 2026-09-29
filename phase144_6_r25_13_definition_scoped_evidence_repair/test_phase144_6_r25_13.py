from pathlib import Path


def test_phase144_6_r25_13_method_evidence_expansion_is_definition_scoped():
    source = Path(
        "toda_group_proof_narrative_argument_multi_renderer.py"
    ).read_text(
        encoding="utf-8"
    )

    marker = """    if (
      argument.role
      is TodaGroupProofNarrativeArgumentRole
      .ESTABLISH_DEFINITION
    ):
      local_body_block_ids = {
"""
    assert source.count(marker) == 1

    unconditional_marker = """    local_body_block_ids = {
      id(
        block
      )
      for block in local_body_blocks
    }
    evidence_block_ids = {
"""
    assert unconditional_marker not in source
