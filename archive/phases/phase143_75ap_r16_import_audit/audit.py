from pathlib import Path

path = Path("toda_group_proof_narrative_argument_body_renderer.py")
text = path.read_bytes().decode("utf-8-sig").replace("\r\n", "\n")
lines = text.splitlines()

print("=" * 78)
print("IMPORT / HEADER")
print("=" * 78)
for i, line in enumerate(lines[:180], 1):
  print(f"{i:04d}: {line}")

print()
print("=" * 78)
print("DISPLAY_STEPS CONTEXT")
print("=" * 78)

hits = [
  i for i, line in enumerate(lines)
  if "display_steps = tuple(" in line
]

if not hits:
  raise RuntimeError("display_steps = tuple( not found")

for hit in hits:
  start = max(0, hit - 35)
  end = min(len(lines), hit + 90)
  print(f"\n--- occurrence at line {hit + 1} ---")
  for i in range(start, end):
    print(f"{i + 1:04d}: {lines[i]}")
