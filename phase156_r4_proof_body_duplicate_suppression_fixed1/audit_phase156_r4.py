from __future__ import annotations

import argparse
import json
import re
from pathlib import Path

from toda_calculation_facade import (
  build_standard_toda_report,
)
from toda_group_proof_narrative_contribution_renderer import (
  _toda_group_proof_narrative_reference_statement_lines_by_number,
)
from toda_group_proof_narrative_references import (
  build_toda_group_proof_narrative_reference_entries,
)
from toda_group_proof_narrative_renderer import (
  render_toda_group_proof_narrative_markdown,
)
from toda_group_proof_narrative_semantics import (
  build_toda_group_proof_narrative_semantic_closure_presentation,
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


def _public_reference_and_body(
  rendered: str,
) -> tuple[
  tuple[
    str,
    ...,
  ],
  str,
]:
  lines = rendered.splitlines()

  if (
    "## 使用する結果" not in lines
    or "## 証明" not in lines
  ):
    return (
      (),
      rendered,
    )

  reference_header = lines.index(
    "## 使用する結果"
  )
  proof_header = lines.index(
    "## 証明"
  )

  if reference_header >= proof_header:
    return (
      (),
      rendered,
    )

  reference_lines = tuple(
    line
    for line in lines[
      reference_header
      + 1:
      proof_header
    ]
    if line.strip()
  )
  body = "\n".join(
    lines[
      proof_header
      + 1:
    ]
  )

  return (
    reference_lines,
    body,
  )


def _displayed_canonical_statements(
  presentation,
  rendered: str,
) -> tuple[
  str,
  ...,
]:
  reference_entries = (
    build_toda_group_proof_narrative_reference_entries(
      presentation
    )
  )
  selected_by_number = (
    _toda_group_proof_narrative_reference_statement_lines_by_number(
      presentation,
      reference_entries,
    )
  )
  canonical_statements = tuple(
    statement
    for statements in selected_by_number.values()
    for statement in statements
  )
  canonical_by_normalized = {
    _normalize(
      statement
    ): statement
    for statement in canonical_statements
    if _normalize(
      statement
    )
  }
  public_reference_lines, _body = (
    _public_reference_and_body(
      rendered
    )
  )

  displayed = []
  seen = set()

  for line in public_reference_lines:
    normalized = _normalize(
      line
    )
    statement = (
      canonical_by_normalized.get(
        normalized
      )
    )

    if statement is None:
      continue

    if normalized in seen:
      continue

    seen.add(
      normalized
    )
    displayed.append(
      statement
    )

  return tuple(
    displayed
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
  displayed_statement_count = 0
  groups_with_public_statements = 0

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
        raw_presentation = (
          build_toda_group_proof_presentation(
            replay
          )
        )
        presentation = (
          build_toda_group_proof_narrative_semantic_closure_presentation(
            raw_presentation
          )
        )
        rendered = (
          render_toda_group_proof_narrative_markdown(
            raw_presentation
          )
        )
        displayed_statements = (
          _displayed_canonical_statements(
            presentation,
            rendered,
          )
        )
        _reference_lines, body = (
          _public_reference_and_body(
            rendered
          )
        )

        if displayed_statements:
          groups_with_public_statements += 1

        displayed_statement_count += len(
          displayed_statements
        )

        for statement in displayed_statements:
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
    "groups_with_public_canonical_statements": (
      groups_with_public_statements
    ),
    "displayed_canonical_statement_count": (
      displayed_statement_count
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
      "groups with public canonical statements: "
      + str(
        groups_with_public_statements
      ),
      "displayed canonical statements: "
      + str(
        displayed_statement_count
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
        "  only canonical Reference statements that are actually displayed "
        "in the public Reference section are compared with the proof body."
      ),
      (
        "  exact displayed Reference statements may remain in the body "
        "only when the surrounding sentence carries derivation/calculation "
        "context."
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
      "PASS: no suppressible exact displayed Reference/body "
      "restatements remain."
    )
    return 0

  print(
    "FAIL: suppressible displayed Reference/body restatements remain."
  )
  return 1


if __name__ == "__main__":
  raise SystemExit(
    main()
  )
