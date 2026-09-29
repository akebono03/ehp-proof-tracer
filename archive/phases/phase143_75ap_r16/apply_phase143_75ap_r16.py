from pathlib import Path
import ast

BODY = Path("toda_group_proof_narrative_argument_body_renderer.py")

def read(path):
  raw = path.read_bytes()
  bom = raw.startswith(b"\xef\xbb\xbf")
  nl = "\r\n" if b"\r\n" in raw else "\n"
  return raw.decode("utf-8-sig").replace("\r\n", "\n"), bom, nl

def write(path, text, bom, nl):
  ast.parse(text)
  if nl == "\r\n":
    text = text.replace("\n", "\r\n")
  path.write_text(
    text,
    encoding="utf-8-sig" if bom else "utf-8",
    newline="",
  )

text, bom, nl = read(BODY)

# Ensure aggregate predicate is available. Prefer an existing import.
if "is_toda_group_proof_aggregate_statement" not in text:
  marker = "from toda_group_proof_narrative_provenance import ("
  if marker not in text:
    raise RuntimeError(
      "Expected provenance import block not found; no files changed."
    )
  text = text.replace(
    marker,
    "from toda_group_proof_narrative_aggregate import (\n"
    "  is_toda_group_proof_aggregate_statement,\n"
    ")\n"
    + marker,
    1,
  )

old = """      preserve_direct_derivation_premises = (
        id(
          block
        ) in preserve_provenance_block_ids
      )

      display_steps = tuple(
        proof_step
        for proof_step in block.steps
        if (
          (
            context_hidden_step_ids is None
            or id(
              proof_step
            ) not in context_hidden_step_ids
          )
          and (
            preserve_direct_derivation_premises
            or id(
              proof_step
            ) not in redundant_direct_premise_step_ids
          )
          and (
            preserve_direct_derivation_premises
            or id(
              proof_step
            ) not in relocated_direct_premise_ids
            or (
              conclusion_step is not None
              and conclusion_step in block.steps
            )
          )
        )
      )
"""

new = """      display_steps = tuple(
        proof_step
        for proof_step in block.steps
        if (
          (
            context_hidden_step_ids is None
            or id(
              proof_step
            ) not in context_hidden_step_ids
          )
          and (
            (
              id(
                block
              ) in preserve_provenance_block_ids
              and is_toda_group_proof_aggregate_statement(
                proof_step.conclusion
              )
            )
            or id(
              proof_step
            ) not in redundant_direct_premise_step_ids
          )
          and (
            (
              id(
                block
              ) in preserve_provenance_block_ids
              and is_toda_group_proof_aggregate_statement(
                proof_step.conclusion
              )
            )
            or id(
              proof_step
            ) not in relocated_direct_premise_ids
            or (
              conclusion_step is not None
              and conclusion_step in block.steps
            )
          )
        )
      )
"""

if old not in text:
  raise RuntimeError(
    "R13 display_steps block not found exactly; no files changed."
  )

text = text.replace(old, new, 1)
write(BODY, text, bom, nl)

# Update only the three obsolete expectations that conflict with Phase143-51B.
updates = {
  Path("tests/test_phase143_59b_group_structure_duplicate_suppression.py"): (
    "test_phase143_59b_pi15_8_suppresses_transported_duplicate",
    "test_phase143_59b_pi15_8_keeps_transported_semantic_decomposition",
  ),
  Path("tests/test_phase143_61b_direct_premise_narrative.py"): (
    "test_phase143_61b_pi15_8_final_group_remains_single",
    "test_phase143_61b_pi15_8_keeps_transported_and_final_group",
  ),
  Path("tests/test_phase143_61b_r_semantic_suppression_priority.py"): (
    "test_phase143_61b_r_semantic_duplicate_suppression_precedes_relocation",
    "test_phase143_61b_r_semantic_aggregate_survives_relocation",
  ),
}

needle = """  assert (
    r"$\\pi_{15}^{8} \\cong "
    r"\\mathbb{Z}/8\\{E\\sigma'\\} "
    r"\\oplus \\mathbb{Z}\\{\\sigma_{8}\\}$"
    not in rendered
  )
"""
replacement = """  assert (
    r"$\\pi_{15}^{8} \\cong "
    r"\\mathbb{Z}/8\\{E\\sigma'\\} "
    r"\\oplus \\mathbb{Z}\\{\\sigma_{8}\\}$"
    in rendered
  )
"""

for path, (old_name, new_name) in updates.items():
  t, b, n = read(path)
  if old_name not in t:
    raise RuntimeError(f"Expected test function not found: {old_name}")
  if needle not in t:
    raise RuntimeError(f"Expected obsolete assertion not found in {path}")
  t = t.replace(old_name, new_name, 1)
  t = t.replace(needle, replacement, 1)
  write(path, t, b, n)

print("Phase 143-75AP R16 aggregate-only preservation patch applied.")
