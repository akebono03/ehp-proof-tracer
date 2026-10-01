import re

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


TARGETS = (
  ("pi6_3", 3, 3),
  ("pi10_4", 4, 6),
  ("pi12_5", 5, 7),
  ("pi16_9", 9, 7),
)


def render(
  n,
  k,
):
  report = build_standard_toda_report(
    n=n,
    k=k,
  )
  result = (
    report
    .candidates[0]
    .source_candidate
    .group_result
  )
  replay = build_toda_group_result_proof_replay(
    result,
    max_depth=2,
  )
  presentation = build_toda_group_proof_presentation(
    replay
  )
  rendered = render_toda_group_proof_narrative_markdown(
    presentation
  )

  return (
    presentation,
    rendered,
  )


def main():
  failures = []

  print(
    "=" * 72
  )
  print(
    "Phase 153-R11 depth-sensitive Reference audit"
  )
  print(
    "=" * 72
  )

  for label, n, k in TARGETS:
    presentation, rendered = render(
      n,
      k,
    )
    reference_headers = tuple(
      re.findall(
        r"\\*\\*\\[R[0-9]+\\] ([^\\n]+?)\\.\\*\\*",
        rendered,
      )
    )
    root_rule = presentation.root_step.inference_rule
    root_reference = (
      None
      if root_rule is None
      else root_rule.literature_reference
    )

    print(
      f"{label}: references={reference_headers}"
    )

    if (
      root_reference is not None
      and root_reference.locator is not None
      and any(
        root_reference.locator in header
        for header in reference_headers
      )
    ):
      failures.append(
        (
          label,
          "root self-reference remains",
          root_reference.locator,
        )
      )

    numbers = tuple(
      int(
        value
      )
      for value in re.findall(
        r"\\*\\*\\[R([0-9]+)\\]",
        rendered,
      )
    )

    if numbers != tuple(
      range(
        1,
        len(
          numbers
        )
        + 1,
      )
    ):
      failures.append(
        (
          label,
          "reference numbering is not contiguous",
          numbers,
        )
      )

    if label == "pi6_3":
      reference_part = rendered.split(
        "まず",
        1,
      )[0]

      if "Proposition 5.6" in reference_part:
        failures.append(
          (
            label,
            "Proposition 5.6 self-reference remains",
          )
        )

      if "(5.3) / Lemma 5.2" not in rendered:
        failures.append(
          (
            label,
            "definition reference is missing",
          )
        )

      if "(5.2)" not in rendered:
        failures.append(
          (
            label,
            "eta2 composition reference is missing",
          )
        )

  print()

  if failures:
    print(
      "FAIL"
    )

    for failure in failures:
      print(
        "  ",
        failure,
      )

    raise SystemExit(
      1
    )

  print(
    "PASS"
  )
  print(
    "Depth-2 generic Reference filtering is self-reference-free and "
    "does not require deeper-scope References to remain."
  )


if __name__ == "__main__":
  main()
