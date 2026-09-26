from pathlib import Path

from toda_calculation_facade import build_standard_toda_report
from toda_group_proof_narrative_argument_multi_renderer import (
  render_toda_group_proof_narrative_multi_argument_markdown,
)
from toda_group_proof_narrative_arguments import (
  build_toda_group_proof_narrative_arguments,
)
from toda_group_proof_narrative_blocks import (
  build_toda_group_proof_narrative_blocks,
)
from toda_group_proof_narrative_renderer import (
  render_toda_group_proof_narrative_markdown,
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


TARGETS = (
  (3, 3, "pi_6^3"),
  (5, 3, "pi_8^5"),
  (4, 6, "pi_10^4"),
  (5, 7, "pi_12^5"),
  (8, 7, "pi_15^8"),
  (9, 7, "pi_16^9"),
)


def _build(n, k):
  report = build_standard_toda_report(n=n, k=k)
  group_result = report.candidates[0].source_candidate.group_result
  replay = build_toda_group_result_proof_replay(
    group_result,
    max_depth=3,
  )
  presentation = build_toda_group_proof_presentation(replay)
  sidecar = build_toda_group_proof_narrative_semantic_sidecar(
    presentation
  )
  blocks = build_toda_group_proof_narrative_blocks(
    presentation,
    semantic_sidecar=sidecar,
  )
  arguments = build_toda_group_proof_narrative_arguments(
    presentation,
    blocks,
    semantic_sidecar=sidecar,
  )
  return presentation, sidecar, blocks, arguments


def _display_math_lines(markdown):
  lines = markdown.splitlines()
  result = []
  in_display = False
  current = []

  for line in lines:
    stripped = line.strip()

    if stripped == r"\[":
      in_display = True
      current = []
      continue

    if stripped == r"\]" and in_display:
      result.append(" ".join(current))
      in_display = False
      current = []
      continue

    if in_display:
      current.append(stripped)
      continue

    if stripped.startswith("$") and stripped.endswith("$"):
      result.append(stripped)

  return tuple(result)


def main():
  output_dir = Path(__file__).resolve().parent / "output"
  output_dir.mkdir(exist_ok=True)

  summary = []

  for n, k, label in TARGETS:
    presentation, sidecar, blocks, arguments = _build(n, k)

    legacy = render_toda_group_proof_narrative_markdown(
      presentation
    )
    generic = (
      render_toda_group_proof_narrative_multi_argument_markdown(
        presentation,
        blocks,
        sidecar,
        arguments,
      )
    )

    legacy_math = _display_math_lines(legacy)
    generic_math = _display_math_lines(generic)

    report = "\n".join(
      (
        "=" * 100,
        f"{label}: n={n}, k={k}",
        "=" * 100,
        "",
        "LEGACY / CURRENT CLI-WEB RENDERER",
        "-" * 100,
        legacy,
        "",
        "GENERIC MULTI-ARGUMENT RENDERER",
        "-" * 100,
        generic,
        "",
        "DISPLAY-MATH SUMMARY",
        "-" * 100,
        f"legacy_display_math_count={len(legacy_math)}",
        f"generic_display_math_count={len(generic_math)}",
        "",
        "legacy display math:",
        *(
          f"  {index + 1}: {line}"
          for index, line in enumerate(legacy_math)
        ),
        "",
        "generic display math:",
        *(
          f"  {index + 1}: {line}"
          for index, line in enumerate(generic_math)
        ),
        "",
      )
    )

    (output_dir / f"{label}_renderer_comparison.txt").write_text(
      report,
      encoding="utf-8",
    )

    summary.extend(
      (
        "=" * 78,
        label,
        f"blocks={len(blocks)}",
        f"arguments={len(arguments)}",
        f"legacy_chars={len(legacy)}",
        f"generic_chars={len(generic)}",
        f"legacy_display_math_count={len(legacy_math)}",
        f"generic_display_math_count={len(generic_math)}",
        f"same_output={legacy == generic}",
      )
    )

  summary_text = "\n".join(summary) + "\n"
  print(summary_text)

  (output_dir / "summary.txt").write_text(
    summary_text,
    encoding="utf-8",
  )

  print(
    "Detailed comparisons written to: "
    + str(output_dir)
  )


if __name__ == "__main__":
  main()
