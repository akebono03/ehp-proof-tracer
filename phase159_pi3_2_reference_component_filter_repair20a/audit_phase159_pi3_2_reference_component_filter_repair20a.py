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


def main() -> None:
  report = build_standard_toda_report(
    n=2,
    k=1,
  )
  group_result = (
    report.candidates[
      0
    ].source_candidate.group_result
  )
  replay = (
    build_toda_group_result_proof_replay(
      group_result,
      max_depth=2,
    )
  )
  presentation = (
    build_toda_group_proof_presentation(
      replay
    )
  )
  rendered = (
    render_toda_group_proof_narrative_markdown(
      presentation
    )
  )

  reference = (
    rendered.split(
      "## 使用する結果\n\n",
      1,
    )[1].split(
      "\n---\n",
      1,
    )[0]
  )
  proof = (
    rendered.split(
      "## 証明\n\n",
      1,
    )[1]
  )

  print(
    "=== Reference ==="
  )
  print(
    reference.strip()
  )
  print()
  print(
    "=== Proof ==="
  )
  print(
    proof.strip()
  )
  print()

  assert (
    r"$\pi_{i}^{1} = 0\ (i > 1)$."
    in reference
  )
  assert (
    r"$\pi_{n}^{n} = "
    r"\mathbb{Z}\{\iota_{n}\}$."
    in reference
  )
  assert (
    r"$\pi_{i}^{n} = 0\ (i < n)$."
    not in reference
  )
  assert (
    r"$E: \pi_{1}^{1} \to \pi_{2}^{2}$"
    not in reference
  )

  assert (
    r"$\pi_{2}^{1} = 0$."
    in proof
  )
  assert (
    r"$\pi_{3}^{3} = "
    r"\mathbb{Z}\{\iota_{3}\}$."
    in proof
  )
  assert (
    r"$E: \pi_{1}^{1} \to \pi_{2}^{2}$ "
    r"は同型."
    in proof
    or
    r"$E: \pi_{1}^{1} \to \pi_{2}^{2}$ "
    r"は同型写像である."
    in proof
  )

  print(
    "PASS: Reference display is minimal "
    "and proof-body dependencies remain present."
  )


if __name__ == "__main__":
  main()
