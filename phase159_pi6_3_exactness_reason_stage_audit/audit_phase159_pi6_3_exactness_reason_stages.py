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
  render_toda_group_proof_narrative_reason_sentence,
)
from toda_group_proof_narrative_reasons import (
  TodaGroupProofNarrativeReasonKind,
  build_toda_group_proof_narrative_reason_sidecar,
)
from toda_group_proof_narrative_references import (
  build_toda_group_proof_narrative_reference_entries,
  exclude_toda_group_proof_narrative_root_reference,
  filter_toda_group_proof_narrative_reference_entries_by_fixed_statement_boundary,
)
from toda_group_proof_narrative_semantics import (
  build_toda_group_proof_narrative_semantic_sidecar,
)


TARGET_FRAGMENT = (
  r"この完全性と $Δ=0$ より, "
  r"$\ker E=\operatorname{Im}Δ=0$"
)


def record(
  records,
  name: str,
  markdown: str,
) -> None:
  paragraphs = markdown.split(
    "\n\n"
  )
  matches = tuple(
    (
      index,
      paragraph,
    )
    for index, paragraph in enumerate(
      paragraphs
    )
    if (
      TARGET_FRAGMENT in paragraph
      or r"\ker E=\operatorname{Im}Δ=0" in paragraph
      or "したがって," in paragraph
    )
  )
  records.append(
    (
      name,
      TARGET_FRAGMENT in markdown,
      matches,
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
    3,
  )

  reason_sidecar = (
    build_toda_group_proof_narrative_reason_sidecar(
      presentation,
      semantic_sidecar,
    )
  )
  exactness_reasons = tuple(
    reason
    for reason in reason_sidecar.reasons
    if (
      reason.kind
      is TodaGroupProofNarrativeReasonKind
      .EXACTNESS_TO_MAP_PROPERTY
    )
  )

  lines = [
    "# Phase 159 pi6_3 exactness reason stage audit",
    "",
    "exactness_reason_count="
    + str(
      len(
        exactness_reasons
      )
    ),
  ]

  for index, reason in enumerate(
    exactness_reasons
  ):
    sentence = (
      render_toda_group_proof_narrative_reason_sentence(
        reason
      )
    )
    lines.extend(
      (
        "",
        "reason_"
        + str(
          index
        )
        + "_sentence="
        + repr(
          sentence
        ),
        "reason_"
        + str(
          index
        )
        + "_conclusion_rule="
        + str(
          (
            reason.conclusion_step.inference_rule.name
            if (
              reason.conclusion_step.inference_rule
              is not None
            )
            else reason.conclusion_step.rule
          )
        ),
      )
    )

  proof_chains = (
    build_toda_group_proof_narrative_proof_chains(
      presentation,
      semantic_sidecar,
      arguments,
    )
  )
  rendered = (
    render_toda_group_proof_narrative_multi_argument_markdown(
      presentation,
      blocks,
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
      current_markdown=rendered,
    )
  )

  records = []
  record(
    records,
    "00_base_multi_argument",
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
    records,
    "01_contribution_insertion",
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
  boundary_filtered_reason_sidecar = type(
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

  lines.extend(
    (
      "",
      "boundary_filtered_exactness_reason_count="
      + str(
        sum(
          1
          for reason
          in boundary_filtered_reason_sidecar.reasons
          if (
            reason.kind
            is TodaGroupProofNarrativeReasonKind
            .EXACTNESS_TO_MAP_PROPERTY
          )
        )
      ),
    )
  )

  rendered = (
    insert_toda_group_proof_narrative_reason_prose(
      rendered,
      boundary_filtered_reason_sidecar,
    )
  )
  record(
    records,
    "02_reason_insertion",
    rendered,
  )

  stages = (
    (
      "03_reference_internal_body",
      lambda text: suppress_toda_group_proof_narrative_reference_internal_body(
        presentation,
        text,
        reference_entries,
        arguments,
        semantic_sidecar,
      ),
    ),
    (
      "04_irrelevant_aggregate_ancestry",
      lambda text: suppress_toda_group_proof_narrative_irrelevant_aggregate_ancestry(
        presentation,
        text,
        reference_entries,
      ),
    ),
    (
      "05_reference_body_duplicates",
      lambda text: suppress_toda_group_proof_narrative_reference_body_duplicates(
        text,
        statement_lines,
      ),
    ),
    (
      "06_reference_body_consumers",
      lambda text: link_toda_group_proof_narrative_reference_body_consumers(
        presentation,
        text,
        reference_entries,
      ),
    ),
    (
      "07_normalize_connectors_a",
      normalize_toda_group_proof_narrative_connectors,
    ),
    (
      "08_local_equation_derivations",
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
      "10_hidden_zero_map",
      lambda text: insert_toda_group_proof_narrative_hidden_zero_map_premises(
        presentation,
        text,
        reference_entries,
      ),
    ),
    (
      "11_map_property_dependencies_a",
      lambda text: insert_toda_group_proof_narrative_map_property_dependencies(
        presentation,
        text,
        reference_entries,
      ),
    ),
    (
      "12_eta_suspension_bridges",
      lambda text: insert_toda_group_proof_narrative_adjacent_eta_suspension_bridges(
        presentation,
        text,
        reference_entries,
      ),
    ),
    (
      "13_merge_exactness_windows",
      lambda text: merge_toda_group_proof_narrative_adjacent_ehp_exactness_windows(
        presentation,
        text,
      ),
    ),
    (
      "14_trim_left_ehp_terms",
      trim_toda_group_proof_narrative_redundant_left_ehp_terms,
    ),
    (
      "15_normalize_connectors_b",
      normalize_toda_group_proof_narrative_connectors,
    ),
    (
      "16_numeric_equalities",
      normalize_toda_group_proof_narrative_repeated_numeric_equalities,
    ),
    (
      "17_unmarked_reference_consumers",
      lambda text: link_toda_group_proof_narrative_unmarked_reference_consumers(
        presentation,
        text,
        reference_entries,
      ),
    ),
    (
      "18_reflexive_equalities",
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
      "20_short_exact_support",
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
      "22_dangling_connectors",
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
      "24_repeated_unique_step_statements",
      lambda text: suppress_toda_group_proof_narrative_repeated_unique_step_statements(
        presentation,
        text,
      ),
    ),
    (
      "25_map_property_dependencies_b",
      lambda text: insert_toda_group_proof_narrative_map_property_dependencies(
        presentation,
        text,
        reference_entries,
      ),
    ),
    (
      "26_injective_image_order_reason",
      lambda text: order_toda_group_proof_narrative_injective_image_order_reason(
        text,
        reason_sidecar,
      ),
    ),
  )

  previous_present = (
    TARGET_FRAGMENT in rendered
  )

  for name, transform in stages:
    rendered = transform(
      rendered
    )
    present = (
      TARGET_FRAGMENT in rendered
    )
    record(
      records,
      name,
      rendered,
    )

    if present != previous_present:
      lines.append(
        ""
      )
      lines.append(
        "TARGET PRESENCE CHANGED at "
        + name
        + ": "
        + str(
          previous_present
        )
        + " -> "
        + str(
          present
        )
      )

    previous_present = present

  lines.extend(
    (
      "",
      "## Stage summaries",
      "",
    )
  )

  for name, present, matches in records:
    lines.append(
      name
      + ": target_present="
      + str(
        present
      )
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
    / "phase159_pi6_3_exactness_reason_stage_audit.txt"
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
