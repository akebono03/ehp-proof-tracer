from pathlib import Path
import sys


REPO_ROOT = Path(__file__).resolve().parent.parent

if str(
  REPO_ROOT
) not in sys.path:
  sys.path.insert(
    0,
    str(
      REPO_ROOT
    ),
  )


from toda_calculation_facade import (
  build_standard_toda_report,
)
from toda_group_proof_generic_narrative_renderer import (
  _render_generic_narrative_step,
)
from toda_group_proof_narrative_renderer import (
  render_toda_group_proof_narrative_markdown,
)
from toda_group_proof_narrative_reasons import (
  TodaGroupProofNarrativeReasonKind,
  build_toda_group_proof_narrative_reason_sidecar,
)
from toda_group_proof_narrative_semantics import (
  build_toda_group_proof_narrative_semantic_sidecar,
)
from toda_group_proof_presentation import (
  build_toda_group_proof_presentation,
)
from toda_group_result_proof_replay import (
  build_toda_group_result_proof_replay,
)


def main() -> int:
  report = build_standard_toda_report(
    n=2,
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
  presentation = (
    build_toda_group_proof_presentation(
      replay
    )
  )
  semantic_sidecar = (
    build_toda_group_proof_narrative_semantic_sidecar(
      presentation
    )
  )
  reason_sidecar = (
    build_toda_group_proof_narrative_reason_sidecar(
      presentation,
      semantic_sidecar,
    )
  )
  rendered = (
    render_toda_group_proof_narrative_markdown(
      presentation
    )
  )

  before, marker, after = rendered.partition(
    "## 証明"
  )

  if marker != "## 証明":
    raise RuntimeError(
      "proof section marker not found"
    )

  if not before:
    raise RuntimeError(
      "unexpected empty prefix before proof section"
    )

  paragraphs = tuple(
    paragraph.strip()
    for paragraph in after.split(
      "\n\n"
    )
    if paragraph.strip()
  )

  print(
    "=============================================================="
  )
  print(
    "Phase 159 pi3_2 exactness reason locality audit8"
  )
  print(
    "=============================================================="
  )
  print()
  print(
    "=== Public proof paragraphs ==="
  )

  for index, paragraph in enumerate(
    paragraphs
  ):
    print(
      f"[{index:02d}] {paragraph}"
    )

  print()
  print(
    "=== EXACTNESS_TO_MAP_PROPERTY reasons ==="
  )

  exactness_reasons = tuple(
    reason
    for reason in reason_sidecar.reasons
    if (
      reason.kind
      is TodaGroupProofNarrativeReasonKind
      .EXACTNESS_TO_MAP_PROPERTY
    )
  )

  for reason_index, reason in enumerate(
    exactness_reasons
  ):
    conclusion = (
      _render_generic_narrative_step(
        reason.conclusion_step
      )
    )

    print()
    print(
      f"reason[{reason_index}] conclusion:"
    )
    print(
      conclusion
    )
    print(
      "premises:"
    )

    for premise_index, premise in enumerate(
      reason.premise_steps
    ):
      premise_rendered = (
        _render_generic_narrative_step(
          premise
        )
      )
      print(
        f"  premise[{premise_index}]: "
        + str(
          premise_rendered
        )
      )

  print()
  print(
    "=== Focused positions ==="
  )

  targets = (
    (
      "zero_group",
      "[R1]より, "
      r"$\pi_{2}^{1} = 0$.",
    ),
    (
      "pi3_target",
      "[R1]より, "
      r"$\pi_{3}^{3} = "
      r"\mathbb{Z}\{\iota_{3}\}$.",
    ),
    (
      "h_injective",
      "完全性より, "
      r"$H: \pi_{3}^{2} \to \pi_{3}^{3}$ "
      "は単射.",
    ),
    (
      "e_isomorphism",
      "[R1]より, "
      r"$E: \pi_{1}^{1} \to \pi_{2}^{2}$ "
      "は同型.",
    ),
    (
      "e_injective",
      r"$E: \pi_{1}^{1} \to \pi_{2}^{2}$ "
      "は単射.",
    ),
    (
      "delta_zero",
      "完全性より, "
      r"$\Delta: \pi_{3}^{3} \to \pi_{1}^{1}$ "
      "は零写像.",
    ),
    (
      "h_surjective",
      "完全性より, "
      r"$H: \pi_{3}^{2} \to \pi_{3}^{3}$ "
      "は全射.",
    ),
    (
      "h_isomorphism",
      r"$H: \pi_{3}^{2} \to \pi_{3}^{3}$ "
      "は同型.",
    ),
  )

  for label, target in targets:
    matches = tuple(
      index
      for index, paragraph in enumerate(
        paragraphs
      )
      if paragraph == target
    )
    print(
      label
      + "="
      + repr(
        matches
      )
    )

  return 0


if __name__ == "__main__":
  raise SystemExit(
    main()
  )
