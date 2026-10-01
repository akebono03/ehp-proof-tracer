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
  ("pi4_2", 2, 2),
  ("pi5_2", 2, 3),
  ("pi6_2", 2, 4),
  ("pi7_2", 2, 5),
  ("pi8_2", 2, 6),
  ("pi9_2", 2, 7),
  ("pi10_6", 6, 4),
  ("pi12_7", 7, 5),
)

def render(n, k):
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
  return render_toda_group_proof_narrative_markdown(
    presentation
  )

def main():
  failures = []

  print("=" * 72)
  print("Phase 153-R10 route-boundary repair R1 audit")
  print("=" * 72)

  for label, n, k in TARGETS:
    rendered = render(
      n,
      k,
    )
    marker = "## 証明\n\n"
    body = (
      rendered.split(
        marker,
        1,
      )[1]
      if marker in rendered
      else rendered
    )
    section_numbers = tuple(
      int(value)
      for value in re.findall(
        r"\*\*\[R([0-9]+)\]",
        rendered,
      )
    )
    body_numbers = tuple(
      sorted(
        {
          int(value)
          for value in re.findall(
            r"\[R([0-9]+)\]",
            body,
          )
        }
      )
    )

    print(
      f"{label}: section={section_numbers} "
      f"body-markers={body_numbers}"
    )

    if body_numbers:
      if section_numbers != body_numbers:
        failures.append(
          (
            label,
            "marker-bearing route mismatch",
            section_numbers,
            body_numbers,
          )
        )

      if section_numbers != tuple(
        range(
          1,
          len(section_numbers) + 1,
        )
      ):
        failures.append(
          (
            label,
            "marker-bearing route numbering is not contiguous",
            section_numbers,
          )
        )

    if label == "pi6_2":
      if section_numbers != (
        1,
        2,
      ):
        failures.append(
          (
            label,
            "expected exactly two used references",
            section_numbers,
          )
        )

      if "Lemma 5.7" in rendered:
        failures.append(
          (
            label,
            "unused Lemma 5.7 remains",
          )
        )

      if "Proposition 4.4" in rendered:
        failures.append(
          (
            label,
            "unused Proposition 4.4 remains",
          )
        )

      if marker not in rendered:
        failures.append(
          (
            label,
            "proof heading spacing is not canonical",
          )
        )

  print()

  if failures:
    print("FAIL")
    for failure in failures:
      print("  ", failure)
    raise SystemExit(1)

  print("PASS")
  print(
    "Marker-bearing narrative routes filter and renumber used References; "
    "marker-free generic routes preserve their structured Reference section."
  )

if __name__ == "__main__":
  main()
