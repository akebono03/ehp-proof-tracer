from pathlib import Path

ROOT=Path.cwd()
multi_path=ROOT/"toda_group_proof_narrative_argument_multi_renderer.py"
multi=multi_path.read_text(encoding="utf-8-sig")

# The body renderer already supports context_hidden_step_ids. R18 proved that
# completed premise/support steps are being reintroduced by a later Argument's
# local body. Add the actually completed direct premise/support steps to the
# cross-Argument hidden set for subsequent Arguments.
anchor="""    seen_non_exact_step_ids.update(
      id(
        support_step
      )
      for support_step in direct_derivation_support_steps
    )

    for block in local_body_blocks:
"""
replacement="""    seen_non_exact_step_ids.update(
      id(
        proof_step
      )
      for proof_step in (
        direct_derivation_support_steps
        + direct_derivation_premises
      )
    )

    for block in local_body_blocks:
"""
if anchor not in multi:
    raise RuntimeError("R17 seen-support anchor not found")
multi=multi.replace(anchor,replacement,1)

# Ensure the accumulated cross-Argument seen-step set participates in the
# existing body-renderer hidden-step channel.
context_anchor="""    context_hidden_step_ids = frozenset(
      (
        _toda_group_proof_narrative_argument_context_hidden_step_ids(
          argument,
          blocks,
          local_body_blocks,
        )
      )
      | (
        _toda_group_proof_narrative_argument_frontier_hidden_step_ids(
          argument,
          blocks,
          local_body_blocks,
        )
      )
    )
"""
context_replacement="""    context_hidden_step_ids = frozenset(
      (
        _toda_group_proof_narrative_argument_context_hidden_step_ids(
          argument,
          blocks,
          local_body_blocks,
        )
      )
      | (
        _toda_group_proof_narrative_argument_frontier_hidden_step_ids(
          argument,
          blocks,
          local_body_blocks,
        )
      )
      | seen_non_exact_step_ids
    )
"""
if context_anchor not in multi:
    raise RuntimeError("context hidden-step anchor not found")
multi=multi.replace(context_anchor,context_replacement,1)

multi_path.write_text(multi,encoding="utf-8")
print("Phase 144-6 R19 applied.")
print("Production: toda_group_proof_narrative_argument_multi_renderer.py")
print("Tests: unchanged from R16/R17.")
