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


from tests.test_phase143_19_method_evidence import (
  _method_evidence_data,
)
from toda_group_proof_narrative_argument_multi_renderer import (
  render_toda_group_proof_narrative_multi_argument_markdown,
)
from toda_group_proof_narrative_contribution_ordering import (
  build_toda_group_proof_narrative_ordered_contributions,
)
from toda_group_proof_narrative_contribution_renderer import (
  _insert_toda_group_proof_narrative_argument_contributions,
  _toda_group_proof_narrative_reference_owned_step_ids,
  _toda_group_proof_narrative_reference_statement_lines_by_number,
  insert_toda_group_proof_narrative_adjacent_eta_suspension_bridges,
  insert_toda_group_proof_narrative_hidden_zero_map_premises,
  insert_toda_group_proof_narrative_map_property_dependencies,
  link_toda_group_proof_narrative_reference_body_consumers,
  link_toda_group_proof_narrative_unmarked_reference_consumers,
  merge_toda_group_proof_narrative_adjacent_ehp_exactness_windows,
  normalize_toda_group_proof_narrative_connectors,
  normalize_toda_group_proof_narrative_repeated_numeric_equalities,
  order_toda_group_proof_narrative_injective_image_order_reason,
  order_toda_group_proof_narrative_local_equation_derivations,
  order_toda_group_proof_narrative_order_support,
  order_toda_group_proof_narrative_short_exact_support,
  order_toda_group_proof_narrative_surjectivity_support,
  order_toda_group_proof_narrative_visible_relation_dependencies,
  suppress_toda_group_proof_narrative_dangling_connectors,
  suppress_toda_group_proof_narrative_irrelevant_aggregate_ancestry,
  suppress_toda_group_proof_narrative_reference_body_duplicates,
  suppress_toda_group_proof_narrative_reference_internal_body,
  suppress_toda_group_proof_narrative_reflexive_equalities,
  suppress_toda_group_proof_narrative_repeated_reference_restatements,
  suppress_toda_group_proof_narrative_repeated_unique_step_statements,
  trim_toda_group_proof_narrative_redundant_left_ehp_terms,
)
from toda_group_proof_narrative_proof_chains import (
  build_toda_group_proof_narrative_proof_chains,
)
from toda_group_proof_narrative_reason_renderer import (
  insert_toda_group_proof_narrative_reason_prose,
)
from toda_group_proof_narrative_reasons import (
  build_toda_group_proof_narrative_reason_sidecar,
)
from toda_group_proof_narrative_references import (
  build_toda_group_proof_narrative_reference_entries,
  exclude_toda_group_proof_narrative_root_reference,
  filter_toda_group_proof_narrative_reference_entries_by_fixed_statement_boundary,
)


ROOT_FRAGMENT = (
  r"\pi_{4}^{3} = "
  r"\mathbb{Z}/2\{\eta_{3}\}"
)
PREMISE_FRAGMENT = (
  r"\pi_{3}^{2} = "
  r"\mathbb{Z}\{\eta_{2}\}"
)


def record(
  rows,
  name: str,
  markdown: str,
) -> None:
  paragraphs = markdown.split(
    "\n\n"
  )

  root_indices = tuple(
    index
    for index, paragraph in enumerate(
      paragraphs
    )
    if ROOT_FRAGMENT in paragraph
  )
  premise_indices = tuple(
    index
    for index, paragraph in enumerate(
      paragraphs
    )
    if PREMISE_FRAGMENT in paragraph
  )

  rows.append(
    (
      name,
      root_indices,
      premise_indices,
      tuple(
        (
          index,
          paragraph,
        )
        for index, paragraph in enumerate(
          paragraphs
        )
        if (
          ROOT_FRAGMENT in paragraph
          or PREMISE_FRAGMENT in paragraph
          or "以上より," in paragraph
        )
      ),
    )
  )


def main() -> int:
  (
    presentation,
    blocks,
    semantic_sidecar,
    arguments,
  ) = _method_evidence_data(
    3,
    1,
  )

  root_step = presentation.root_step

  lines = [
    "# Phase 159 pi4_3 trailing premise stage audit",
    "",
    "root_rule="
    + (
      root_step.inference_rule.name
      if root_step.inference_rule is not None
      else str(
        root_step.rule
      )
    ),
    "root_direct_premise_count="
    + str(
      len(
        root_step.premises
      )
    ),
  ]

  for index, premise in enumerate(
    root_step.premises
  ):
    lines.extend(
      (
        "root_premise_"
        + str(
          index
        )
        + "_rule="
        + (
          premise.inference_rule.name
          if premise.inference_rule is not None
          else str(
            premise.rule
          )
        ),
        "root_premise_"
        + str(
          index
        )
        + "_conclusion="
        + repr(
          premise.conclusion
        ),
      )
    )

  base = (
    render_toda_group_proof_narrative_multi_argument_markdown(
      presentation,
      blocks,
      semantic_sidecar,
      arguments,
    )
  )
  proof_chains = (
    build_toda_group_proof_narrative_proof_chains(
      presentation,
      semantic_sidecar,
      arguments,
    )
  )
  ordered_contributions = (
    build_toda_group_proof_narrative_ordered_contributions(
      presentation,
      blocks,
      semantic_sidecar,
      arguments,
      proof_chains,
      current_markdown=base,
    )
  )

  rows = []
  rendered = base
  record(
    rows,
    "00_base",
    rendered,
  )

  rendered = (
    _insert_toda_group_proof_narrative_argument_contributions(
      presentation,
      rendered,
      blocks,
      arguments,
      ordered_contributions,
    )
  )
  record(
    rows,
    "01_contributions",
    rendered,
  )

  reference_entries = (
    build_toda_group_proof_narrative_reference_entries(
      presentation
    )
  )
  reference_entries = (
    filter_toda_group_proof_narrative_reference_entries_by_fixed_statement_boundary(
      reference_entries,
      presentation.root_step,
    )
  )
  statement_lines = (
    _toda_group_proof_narrative_reference_statement_lines_by_number(
      presentation,
      reference_entries,
    )
  )
  (
    reference_entries,
    statement_lines,
  ) = (
    exclude_toda_group_proof_narrative_root_reference(
      reference_entries,
      statement_lines,
      presentation.root_step,
    )
  )
  reference_owned_step_ids = (
    _toda_group_proof_narrative_reference_owned_step_ids(
      presentation,
      reference_entries,
    )
  )
  reason_sidecar = (
    build_toda_group_proof_narrative_reason_sidecar(
      presentation,
      semantic_sidecar,
    )
  )
  boundary_reason_sidecar = type(
    reason_sidecar
  )(
    presentation=reason_sidecar.presentation,
    reasons=tuple(
      reason
      for reason in reason_sidecar.reasons
      if id(
        reason.conclusion_step
      )
      not in reference_owned_step_ids
    ),
  )

  transforms = (
    (
      "02_reason_insertion",
      lambda text: insert_toda_group_proof_narrative_reason_prose(
        text,
        boundary_reason_sidecar,
      ),
    ),
    (
      "03_reference_internal",
      lambda text: suppress_toda_group_proof_narrative_reference_internal_body(
        presentation,
        text,
        reference_entries,
        arguments,
        semantic_sidecar,
      ),
    ),
    (
      "04_irrelevant_aggregate",
      lambda text: suppress_toda_group_proof_narrative_irrelevant_aggregate_ancestry(
        presentation,
        text,
        reference_entries,
      ),
    ),
    (
      "05_reference_duplicates",
      lambda text: suppress_toda_group_proof_narrative_reference_body_duplicates(
        text,
        statement_lines,
      ),
    ),
    (
      "06_reference_consumers",
      lambda text: link_toda_group_proof_narrative_reference_body_consumers(
        presentation,
        text,
        reference_entries,
      ),
    ),
    (
      "07_connectors_a",
      normalize_toda_group_proof_narrative_connectors,
    ),
    (
      "08_local_equations",
      order_toda_group_proof_narrative_local_equation_derivations,
    ),
    (
      "09_order_support",
      lambda text: order_toda_group_proof_narrative_order_support(
        presentation,
        text,
      ),
    ),
    (
      "10_hidden_zero",
      lambda text: insert_toda_group_proof_narrative_hidden_zero_map_premises(
        presentation,
        text,
        reference_entries,
      ),
    ),
    (
      "11_map_dependencies_a",
      lambda text: insert_toda_group_proof_narrative_map_property_dependencies(
        presentation,
        text,
        reference_entries,
      ),
    ),
    (
      "12_eta_bridge",
      lambda text: insert_toda_group_proof_narrative_adjacent_eta_suspension_bridges(
        presentation,
        text,
        reference_entries,
      ),
    ),
    (
      "13_merge_exactness",
      lambda text: merge_toda_group_proof_narrative_adjacent_ehp_exactness_windows(
        presentation,
        text,
      ),
    ),
    (
      "14_trim_left",
      trim_toda_group_proof_narrative_redundant_left_ehp_terms,
    ),
    (
      "15_connectors_b",
      normalize_toda_group_proof_narrative_connectors,
    ),
    (
      "16_numeric",
      normalize_toda_group_proof_narrative_repeated_numeric_equalities,
    ),
    (
      "17_unmarked_reference",
      lambda text: link_toda_group_proof_narrative_unmarked_reference_consumers(
        presentation,
        text,
        reference_entries,
      ),
    ),
    (
      "18_reflexive",
      lambda text: suppress_toda_group_proof_narrative_reflexive_equalities(
        presentation,
        text,
      ),
    ),
    (
      "19_surjectivity_support",
      lambda text: order_toda_group_proof_narrative_surjectivity_support(
        presentation,
        text,
        reference_entries,
        statement_lines,
      ),
    ),
    (
      "20_short_exact",
      lambda text: order_toda_group_proof_narrative_short_exact_support(
        presentation,
        text,
      ),
    ),
    (
      "21_reference_restatements",
      lambda text: suppress_toda_group_proof_narrative_repeated_reference_restatements(
        text,
        statement_lines,
      ),
    ),
    (
      "22_dangling",
      suppress_toda_group_proof_narrative_dangling_connectors,
    ),
    (
      "23_visible_relation_dependencies",
      lambda text: order_toda_group_proof_narrative_visible_relation_dependencies(
        presentation,
        text,
      ),
    ),
    (
      "24_unique_steps",
      lambda text: suppress_toda_group_proof_narrative_repeated_unique_step_statements(
        presentation,
        text,
      ),
    ),
    (
      "25_map_dependencies_b",
      lambda text: insert_toda_group_proof_narrative_map_property_dependencies(
        presentation,
        text,
        reference_entries,
      ),
    ),
    (
      "26_injective_reason",
      lambda text: order_toda_group_proof_narrative_injective_image_order_reason(
        text,
        reason_sidecar,
      ),
    ),
  )

  for name, transform in transforms:
    rendered = transform(
      rendered
    )
    record(
      rows,
      name,
      rendered,
    )

  lines.extend(
    (
      "",
      "## Stage order",
      "",
    )
  )

  previous_relation = None

  for (
    name,
    root_indices,
    premise_indices,
    matches,
  ) in rows:
    relation = (
      "premise_before_root"
      if (
        root_indices
        and premise_indices
        and min(
          premise_indices
        )
        < min(
          root_indices
        )
      )
      else "premise_after_root"
      if (
        root_indices
        and premise_indices
      )
      else "missing"
    )

    change = (
      ""
      if (
        previous_relation is None
        or previous_relation == relation
      )
      else (
        "  <-- ORDER CHANGED "
        + previous_relation
        + " -> "
        + relation
      )
    )

    lines.append(
      name
      + ": root="
      + repr(
        root_indices
      )
      + ", premise="
      + repr(
        premise_indices
      )
      + ", relation="
      + relation
      + change
    )

    for paragraph_index, paragraph in matches:
      lines.append(
        "  P"
        + str(
          paragraph_index
        )
        + ": "
        + repr(
          paragraph
        )
      )

    previous_relation = relation

  lines.extend(
    (
      "",
      "## Final staged markdown",
      "",
      rendered,
      "",
    )
  )

  output = "\n".join(
    lines
  )
  output_path = (
    Path(__file__).resolve().parent
    / "phase159_pi4_3_trailing_premise_stage_audit.txt"
  )
  output_path.write_text(
    output,
    encoding="utf-8",
  )

  print(
    output
  )

  return 0


if __name__ == "__main__":
  raise SystemExit(
    main()
  )
