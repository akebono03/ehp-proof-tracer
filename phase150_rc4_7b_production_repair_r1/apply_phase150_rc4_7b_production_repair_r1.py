from pathlib import Path
import shutil

ROOT = Path.cwd()
TARGET = ROOT / "toda_group_proof_narrative_transition_renderer.py"
PACKAGE = ROOT / "phase150_rc4_7b_production_repair_r1"
UPDATED = PACKAGE / "updated_toda_group_proof_narrative_transition_renderer.py.txt"
TEST_SOURCE = PACKAGE / "test_phase150_rc4_7b_production_repair.py"
TEST_TARGET = ROOT / "tests" / "test_phase150_rc4_7b_production_repair.py"

if not TARGET.exists():
  raise SystemExit(f"missing production file: {TARGET}")

if not UPDATED.exists():
  raise SystemExit(f"missing updated source: {UPDATED}")

if not TEST_SOURCE.exists():
  raise SystemExit(f"missing test source: {TEST_SOURCE}")

current = TARGET.read_text(encoding="utf-8")
required_fragments = (
  "def render_toda_group_proof_narrative_transition_connector(",
  'return "以上より、"',
  "TodaGroupProofNarrativeTransitionRole",
)

for fragment in required_fragments:
  if fragment not in current:
    raise SystemExit(
      "current production file does not match the expected RC4-7B baseline: "
      + repr(fragment)
    )

backup = PACKAGE / "backup_toda_group_proof_narrative_transition_renderer.py"
if not backup.exists():
  shutil.copy2(TARGET, backup)

TARGET.write_text(
  UPDATED.read_text(encoding="utf-8"),
  encoding="utf-8",
)

TEST_TARGET.write_text(
  TEST_SOURCE.read_text(encoding="utf-8"),
  encoding="utf-8",
)

print("RC4-7B Production Repair R1 applied.")
print("Changed production file:")
print("  toda_group_proof_narrative_transition_renderer.py")
print("Added test file:")
print("  tests/test_phase150_rc4_7b_production_repair.py")
