from contextlib import redirect_stdout
from io import StringIO
from pathlib import Path

from main import _run_group_proof_command


TARGETS = (
  (3, 3),
  (5, 3),
  (4, 6),
  (5, 7),
  (8, 7),
  (9, 7),
)


def _label(n: int, k: int) -> str:
  return f"pi_{n + k}^{n}"


def _render(n: int, k: int) -> str:
  stream = StringIO()

  with redirect_stdout(stream):
    exit_code = _run_group_proof_command(
      n,
      k,
      max_depth=2,
      mode="narrative",
    )

  if exit_code != 0:
    raise RuntimeError(
      f"group-proof failed for {_label(n, k)}: {exit_code}"
    )

  return stream.getvalue()


def main() -> None:
  output_dir = Path(
    "phase144_6_r25_20_six_group_generic_production_narrative"
  ) / "outputs"
  output_dir.mkdir(
    parents=True,
    exist_ok=True,
  )

  combined = []

  print("=" * 78)
  print("Phase 144-6 R25-20 six-group generic production Narrative")
  print("depth=2 CLI request; Narrative presentation uses complete replay")
  print("=" * 78)

  for n, k in TARGETS:
    label = _label(n, k)
    narrative = _render(n, k)
    path = output_dir / f"{label}_generic_narrative.txt"
    path.write_text(
      narrative,
      encoding="utf-8",
    )

    section = (
      "\n"
      + "=" * 78
      + "\n"
      + label
      + "\n"
      + "=" * 78
      + "\n"
      + narrative.rstrip()
      + "\n"
    )
    combined.append(section)

    print()
    print("=" * 78)
    print(label)
    print("=" * 78)
    print(narrative, end="")
    if not narrative.endswith("\n"):
      print()
    print(f"[saved] {path}")

  combined_path = output_dir / "six_group_generic_narratives.txt"
  combined_path.write_text(
    "".join(combined),
    encoding="utf-8",
  )

  print()
  print("=" * 78)
  print("R25-20 output files")
  print("=" * 78)
  print(combined_path)
  print("Production code changes: none")
  print("Repository-wide pytest: not run")


if __name__ == "__main__":
  main()
