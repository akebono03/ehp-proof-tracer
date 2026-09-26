from pathlib import Path

needles = (
  "以上より",
  "transported_group",
  "final_relation_latex",
  "render_toda_proof_statement_latex",
  "Toda515Sigma8TransportedDecompositionStatement",
)

for path in sorted(Path(".").glob("*.py")):
  text = path.read_text(
    encoding="utf-8",
    errors="replace",
  )

  matches = [
    needle
    for needle in needles
    if needle in text
  ]

  if not matches:
    continue

  print("=" * 78)
  print(path)
  print("matches:", ", ".join(matches))
  print("-" * 78)

  lines = text.splitlines()

  hit_lines = set()

  for index, line in enumerate(lines):
    if any(
      needle in line
      for needle in needles
    ):
      hit_lines.add(index)

  shown = set()

  for index in sorted(hit_lines):
    start = max(0, index - 12)
    end = min(len(lines), index + 18)

    key = (start, end)

    if key in shown:
      continue

    shown.add(key)

    print(
      f"\n--- lines {start + 1}-{end} ---"
    )

    for number in range(start, end):
      print(
        f"{number + 1:5}: {lines[number]}"
      )
