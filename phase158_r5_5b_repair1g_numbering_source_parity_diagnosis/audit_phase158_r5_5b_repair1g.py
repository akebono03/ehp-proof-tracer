from __future__ import annotations

import hashlib
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

import toda_group_proof_narrative_equation_numbering as numbering_module
import toda_group_proof_narrative_argument_multi_renderer as multi_renderer
from toda_group_proof_narrative_equation_numbering import (
  _numbered_step_line,
  number_toda_group_proof_narrative_equations,
)


def sha256_text(
  text: str,
) -> str:
  return hashlib.sha256(
    text.encode(
      "utf-8"
    )
  ).hexdigest()


def main() -> int:
  numbering_source = inspect.getsource(
    number_toda_group_proof_narrative_equations
  )
  numbered_line_source = inspect.getsource(
    _numbered_step_line
  )

  module_path = Path(
    inspect.getsourcefile(
      numbering_module
    )
    or ""
  ).resolve()

  multi_numbering_object = (
    multi_renderer
    .number_toda_group_proof_narrative_equations
  )

  lines = [
    "=" * 100,
    "Phase 158-R5-5b repair1g - numbering source parity diagnosis",
    "=" * 100,
    "",
    "A. MODULE / FUNCTION IDENTITY",
    "-" * 100,
    "numbering_module_path="
    + str(
      module_path
    ),
    "numbering_function_module="
    + str(
      number_toda_group_proof_narrative_equations.__module__
    ),
    "multi_renderer_alias_module="
    + str(
      multi_numbering_object.__module__
    ),
    "same_function_object="
    + str(
      (
        multi_numbering_object
        is number_toda_group_proof_narrative_equations
      )
    ),
    "numbering_source_sha256="
    + sha256_text(
      numbering_source
    ),
    "numbered_line_source_sha256="
    + sha256_text(
      numbered_line_source
    ),
    "",
    "B. RUNTIME SOURCE: number_toda_group_proof_narrative_equations",
    "-" * 100,
    numbering_source,
    "",
    "C. RUNTIME SOURCE: _numbered_step_line",
    "-" * 100,
    numbered_line_source,
    "",
    "D. MODULE FILE TEXT AROUND NUMBERING FUNCTION",
    "-" * 100,
  ]

  module_text = module_path.read_text(
    encoding="utf-8"
  )

  marker = (
    "def number_toda_group_proof_narrative_equations("
  )
  start = module_text.find(
    marker
  )

  if start < 0:
    lines.append(
      "FUNCTION MARKER NOT FOUND IN MODULE FILE"
    )
  else:
    next_function = module_text.find(
      "\ndef ",
      start + len(
        marker
      ),
    )

    if next_function < 0:
      end = len(
        module_text
      )
    else:
      end = next_function + 1

    lines.append(
      module_text[
        start:end
      ]
    )

  lines.extend(
    (
      "",
      "E. KEY SOURCE CHECKS",
      "-" * 100,
      "contains_plain_by_id="
      + str(
        "plain_by_id" in numbering_source
      ),
      "contains_tagged_by_id="
      + str(
        "tagged_by_id" in numbering_source
      ),
      "contains_matching_id="
      + str(
        "matching_id" in numbering_source
      ),
      "contains_lines_index_assignment="
      + str(
        "lines[index] = tagged_by_id[matching_id]"
        in numbering_source
      ),
      "contains_duplicate_guard="
      + str(
        (
          "count(" in numbering_source
          or "ambiguous" in numbering_source
          or "duplicate" in numbering_source
        )
      ),
      "",
      "=" * 100,
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

  output_path = (
    output_dir
    / "numbering_source_parity.txt"
  )
  output_path.write_text(
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
