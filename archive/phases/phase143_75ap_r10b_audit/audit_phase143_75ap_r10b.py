from pathlib import Path

needles = (
  "_render_multi_argument",
  "群構造を決定する",
  "以上より",
  "test_phase143_51a_r",
  "test_phase143_51b",
  "render_toda_group_proof_narrative",
  "TodaGroupProofNarrativeArgument",
)

excluded_parts = {
  ".git",
  ".pytest_cache",
  "__pycache__",
  ".venv",
  "venv",
}

paths = []

for path in Path(".").rglob("*.py"):
  if any(
    part in excluded_parts
    for part in path.parts
  ):
    continue

  text = path.read_text(
    encoding="utf-8",
    errors="replace",
  )

  if any(
    needle in text
    for needle in needles
  ):
    paths.append((path, text))

print("=" * 78)
print("Phase 143-75AP R10B recursive narrative-path audit")
print("=" * 78)
print("matched files:", len(paths))

for path, text in sorted(
  paths,
  key=lambda item: str(item[0]),
):
  lines = text.splitlines()

  hit_indices = [
    index
    for index, line in enumerate(lines)
    if any(
      needle in line
      for needle in needles
    )
  ]

  if not hit_indices:
    continue

  print()
  print("=" * 78)
  print(path)
  print("-" * 78)

  merged = []

  for index in hit_indices:
    start = max(0, index - 20)
    end = min(len(lines), index + 35)

    if (
      merged
      and start <= merged[-1][1]
    ):
      merged[-1] = (
        merged[-1][0],
        max(
          merged[-1][1],
          end,
        ),
      )
    else:
      merged.append(
        (
          start,
          end,
        )
      )

  for start, end in merged:
    print()
    print(
      f"--- lines {start + 1}-{end} ---"
    )

    for number in range(
      start,
      end,
    ):
      print(
        f"{number + 1:5}: {lines[number]}"
      )
