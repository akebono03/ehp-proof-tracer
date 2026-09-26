from pathlib import Path
import ast

PATH = Path(
  "toda_group_proof_narrative_argument_body_renderer.py"
)

raw = PATH.read_bytes()
text = raw.decode(
  "utf-8-sig"
)
tree = ast.parse(
  text
)

TARGETS = {
  "render_toda_group_proof_narrative_argument_body_markdown",
  "_render_toda_group_proof_narrative_non_exact_block",
  "_render_toda_group_proof_narrative_exactness_block",
}

print(
  "=" * 78
)
print(
  "Phase 143-75AP R12B body selection source audit"
)
print(
  "=" * 78
)

for node in tree.body:
  if not isinstance(
    node,
    ast.FunctionDef,
  ):
    continue

  source = ast.get_source_segment(
    text,
    node,
  )

  if source is None:
    continue

  if (
    node.name in TARGETS
    or "render_blocks" in source
    or "excluded_non_exact_block_ids" in source
    or "seen_local_block_ids" in source
    or "filter_toda_group_proof_narrative_exactness_body_contributions"
    in source
  ):
    print(
      "\n"
      + "=" * 78
    )
    print(
      "FUNCTION:",
      node.name
    )
    print(
      "=" * 78
    )
    print(
      source
    )
