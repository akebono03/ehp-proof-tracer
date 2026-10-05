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

import toda_group_proof_narrative_renderer as renderer_module
from toda_calculation_facade import (
  build_standard_toda_report,
)
from toda_group_proof_narrative_renderer import (
  _phase158_baseline_render_toda_group_proof_narrative_markdown,
  _phase158_normalize_public_equation_numbers,
)
from toda_group_proof_presentation import (
  build_toda_group_proof_presentation,
)
from toda_group_result_proof_replay import (
  build_toda_group_result_proof_replay,
)


def build_raw():
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


def proof_body_lines(
  rendered: str,
) -> list[str]:
  lines = rendered.rstrip().splitlines()
  proof_header = "## 証明"

  if proof_header not in lines:
    return lines

  proof_index = lines.index(
    proof_header
  )
  result = lines[
    proof_index + 1:
  ]

  while (
    result
    and not result[0].strip()
  ):
    result.pop(0)

  return result


def main() -> int:
  presentation = build_raw()
  baseline = (
    _phase158_baseline_render_toda_group_proof_narrative_markdown(
      presentation
    )
  )
  proof_body = proof_body_lines(
    baseline
  )
  normalized = (
    _phase158_normalize_public_equation_numbers(
      proof_body
    )
  )

  helper_source = inspect.getsource(
    _phase158_normalize_public_equation_numbers
  )
  module_path = Path(
    inspect.getsourcefile(
      renderer_module
    )
    or ""
  ).resolve()

  lines = [
    "=" * 120,
    "Phase 158-R5-5b repair1r - equation-number helper source diagnosis",
    "=" * 120,
    "",
    "A. SOURCE LOCATION",
    "-" * 120,
    "module_path="
    + str(
      module_path
    ),
    "helper_module="
    + _phase158_normalize_public_equation_numbers.__module__,
    "",
    "B. RUNTIME HELPER SOURCE",
    "-" * 120,
    helper_source,
    "",
    "C. SOURCE CHECKS",
    "-" * 120,
    "contains_tag="
    + str(
      r"\tag{" in helper_source
    ),
    "contains_regex="
    + str(
      (
        "re." in helper_source
        or "regex" in helper_source.lower()
      )
    ),
    "contains_replace="
    + str(
      ".replace(" in helper_source
    ),
    "contains_connector="
    + str(
      (
        "(1)" in helper_source
        or "より" in helper_source
        or "connector" in helper_source.lower()
      )
    ),
    "",
    "D. BEFORE / AFTER",
    "-" * 120,
  ]

  max_len = max(
    len(
      proof_body
    ),
    len(
      normalized
    ),
  )

  for index in range(
    max_len
  ):
    before = (
      proof_body[
        index
      ]
      if index < len(
        proof_body
      )
      else "<MISSING>"
    )
    after = (
      normalized[
        index
      ]
      if index < len(
        normalized
      )
      else "<MISSING>"
    )

    if (
      before == after
      and r"\tag{" not in before
      and "(1)" not in before
      and "(2)" not in before
      and "(3)" not in before
    ):
      continue

    lines.append(
      f"{index:03d}"
    )
    lines.append(
      "  before="
      + before
    )
    lines.append(
      "  after ="
      + after
    )
    lines.append(
      "  changed="
      + str(
        before != after
      )
    )

  lines.extend(
    (
      "",
      "E. FULL INPUT",
      "-" * 120,
      "\n".join(
        proof_body
      ),
      "",
      "F. FULL OUTPUT",
      "-" * 120,
      "\n".join(
        normalized
      ),
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
    / "equation_number_helper_source.txt"
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
