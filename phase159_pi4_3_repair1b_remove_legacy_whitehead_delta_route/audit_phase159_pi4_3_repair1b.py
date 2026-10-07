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

from expression import (
  Multiple,
  WhiteheadProduct,
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

  result_steps = phase50[
    "result"
  ].steps

  delta_steps = tuple(
    step
    for step in result_steps
    if isinstance(
      step.conclusion,
      TodaDeltaImageUpToSignStatement,
    )
  )

  direct_delta_steps = tuple(
    step
    for step in delta_steps
    if isinstance(
      step.conclusion.positive_value,
      Multiple,
    )
  )

  whitehead_delta_steps = tuple(
    step
    for step in delta_steps
    if isinstance(
      step.conclusion.positive_value,
      WhiteheadProduct,
    )
  )

  image_steps = tuple(
    step
    for step in result_steps
    if isinstance(
      step.conclusion,
      TodaDeltaImageFreeCyclicStatement,
    )
  )

  print(
    "Phase 159 pi_4^3 repair1b verification"
  )
  print(
    "TodaDeltaImageUpToSignStatement count:",
    len(
      delta_steps
    ),
  )
  print(
    "direct Delta(iota_5)=+/-2eta_2 count:",
    len(
      direct_delta_steps
    ),
  )
  print(
    "legacy Whitehead Delta count:",
    len(
      whitehead_delta_steps
    ),
  )
  print(
    "Im(Delta) step count:",
    len(
      image_steps
    ),
  )

  if len(
    direct_delta_steps
  ) != 1:
    raise AssertionError(
      "expected exactly one direct Delta statement"
    )

  if whitehead_delta_steps:
    raise AssertionError(
      "legacy Whitehead Delta statement is still "
      "present in Phase 50 result"
    )

  if len(
    image_steps
  ) != 1:
    raise AssertionError(
      "expected exactly one Im(Delta) step"
    )

  image_step = image_steps[0]

  if (
    image_step.inference_rule
    is None
  ):
    raise AssertionError(
      "Im(Delta) step has no inference rule"
    )

  if (
    image_step.inference_rule.name
    != "free cyclic generator Delta image"
  ):
    raise AssertionError(
      "unexpected Im(Delta) rule: "
      + image_step.inference_rule.name
    )

  direct_premises = tuple(
    premise
    for premise in image_step.premises
    if isinstance(
      premise.conclusion,
      TodaDeltaImageUpToSignStatement,
    )
  )

  if len(
    direct_premises
  ) != 1:
    raise AssertionError(
      "Im(Delta) must have exactly one "
      "direct Delta premise"
    )

  direct_rule = (
    direct_premises[0]
    .inference_rule
  )

  if (
    direct_rule is None
    or direct_rule.literature_reference
    is None
    or (
      direct_rule
      .literature_reference
      .locator
      != "Proposition 5.1"
    )
  ):
    raise AssertionError(
      "Im(Delta) does not depend directly on "
      "Toda Proposition 5.1"
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

  ancestry_whitehead_delta = tuple(
    step
    for step in ancestry
    if (
      isinstance(
        step.conclusion,
        TodaDeltaImageUpToSignStatement,
      )
      and isinstance(
        step.conclusion.positive_value,
        WhiteheadProduct,
      )
    )
  )

  ancestry_image_steps = tuple(
    step
    for step in ancestry
    if isinstance(
      step.conclusion,
      TodaDeltaImageFreeCyclicStatement,
    )
  )

  print(
    "final ancestry legacy Whitehead Delta count:",
    len(
      ancestry_whitehead_delta
    ),
  )
  print(
    "final ancestry Im(Delta) count:",
    len(
      ancestry_image_steps
    ),
  )
  print(
    "Im(Delta) rule:",
    image_step.inference_rule.name,
  )
  print(
    "direct Delta locator:",
    (
      direct_rule
      .literature_reference
      .locator
    ),
  )

  if ancestry_whitehead_delta:
    raise AssertionError(
      "final pi_4^3 ancestry still contains "
      "legacy Whitehead Delta route"
    )

  if len(
    ancestry_image_steps
  ) != 1:
    raise AssertionError(
      "final pi_4^3 ancestry must contain "
      "exactly one Im(Delta) step"
    )

  print(
    "AUDIT_RESULT=PASS"
  )

  return 0


if __name__ == "__main__":
  raise SystemExit(
    main()
  )
