from pathlib import Path

path = Path("toda_group_proof_narrative_arguments.py")
text = path.read_text(encoding="utf-8")

old = """  return tuple(
    block_index
    for block_index in range(
      len(
        direct_dependencies
      )
    )
    if block_index in visited
  )
"""

new = """  visited.discard(
    conclusion_index
  )

  return tuple(
    block_index
    for block_index in range(
      len(
        direct_dependencies
      )
    )
    if block_index in visited
  )
"""

if old not in text:
    raise RuntimeError(
        "Phase 143-7 closure return block was not found; no file was changed."
    )

path.write_text(
    text.replace(old, new, 1),
    encoding="utf-8",
)
print("Updated:", path)
