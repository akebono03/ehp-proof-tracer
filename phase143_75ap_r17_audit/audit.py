from pathlib import Path
import ast

paths = [
  Path("toda_group_proof_narrative_argument_body_renderer.py"),
  Path("toda_group_proof_generic_narrative_renderer.py"),
]

needles = (
  "preserve_provenance_step_ids",
  "preserve_provenance_block_ids",
  "display_steps",
  "_render_generic_narrative_proof_block",
  "redundant_direct_premise_step_ids",
  "relocated_direct_premise_ids",
)

def read(path):
  return path.read_bytes().decode("utf-8-sig").replace("\r\n", "\n")

for path in paths:
  print("=" * 78)
  print(path)
  print("=" * 78)
  text = read(path)
  lines = text.splitlines()

  hits = sorted({
    i
    for i, line in enumerate(lines)
    if any(needle in line for needle in needles)
  })

  ranges = []
  for hit in hits:
    start = max(0, hit - 25)
    end = min(len(lines), hit + 45)
    if ranges and start <= ranges[-1][1]:
      ranges[-1] = (ranges[-1][0], max(ranges[-1][1], end))
    else:
      ranges.append((start, end))

  for start, end in ranges:
    print(f"\n--- lines {start + 1}-{end} ---")
    for i in range(start, end):
      print(f"{i + 1:04d}: {lines[i]}")
