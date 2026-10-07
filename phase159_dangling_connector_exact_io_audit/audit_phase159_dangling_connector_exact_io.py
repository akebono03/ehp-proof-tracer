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
  suppress_toda_group_proof_narrative_dangling_connectors,
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


def build_stage21(
  n: int,
  k: int,
):
  report = build_standard_toda_report(
    n=n,
    k=k,
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

  rendered = insert_toda_group_proof_narrative_reason_prose(
    rendered,
    filtered_reason_sidecar,
  )
  rendered = suppress_toda_group_proof_narrative_reference_internal_body(
    presentation,
    rendered,
    reference_entries,
    arguments,
    semantic_sidecar,
  )
  rendered = suppress_toda_group_proof_narrative_irrelevant_aggregate_ancestry(
    presentation,
    rendered,
    reference_entries,
  )
  rendered = suppress_toda_group_proof_narrative_reference_body_duplicates(
    rendered,
    statement_lines,
  )
  rendered = link_toda_group_proof_narrative_reference_body_consumers(
    presentation,
    rendered,
    reference_entries,
  )
  rendered = normalize_toda_group_proof_narrative_connectors(
    rendered
  )
  rendered = order_toda_group_proof_narrative_local_equation_derivations(
    rendered
  )
  rendered = order_toda_group_proof_narrative_order_support(
    presentation,
    rendered,
  )
  rendered = insert_toda_group_proof_narrative_hidden_zero_map_premises(
    presentation,
    rendered,
    reference_entries,
  )
  rendered = insert_toda_group_proof_narrative_map_property_dependencies(
    presentation,
    rendered,
    reference_entries,
  )
  rendered = insert_toda_group_proof_narrative_adjacent_eta_suspension_bridges(
    presentation,
    rendered,
    reference_entries,
  )
  rendered = merge_toda_group_proof_narrative_adjacent_ehp_exactness_windows(
    presentation,
    rendered,
  )
  rendered = trim_toda_group_proof_narrative_redundant_left_ehp_terms(
    rendered
  )
  rendered = normalize_toda_group_proof_narrative_connectors(
    rendered
  )
  rendered = normalize_toda_group_proof_narrative_repeated_numeric_equalities(
    rendered
  )
  rendered = link_toda_group_proof_narrative_unmarked_reference_consumers(
    presentation,
    rendered,
    reference_entries,
  )
  rendered = suppress_toda_group_proof_narrative_reflexive_equalities(
    presentation,
    rendered,
  )
  rendered = order_toda_group_proof_narrative_surjectivity_support(
    presentation,
    rendered,
    reference_entries,
    statement_lines,
  )
  rendered = order_toda_group_proof_narrative_short_exact_support(
    presentation,
    rendered,
  )
  rendered = suppress_toda_group_proof_narrative_repeated_reference_restatements(
    rendered,
    statement_lines,
  )

  return rendered


def dump_paragraphs(
  markdown: str,
) -> str:
  lines = []

  for index, paragraph in enumerate(
    markdown.split(
      "\n\n"
    )
  ):
    lines.append(
      "P"
      + str(
        index
      )
      + ": "
      + repr(
        paragraph
      )
    )

  return "\n".join(
    lines
  )


def audit_target(
  label: str,
  n: int,
  k: int,
) -> str:
  before = build_stage21(
    n,
    k,
  )
  after = suppress_toda_group_proof_narrative_dangling_connectors(
    before
  )

  return "\n".join(
    (
      "============================================================",
      label,
      "============================================================",
      "",
      "BEFORE connector count: "
      + str(
        before.count(
          "以上より,"
        )
      ),
      "AFTER connector count: "
      + str(
        after.count(
          "以上より,"
        )
      ),
      "",
      "## BEFORE paragraphs",
      "",
      dump_paragraphs(
        before
      ),
      "",
      "## AFTER paragraphs",
      "",
      dump_paragraphs(
        after
      ),
      "",
      "## BEFORE raw",
      "",
      before,
      "",
      "## AFTER raw",
      "",
      after,
      "",
    )
  )


def main() -> int:
  report = "\n".join(
    (
      "# Phase 159 dangling connector exact I/O audit",
      "",
      audit_target(
        "pi_4^3",
        3,
        1,
      ),
      audit_target(
        "pi_6^3",
        3,
        3,
      ),
    )
  )

  output_path = (
    Path(__file__).resolve().parent
    / "phase159_dangling_connector_exact_io_audit.txt"
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
