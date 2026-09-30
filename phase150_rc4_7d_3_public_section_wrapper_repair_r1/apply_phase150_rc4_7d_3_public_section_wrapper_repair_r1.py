from pathlib import Path
import shutil

ROOT = Path.cwd()
PACKAGE = ROOT / "phase150_rc4_7d_3_public_section_wrapper_repair_r1"
TARGET = ROOT / "toda_group_proof_narrative_renderer.py"

if not TARGET.exists():
  raise SystemExit(f"missing production file: {TARGET}")

backup = PACKAGE / "backup_toda_group_proof_narrative_renderer.py"
if not backup.exists():
  shutil.copy2(TARGET, backup)

source = TARGET.read_text(encoding="utf-8")

target_helper_anchor = "def _is_phase150_rc4_generic_route_target(\n"

wrapper_helper = """def _wrap_phase150_rc4_generic_public_narrative(
  rendered: str,
) -> str:
  if not isinstance(rendered, str):
    raise TypeError("rendered must be a str")

  lines = rendered.splitlines()
  reference_line_indices = [
    index
    for index, line in enumerate(lines)
    if line.startswith("**[R")
  ]

  if not reference_line_indices:
    return rendered

  last_reference_index = reference_line_indices[-1]
  reference_lines = lines[
    :last_reference_index + 1
  ]
  proof_lines = lines[
    last_reference_index + 1:
  ]

  while proof_lines and not proof_lines[0]:
    proof_lines.pop(0)

  wrapped_lines = [
    "# Group proof narrative",
    "",
    "## 使用する結果",
    "",
    *reference_lines,
    "",
    "## 証明",
    "",
    *proof_lines,
  ]

  return "\\n".join(wrapped_lines).rstrip() + "\\n"


"""

if "_wrap_phase150_rc4_generic_public_narrative(" not in source:
  if target_helper_anchor not in source:
    raise SystemExit(
      "RC4 generic-route target helper not found; "
      "RC4-7D-3 R1 must already be applied"
    )
  source = source.replace(
    target_helper_anchor,
    wrapper_helper + target_helper_anchor,
    1,
  )

old_return = """    return (
      render_toda_group_proof_narrative_multi_argument_with_contributions_markdown(
        presentation,
        blocks,
        semantic_sidecar,
        arguments,
      )
    )
"""

new_return = """    rendered = (
      render_toda_group_proof_narrative_multi_argument_with_contributions_markdown(
        presentation,
        blocks,
        semantic_sidecar,
        arguments,
      )
    )

    if _is_phase150_rc4_generic_route_target(
      presentation
    ):
      return _wrap_phase150_rc4_generic_public_narrative(
        rendered
      )

    return rendered
"""

if old_return not in source:
  if new_return in source:
    print("RC4-7D-3 public section wrapper already applied.")
    raise SystemExit(0)
  raise SystemExit("generic contribution return block not found")

source = source.replace(old_return, new_return, 1)
TARGET.write_text(source, encoding="utf-8")

print("RC4-7D-3 public section wrapper repair applied.")
print("Changed: toda_group_proof_narrative_renderer.py")
print("Import changes: none.")
