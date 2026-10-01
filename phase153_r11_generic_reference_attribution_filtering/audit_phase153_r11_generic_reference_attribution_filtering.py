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
    "Phase 153-R11 Generic-route Reference attribution/filtering audit"
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
        r"\*\*\[R[0-9]+\] ([^\n]+?)\.\*\*",
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

    if label == "pi6_3":
      for required in (
        "(5.3) / Lemma 5.2",
        "(5.2)",
        "Proposition 4.4",
        "Proposition 5.1",
      ):
        if required not in rendered:
          failures.append(
            (
              label,
              "required external reference missing",
              required,
            )
          )

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
    "Generic-route Reference sections are attributed from used ProofSteps "
    "and exclude the root theorem self-reference."
  )


if __name__ == "__main__":
  main()
