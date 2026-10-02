from __future__ import annotations

import argparse
import json
import re
from pathlib import Path

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


DERIVATION_TOKENS = (
  "これらから",
  "このことから",
  "したがって",
  "従って",
  "よって",
  "ゆえに",
  "以上より",
  "ここから",
  "計算",
  "導く",
  "導か",
  "得る",
  "従う",
  "分かる",
  "わかる",
  "示す",
  "確認",
)


def _normalize(
  text: str,
) -> str:
  normalized = text
  normalized = normalized.replace(
    "\\[",
    "$",
  )
  normalized = normalized.replace(
    "\\]",
    "$",
  )
  normalized = normalized.replace(
    "$$",
    "$",
  )
  normalized = normalized.replace(
    "**",
    "",
  )
  normalized = normalized.replace(
    "`",
    "",
  )
  normalized = re.sub(
    r"\s+",
    "",
    normalized,
  )
  return normalized


def _split_public_render(
  rendered: str,
):
  lines = rendered.splitlines()

  if "## 使用する結果" not in lines:
    return (
      {},
      rendered,
    )

  reference_header = lines.index(
    "## 使用する結果"
  )

  if "## 証明" not in lines:
    return (
      {},
      rendered,
    )

  proof_header = lines.index(
    "## 証明"
  )

  if reference_header >= proof_header:
    return (
      {},
      rendered,
    )

  statements = {}
  current_reference = None

  for line in lines[
    reference_header
    + 1:
    proof_header
  ]:
    match = re.match(
      r"^\*\*\[R([0-9]+)\]",
      line,
    )

    if match is not None:
      current_reference = int(
        match.group(
          1
        )
      )
      statements.setdefault(
        current_reference,
        [],
      )
      continue

    if (
      current_reference is None
      or not line.strip()
      or line.strip()
      == "使用する結果を先にまとめる."
    ):
      continue

    statements[
      current_reference
    ].append(
      line
    )

  body = "\n".join(
    lines[
      proof_header
      + 1:
    ]
  )

  return (
    {
      key: tuple(
        value
      )
      for key, value in statements.items()
    },
    body,
  )


def run_audit(
  output_dir: Path,
):
  output_dir.mkdir(
    parents=True,
    exist_ok=True,
  )

  groups = 0
  exceptions = []
  suppressible = []
  derivational = []

  for n in range(
    2,
    16,
  ):
    for k in range(
      0,
      8,
    ):
      groups += 1

      try:
        report = build_standard_toda_report(
          n=n,
          k=k,
        )
        group_result = (
          report.candidates[
            0
          ].source_candidate.group_result
        )
        replay = build_toda_group_result_proof_replay(
          group_result,
          max_depth=2,
        )
        presentation = (
          build_toda_group_proof_presentation(
            replay
          )
        )
        rendered = (
          render_toda_group_proof_narrative_markdown(
            presentation
          )
        )
        statements, body = (
          _split_public_render(
            rendered
          )
        )

        for reference_number, lines in (
          statements.items()
        ):
          for statement in lines:
            normalized_statement = _normalize(
              statement
            )

            if not normalized_statement:
              continue

            for line_number, body_line in enumerate(
              body.splitlines(),
              start=1,
            ):
              if normalized_statement not in _normalize(
                body_line
              ):
                continue

              row = {
                "n": n,
                "k": k,
                "reference_number": (
                  reference_number
                ),
                "statement": statement,
                "body_line_number": (
                  line_number
                ),
                "body_line": body_line,
              }

              if any(
                token in body_line
                for token in DERIVATION_TOKENS
              ):
                derivational.append(
                  row
                )
              else:
                suppressible.append(
                  row
                )

      except Exception as exc:
        exceptions.append(
          {
            "n": n,
            "k": k,
            "type": type(
              exc
            ).__name__,
            "message": str(
              exc
            ),
          }
        )

  payload = {
    "phase": "Phase156-R4",
    "groups": groups,
    "exceptions": len(
      exceptions
    ),
    "suppressible_exact_restatements": len(
      suppressible
    ),
    "preserved_derivational_occurrences": len(
      derivational
    ),
    "production_changes": True,
    "full_pytest_run": False,
  }

  (
    output_dir
    / "phase156_r4_result.json"
  ).write_text(
    json.dumps(
      payload,
      ensure_ascii=False,
      indent=2,
    )
    + "\n",
    encoding="utf-8",
  )
  (
    output_dir
    / "phase156_r4_suppressible.json"
  ).write_text(
    json.dumps(
      suppressible,
      ensure_ascii=False,
      indent=2,
    )
    + "\n",
    encoding="utf-8",
  )
  (
    output_dir
    / "phase156_r4_preserved_derivational.json"
  ).write_text(
    json.dumps(
      derivational,
      ensure_ascii=False,
      indent=2,
    )
    + "\n",
    encoding="utf-8",
  )
  (
    output_dir
    / "phase156_r4_exceptions.json"
  ).write_text(
    json.dumps(
      exceptions,
      ensure_ascii=False,
      indent=2,
    )
    + "\n",
    encoding="utf-8",
  )

  summary = "\n".join(
    [
      "=" * 78,
      "Phase156-R4 — proof-body duplicate suppression audit",
      "=" * 78,
      "groups: "
      + str(
        groups
      ),
      "exceptions: "
      + str(
        len(
          exceptions
        )
      ),
      "suppressible exact restatements: "
      + str(
        len(
          suppressible
        )
      ),
      "preserved derivational occurrences: "
      + str(
        len(
          derivational
        )
      ),
      "",
      "Completion rule:",
      (
        "  exact Reference statements may remain in the body only when "
        "the surrounding sentence carries derivation/calculation context."
      ),
      "=" * 78,
    ]
  ) + "\n"

  (
    output_dir
    / "phase156_r4_summary.txt"
  ).write_text(
    summary,
    encoding="utf-8",
  )
  print(
    summary
  )

  return payload


def main() -> int:
  parser = argparse.ArgumentParser()
  parser.add_argument(
    "--output-dir",
    type=Path,
    default=Path(
      "phase156_r4_audit_output"
    ),
  )
  args = parser.parse_args()

  result = run_audit(
    args.output_dir
  )

  passed = (
    result[
      "groups"
    ]
    == 112
    and result[
      "exceptions"
    ]
    == 0
    and result[
      "suppressible_exact_restatements"
    ]
    == 0
  )

  if passed:
    print(
      "PASS: no suppressible exact Reference/body restatements remain."
    )
    return 0

  print(
    "FAIL: suppressible Reference/body restatements remain."
  )
  return 1


if __name__ == "__main__":
  raise SystemExit(
    main()
  )
