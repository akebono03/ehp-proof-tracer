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


from toda_calculation_facade import (
  build_standard_toda_report,
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
from toda_group_proof_narrative_contribution_ordering import (
  build_toda_group_proof_narrative_ordered_contributions,
)
from toda_group_proof_narrative_contribution_renderer import (
  _insert_toda_group_proof_narrative_argument_contributions,
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
  _toda_group_proof_narrative_reference_owned_step_ids,
  _toda_group_proof_narrative_reference_statement_lines_by_number,
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
from toda_group_proof_narrative_semantics import (
  build_toda_group_proof_narrative_semantic_closure_presentation,
  build_toda_group_proof_narrative_semantic_sidecar,
)
from toda_group_proof_presentation import (
  build_toda_group_proof_presentation,
)
from toda_group_result_proof_replay import (
  build_toda_group_result_proof_replay,
)


ROOT_FRAGMENT = (
  r"\pi_{4}^{3} = "
  r"\mathbb{Z}/2\{\eta_{3}\}"
)


def build_data():
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
  presentation = (
    build_toda_group_proof_narrative_semantic_closure_presentation(
      raw_presentation
    )
  )
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
  proof_chains = (
    build_toda_group_proof_narrative_proof_chains(
      presentation,
      semantic_sidecar,
      arguments,
    )
  )
  base_markdown = (
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
      current_markdown=base_markdown,
    )
  )

  return (
    presentation,
    semantic_sidecar,
    blocks,
    arguments,
    base_markdown,
    ordered_contributions,
  )


def count_root(
  markdown: str,
) -> int:
  return markdown.count(
    ROOT_FRAGMENT
  )


def root_paragraphs(
  markdown: str,
) -> tuple[
  str,
  ...,
]:
  return tuple(
    paragraph
    for paragraph in markdown.split(
      "\n\n"
    )
    if ROOT_FRAGMENT in paragraph
  )


def record(
  records,
  name: str,
  markdown: str,
) -> None:
  records.append(
    (
      name,
      count_root(
        markdown
      ),
      root_paragraphs(
        markdown
      ),
    )
  )


def main() -> int:
  (
    presentation,
    semantic_sidecar,
    blocks,
    arguments,
    rendered,
    ordered_contributions,
  ) = build_data()

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
    "01_after_contribution_insertion",
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
  statement_lines_by_reference_number = (
    _toda_group_proof_narrative_reference_statement_lines_by_number(
      presentation,
      reference_entries,
    )
  )
  (
    reference_entries,
    statement_lines_by_reference_number,
  ) = (
    exclude_toda_group_proof_narrative_root_reference(
      reference_entries,
      statement_lines_by_reference_number,
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

  rendered = (
    insert_toda_group_proof_narrative_reason_prose(
      rendered,
      boundary_filtered_reason_sidecar,
    )
  )
  record(
    records,
    "02_after_reason_prose",
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
        statement_lines_by_reference_number,
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
        statement_lines_by_reference_number,
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
        statement_lines_by_reference_number,
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

  for name, transform in stages:
    rendered = transform(
      rendered
    )
    record(
      records,
      name,
      rendered,
    )

  lines = [
    "# Phase 159 pi4_3 semantic duplication stage audit",
    "",
    "root_fragment: "
    + ROOT_FRAGMENT,
    "",
  ]

  previous_count = None

  for name, count, paragraphs in records:
    marker = ""

    if (
      previous_count is not None
      and count != previous_count
    ):
      marker = (
        "  <-- CHANGED FROM "
        + str(
          previous_count
        )
      )

    lines.append(
      name
      + ": "
      + str(
        count
      )
      + marker
    )

    for paragraph in paragraphs:
      lines.append(
        "  ROOT: "
        + repr(
          paragraph
        )
      )

    previous_count = count

  lines.extend(
    (
      "",
      "## Final staged body",
      "",
      rendered,
      "",
    )
  )

  report = "\n".join(
    lines
  )

  output_path = (
    Path(__file__).resolve().parent
    / "phase159_pi4_3_semantic_duplication_stage_audit.txt"
  )
  output_path.write_text(
    report,
    encoding="utf-8",
  )

  print(
    report
  )

  return 0


if __name__ == "__main__":
  raise SystemExit(
    main()
  )
