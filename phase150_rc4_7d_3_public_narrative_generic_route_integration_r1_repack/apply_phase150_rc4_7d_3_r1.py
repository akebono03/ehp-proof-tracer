from pathlib import Path
import shutil

ROOT = Path.cwd()
PACKAGE = ROOT / "phase150_rc4_7d_3_public_narrative_generic_route_integration_r1_repack"
TARGET = ROOT / "toda_group_proof_narrative_renderer.py"
TEST_TARGET = ROOT / "tests" / "test_phase150_rc4_7d_3_public_narrative_generic_route.py"

if not TARGET.exists():
  raise SystemExit(f"missing production file: {TARGET}")

backup = PACKAGE / "backup_toda_group_proof_narrative_renderer.py"
if not backup.exists():
  shutil.copy2(TARGET, backup)

source = TARGET.read_text(encoding="utf-8")
anchor = "def render_toda_group_proof_narrative_markdown(\n"

helper = '''def _is_phase150_rc4_generic_route_target(
  presentation: TodaGroupProofPresentation,
) -> bool:
  if presentation.max_depth < 2:
    return False

  target = (
    presentation
    .source_replay
    .group_result
    .target
  )

  return (
    (
      target.group_dimension == 10
      and target.sphere_dimension == 4
    )
    or (
      target.group_dimension == 12
      and target.sphere_dimension == 5
    )
    or (
      target.group_dimension == 16
      and target.sphere_dimension == 9
    )
  )


'''

if "_is_phase150_rc4_generic_route_target(" not in source:
  if anchor not in source:
    raise SystemExit("public narrative renderer anchor not found")
  source = source.replace(anchor, helper + anchor, 1)

start = source.find(anchor)
if start < 0:
  raise SystemExit("public narrative renderer not found")

old_function = source[start:]
needle = '''  if (
    _is_phase134_3_pi6_3_presentation(
      presentation
    )
  ):
'''
replacement = '''  if (
    _is_phase134_3_pi6_3_presentation(
      presentation
    )
    or _is_phase150_rc4_generic_route_target(
      presentation
    )
  ):
'''
if needle not in old_function:
  raise SystemExit("existing generic-route dispatch not found")

new_function = old_function.replace(
  needle,
  replacement,
  1,
)
source = source[:start] + new_function
TARGET.write_text(source, encoding="utf-8")

test_source = PACKAGE / "test_phase150_rc4_7d_3_public_narrative_generic_route.py"
if not test_source.exists():
  raise SystemExit(f"missing packaged test source: {test_source}")
TEST_TARGET.write_text(
  test_source.read_text(encoding="utf-8"),
  encoding="utf-8",
)

print("RC4-7D-3 Public Narrative Generic Route Integration R1 applied.")
print("Changed: toda_group_proof_narrative_renderer.py")
print("Added: tests/test_phase150_rc4_7d_3_public_narrative_generic_route.py")
