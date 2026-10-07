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
  order_toda_group_proof_narrative_local_equation_derivations,
  order_toda_group_proof_narrative_order_support,
  order_toda_group_proof_narrative_short_exact_support,
  order_toda_group_proof_narrative_surjectivity_support,
  suppress_toda_group_proof_narrative_irrelevant_aggregate_ancestry,
  suppress_toda_group_proof_narrative_reference_body_duplicates,
  suppress_toda_group_proof_narrative_reference_internal_body,
  suppress_toda_group_proof_narrative_reflexive_equalities,
  suppress_toda_group_proof_narrative_repeated_reference_restatements,
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
CONNECTOR = "以上より,"


def paragraph_summary(
  markdown: str,
) -> str:
  paragraphs = markdown.split(
    "\n\n"
  )

  connector_indices = tuple(
    index
    for index, paragraph in enumerate(
      paragraphs
    )
    if CONNECTOR in paragraph
  )
  root_indices = tuple(
    index
    for index, paragraph in enumerate(
      paragraphs
    )
    if ROOT_FRAGMENT in paragraph
  )

  selected_indices = sorted(
    set(
      connector_indices
      + root_indices
      + tuple(
        index
        for source_index in (
          connector_indices
          + root_indices
        )
        for index in (
          source_index - 1,
          source_index,
          source_index + 1,
        )
        if 0 <= index < len(
          paragraphs
        )
      )
    )
  )

  lines = [
    "connector_indices="
    + repr(
      connector_indices
    ),
    "root_indices="
    + repr(
      root_indices
    ),
  ]

  for index in selected_indices:
    lines.append(
      "  P"
      + str(
        index
      )
      + ": "
      + repr(
        paragraphs[
          index
        ]
      )
    )

  return "\n".join(
    lines
  )


def record(
  records,
  name: str,
  markdown: str,
) -> None:
  records.append(
    (
      name,
      paragraph_summary(
        markdown
      ),
    )
  )


def main() -> int:
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
  raw_presentation = build_toda_group_proof_presentation(
    replay
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
  blocks = build_toda_group_proof_narrative_blocks(
    presentation,
    semantic_sidecar=semantic_sidecar,
  )
  arguments = build_toda_group_proof_narrative_arguments(
    presentation,
    blocks,
    semantic_sidecar=semantic_sidecar,
  )
  proof_chains = build_toda_group_proof_narrative_proof_chains(
    presentation,
    semantic_sidecar,
    arguments,
  )

  rendered = render_toda_group_proof_narrative_multi_argument_markdown(
    presentation,
    blocks,
    semantic_sidecar,
    arguments,
  )

  records = []
  record(
    records,
    "00_base_multi_argument",
    rendered,
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
  rendered = _insert_toda_group_proof_narrative_argument_contributions(
    presentation,
    rendered,
    blocks,
    arguments,
    ordered_contributions,
  )
  record(
    records,
    "01_contribution_insertion",
    rendered,
  )

  reference_entries = build_toda_group_proof_narrative_reference_entries(
    presentation
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
  reference_entries, statement_lines = (
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
  reason_sidecar = build_toda_group_proof_narrative_reason_sidecar(
    presentation,
    semantic_sidecar,
  )
  filtered_reason_sidecar = type(
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

  stages = (
    (
      "02_reason_prose",
      lambda text: insert_toda_group_proof_narrative_reason_prose(
        text,
        filtered_reason_sidecar,
      ),
    ),
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
    "# Phase 159 pi4_3 connector position stage audit",
    "",
  ]

  for name, summary in records:
    lines.extend(
      (
        "## " + name,
        "",
        summary,
        "",
      )
    )

  output = "\n".join(
    lines
  )
  output_path = (
    Path(__file__).resolve().parent
    / "phase159_pi4_3_connector_position_stage_audit.txt"
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
