from toda_calculation_facade import (
  build_standard_toda_report,
)
from toda_group_proof_generic_narrative_renderer import (
  _render_generic_narrative_step,
)
from toda_group_proof_narrative_argument_local_body import (
  extract_toda_group_proof_narrative_argument_local_body_blocks,
)
from toda_group_proof_narrative_argument_multi_renderer import (
  render_toda_group_proof_narrative_multi_argument_markdown,
)
from toda_group_proof_narrative_arguments import (
  build_toda_group_proof_narrative_arguments,
)
from toda_group_proof_narrative_blocks import (
  build_toda_group_proof_narrative_blocks,
)
from toda_group_proof_narrative_semantics import (
  build_toda_group_proof_narrative_semantic_closure_presentation,
  build_toda_group_proof_narrative_semantic_sidecar,
)
from toda_group_proof_presentation import (
  build_toda_group_proof_presentation,
)
from toda_group_result_proof_replay import (
  build_complete_toda_group_result_proof_replay,
  build_toda_group_result_proof_replay,
)
from toda_proof_dependency import (
  extract_toda_recursive_proof_provenance,
)


EQUATIONS = (
  (
    "EQ1",
    r"2\nu' = \eta_{3}E\eta_{3}\eta_{5}",
  ),
  (
    "EQ2",
    (
      r"\eta_{3}E\eta_{3}\eta_{5} = "
      r"\eta_{3}^{3}"
    ),
  ),
  (
    "EQ3",
    r"2\nu' = \eta_{3}^{3}",
  ),
)


def _group_result():
  report = build_standard_toda_report(
    n=3,
    k=3,
  )
  return (
    report.candidates[
      0
    ].source_candidate.group_result
  )


def _contexts(
  group_result,
):
  result = {}

  for label, replay in (
    (
      "depth2",
      build_toda_group_result_proof_replay(
        group_result,
        max_depth=2,
      ),
    ),
    (
      "depth3",
      build_toda_group_result_proof_replay(
        group_result,
        max_depth=3,
      ),
    ),
    (
      "complete",
      build_complete_toda_group_result_proof_replay(
        group_result
      ),
    ),
  ):
    presentation = (
      build_toda_group_proof_presentation(
        replay
      )
    )
    closure = (
      build_toda_group_proof_narrative_semantic_closure_presentation(
        presentation
      )
    )
    sidecar = (
      build_toda_group_proof_narrative_semantic_sidecar(
        closure
      )
    )
    blocks = (
      build_toda_group_proof_narrative_blocks(
        closure,
        semantic_sidecar=sidecar,
      )
    )
    arguments = (
      build_toda_group_proof_narrative_arguments(
        closure,
        blocks,
        semantic_sidecar=sidecar,
      )
    )
    rendered = (
      render_toda_group_proof_narrative_multi_argument_markdown(
        closure,
        blocks,
        sidecar,
        arguments,
      )
    )
    result[
      label
    ] = {
      "replay": replay,
      "presentation": presentation,
      "closure": closure,
      "sidecar": sidecar,
      "blocks": blocks,
      "arguments": arguments,
      "rendered": rendered,
    }

  return result


def _matching_steps(
  presentation,
  equation_latex,
):
  matches = []

  for node in presentation.nodes:
    rendered = (
      _render_generic_narrative_step(
        node.proof_step
      )
    )
    if equation_latex in rendered:
      matches.append(
        (
          node,
          rendered,
        )
      )

  return tuple(
    matches
  )


def _block_locations(
  blocks,
  proof_step,
):
  return tuple(
    (
      index,
      block.role.value,
    )
    for index, block in enumerate(
      blocks
    )
    if proof_step in block.steps
  )


def _argument_locations(
  presentation,
  sidecar,
  arguments,
  blocks,
  proof_step,
):
  result = []

  for index, argument in enumerate(
    arguments
  ):
    model_support_indexes = tuple(
      block_index
      for block_index, block in enumerate(
        blocks
      )
      if (
        block in argument.supporting_blocks
        and proof_step in block.steps
      )
    )
    conclusion_indexes = tuple(
      block_index
      for block_index, block in enumerate(
        blocks
      )
      if (
        block is argument.conclusion_block
        and proof_step in block.steps
      )
    )
    local_body_blocks = (
      extract_toda_group_proof_narrative_argument_local_body_blocks(
        presentation,
        blocks,
        sidecar,
        arguments,
        index,
      )
    )
    local_body_indexes = tuple(
      block_index
      for block_index, block in enumerate(
        blocks
      )
      if (
        block in local_body_blocks
        and proof_step in block.steps
      )
    )

    if (
      model_support_indexes
      or conclusion_indexes
      or local_body_indexes
    ):
      result.append(
        (
          index,
          argument.role.value,
          {
            "supporting": model_support_indexes,
            "conclusion": conclusion_indexes,
            "local_body": local_body_indexes,
          },
        )
      )

  return tuple(
    result
  )


def _edge_rows(
  provenance,
  proof_step,
):
  rows = []

  for edge in provenance.edges:
    if (
      edge.parent_step is proof_step
      or edge.premise_step is proof_step
    ):
      rows.append(
        (
          "PARENT"
          if edge.parent_step is proof_step
          else "PREMISE",
          edge.premise_index,
          edge.parent_step,
          edge.premise_step,
        )
      )

  return tuple(
    rows
  )


def _step_label(
  proof_step,
):
  return (
    _render_generic_narrative_step(
      proof_step
    )
    .replace(
      "\n",
      " ",
    )
  )


def main():
  group_result = (
    _group_result()
  )
  contexts = (
    _contexts(
      group_result
    )
  )
  provenance = (
    extract_toda_recursive_proof_provenance(
      group_result
    )
  )

  print("=" * 92)
  print(
    "Phase 148 RC2-4 Repair R4.1 "
    "numbered-equation dependency audit"
  )
  print(
    "Production changes: none"
  )
  print("=" * 92)

  print()
  print("A. CONTEXT SUMMARY")
  print("-" * 92)

  for label in (
    "depth2",
    "depth3",
    "complete",
  ):
    data = contexts[
      label
    ]
    print(
      label
      + ": replay_nodes="
      + str(
        len(
          data[
            "presentation"
          ].nodes
        )
      )
      + " closure_nodes="
      + str(
        len(
          data[
            "closure"
          ].nodes
        )
      )
      + " closure_max_depth="
      + str(
        data[
          "closure"
        ].max_depth
      )
      + " blocks="
      + str(
        len(
          data[
            "blocks"
          ]
        )
      )
      + " arguments="
      + str(
        len(
          data[
            "arguments"
          ]
        )
      )
    )

  print()
  print("B. EQUATION PRESENCE / DEPTH / OWNERSHIP")
  print("-" * 92)

  complete = contexts[
    "complete"
  ]

  for equation_name, equation_latex in EQUATIONS:
    print()
    print(
      equation_name
      + ": "
      + equation_latex
    )

    complete_matches = (
      _matching_steps(
        complete[
          "closure"
        ],
        equation_latex,
      )
    )

    print(
      "complete match count="
      + str(
        len(
          complete_matches
        )
      )
    )

    for node, rendered in complete_matches:
      proof_step = node.proof_step
      print(
        "  shortest_depth="
        + str(
          node.depth
        )
      )
      print(
        "  role="
        + node.role.value
      )
      print(
        "  rule="
        + (
          "<none>"
          if proof_step.inference_rule is None
          else proof_step.inference_rule.name
        )
      )
      print(
        "  rendered="
        + rendered
      )
      print(
        "  complete blocks="
        + repr(
          _block_locations(
            complete[
              "blocks"
            ],
            proof_step,
          )
        )
      )
      print(
        "  complete arguments="
        + repr(
          _argument_locations(
            complete[
              "closure"
            ],
            complete[
              "sidecar"
            ],
            complete[
              "arguments"
            ],
            complete[
              "blocks"
            ],
            proof_step,
          )
        )
      )

      for label in (
        "depth2",
        "depth3",
        "complete",
      ):
        data = contexts[
          label
        ]
        raw_ids = {
          id(
            item.proof_step
          )
          for item in data[
            "presentation"
          ].nodes
        }
        closure_ids = {
          id(
            item.proof_step
          )
          for item in data[
            "closure"
          ].nodes
        }
        print(
          "  "
          + label
          + ": raw="
          + str(
            id(
              proof_step
            )
            in raw_ids
          )
          + " closure="
          + str(
            id(
              proof_step
            )
            in closure_ids
          )
          + " rendered="
          + str(
            equation_latex
            in data[
              "rendered"
            ]
          )
        )

      print(
        "  dependency edges:"
      )
      for (
        direction,
        premise_index,
        parent_step,
        premise_step,
      ) in _edge_rows(
        provenance,
        proof_step,
      ):
        print(
          "    "
          + direction
          + " premise_index="
          + str(
            premise_index
          )
        )
        print(
          "      parent:  "
          + _step_label(
            parent_step
          )
        )
        print(
          "      premise: "
          + _step_label(
            premise_step
          )
        )

  print()
  print("C. SEMANTIC CLOSURE DELTA AT DEPTH=2")
  print("-" * 92)

  depth2 = contexts[
    "depth2"
  ]
  raw_ids = {
    id(
      node.proof_step
    )
    for node in depth2[
      "presentation"
    ].nodes
  }
  added = tuple(
    node
    for node in depth2[
      "closure"
    ].nodes
    if id(
      node.proof_step
    ) not in raw_ids
  )

  print(
    "closure-added steps="
    + str(
      len(
        added
      )
    )
  )

  for node in added:
    print(
      "  depth="
      + str(
        node.depth
      )
      + " role="
      + node.role.value
      + " step="
      + _step_label(
        node.proof_step
      )
    )

  print()
  print("D. NUMBERING / CONNECTOR VISIBILITY")
  print("-" * 92)

  for label in (
    "depth2",
    "depth3",
    "complete",
  ):
    rendered = contexts[
      label
    ][
      "rendered"
    ]
    print(
      label
      + ": "
      + "tag1="
      + str(
        r"\tag{1}"
        in rendered
      )
      + " tag2="
      + str(
        r"\tag{2}"
        in rendered
      )
      + " tag3="
      + str(
        r"\tag{3}"
        in rendered
      )
      + " connector12="
      + str(
        "(1) と (2) より、"
        in rendered
      )
    )

  print()
  print("E. AUDIT INTERPRETATION INPUT")
  print("-" * 92)
  print(
    "If EQ1/EQ2/EQ3 exist in complete/depth3 but not "
    "depth2 closure, the loss occurs before rendering."
  )
  print(
    "If they exist in depth2 closure but are not rendered, "
    "the loss occurs in block/argument selection or rendering."
  )
  print(
    "The current semantic closure is expected to add only "
    "registered semantic prerequisites; R4.1 does not modify it."
  )


if __name__ == "__main__":
  main()
