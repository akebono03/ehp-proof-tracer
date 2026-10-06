from __future__ import annotations

import sys
from pathlib import Path

REPOSITORY_ROOT = (
  Path(__file__).resolve().parents[1]
)
if str(REPOSITORY_ROOT) not in sys.path:
  sys.path.insert(
    0,
    str(REPOSITORY_ROOT),
  )

from toda_rules import (
  TodaDeltaImageFreeCyclicStatement,
  TodaDeltaImageUpToSignStatement,
)
from toda_upstream_bootstrap import (
  _build_phase50_result,
)


def main() -> int:
  phase50 = _build_phase50_result()

  image_steps = tuple(
    step
    for step in phase50[
      "result"
    ].steps
    if isinstance(
      step.conclusion,
      TodaDeltaImageFreeCyclicStatement,
    )
  )

  if len(
    image_steps
  ) != 1:
    raise AssertionError(
      "expected exactly one Im(Delta) step, "
      f"found {len(image_steps)}"
    )

  image_step = image_steps[0]

  direct_delta_premises = tuple(
    premise
    for premise in image_step.premises
    if isinstance(
      premise.conclusion,
      TodaDeltaImageUpToSignStatement,
    )
  )

  if len(
    direct_delta_premises
  ) != 1:
    raise AssertionError(
      "expected exactly one direct Delta premise, "
      f"found {len(direct_delta_premises)}"
    )

  direct_delta_step = (
    direct_delta_premises[0]
  )

  rule = (
    direct_delta_step
    .inference_rule
  )

  if rule is None:
    raise AssertionError(
      "direct Delta premise has no inference rule"
    )

  reference = (
    rule.literature_reference
  )

  if reference is None:
    raise AssertionError(
      "direct Delta premise has no literature reference"
    )

  if (
    reference.locator
    != "Proposition 5.1"
  ):
    raise AssertionError(
      "unexpected direct Delta locator: "
      + str(
        reference.locator
      )
    )

  pending = [
    phase50[
      "final_group_step"
    ]
  ]
  seen = set()
  ancestry = []

  while pending:
    step = pending.pop()
    step_id = id(step)

    if step_id in seen:
      continue

    seen.add(
      step_id
    )
    ancestry.append(
      step
    )
    pending.extend(
      step.premises
    )

  ancestry_image_steps = tuple(
    step
    for step in ancestry
    if isinstance(
      step.conclusion,
      TodaDeltaImageFreeCyclicStatement,
    )
  )

  ancestry_direct_steps = tuple(
    step
    for step in ancestry
    if (
      isinstance(
        step.conclusion,
        TodaDeltaImageUpToSignStatement,
      )
      and (
        step.inference_rule
        is not None
      )
      and (
        step.inference_rule
        .literature_reference
        is not None
      )
      and (
        step.inference_rule
        .literature_reference
        .locator
        == "Proposition 5.1"
      )
    )
  )

  print(
    "Phase 159 pi_4^3 repair1a verification"
  )
  print(
    "all Im(Delta) steps:",
    len(
      image_steps
    ),
  )
  print(
    "final ancestry Im(Delta) steps:",
    len(
      ancestry_image_steps
    ),
  )
  print(
    "final ancestry Proposition 5.1 "
    "direct Delta steps:",
    len(
      ancestry_direct_steps
    ),
  )
  print(
    "Im(Delta) rule:",
    (
      image_step
      .inference_rule
      .name
      if image_step.inference_rule
      is not None
      else ""
    ),
  )
  print(
    "direct Delta rule:",
    rule.name,
  )
  print(
    "direct Delta locator:",
    reference.locator,
  )

  if len(
    ancestry_image_steps
  ) != 1:
    raise AssertionError(
      "final ancestry must contain exactly "
      "one Im(Delta) step"
    )

  if len(
    ancestry_direct_steps
  ) != 1:
    raise AssertionError(
      "final ancestry must contain exactly "
      "one Proposition 5.1 direct Delta step"
    )

  print(
    "AUDIT_RESULT=PASS"
  )

  return 0


if __name__ == "__main__":
  raise SystemExit(
    main()
  )
