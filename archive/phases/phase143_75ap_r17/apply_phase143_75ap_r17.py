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

old = """      display_steps = tuple(
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
              and is_toda_group_proof_narrative_provenance_only_statement(
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
              and is_toda_group_proof_narrative_provenance_only_statement(
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
              and id(
                proof_step
              ) in redundant_direct_premise_step_ids
            )
            or id(
              proof_step
            ) not in redundant_direct_premise_step_ids
          )
          and (
            id(
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
    "Exact R16-R2 display_steps block not found; no files changed."
  )

text = text.replace(old, new, 1)
write(BODY, text, bom, nl)

print("Phase 143-75AP R17 patch applied.")
