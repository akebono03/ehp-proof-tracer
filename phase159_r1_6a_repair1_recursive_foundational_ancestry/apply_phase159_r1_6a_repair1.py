from pathlib import Path
from datetime import datetime
import shutil

ROOT = Path(__file__).resolve().parents[1]
RENDERER = ROOT / "toda_group_proof_narrative_renderer.py"

NEW_RENDER_FOUNDATIONAL = 'def _phase159_render_foundational_reference_section(\n  presentation: TodaGroupProofPresentation,\n) -> str:\n  if not isinstance(\n    presentation,\n    TodaGroupProofPresentation,\n  ):\n    raise TypeError(\n      "presentation must be a "\n      "TodaGroupProofPresentation"\n    )\n\n  entries = []\n  index_by_key = {}\n  seen_step_ids = set()\n\n  def visit(\n    proof_step: ProofStep,\n  ) -> None:\n    step_id = id(\n      proof_step\n    )\n\n    if step_id in seen_step_ids:\n      return\n\n    seen_step_ids.add(\n      step_id\n    )\n\n    identity = (\n      proof_step.foundational_reference\n    )\n\n    if identity is not None:\n      if not isinstance(\n        identity,\n        FoundationalReferenceIdentity,\n      ):\n        raise TypeError(\n          "foundational_reference must be a "\n          "FoundationalReferenceIdentity or None"\n        )\n\n      existing_index = (\n        index_by_key.get(\n          identity.key\n        )\n      )\n\n      if existing_index is None:\n        index_by_key[\n          identity.key\n        ] = len(\n          entries\n        )\n        entries.append(\n          [\n            identity,\n            [\n              proof_step,\n            ],\n          ]\n        )\n      else:\n        entries[\n          existing_index\n        ][\n          1\n        ].append(\n          proof_step\n        )\n\n    for premise in proof_step.premises:\n      if isinstance(\n        premise,\n        ProofStep,\n      ):\n        visit(\n          premise\n        )\n\n  visit(\n    presentation.root_step\n  )\n\n  if not entries:\n    return ""\n\n  lines = []\n\n  for number, (\n    identity,\n    proof_steps,\n  ) in enumerate(\n    entries,\n    start=1,\n  ):\n    lines.append(\n      "**[F"\n      + str(\n        number\n      )\n      + "] "\n      + identity.label\n      + ".**"\n    )\n\n    seen_statements = set()\n\n    for proof_step in proof_steps:\n      statement = (\n        _phase159_foundational_reference_statement(\n          proof_step\n        )\n      )\n\n      if statement in seen_statements:\n        continue\n\n      seen_statements.add(\n        statement\n      )\n      lines.append(\n        statement\n      )\n\n  return "\\n".join(\n    lines\n  )\n'
NEW_INJECT = 'def _phase159_inject_foundational_reference_section(\n  presentation: TodaGroupProofPresentation,\n  rendered: str,\n) -> str:\n  if not isinstance(\n    rendered,\n    str,\n  ):\n    raise TypeError(\n      "rendered must be a str"\n    )\n\n  foundational = (\n    _phase159_render_foundational_reference_section(\n      presentation\n    )\n  )\n\n  if not foundational:\n    return rendered\n\n  reference_marker = (\n    "## 使用する結果\\n\\n"\n  )\n  proof_boundary = (\n    "---\\n\\n## 証明"\n  )\n  reference_start = rendered.find(\n    reference_marker\n  )\n\n  if reference_start < 0:\n    return rendered\n\n  content_start = (\n    reference_start\n    + len(\n      reference_marker\n    )\n  )\n  boundary_index = rendered.find(\n    proof_boundary,\n    content_start,\n  )\n\n  if boundary_index < 0:\n    return rendered\n\n  existing = rendered[\n    content_start:\n    boundary_index\n  ].strip()\n\n  if existing:\n    replacement = (\n      existing\n      + "\\n\\n"\n      + foundational\n    )\n  else:\n    replacement = foundational\n\n  return (\n    rendered[\n      :content_start\n    ]\n    + replacement\n    + "\\n\\n"\n    + rendered[\n      boundary_index:\n    ]\n  )\n'

def replace_function(
  source,
  function_name,
  replacement,
):
  marker = (
    "def "
    + function_name
    + "("
  )
  start = source.find(
    marker
  )

  if start < 0:
    raise RuntimeError(
      "function not found: "
      + function_name
    )

  next_function = source.find(
    "\ndef ",
    start + len(
      marker
    ),
  )

  end = (
    len(
      source
    )
    if next_function < 0
    else next_function + 1
  )

  return (
    source[:start]
    + replacement.rstrip()
    + "\n\n"
    + source[end:]
  )

def main():
  if not RENDERER.exists():
    raise FileNotFoundError(
      RENDERER
    )

  stamp = datetime.now().strftime(
    "%Y%m%d_%H%M%S"
  )
  backup_dir = (
    ROOT
    / (
      "phase159_r1_6a_repair1_backup_"
      + stamp
    )
  )
  backup_dir.mkdir(
    parents=True,
    exist_ok=False,
  )
  shutil.copy2(
    RENDERER,
    backup_dir / RENDERER.name,
  )

  source = RENDERER.read_text(
    encoding="utf-8-sig"
  )

  source = replace_function(
    source,
    "_phase159_render_foundational_reference_section",
    NEW_RENDER_FOUNDATIONAL,
  )
  source = replace_function(
    source,
    "_phase159_inject_foundational_reference_section",
    NEW_INJECT,
  )

  RENDERER.write_text(
    source,
    encoding="utf-8",
    newline="\n",
  )

  print(
    "Phase 159-R1-6a repair1 applied."
  )
  print(
    "Backup:",
    backup_dir,
  )
  print(
    "Foundational references now use recursive premise ancestry."
  )
  print(
    "Reference separator matching was corrected."
  )

if __name__ == "__main__":
  main()
