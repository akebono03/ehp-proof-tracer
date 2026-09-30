from pathlib import Path
import shutil

ROOT = Path.cwd()
PACKAGE = ROOT / "phase150_rc4_7d_r1_repair1"
TARGET = ROOT / "toda_group_proof_narrative_reason_renderer.py"
TEST_TARGET = ROOT / "tests" / "test_phase150_rc4_7d_reason_hidden_conclusion_anchor.py"

if not TARGET.exists():
  raise SystemExit(f"missing production file: {TARGET}")

backup = PACKAGE / "backup_toda_group_proof_narrative_reason_renderer.py"
if not backup.exists():
  shutil.copy2(TARGET, backup)

source = TARGET.read_text(encoding="utf-8")

anchor = "def insert_toda_group_proof_narrative_reason_prose(\n"
helper = '''def _toda_group_proof_narrative_reason_insertion_index(
  markdown: str,
  reason: TodaGroupProofNarrativeReason,
  reason_sidecar: TodaGroupProofNarrativeReasonSidecar,
) -> int | None:
  conclusion_line = _render_generic_narrative_step(
    reason.conclusion_step
  )
  if conclusion_line:
    conclusion_index = markdown.find(conclusion_line)
    if conclusion_index >= 0:
      return conclusion_index

  children_by_step_id = {}
  for edge in reason_sidecar.presentation.edges:
    children_by_step_id.setdefault(
      id(edge.premise_step),
      [],
    ).append(edge.parent_step)

  queue = list(
    children_by_step_id.get(
      id(reason.conclusion_step),
      (),
    )
  )
  visited_step_ids = {
    id(reason.conclusion_step),
  }

  while queue:
    next_queue = []
    for proof_step in queue:
      proof_step_id = id(proof_step)
      if proof_step_id in visited_step_ids:
        continue
      visited_step_ids.add(proof_step_id)

      rendered_line = _render_generic_narrative_step(
        proof_step
      )
      if rendered_line:
        rendered_index = markdown.find(rendered_line)
        if rendered_index >= 0:
          return rendered_index

      next_queue.extend(
        children_by_step_id.get(
          proof_step_id,
          (),
        )
      )
    queue = next_queue

  return None


'''
if "_toda_group_proof_narrative_reason_insertion_index(" not in source:
  if anchor not in source:
    raise SystemExit("insert function anchor not found")
  source = source.replace(anchor, helper + anchor, 1)

old = '''    conclusion_line = _render_generic_narrative_step(
      reason.conclusion_step
    )
    if not conclusion_line:
      continue

    conclusion_index = rendered.find(conclusion_line)
    if conclusion_index < 0:
      continue

    prefix = sentence + "\\n\\n"
    if rendered[
      max(0, conclusion_index - len(prefix)):
      conclusion_index
    ] == prefix:
      continue

    rendered = (
      rendered[:conclusion_index]
      + prefix
      + rendered[conclusion_index:]
    )
'''
new = '''    insertion_index = (
      _toda_group_proof_narrative_reason_insertion_index(
        rendered,
        reason,
        reason_sidecar,
      )
    )
    if insertion_index is None:
      continue

    prefix = sentence + "\\n\\n"
    if rendered[
      max(0, insertion_index - len(prefix)):
      insertion_index
    ] == prefix:
      continue

    rendered = (
      rendered[:insertion_index]
      + prefix
      + rendered[insertion_index:]
    )
'''
if old not in source:
  raise SystemExit(
    "expected reason insertion body not found; "
    "local file differs from RC4-7D R1 state"
  )

source = source.replace(old, new, 1)
TARGET.write_text(source, encoding="utf-8")

test_source = PACKAGE / "test_phase150_rc4_7d_reason_hidden_conclusion_anchor.py"
TEST_TARGET.write_text(
  test_source.read_text(encoding="utf-8"),
  encoding="utf-8",
)

print("RC4-7D R1 Repair 1 applied.")
