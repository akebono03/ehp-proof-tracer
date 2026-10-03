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
from toda_rules import (
  toda_53_nu_prime_lemma52_double_inference_rule,
  toda_53_nu_prime_lemma52_hopf_inference_rule,
  toda_53_nu_prime_lemma52_membership_inference_rule,
)


EXPECTED_GROUPS = 112


def run_audit(
  output_dir: Path,
) -> dict[
  str,
  object,
]:
  output_dir.mkdir(
    parents=True,
    exist_ok=True,
  )

  rules = (
    toda_53_nu_prime_lemma52_hopf_inference_rule(),
    toda_53_nu_prime_lemma52_double_inference_rule(),
    toda_53_nu_prime_lemma52_membership_inference_rule(),
  )
  correct_rules = sum(
    1
    for rule in rules
    if (
      rule.literature_reference is not None
      and rule.literature_reference.label
      == "Toda Lemma 5.2"
      and rule.literature_reference.locator
      == "Lemma 5.2"
    )
  )

  groups = 0
  exceptions = []
  composite_headers = []
  pi6_headers = []

  for n in range(
    2,
    16,
  ):
    for k in range(
      0,
      8,
    ):
      groups += 1
      group = (
        "pi_"
        + str(
          n + k
        )
        + "^"
        + str(
          n
        )
      )

      try:
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
        presentation = build_toda_group_proof_presentation(
          replay
        )
        rendered = render_toda_group_proof_narrative_markdown(
          presentation
        )
        reference_part = rendered.split(
          "まず",
          1,
        )[0]
        headers = re.findall(
          r"\*\*\[R\d+\] ([^\n]+?)\.\*\*",
          reference_part,
        )

        for header in headers:
          if (
            "(5.3)" in header
            and "Lemma 5.2" in header
          ):
            composite_headers.append(
              (
                group,
                header,
              )
            )

        if group == "pi_6^3":
          pi6_headers = list(
            headers
          )

      except Exception as exc:
        exceptions.append(
          (
            group,
            type(
              exc
            ).__name__,
            str(
              exc
            ),
          )
        )

  passed = (
    groups
    == EXPECTED_GROUPS
    and not exceptions
    and correct_rules
    == 3
    and not composite_headers
    and pi6_headers.count(
      "(5.3)"
    )
    == 1
    and pi6_headers.count(
      "Lemma 5.2"
    )
    == 1
  )

  result = {
    "groups": groups,
    "exceptions": len(
      exceptions
    ),
    "lemma52_rules_correct": correct_rules,
    "composite_53_lemma52_headers": len(
      composite_headers
    ),
    "pi6_3_reference_headers": pi6_headers,
    "pi6_3_53_header_count": pi6_headers.count(
      "(5.3)"
    ),
    "pi6_3_lemma52_header_count": pi6_headers.count(
      "Lemma 5.2"
    ),
    "pass": passed,
  }

  (
    output_dir
    / "phase156_r5_repair2_result.json"
  ).write_text(
    json.dumps(
      result,
      ensure_ascii=False,
      indent=2,
    )
    + "\n",
    encoding="utf-8",
  )

  summary = "\n".join(
    (
      "=" * 78,
      "Phase156-R5 repair2 — Lemma 5.2 specialization attribution",
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
      "Lemma 5.2 rules with correct explicit attribution: "
      + str(
        correct_rules
      )
      + "/3",
      "composite (5.3) / Lemma 5.2 headers: "
      + str(
        len(
          composite_headers
        )
      ),
      "pi_6^3 (5.3) header count: "
      + str(
        pi6_headers.count(
          "(5.3)"
        )
      ),
      "pi_6^3 Lemma 5.2 header count: "
      + str(
        pi6_headers.count(
          "Lemma 5.2"
        )
      ),
      "pi_6^3 headers: "
      + ", ".join(
        pi6_headers
      ),
      "",
      (
        "PASS"
        if passed
        else "FAIL"
      ),
      "=" * 78,
      "",
    )
  )

  (
    output_dir
    / "phase156_r5_repair2_summary.txt"
  ).write_text(
    summary,
    encoding="utf-8",
  )
  print(
    summary
  )

  return result


def main() -> int:
  parser = argparse.ArgumentParser()
  parser.add_argument(
    "--output-dir",
    type=Path,
    default=Path(
      "phase156_r5_repair2_audit_output"
    ),
  )
  args = parser.parse_args()
  result = run_audit(
    args.output_dir
  )
  return (
    0
    if result[
      "pass"
    ]
    else 1
  )


if __name__ == "__main__":
  raise SystemExit(
    main()
  )
