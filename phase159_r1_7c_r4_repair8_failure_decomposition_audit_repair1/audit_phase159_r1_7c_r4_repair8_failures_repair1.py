
from __future__ import annotations

from pathlib import Path
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


PACKAGE_DIR = Path(__file__).resolve().parent
OUTPUT_DIR = PACKAGE_DIR / "output"

TARGETS = (
  ("pi3_2", 2, 1),
  ("pi6_3", 3, 3),
  ("pi8_5", 5, 3),
  ("pi10_4", 4, 6),
  ("pi11_4", 4, 7),
  ("pi12_5", 5, 7),
  ("pi15_8", 8, 7),
  ("pi16_9", 9, 7),
)

REFERENCE_HEADER_RE = re.compile(
  r"\*\*\[R([0-9]+)\] ([^\n]+?)\.\*\*"
)
REFERENCE_MARKER_RE = re.compile(
  r"\[R([0-9]+)\]"
)

REFLEXIVE_ETA5 = (
  r"$\eta_{5} = \eta_{5}$"
)


def render_group(
  n: int,
  k: int,
) -> str:
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

  return render_toda_group_proof_narrative_markdown(
    presentation
  )


def split_reference_body(
  rendered: str,
) -> tuple[
  str,
  str,
]:
  if "\n## 証明\n" not in rendered:
    return (
      rendered,
      "",
    )

  reference, body = rendered.split(
    "\n## 証明\n",
    1,
  )

  return (
    reference,
    body,
  )


def reference_summary(
  reference: str,
  body: str,
) -> str:
  headers = tuple(
    (
      int(
        match.group(
          1
        )
      ),
      match.group(
        2
      ),
    )
    for match in REFERENCE_HEADER_RE.finditer(
      reference
    )
  )

  body_markers = {
    int(
      match.group(
        1
      )
    )
    for match in REFERENCE_MARKER_RE.finditer(
      body
    )
  }

  lines = [
    "Reference headers:",
  ]

  if headers:
    for number, label in headers:
      lines.append(
        f"  R{number}: {label}"
      )
  else:
    lines.append(
      "  <none>"
    )

  lines.extend(
    (
      "",
      "Body markers:",
      (
        "  "
        + ", ".join(
          f"R{number}"
          for number in sorted(
            body_markers
          )
        )
        if body_markers
        else "  <none>"
      ),
      "",
      "Missing body markers:",
    )
  )

  missing = tuple(
    number
    for number, _ in headers
    if number not in body_markers
  )

  if missing:
    lines.append(
      "  "
      + ", ".join(
        f"R{number}"
        for number in missing
      )
    )
  else:
    lines.append(
      "  <none>"
    )

  return "\n".join(
    lines
  )


def defect_summary(
  body: str,
) -> str:
  checks = (
    (
      "reflexive_eta5",
      REFLEXIVE_ETA5,
    ),
    (
      "eta6_old_suffix",
      r"$\eta_{6}=E\eta_{5}$ である.",
    ),
    (
      "kernel_old_suffix",
      r"$\ker \Delta=\operatorname{Im}H=\pi_{7}^{5}$ である.",
    ),
    (
      "exactness_to_map_old_suffix",
      r"$\ker E=\operatorname{Im}Δ=0$ である.",
    ),
    (
      "multiple_order_old_suffix",
      r"$4\nu'=0$ かつ $2\nu'\neq0$ である.",
    ),
    (
      "short_exact_old_phrase",
      "次の短完全列を得る.",
    ),
    (
      "duplicate_transition",
      "以上より, この完全性と ",
    ),
    (
      "repeated_numeric_equality",
      r"\operatorname{ord}(\nu')=4=4",
    ),
  )

  lines = []

  for label, fragment in checks:
    lines.append(
      f"{label}: {body.count(fragment)}"
    )

  return "\n".join(
    lines
  )


def main() -> None:
  OUTPUT_DIR.mkdir(
    parents=True,
    exist_ok=True,
  )

  summary_lines = [
    "# Phase 159 R1-7c R4 repair8 failure decomposition audit",
    "",
  ]

  for label, n, k in TARGETS:
    rendered = render_group(
      n,
      k,
    )

    reference, body = split_reference_body(
      rendered
    )

    output_path = (
      OUTPUT_DIR
      / f"{label}.md"
    )

    output_path.write_text(
      rendered,
      encoding="utf-8",
    )

    diagnostics = (
      "# Diagnostics\n\n"
      + reference_summary(
        reference,
        body,
      )
      + "\n\nDefect counts:\n"
      + defect_summary(
        body
      )
      + "\n"
    )

    diagnostics_path = (
      OUTPUT_DIR
      / f"{label}_diagnostics.txt"
    )

    diagnostics_path.write_text(
      diagnostics,
      encoding="utf-8",
    )

    headers = tuple(
      REFERENCE_HEADER_RE.finditer(
        reference
      )
    )

    markers = {
      int(
        match.group(
          1
        )
      )
      for match in REFERENCE_MARKER_RE.finditer(
        body
      )
    }

    missing = tuple(
      int(
        match.group(
          1
        )
      )
      for match in headers
      if int(
        match.group(
          1
        )
      ) not in markers
    )

    reflexive_eta5_count = body.count(
      REFLEXIVE_ETA5
    )

    summary_lines.append(
      (
        f"- {label}: "
        f"references={len(headers)}, "
        f"body_markers={len(markers)}, "
        f"missing_markers={len(missing)}, "
        f"reflexive_eta5={reflexive_eta5_count}"
      )
    )

  summary_path = (
    OUTPUT_DIR
    / "summary.md"
  )

  summary_path.write_text(
    "\n".join(
      summary_lines
    )
    + "\n",
    encoding="utf-8",
  )

  print(
    "\n".join(
      summary_lines
    )
  )

  print("")
  print(
    "Audit only. Production changes: none."
  )
  print(
    "Existing test changes: none."
  )


if __name__ == "__main__":
  main()
