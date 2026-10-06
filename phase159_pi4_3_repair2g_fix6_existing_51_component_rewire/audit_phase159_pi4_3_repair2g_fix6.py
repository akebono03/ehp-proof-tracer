from __future__ import annotations

from pathlib import Path
import sys


ROOT = Path(__file__).resolve().parents[1]

if str(ROOT) not in sys.path:
  sys.path.insert(
    0,
    str(ROOT),
  )

from low_dimensional_facts import (
  pi_4_5_zero_fact,
  pi_5_5_free_cyclic_fact,
)
from toda_calculation_facade import (
  build_standard_toda_report,
)
from toda_group_proof_narrative_references import (
  extract_toda_group_proof_step_literature_reference,
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
from toda_literature_statement_boundary import (
  classify_toda_literature_statement_step,
)
from toda_upstream_bootstrap import (
  _build_phase50_result,
)


def main() -> int:
  print(
    "=== Phase159 pi_4^3 repair2g fix6 audit ==="
  )

  phase50 = _build_phase50_result()

  for conclusion, label in (
    (
      pi_5_5_free_cyclic_fact(),
      "pi_5^5",
    ),
    (
      pi_4_5_zero_fact(),
      "pi_4^5=0",
    ),
  ):
    step = next(
      step
      for step in phase50[
        "result"
      ].steps
      if step.conclusion == conclusion
    )
    boundary = (
      classify_toda_literature_statement_step(
        step
      )
    )
    reference = (
      extract_toda_group_proof_step_literature_reference(
        step
      )
    )

    print(
      label,
      "rule=",
      (
        None
        if step.inference_rule is None
        else step.inference_rule.name
      ),
    )
    print(
      label,
      "boundary=",
      boundary,
    )
    print(
      label,
      "reference=",
      (
        None
        if reference is None
        else reference.locator
      ),
    )

  report = build_standard_toda_report(
    n=3,
    k=1,
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
  raw = build_toda_group_proof_presentation(
    replay
  )
  rendered = (
    render_toda_group_proof_narrative_markdown(
      raw
    )
  )

  print()
  print(
    "=== pi_4^3 public Narrative ==="
  )
  print(
    rendered
  )

  return 0


if __name__ == "__main__":
  raise SystemExit(main())
