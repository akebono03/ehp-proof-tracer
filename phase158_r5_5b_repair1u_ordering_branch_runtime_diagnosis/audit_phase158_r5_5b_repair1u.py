from __future__ import annotations

import inspect
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

import toda_group_proof_narrative_argument_multi_renderer as multi_module
from toda_group_proof_narrative_argument_multi_renderer import (
  render_toda_group_proof_narrative_multi_argument_markdown,
)
from toda_group_proof_narrative_equation_numbering import (
  number_toda_group_proof_narrative_equations,
)


def extract_relevant_slice(
  source: str,
) -> str:
  anchors = (
    "local_body_blocks = (",
    "local_body_block_ids = {",
    "evidence_block_ids = {",
  )

  start_candidates = tuple(
    source.find(
      anchor
    )
    for anchor in anchors
    if source.find(
      anchor
    ) >= 0
  )

  if not start_candidates:
    return source

  start = min(
    start_candidates
  )
  end = source.find(
    "context_hidden_step_ids =",
    start,
  )

  if end < 0:
    return source[
      start:
    ]

  return source[
    start:end
  ]


def main() -> int:
  multi_source = inspect.getsource(
    render_toda_group_proof_narrative_multi_argument_markdown
  )
  numbering_source = inspect.getsource(
    number_toda_group_proof_narrative_equations
  )

  lines = [
    "=" * 120,
    "Phase 158-R5-5b repair1u - ordering branch runtime diagnosis",
    "=" * 120,
    "",
    "A. RUNTIME MODULE PATH",
    "-" * 120,
    "multi_module="
    + str(
      Path(
        inspect.getsourcefile(
          multi_module
        )
        or ""
      ).resolve()
    ),
    "",
    "B. MULTI-RENDERER LOCAL-BODY BRANCH",
    "-" * 120,
    extract_relevant_slice(
      multi_source
    ),
    "",
    "C. BRANCH CHECKS",
    "-" * 120,
    "contains_TARGET_branch="
    + str(
      "role is TARGET" in multi_source
      or ".TARGET" in extract_relevant_slice(
        multi_source
      )
    ),
    "contains_missing_evidence="
    + str(
      "missing_evidence" in multi_source
    ),
    "contains_global_blocks_merge="
    + str(
      "for block in blocks" in extract_relevant_slice(
        multi_source
      )
    ),
    "",
    "D. NUMBERING CHECKS",
    "-" * 120,
    "numbers_target_explicitly="
    + str(
      (
        "ordered_steps.append(target_step)"
        in numbering_source
        or "tagged_by_id" in numbering_source
      )
    ),
    "source_only_runtime="
    + str(
      (
        "ordered_source_ids" in numbering_source
        and "target_tagged" not in numbering_source
      )
    ),
    "",
    "E. FULL NUMBERING SOURCE",
    "-" * 120,
    numbering_source,
    "",
    "=" * 120,
    "Production code changes: none",
    "Repository-wide pytest: not run",
    "=" * 120,
  ]

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
    / "ordering_branch_runtime.txt"
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
