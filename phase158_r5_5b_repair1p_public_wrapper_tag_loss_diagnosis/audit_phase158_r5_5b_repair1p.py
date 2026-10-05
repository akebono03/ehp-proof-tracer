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

import toda_group_proof_narrative_renderer as renderer_module
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
from toda_group_proof_narrative_contribution_renderer import (
  render_toda_group_proof_narrative_multi_argument_with_contributions_markdown,
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


def state(
  text: str,
) -> str:
  return " ".join(
    label
    + "="
    + str(
      text.count(
        pattern
      )
    )
    for label, pattern in PATTERNS
  )


def build_data():
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
  raw = build_toda_group_proof_presentation(
    replay
  )
  presentation = (
    build_toda_group_proof_narrative_semantic_closure_presentation(
      raw
    )
  )
  sidecar = (
    build_toda_group_proof_narrative_semantic_sidecar(
      presentation
    )
  )
  blocks = (
    build_toda_group_proof_narrative_blocks(
      presentation,
      semantic_sidecar=sidecar,
    )
  )
  arguments = (
    build_toda_group_proof_narrative_arguments(
      presentation,
      blocks,
      semantic_sidecar=sidecar,
    )
  )

  return (
    raw,
    presentation,
    sidecar,
    blocks,
    arguments,
  )


def main() -> int:
  (
    raw,
    presentation,
    sidecar,
    blocks,
    arguments,
  ) = build_data()

  base = (
    render_toda_group_proof_narrative_multi_argument_markdown(
      presentation,
      blocks,
      sidecar,
      arguments,
    )
  )
  contribution = (
    render_toda_group_proof_narrative_multi_argument_with_contributions_markdown(
      presentation,
      blocks,
      sidecar,
      arguments,
    )
  )

  calls = []
  original_suppress = (
    renderer_module
    .suppress_toda_group_proof_narrative_reference_body_restatements
  )

  def capture_suppress(
    body_markdown,
    statement_lines_by_reference_number,
  ):
    before = body_markdown
    result = original_suppress(
      body_markdown,
      statement_lines_by_reference_number,
    )
    calls.append(
      (
        state(
          before
        ),
        state(
          result
        ),
        before,
        result,
      )
    )
    return result

  renderer_module.suppress_toda_group_proof_narrative_reference_body_restatements = (
    capture_suppress
  )

  try:
    wrapped = (
      renderer_module
      ._wrap_phase150_rc4_generic_public_narrative(
        presentation,
        contribution,
      )
    )
  finally:
    renderer_module.suppress_toda_group_proof_narrative_reference_body_restatements = (
      original_suppress
    )

  finalized = (
    renderer_module
    ._finalize_toda_group_proof_narrative_markdown(
      wrapped
    )
  )
  normalized = (
    renderer_module
    ._phase158_normalize_public_narrative_contract(
      presentation,
      finalized,
    )
  )

  lines = [
    "=" * 120,
    "Phase 158-R5-5b repair1p - public wrapper tag-loss diagnosis",
    "=" * 120,
    "",
    "A. SURFACE SUMMARY",
    "-" * 120,
    "base_multi:   "
    + state(
      base
    ),
    "contribution: "
    + state(
      contribution
    ),
    "wrapped:      "
    + state(
      wrapped
    ),
    "finalized:    "
    + state(
      finalized
    ),
    "normalized:   "
    + state(
      normalized
    ),
    "",
    "B. REFERENCE-BODY RESTATEMENT SUPPRESSION CALLS",
    "-" * 120,
  ]

  for index, (
    before_state,
    after_state,
    before,
    after,
  ) in enumerate(
    calls
  ):
    lines.append(
      f"call={index}"
    )
    lines.append(
      "  before: "
      + before_state
    )
    lines.append(
      "  after:  "
      + after_state
    )
    lines.append(
      "  changed="
      + str(
        before_state != after_state
      )
    )
    lines.append(
      ""
    )
    lines.append(
      "  BEFORE TEXT"
    )
    lines.append(
      "  "
      + "\n  ".join(
        before.splitlines()
      )
    )
    lines.append(
      ""
    )
    lines.append(
      "  AFTER TEXT"
    )
    lines.append(
      "  "
      + "\n  ".join(
        after.splitlines()
      )
    )
    lines.append(
      ""
    )

  lines.extend(
    (
      "C. WRAPPED OUTPUT",
      "-" * 120,
      wrapped,
      "",
      "D. FINALIZED OUTPUT",
      "-" * 120,
      finalized,
      "",
      "E. NORMALIZED OUTPUT",
      "-" * 120,
      normalized,
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
    / "pi6_public_wrapper_tag_loss.txt"
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
