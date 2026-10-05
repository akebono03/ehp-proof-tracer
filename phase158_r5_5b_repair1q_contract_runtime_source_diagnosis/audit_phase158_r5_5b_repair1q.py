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
  _phase158_normalize_public_narrative_contract,
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


def interesting(
  line: str,
) -> bool:
  markers = (
    r"\tag{",
    r"2\nu'",
    r"\eta_{3}\eta_{4}\eta_{5}",
    "(1) と (2) より",
  )

  return any(
    marker in line
    for marker in markers
  )


def main() -> int:
  presentation = build_raw()
  baseline = (
    _phase158_baseline_render_toda_group_proof_narrative_markdown(
      presentation
    )
  )
  normalized = (
    _phase158_normalize_public_narrative_contract(
      presentation,
      baseline,
    )
  )

  runtime_source = inspect.getsource(
    _phase158_normalize_public_narrative_contract
  )
  module_path = Path(
    inspect.getsourcefile(
      renderer_module
    )
    or ""
  ).resolve()

  baseline_lines = baseline.splitlines()
  normalized_lines = normalized.splitlines()

  lines = [
    "=" * 120,
    "Phase 158-R5-5b repair1q - contract runtime source diagnosis",
    "=" * 120,
    "",
    "A. RUNTIME SOURCE LOCATION",
    "-" * 120,
    "module_path="
    + str(
      module_path
    ),
    "function_module="
    + _phase158_normalize_public_narrative_contract.__module__,
    "",
    "B. RUNTIME SOURCE",
    "-" * 120,
    runtime_source,
    "",
    "C. TAG-RELATED SOURCE CHECKS",
    "-" * 120,
    "contains_tag_literal="
    + str(
      r"\tag{" in runtime_source
    ),
    "contains_replace="
    + str(
      ".replace(" in runtime_source
    ),
    "contains_re_sub="
    + str(
      "re.sub" in runtime_source
    ),
    "contains_splitlines="
    + str(
      "splitlines" in runtime_source
    ),
    "",
    "D. BASELINE INTERESTING LINES",
    "-" * 120,
  ]

  for index, line in enumerate(
    baseline_lines
  ):
    if interesting(
      line
    ):
      lines.append(
        f"{index:03d}: {line}"
      )

  lines.extend(
    (
      "",
      "E. NORMALIZED INTERESTING LINES",
      "-" * 120,
    )
  )

  for index, line in enumerate(
    normalized_lines
  ):
    if interesting(
      line
    ):
      lines.append(
        f"{index:03d}: {line}"
      )

  lines.extend(
    (
      "",
      "F. LINE-BY-LINE TAG LOSS",
      "-" * 120,
    )
  )

  tagged_baseline = tuple(
    line
    for line in baseline_lines
    if r"\tag{" in line
  )

  for line in tagged_baseline:
    untagged = line
    start = untagged.find(
      r"\tag{"
    )

    if start >= 0:
      end = untagged.find(
        "}",
        start,
      )

      if end >= 0:
        untagged = (
          untagged[
            :start
          ]
          + untagged[
            end + 1:
          ]
        )

    lines.append(
      "baseline="
      + line
    )
    lines.append(
      "  exact_in_normalized="
      + str(
        line in normalized_lines
      )
    )
    lines.append(
      "  untagged_in_normalized="
      + str(
        untagged in normalized_lines
      )
    )
    lines.append(
      "  untagged="
      + untagged
    )

  lines.extend(
    (
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
    / "contract_runtime_source.txt"
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
