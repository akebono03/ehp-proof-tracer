from __future__ import annotations

import sys
from pathlib import Path

REPOSITORY_ROOT = Path(__file__).resolve().parents[1]

if str(REPOSITORY_ROOT) not in sys.path:
  sys.path.insert(
    0,
    str(
      REPOSITORY_ROOT
    ),
  )

import toda_group_proof_narrative_contribution_renderer as contribution_module
from tests.test_phase143_19_method_evidence import (
  _method_evidence_data,
)
from toda_calculation_facade import (
  build_standard_toda_report,
)
from toda_group_proof_narrative_argument_multi_renderer import (
  render_toda_group_proof_narrative_multi_argument_markdown,
)
from toda_group_proof_narrative_contribution_renderer import (
  render_toda_group_proof_narrative_multi_argument_with_contributions_markdown,
)
from toda_group_proof_narrative_renderer import (
  render_toda_group_proof_narrative_markdown,
)
from toda_group_proof_presentation import (
  build_toda_group_proof_presentation,
)
from toda_group_result_proof_replay import (
  build_toda_group_result_proof_replay,
)
from web_group_proof import (
  build_standard_web_group_proof_view,
)


PATTERNS = (
  (
    "eq1_tagged",
    r"$2\nu' = \eta_{3}\eta_{4}\eta_{5}\tag{1}$",
  ),
  (
    "eq1_plain",
    r"$2\nu' = \eta_{3}\eta_{4}\eta_{5}$",
  ),
  (
    "eq2_tagged",
    r"$\eta_{3}\eta_{4}\eta_{5} = \eta_{3}^{3}\tag{2}$",
  ),
  (
    "eq2_plain",
    r"$\eta_{3}\eta_{4}\eta_{5} = \eta_{3}^{3}$",
  ),
  (
    "connector",
    "(1) と (2) より,",
  ),
  (
    "eq3_tagged",
    r"$2\nu' = \eta_{3}^{3}\tag{3}$",
  ),
  (
    "eq3_plain",
    r"$2\nu' = \eta_{3}^{3}$",
  ),
)


TRANSFORM_NAMES = (
  "insert_toda_group_proof_narrative_reason_prose",
  "suppress_toda_group_proof_narrative_reference_internal_body",
  "suppress_toda_group_proof_narrative_irrelevant_aggregate_ancestry",
  "suppress_toda_group_proof_narrative_reference_body_duplicates",
  "link_toda_group_proof_narrative_reference_body_consumers",
  "normalize_toda_group_proof_narrative_connectors",
  "order_toda_group_proof_narrative_local_equation_derivations",
  "order_toda_group_proof_narrative_order_support",
  "insert_toda_group_proof_narrative_hidden_zero_map_premises",
  "insert_toda_group_proof_narrative_map_property_dependencies",
  "insert_toda_group_proof_narrative_adjacent_eta_suspension_bridges",
  "merge_toda_group_proof_narrative_adjacent_ehp_exactness_windows",
  "trim_toda_group_proof_narrative_redundant_left_ehp_terms",
  "normalize_toda_group_proof_narrative_repeated_numeric_equalities",
  "link_toda_group_proof_narrative_unmarked_reference_consumers",
  "suppress_toda_group_proof_narrative_reflexive_equalities",
  "order_toda_group_proof_narrative_surjectivity_support",
  "order_toda_group_proof_narrative_short_exact_support",
  "suppress_toda_group_proof_narrative_repeated_reference_restatements",
  "suppress_toda_group_proof_narrative_dangling_connectors",
  "order_toda_group_proof_narrative_visible_relation_dependencies",
  "suppress_toda_group_proof_narrative_repeated_unique_step_statements",
  "order_toda_group_proof_narrative_injective_image_order_reason",
)


def pattern_state(
  text: str,
) -> tuple[
  tuple[
    str,
    int,
  ],
  ...,
]:
  return tuple(
    (
      label,
      text.count(
        pattern
      ),
    )
    for label, pattern in PATTERNS
  )


def state_text(
  text: str,
) -> str:
  return " ".join(
    label
    + "="
    + str(
      count
    )
    for label, count in pattern_state(
      text
    )
  )


def extract_string(
  value,
) -> str | None:
  if isinstance(
    value,
    str,
  ):
    return value

  if isinstance(
    value,
    tuple,
  ):
    for item in reversed(
      value
    ):
      if isinstance(
        item,
        str,
      ):
        return item

  return None


def web_text() -> str:
  view = build_standard_web_group_proof_view(
    3,
    3,
    max_depth=2,
    mode="narrative",
  )
  parts = []

  for line in view.rendered_lines:
    if line.segments:
      parts.append(
        "".join(
          segment.value
          for segment in line.segments
        )
      )
    else:
      parts.append(
        line.prefix
        + (
          ""
          if line.statement_latex is None
          else line.statement_latex
        )
        + line.suffix
      )

  return "\n".join(
    parts
  )


def raw_presentation():
  report = build_standard_toda_report(
    n=3,
    k=3,
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
  return build_toda_group_proof_presentation(
    replay
  )


def main() -> int:
  (
    presentation,
    blocks,
    sidecar,
    arguments,
  ) = _method_evidence_data(
    3,
    3,
  )

  base_markdown = (
    render_toda_group_proof_narrative_multi_argument_markdown(
      presentation,
      blocks,
      sidecar,
      arguments,
    )
  )

  stage_records = []
  originals = {}

  for name in TRANSFORM_NAMES:
    original = getattr(
      contribution_module,
      name,
      None,
    )

    if original is None:
      stage_records.append(
        (
          name,
          "MISSING",
          "",
          "",
        )
      )
      continue

    originals[
      name
    ] = original

    def make_wrapper(
      transform_name,
      transform,
    ):
      def wrapper(
        *args,
        **kwargs,
      ):
        before = next(
          (
            value
            for value in args
            if isinstance(
              value,
              str,
            )
          ),
          None,
        )
        result = transform(
          *args,
          **kwargs,
        )
        after = extract_string(
          result
        )

        stage_records.append(
          (
            transform_name,
            "CALLED",
            (
              ""
              if before is None
              else state_text(
                before
              )
            ),
            (
              ""
              if after is None
              else state_text(
                after
              )
            ),
          )
        )

        return result

      return wrapper

    setattr(
      contribution_module,
      name,
      make_wrapper(
        name,
        original,
      ),
    )

  try:
    contribution_output = (
      render_toda_group_proof_narrative_multi_argument_with_contributions_markdown(
        presentation,
        blocks,
        sidecar,
        arguments,
      )
    )
  finally:
    for name, original in originals.items():
      setattr(
        contribution_module,
        name,
        original,
      )

  raw = raw_presentation()
  public_output = render_toda_group_proof_narrative_markdown(
    raw
  )
  web_output = web_text()

  lines = [
    "=" * 120,
    "Phase 158-R5-5b repair1n - public pipeline chain diagnosis",
    "=" * 120,
    "",
    "A. SURFACE SUMMARY",
    "-" * 120,
    "base_multi:      "
    + state_text(
      base_markdown
    ),
    "contribution:    "
    + state_text(
      contribution_output
    ),
    "public_markdown: "
    + state_text(
      public_output
    ),
    "web_text:        "
    + state_text(
      web_output
    ),
    "",
    "B. CONTRIBUTION TRANSFORM STAGES",
    "-" * 120,
  ]

  previous_after = None

  for name, status, before, after in stage_records:
    changed = (
      None
      if not before
      or not after
      else before != after
    )
    lines.append(
      (
        name
        + " status="
        + status
        + " changed="
        + str(
          changed
        )
      )
    )

    if before:
      lines.append(
        "  before: "
        + before
      )

    if after:
      lines.append(
        "  after:  "
        + after
      )

    previous_after = after or previous_after

  lines.extend(
    (
      "",
      "C. BASE MULTI-ARGUMENT OUTPUT",
      "-" * 120,
      base_markdown,
      "",
      "D. CONTRIBUTION OUTPUT",
      "-" * 120,
      contribution_output,
      "",
      "E. PUBLIC MARKDOWN OUTPUT",
      "-" * 120,
      public_output,
      "",
      "F. WEB TEXT",
      "-" * 120,
      web_output,
      "",
      "=" * 120,
      "Production code changes: none",
      "Repository-wide pytest: not run",
      "=" * 120,
    )
  )

  output_dir = (
    Path(__file__).resolve().parent
    / "audit_output"
  )
  output_dir.mkdir(
    parents=True,
    exist_ok=True,
  )
  (
    output_dir
    / "pi6_public_pipeline_chain.txt"
  ).write_text(
    "\n".join(
      lines
    )
    + "\n",
    encoding="utf-8",
    newline="\n",
  )

  print(
    "\n".join(
      lines
    )
  )

  return 0


if __name__ == "__main__":
  raise SystemExit(
    main()
  )
