"""Minimal and guarded installation into the repository root."""
from pathlib import Path
import shutil

root = Path.cwd()
package = Path(__file__).resolve().parent
provider = root / "phase165_r8_rule_provider.py"
registry = root / "phase165_r10_rule_registry.py"
if not provider.is_file() or not registry.is_file():
    raise SystemExit("Run from the EHP Proof Tracer repository root")
original = provider.read_text(encoding="utf-8")
old = '    "homomorphism_rules", "indeterminacy_rules",'
new = '    "homomorphism_rules", "indeterminacy_rules", "phase165_r12_r2_quotient_rules",'
if old not in original and new not in original:
    raise SystemExit("Provider catalog differs from audited GitHub code; no changes applied")
if not (root / "proof.py").is_file() or not (root / "map_property_rules.py").is_file():
    raise SystemExit("Missing required project modules")
source = package / "phase165_r12_r2_quotient_rules.py"
target = root / source.name
if target.exists() and target.read_bytes() != source.read_bytes():
    raise SystemExit("Rule module already exists with different content; no changes applied")
tests_dir = root / "tests"
if not tests_dir.is_dir():
    raise SystemExit("Missing tests directory")
test_source = package / "tests" / "test_phase165_r12_r2_quotient_rules.py"
test_target = tests_dir / test_source.name
if test_target.exists() and test_target.read_bytes() != test_source.read_bytes():
    raise SystemExit("Test file already exists with different content; no changes applied")
if original != original.replace(old, new):
    provider.write_text(original.replace(old, new), encoding="utf-8")
shutil.copy2(source, target)
shutil.copy2(test_source, test_target)
print("R12-R2 installed: two shared inference rules; no target-specific adapter")
