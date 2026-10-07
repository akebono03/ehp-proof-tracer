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


from tests.test_phase143_19_method_evidence import (
  _method_evidence_data,
)
from toda_group_proof_narrative_contribution_renderer import (
  render_toda_group_proof_narrative_multi_argument_with_contributions_markdown,
)
from toda_group_proof_narrative_renderer import (
  _finalize_toda_group_proof_narrative_markdown,
  _phase158_normalize_public_narrative_contract,
  _wrap_phase150_rc4_generic_public_narrative,
  render_toda_group_proof_narrative_markdown,
)


ZERO_MAP = (
  r"$\Delta: \pi_{7}^{5} "
  r"\to \pi_{5}^{2}$ "
  "は零写像である."
)
INJECTIVE_REASON = (
  "完全性より, "
  r"$E: \pi_{5}^{2} "
  r"\to \pi_{6}^{3}$ "
  "は単射."
)


def paragraph_matches(
  markdown: str,
) -> tuple[
  tuple[
    int,
    str,
  ],
  ...,
]:
  return tuple(
    (
      index,
      paragraph,
    )
    for index, paragraph in enumerate(
      markdown.split(
        "\n\n"
      )
    )
    if (
      ZERO_MAP in paragraph
      or INJECTIVE_REASON in paragraph
      or r"\ker E" in paragraph
      or "$Δ=0$" in paragraph
    )
  )


def record(
  rows,
  name: str,
  markdown: str,
) -> None:
  rows.append(
    (
      name,
      ZERO_MAP in markdown,
      INJECTIVE_REASON in markdown,
      paragraph_matches(
        markdown
      ),
    )
  )


def main() -> int:
  (
    presentation,
    blocks,
    semantic_sidecar,
    arguments,
  ) = _method_evidence_data(
    3,
    3,
  )

  rows = []

  contributions = (
    render_toda_group_proof_narrative_multi_argument_with_contributions_markdown(
      presentation,
      blocks,
      semantic_sidecar,
      arguments,
    )
  )
  record(
    rows,
    "00_with_contributions",
    contributions,
  )

  wrapped = (
    _wrap_phase150_rc4_generic_public_narrative(
      presentation,
      contributions,
    )
  )
  record(
    rows,
    "01_public_wrapper",
    wrapped,
  )

  finalized = (
    _finalize_toda_group_proof_narrative_markdown(
      wrapped
    )
  )
  record(
    rows,
    "02_finalizer",
    finalized,
  )

  normalized = (
    _phase158_normalize_public_narrative_contract(
      presentation,
      finalized,
    )
  )
  record(
    rows,
    "03_public_contract_normalization",
    normalized,
  )

  actual = (
    render_toda_group_proof_narrative_markdown(
      presentation
    )
  )
  record(
    rows,
    "04_actual_public_renderer",
    actual,
  )

  lines = [
    "# Phase 159 pi6_3 zero-map outer-stage audit",
    "",
  ]

  previous_zero_map = None
  previous_reason = None

  for (
    name,
    has_zero_map,
    has_reason,
    matches,
  ) in rows:
    suffixes = []

    if (
      previous_zero_map is not None
      and has_zero_map != previous_zero_map
    ):
      suffixes.append(
        "ZERO_MAP CHANGED "
        + str(
          previous_zero_map
        )
        + " -> "
        + str(
          has_zero_map
        )
      )

    if (
      previous_reason is not None
      and has_reason != previous_reason
    ):
      suffixes.append(
        "REASON CHANGED "
        + str(
          previous_reason
        )
        + " -> "
        + str(
          has_reason
        )
      )

    suffix = (
      "  <-- "
      + "; ".join(
        suffixes
      )
      if suffixes
      else ""
    )

    lines.append(
      name
      + ": zero_map="
      + str(
        has_zero_map
      )
      + ", injective_reason="
      + str(
        has_reason
      )
      + suffix
    )

    for paragraph_index, paragraph in matches:
      lines.append(
        "  P"
        + str(
          paragraph_index
        )
        + ": "
        + repr(
          paragraph
        )
      )

    previous_zero_map = has_zero_map
    previous_reason = has_reason

  lines.extend(
    (
      "",
      "## With contributions",
      "",
      contributions,
      "",
      "## Public wrapper",
      "",
      wrapped,
      "",
      "## Actual public",
      "",
      actual,
      "",
    )
  )

  output = "\n".join(
    lines
  )

  output_path = (
    Path(__file__).resolve().parent
    / "phase159_pi6_3_zero_map_outer_stage_audit.txt"
  )
  output_path.write_text(
    output,
    encoding="utf-8",
  )

  print(
    output
  )

  return 0


if __name__ == "__main__":
  raise SystemExit(
    main()
  )
