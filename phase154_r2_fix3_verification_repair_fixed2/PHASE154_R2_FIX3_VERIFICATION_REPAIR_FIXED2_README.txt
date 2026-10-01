Phase 154-R2 Fix3 — Verification Repair Fixed2

Production changes
------------------
none

Cause
-----
The previous UTF-8 Python verification file was stored under:

  phase154_r2_fix3_verification_repair_fixed1/

When Python executes a script by file path, sys.path[0] is the script directory.
The repository root is not guaranteed to be importable merely because
PowerShell's current directory is the repository root.

Therefore:

  from toda_calculation_facade import ...

failed with:

  ModuleNotFoundError: No module named 'toda_calculation_facade'

Repair
------
At the top of the verification Python file, derive the repository root from
the script location and insert it into sys.path before importing project
modules.

Production files changed
------------------------
none

Verification Python file
------------------------
check_phase154_r2_fix3_representative_narrative.py

Full file:

from pathlib import Path
import sys


REPO_ROOT = Path(__file__).resolve().parent.parent

if str(REPO_ROOT) not in sys.path:
  sys.path.insert(
    0,
    str(
      REPO_ROOT
    ),
  )


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


def main() -> int:
  report = build_standard_toda_report(
    n=4,
    k=7,
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

  print(rendered)

  assert "まず、[R2]を用いる。" in rendered
  assert "まず、[R2]\n" not in rendered
  assert "Toda Proposition 5.15を用いる。" not in rendered
  assert r"\text{ is injective}" not in rendered
  assert r"\text{ is exact}" not in rendered
  assert "である.を用いる。" not in rendered
  assert (
    r"$\nu_{4}$ の分解写像は同型写像である."
    in rendered
  )
  assert r"\pi_{11}^{4} = 0" in rendered

  return 0


if __name__ == "__main__":
  raise SystemExit(
    main()
  )

Focused tests
-------------
- tests/test_phase154_r2_internal_prose_fallback_leakage.py
- tests/test_phase154_r2_fixed1_nu4_decomposition_semantic_prose.py
- tests/test_phase154_r2_fix2_semantic_sentence_composition.py
- tests/test_phase154_r2_fix3_reference_marker_completion.py
- tests/test_phase153_r7_proof_body_relevance.py
- tests/test_phase153_r8_reference_use_prose_normalization.py
- tests/test_phase153_closure_repair_r13.py

Full suite
----------
not run; reserved for the end of Phase 154.

Completion boundary
-------------------
If this verification passes, Phase 154-R2 is complete.
Proceed to Phase 154-R3 cross-group re-audit.
