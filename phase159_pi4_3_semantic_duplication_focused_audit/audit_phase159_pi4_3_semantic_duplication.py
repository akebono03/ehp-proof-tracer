from dataclasses import fields, is_dataclass
from enum import Enum
from pathlib import Path
import sys


REPO_ROOT = Path(__file__).resolve().parent.parent

if str(REPO_ROOT) not in sys.path:
  sys.path.insert(
    0,
    str(
      REPO_ROOT
    ),
  )


from proof import (
  Relation,
)
from toda_calculation_facade import (
  build_standard_toda_report,
)
from toda_group_proof_narrative_argument_local_body import (
  extract_toda_group_proof_narrative_argument_local_body_blocks,
)
from toda_group_proof_narrative_argument_ordering import (
  order_toda_group_proof_narrative_arguments,
)
from toda_group_proof_narrative_arguments import (
  build_toda_group_proof_narrative_arguments,
  extract_toda_group_proof_narrative_argument_conclusion_step,
)
from toda_group_proof_narrative_blocks import (
  build_toda_group_proof_narrative_blocks,
)
from toda_group_proof_narrative_renderer import (
  render_toda_group_proof_narrative_markdown,
)
from toda_group_proof_narrative_semantics import (
  build_toda_group_proof_narrative_semantic_closure_presentation,
  build_toda_group_proof_narrative_semantic_sidecar,
)
from toda_group_proof_narrative_transitions import (
  extract_toda_group_proof_narrative_transitions,
)
from toda_group_proof_presentation import (
  build_toda_group_proof_presentation,
)
from toda_group_result_proof_replay import (
  build_toda_group_result_proof_replay,
)


def semantic_statement_key(
  value,
):
  if isinstance(
    value,
    Relation,
  ):
    return (
      "Relation",
      semantic_statement_key(
        value.lhs
      ),
      semantic_statement_key(
        value.rhs
      ),
      semantic_statement_key(
        value.relation_type
      ),
    )

  if isinstance(
    value,
    Enum,
  ):
    return (
      type(
        value
      ).__module__,
      type(
        value
      ).__qualname__,
      value.value,
    )

  if is_dataclass(
    value
  ):
    return (
      type(
        value
      ).__module__,
      type(
        value
      ).__qualname__,
      tuple(
        (
          field.name,
          semantic_statement_key(
            getattr(
              value,
              field.name
            )
          ),
        )
        for field in fields(
          value
        )
      ),
    )

  if isinstance(
    value,
    tuple,
  ):
    return (
      "tuple",
      tuple(
        semantic_statement_key(
          item
        )
        for item in value
      ),
    )

  if isinstance(
    value,
    list,
  ):
    return (
      "list",
      tuple(
        semantic_statement_key(
          item
        )
        for item in value
      ),
    )

  if isinstance(
    value,
    dict,
  ):
    return (
      "dict",
      tuple(
        sorted(
          (
            semantic_statement_key(
              key
            ),
            semantic_statement_key(
              item
            ),
          )
          for key, item in value.items()
        )
      ),
    )

  if isinstance(
    value,
    (
      str,
      int,
      float,
      bool,
      type(
        None
      ),
    ),
  ):
    return value

  return (
    type(
      value
    ).__module__,
    type(
      value
    ).__qualname__,
    repr(
      value
    ),
  )


def rule_name(
  proof_step,
) -> str:
  inference_rule = (
    proof_step.inference_rule
  )

  if inference_rule is not None:
    return inference_rule.name

  rule = proof_step.rule

  return (
    rule.value
    if hasattr(
      rule,
      "value"
    )
    else str(
      rule
    )
  )


def build_presentation():
  report = build_standard_toda_report(
    n=3,
    k=1,
  )
  group_result = (
    report
    .candidates[0]
    .source_candidate
    .group_result
  )
  replay = build_toda_group_result_proof_replay(
    group_result,
    max_depth=2,
  )
  raw_presentation = (
    build_toda_group_proof_presentation(
      replay
    )
  )
  closure_presentation = (
    build_toda_group_proof_narrative_semantic_closure_presentation(
      raw_presentation
    )
  )

  return (
    raw_presentation,
    closure_presentation,
  )


def main() -> int:
  (
    raw_presentation,
    presentation,
  ) = build_presentation()

  semantic_sidecar = (
    build_toda_group_proof_narrative_semantic_sidecar(
      presentation
    )
  )
  blocks = (
    build_toda_group_proof_narrative_blocks(
      presentation,
      semantic_sidecar=semantic_sidecar,
    )
  )
  arguments = (
    build_toda_group_proof_narrative_arguments(
      presentation,
      blocks,
      semantic_sidecar=semantic_sidecar,
    )
  )
  ordered_arguments = (
    order_toda_group_proof_narrative_arguments(
      arguments
    )
  )
  transitions = (
    extract_toda_group_proof_narrative_transitions(
      presentation,
      blocks,
      arguments,
    )
  )

  root_step = presentation.root_step
  root_statement = root_step.conclusion
  root_key = semantic_statement_key(
    root_statement
  )

  matching_steps = tuple(
    node.proof_step
    for node in presentation.nodes
    if (
      semantic_statement_key(
        node.proof_step.conclusion
      )
      == root_key
    )
  )

  output = []

  output.extend(
    (
      "# Phase 159 pi4_3 semantic duplication focused audit",
      "",
      "target: pi_4^3",
      "raw_node_count: "
      + str(
        len(
          raw_presentation.nodes
        )
      ),
      "closure_node_count: "
      + str(
        len(
          presentation.nodes
        )
      ),
      "semantic_root_match_count: "
      + str(
        len(
          matching_steps
        )
      ),
      "",
      "## Root statement",
      "",
      "root_step_id: "
      + str(
        id(
          root_step
        )
      ),
      "root_rule: "
      + rule_name(
        root_step
      ),
      "root_statement_type: "
      + type(
        root_statement
      ).__name__,
      "root_statement_repr: "
      + repr(
        root_statement
      ),
      "root_semantic_key: "
      + repr(
        root_key
      ),
      "",
      "## Semantically matching proof steps",
      "",
    )
  )

  for index, proof_step in enumerate(
    matching_steps,
    start=1,
  ):
    output.extend(
      (
        "### match "
        + str(
          index
        ),
        "",
        "step_id: "
        + str(
          id(
            proof_step
          )
        ),
        "is_root_step: "
        + str(
          proof_step is root_step
        ),
        "statement_is_root_object: "
        + str(
          proof_step.conclusion
          is root_statement
        ),
        "statement_structural_eq_root: "
        + str(
          proof_step.conclusion
          == root_statement
        ),
        "rule: "
        + rule_name(
          proof_step
        ),
        "premise_count: "
        + str(
          len(
            proof_step.premises
          )
        ),
        "statement_repr: "
        + repr(
          proof_step.conclusion
        ),
        "",
      )
    )

  output.extend(
    (
      "## Blocks containing the semantic root statement",
      "",
    )
  )

  matching_step_ids = {
    id(
      proof_step
    )
    for proof_step in matching_steps
  }

  matching_block_ids = set()

  for block_index, block in enumerate(
    blocks
  ):
    block_matching_steps = tuple(
      proof_step
      for proof_step in block.steps
      if (
        id(
          proof_step
        )
        in matching_step_ids
      )
    )

    if not block_matching_steps:
      continue

    matching_block_ids.add(
      id(
        block
      )
    )

    output.extend(
      (
        "### block "
        + str(
          block_index
        ),
        "",
        "block_id: "
        + str(
          id(
            block
          )
        ),
        "block_role: "
        + str(
          block.role.value
          if hasattr(
            block.role,
            "value"
          )
          else block.role
        ),
        "matching_step_ids: "
        + repr(
          tuple(
            id(
              proof_step
            )
            for proof_step in block_matching_steps
          )
        ),
        "all_step_ids: "
        + repr(
          tuple(
            id(
              proof_step
            )
            for proof_step in block.steps
          )
        ),
        "",
      )
    )

  output.extend(
    (
      "## Argument ownership",
      "",
    )
  )

  source_index_by_id = {
    id(
      argument
    ): index
    for index, argument in enumerate(
      arguments
    )
  }

  for ordered_index, argument in enumerate(
    ordered_arguments
  ):
    source_index = source_index_by_id[
      id(
        argument
      )
    ]
    conclusion_step = (
      extract_toda_group_proof_narrative_argument_conclusion_step(
        argument
      )
    )
    local_body_blocks = (
      extract_toda_group_proof_narrative_argument_local_body_blocks(
        presentation,
        blocks,
        semantic_sidecar,
        arguments,
        source_index,
      )
    )

    conclusion_matches = (
      conclusion_step is not None
      and semantic_statement_key(
        conclusion_step.conclusion
      )
      == root_key
    )
    local_matching_blocks = tuple(
      block
      for block in local_body_blocks
      if id(
        block
      ) in matching_block_ids
    )

    if (
      not conclusion_matches
      and not local_matching_blocks
    ):
      continue

    output.extend(
      (
        "### ordered argument "
        + str(
          ordered_index
        ),
        "",
        "source_argument_index: "
        + str(
          source_index
        ),
        "argument_role: "
        + str(
          argument.role.value
          if hasattr(
            argument.role,
            "value"
          )
          else argument.role
        ),
        "conclusion_block_id: "
        + str(
          id(
            argument.conclusion_block
          )
        ),
        "conclusion_step_id: "
        + (
          str(
            id(
              conclusion_step
            )
          )
          if conclusion_step is not None
          else "None"
        ),
        "conclusion_semantically_matches_root: "
        + str(
          conclusion_matches
        ),
        "local_matching_block_ids: "
        + repr(
          tuple(
            id(
              block
            )
            for block in local_matching_blocks
          )
        ),
        "",
      )
    )

  output.extend(
    (
      "## Transitions targeting matching blocks",
      "",
    )
  )

  for transition in transitions:
    if id(
      transition.target_block
    ) not in matching_block_ids:
      continue

    output.extend(
      (
        "transition_role: "
        + str(
          transition.role.value
        ),
        "target_block_id: "
        + str(
          id(
            transition.target_block
          )
        ),
        "source_block_ids: "
        + repr(
          tuple(
            id(
              block
            )
            for block in transition.source_blocks
          )
        ),
        "",
      )
    )

  rendered = (
    render_toda_group_proof_narrative_markdown(
      raw_presentation
    )
  )

  output.extend(
    (
      "## Public Narrative",
      "",
      rendered.rstrip(),
      "",
      "## Interpretation guide",
      "",
      (
        "- semantic_root_match_count = 1 なのに public Narrative で同一結論が"
        " 2回出る場合: 同じ semantic statement / ProofStep が描画経路で二重消費されている。"
      ),
      (
        "- semantic_root_match_count >= 2 の場合: 別 ProofStep が同じ数学的主張を持つ。"
        " id-based suppression では統合できない。"
      ),
      (
        "- statement_structural_eq_root=False だが semantic key が一致する場合:"
        " source/note 等の provenance metadata だけが違う。"
      ),
      (
        "- 修正は prose 文字列ではなく semantic_statement_key 相当の"
        " statement identity で行う候補になる。"
      ),
      "",
    )
  )

  report_text = "\n".join(
    output
  )

  output_path = (
    Path(__file__).resolve().parent
    / "phase159_pi4_3_semantic_duplication_audit.txt"
  )
  output_path.write_text(
    report_text,
    encoding="utf-8",
  )

  print(
    report_text
  )

  return 0


if __name__ == "__main__":
  raise SystemExit(
    main()
  )
