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


from tests.test_phase143_19_method_evidence import (
  _method_evidence_data,
)
from toda_group_proof_generic_narrative_renderer import (
  _render_generic_narrative_step,
)
from toda_group_proof_narrative_reason_renderer import (
  order_toda_group_proof_narrative_injective_image_order_reason,
  render_toda_group_proof_narrative_reason_sentence,
)
from toda_group_proof_narrative_reasons import (
  TodaGroupProofNarrativeReasonKind,
  build_toda_group_proof_narrative_reason_sidecar,
)
from toda_group_proof_narrative_renderer import (
  render_toda_group_proof_narrative_markdown,
)


def _paragraphs(
  markdown: str,
) -> tuple[
  str,
  ...,
]:
  return tuple(
    paragraph.strip()
    for paragraph in markdown.split(
      "\n\n"
    )
    if paragraph.strip()
  )


def _positions(
  paragraphs: tuple[
    str,
    ...,
  ],
) -> dict[
  str,
  tuple[
    int,
    ...,
  ],
]:
  targets = {
    "zero_group": (
      "[R1]より, "
      r"$\pi_{2}^{1} = 0$."
    ),
    "pi3_target": (
      "[R1]より, "
      r"$\pi_{3}^{3} = "
      r"\mathbb{Z}\{\iota_{3}\}$."
    ),
    "h_injective": (
      "完全性より, "
      r"$H: \pi_{3}^{2} \to \pi_{3}^{3}$ "
      "は単射."
    ),
    "e_isomorphism": (
      "[R1]より, "
      r"$E: \pi_{1}^{1} \to \pi_{2}^{2}$ "
      "は同型."
    ),
    "e_injective": (
      r"$E: \pi_{1}^{1} \to \pi_{2}^{2}$ "
      "は単射."
    ),
    "delta_zero": (
      "完全性より, "
      r"$\Delta: \pi_{3}^{3} \to \pi_{1}^{1}$ "
      "は零写像."
    ),
    "h_surjective": (
      "完全性より, "
      r"$H: \pi_{3}^{2} \to \pi_{3}^{3}$ "
      "は全射."
    ),
    "h_isomorphism": (
      r"$H: \pi_{3}^{2} \to \pi_{3}^{3}$ "
      "は同型."
    ),
    "eta2_definition": (
      "この同型写像により, "
      r"$H(\eta_{2}) = \iota_{3}$ となる "
      r"$\eta_{2} \in \pi_{3}^{2}$ "
      "が一意に存在する."
    ),
  }

  return {
    label: tuple(
      index
      for index, paragraph in enumerate(
        paragraphs
      )
      if paragraph == target
    )
    for label, target in targets.items()
  }


def main() -> int:
  (
    presentation,
    _,
    semantic_sidecar,
    _,
  ) = _method_evidence_data(
    2,
    1,
  )
  reason_sidecar = (
    build_toda_group_proof_narrative_reason_sidecar(
      presentation,
      semantic_sidecar,
    )
  )
  public = (
    render_toda_group_proof_narrative_markdown(
      presentation
    )
  )
  _, marker, body = public.partition(
    "## 証明"
  )

  if marker != "## 証明":
    raise RuntimeError(
      "proof section marker not found"
    )

  body = body.lstrip()
  before = _paragraphs(
    body
  )

  print(
    "=============================================================="
  )
  print(
    "Phase 159 pi3_2 locality re-apply audit13"
  )
  print(
    "=============================================================="
  )

  print()
  print(
    "=== Before re-apply ==="
  )

  for index, paragraph in enumerate(
    before
  ):
    print(
      f"[{index:02d}] {paragraph}"
    )

  print()
  print(
    "positions_before="
    + repr(
      _positions(
        before
      )
    )
  )

  print()
  print(
    "=== Reason details ==="
  )

  for index, reason in enumerate(
    reason_sidecar.reasons
  ):
    print()
    print(
      "reason["
      + str(
        index
      )
      + "] kind="
      + str(
        reason.kind
      )
    )
    print(
      "sentence="
      + repr(
        render_toda_group_proof_narrative_reason_sentence(
          reason
        )
      )
    )
    print(
      "conclusion="
      + repr(
        _render_generic_narrative_step(
          reason.conclusion_step
        )
      )
    )

    for premise_index, premise in enumerate(
      reason.premise_steps
    ):
      print(
        "premise["
        + str(
          premise_index
        )
        + "]="
        + repr(
          _render_generic_narrative_step(
            premise
          )
        )
      )

  reapplied = (
    order_toda_group_proof_narrative_injective_image_order_reason(
      body,
      reason_sidecar,
    )
  )
  after = _paragraphs(
    reapplied
  )

  print()
  print(
    "=== After direct re-apply ==="
  )

  for index, paragraph in enumerate(
    after
  ):
    print(
      f"[{index:02d}] {paragraph}"
    )

  print()
  print(
    "positions_after="
    + repr(
      _positions(
        after
      )
    )
  )

  print()
  print(
    "changed="
    + str(
      body != reapplied
    )
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

  print(
    "exactness_reason_count="
    + str(
      len(
        exactness_reasons
      )
    )
  )

  definition_steps = tuple(
    node.proof_step
    for node in presentation.nodes
    if (
      r"H(\eta_{2})"
      in (
        _render_generic_narrative_step(
          node.proof_step
        )
        or ""
      )
    )
  )

  print()
  print(
    "definition_step_count="
    + str(
      len(
        definition_steps
      )
    )
  )

  for definition_index, definition_step in enumerate(
    definition_steps
  ):
    print(
      "definition["
      + str(
        definition_index
      )
      + "]="
      + repr(
        _render_generic_narrative_step(
          definition_step
        )
      )
    )

    for premise_index, premise_step in enumerate(
      definition_step.premises
    ):
      premise_line = (
        _render_generic_narrative_step(
          premise_step
        )
      )
      print(
        "  premise["
        + str(
          premise_index
        )
        + "]="
        + repr(
          premise_line
        )
      )

      if premise_line:
        premise_fragment = (
          premise_line
          .replace(
            " は同型写像である.",
            " は同型.",
          )
          .replace(
            " は単射である.",
            " は単射.",
          )
          .replace(
            " は全射である.",
            " は全射.",
          )
        )
        print(
          "    concise_fragment_present="
          + str(
            premise_fragment
            in body
          )
        )

  return 0


if __name__ == "__main__":
  raise SystemExit(
    main()
  )
