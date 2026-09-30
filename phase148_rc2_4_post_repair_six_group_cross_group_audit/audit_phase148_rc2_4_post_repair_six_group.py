from collections import Counter

from proof import (
  Relation,
  RelationType,
)
from toda_calculation_facade import (
  build_standard_toda_report,
)
from toda_group_proof_narrative_arguments import (
  build_toda_group_proof_narrative_arguments,
)
from toda_group_proof_narrative_blocks import (
  TodaGroupProofNarrativeMathematicalBlockRole,
  build_toda_group_proof_narrative_blocks,
)
from toda_group_proof_narrative_exactness_components import (
  build_toda_group_proof_narrative_exactness_method_components,
)
from toda_group_proof_narrative_exactness_exposure import (
  classify_toda_group_proof_narrative_exactness_component_exposure,
)
from toda_group_proof_narrative_method_evidence import (
  extract_toda_group_proof_narrative_argument_method_evidence,
)
from toda_group_proof_narrative_relevant_groups import (
  extract_toda_group_proof_narrative_argument_relevant_groups,
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
from web_group_proof import (
  build_standard_web_group_proof_view,
)


CASES = (
  ("pi_6^3", 3, 3),
  ("pi_8^5", 5, 3),
  ("pi_10^4", 4, 6),
  ("pi_12^5", 5, 7),
  ("pi_15^8", 8, 7),
  ("pi_16^9", 9, 7),
)


def _group_result(
  n,
  k,
):
  report = build_standard_toda_report(
    n=n,
    k=k,
  )
  return (
    report.candidates[
      0
    ].source_candidate.group_result
  )


def _web_text(
  view,
):
  parts = []

  for line in view.rendered_lines:
    if line.segments:
      for segment in line.segments:
        if segment.kind in (
          "inline_math",
          "display_math",
        ):
          parts.append(
            "$"
            + segment.value
            + "$"
          )
        else:
          parts.append(
            segment.value
          )
      parts.append(
        "\n"
      )
      continue

    parts.append(
      line.prefix
    )
    if line.statement_latex is not None:
      parts.append(
        "$"
        + line.statement_latex
        + "$"
      )
    parts.append(
      line.suffix
    )
    parts.append(
      "\n"
    )

  return "".join(
    parts
  )


def _case_data(
  label,
  n,
  k,
):
  group_result = _group_result(
    n,
    k,
  )
  replay = (
    build_toda_group_result_proof_replay(
      group_result,
      max_depth=2,
    )
  )
  complete_replay = (
    build_complete_toda_group_result_proof_replay(
      group_result
    )
  )
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
  view = (
    build_standard_web_group_proof_view(
      n,
      k,
      max_depth=2,
      mode="narrative",
    )
  )
  rendered = _web_text(
    view
  )

  input_ids = {
    id(
      node.proof_step
    )
    for node in presentation.nodes
  }
  added_nodes = tuple(
    node
    for node in closure.nodes
    if id(
      node.proof_step
    ) not in input_ids
  )
  added_equalities = tuple(
    node
    for node in added_nodes
    if (
      isinstance(
        node.proof_step.conclusion,
        Relation,
      )
      and node.proof_step.conclusion.relation_type
      is RelationType.EQUALITY
    )
  )
  added_exactness = tuple(
    node
    for node in added_nodes
    if node.role.value == "exactness"
  )
  exactness_blocks = tuple(
    block
    for block in blocks
    if (
      block.role
      is TodaGroupProofNarrativeMathematicalBlockRole
      .EXACTNESS
    )
  )

  exposure_counts = Counter()
  component_count = 0

  for argument_index, argument in enumerate(
    arguments
  ):
    evidence = (
      extract_toda_group_proof_narrative_argument_method_evidence(
        closure,
        blocks,
        sidecar,
        arguments,
        argument_index,
      )
    )
    components = (
      build_toda_group_proof_narrative_exactness_method_components(
        evidence
      )
    )
    relevant_groups = (
      extract_toda_group_proof_narrative_argument_relevant_groups(
        closure,
        blocks,
        argument,
      )
    )

    for component in components:
      exposure = (
        classify_toda_group_proof_narrative_exactness_component_exposure(
          relevant_groups,
          components,
          component,
        )
      )
      exposure_counts[
        exposure.value
      ] += 1
      component_count += 1

  return {
    "label": label,
    "n": n,
    "k": k,
    "input_nodes": len(
      presentation.nodes
    ),
    "closure_nodes": len(
      closure.nodes
    ),
    "complete_nodes": len(
      complete_replay.steps
    ),
    "closure_max_depth": closure.max_depth,
    "added_nodes": added_nodes,
    "added_equalities": added_equalities,
    "added_exactness": added_exactness,
    "blocks": len(
      blocks
    ),
    "arguments": len(
      arguments
    ),
    "exactness_blocks": len(
      exactness_blocks
    ),
    "component_count": component_count,
    "exposure_counts": exposure_counts,
    "raw_exactness_phrases": (
      rendered.count(
        "は完全である"
      )
      + rendered.count(
        r"\text{ is exact}"
      )
    ),
    "rendered": rendered,
    "view": view,
  }


def build_audit_data():
  return tuple(
    _case_data(
      label,
      n,
      k,
    )
    for label, n, k in CASES
  )


def main():
  data = build_audit_data()

  print("=" * 100)
  print(
    "Phase 148 RC2-4 post-repair "
    "six-group cross-group audit"
  )
  print(
    "Web source: depth=2 bounded replay"
  )
  print(
    "Production changes: none"
  )
  print("=" * 100)

  for record in data:
    print()
    print("-" * 100)
    print(
      record[
        "label"
      ]
    )
    print("-" * 100)
    print(
      "nodes: input="
      + str(
        record[
          "input_nodes"
        ]
      )
      + " closure="
      + str(
        record[
          "closure_nodes"
        ]
      )
      + " complete="
      + str(
        record[
          "complete_nodes"
        ]
      )
      + " closure_max_depth="
      + str(
        record[
          "closure_max_depth"
        ]
      )
    )
    print(
      "closure added: total="
      + str(
        len(
          record[
            "added_nodes"
          ]
        )
      )
      + " equality="
      + str(
        len(
          record[
            "added_equalities"
          ]
        )
      )
      + " exactness="
      + str(
        len(
          record[
            "added_exactness"
          ]
        )
      )
    )
    print(
      "structure: blocks="
      + str(
        record[
          "blocks"
        ]
      )
      + " arguments="
      + str(
        record[
          "arguments"
        ]
      )
      + " exactness_blocks="
      + str(
        record[
          "exactness_blocks"
        ]
      )
    )
    print(
      "components="
      + str(
        record[
          "component_count"
        ]
      )
      + " exposure="
      + str(
        dict(
          record[
            "exposure_counts"
          ]
        )
      )
    )
    print(
      "Web raw exactness phrases="
      + str(
        record[
          "raw_exactness_phrases"
        ]
      )
    )

    if record[
      "added_nodes"
    ]:
      print(
        "closure-added roles="
        + str(
          dict(
            Counter(
              node.role.value
              for node in record[
                "added_nodes"
              ]
            )
          )
        )
      )

  print()
  print("=" * 100)
  print("AUDIT INVARIANTS")
  print("=" * 100)
  print(
    "all bounded below complete="
    + str(
      all(
        record[
          "closure_nodes"
        ]
        < record[
          "complete_nodes"
        ]
        for record in data
        if record[
          "complete_nodes"
        ]
        > record[
          "input_nodes"
        ]
      )
    )
  )
  print(
    "all closure-added exactness zero="
    + str(
      all(
        not record[
          "added_exactness"
        ]
        for record in data
      )
    )
  )
  print(
    "all Web raw exactness zero="
    + str(
      all(
        record[
          "raw_exactness_phrases"
        ]
        == 0
        for record in data
      )
    )
  )
  print(
    "all ambiguous exposure zero="
    + str(
      all(
        record[
          "exposure_counts"
        ].get(
          "ambiguous_relevant",
          0,
        )
        == 0
        for record in data
      )
    )
  )


if __name__ == "__main__":
  main()
