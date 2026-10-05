from __future__ import annotations

from pathlib import Path
import sys


PACKAGE_DIR = Path(__file__).resolve().parent
REPO_ROOT = PACKAGE_DIR.parent

if str(REPO_ROOT) not in sys.path:
  sys.path.insert(
    0,
    str(REPO_ROOT),
  )


def _render_group(
  n: int,
  k: int,
) -> str:
  from toda_calculation_facade import (
    build_standard_toda_report,
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

  report = build_standard_toda_report(
    n=n,
    k=k,
  )
  group_result = (
    report.candidates[0]
    .source_candidate
    .group_result
  )
  replay = (
    build_toda_group_result_proof_replay(
      group_result,
      max_depth=2,
    )
  )
  presentation = (
    build_toda_group_proof_presentation(
      replay
    )
  )

  return (
    render_toda_group_proof_narrative_markdown(
      presentation
    )
  )


def main() -> int:
  valid = 0
  violations = []
  exceptions = []

  for n in range(
    2,
    16,
  ):
    for k in range(
      0,
      8,
    ):
      label = f"pi_{n + k}^{n}"

      try:
        rendered = _render_group(
          n,
          k,
        )
        lines = rendered.splitlines()
        nonempty = [
          line.strip()
          for line in lines
          if line.strip()
        ]

        target = lines.index(
          "## 証明対象"
        )
        reference = lines.index(
          "## 使用する結果"
        )
        separator = lines.index(
          "---"
        )
        proof = lines.index(
          "## 証明"
        )

        current_valid = (
          target
          < reference
          < separator
          < proof
          and nonempty[-1] == "□"
        )

        if current_valid:
          valid += 1
        else:
          violations.append(
            label
          )

      except Exception as exc:
        exceptions.append(
          (
            label,
            type(exc).__name__,
            str(exc),
          )
        )

  pi15_8 = _render_group(
    8,
    7,
  )
  canonical_formula = (
    r"\left(α, \beta\right) \mapsto "
    r"Eα + \sigma_{8}\beta"
    in pi15_8
  )
  generator_transport = (
    r"\sigma' \longmapsto E\sigma'"
    in pi15_8
    and r"\iota_{15} \longmapsto \sigma_{8}"
    in pi15_8
  )

  summary = "\n".join(
    (
      "=" * 78,
      (
        "Phase 158-R2 repair2 - "
        "Restore Pre-R2 Baseline + Outer Wrapper"
      ),
      "=" * 78,
      "scope: n=2..15, k=0..7, depth=2",
      f"valid contract: {valid}",
      f"violations: {len(violations)}",
      f"exceptions: {len(exceptions)}",
      (
        "pi15_8 canonical Proposition 4.4 formula: "
        + str(canonical_formula)
      ),
      (
        "pi15_8 generator transport preserved: "
        + str(generator_transport)
      ),
      "=" * 78,
    )
  )

  print(summary)

  output_dir = PACKAGE_DIR / "output"
  output_dir.mkdir(
    parents=True,
    exist_ok=True,
  )
  (
    output_dir
    / "phase158_r2_repair2_summary.txt"
  ).write_text(
    summary + "\n",
    encoding="utf-8-sig",
  )

  return (
    0
    if (
      valid == 112
      and not violations
      and not exceptions
      and canonical_formula
      and generator_transport
    )
    else 1
  )


if __name__ == "__main__":
  raise SystemExit(main())
