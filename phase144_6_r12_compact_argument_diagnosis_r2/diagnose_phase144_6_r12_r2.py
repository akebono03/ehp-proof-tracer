from tests.test_phase143_19_method_evidence import (
  _method_evidence_data,
)
from toda_group_proof_narrative_arguments import (
  extract_toda_group_proof_narrative_argument_conclusion_step,
  extract_toda_group_proof_narrative_argument_purpose_subject,
)
from toda_group_proof_narrative_argument_local_body import (
  extract_toda_group_proof_narrative_argument_local_body_blocks,
)
from toda_group_proof_narrative_argument_direct_premises import (
  extract_toda_group_proof_narrative_argument_conclusion_direct_derivation_premises,
)
from toda_group_proof_narrative_argument_multi_renderer import (
  _toda_group_proof_narrative_argument_frontier_hidden_step_ids,
)
from toda_group_proof_generic_narrative_renderer import (
  _render_generic_narrative_step,
)


def show(n, k):
  presentation, blocks, sidecar, arguments = _method_evidence_data(
    n,
    k,
  )
  print("=" * 78)
  print(
    f"target n={n} k={k}: "
    f"blocks={len(blocks)} arguments={len(arguments)}"
  )

  for argument_index, argument in enumerate(arguments):
    subject = extract_toda_group_proof_narrative_argument_purpose_subject(
      argument
    )
    conclusion = extract_toda_group_proof_narrative_argument_conclusion_step(
      argument
    )
    local_blocks = extract_toda_group_proof_narrative_argument_local_body_blocks(
      presentation,
      blocks,
      sidecar,
      arguments,
      argument_index,
    )
    hidden_ids = _toda_group_proof_narrative_argument_frontier_hidden_step_ids(
      presentation,
      blocks,
      local_blocks,
      sidecar,
      argument,
    )
    direct_premises = (
      ()
      if conclusion is None
      else extract_toda_group_proof_narrative_argument_conclusion_direct_derivation_premises(
        argument,
        arguments,
      )
    )

    print()
    print(
      f"ARG {argument_index}: "
      f"role={argument.role.value} "
      f"children={argument.child_argument_indices} "
      f"subject={subject}"
    )
    print(
      "  conclusion:",
      None
      if conclusion is None
      else _render_generic_narrative_step(
        conclusion
      ),
    )
    print("  direct premises:")
    for proof_step in direct_premises:
      print(
        "   ",
        _render_generic_narrative_step(
          proof_step
        ),
      )

    print("  local blocks:")
    for block in local_blocks:
      print(
        "   BLOCK",
        block.role.value,
      )
      for proof_step in block.steps:
        visibility = (
          "HIDDEN"
          if id(proof_step) in hidden_ids
          else "VISIBLE"
        )
        print(
          "    ",
          visibility,
          _render_generic_narrative_step(
            proof_step
          ),
        )


show(3, 3)
show(5, 3)
