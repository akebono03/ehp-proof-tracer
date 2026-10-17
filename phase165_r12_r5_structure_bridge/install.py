"""Guarded R12-R5 installation from the repository root."""
from pathlib import Path
import shutil

root = Path.cwd()
package = Path(__file__).resolve().parent
provider = root / "phase165_r8_rule_provider.py"
needed = ("proof.py", "phase165_r10_rule_registry.py", "phase165_r12_r2_quotient_rules.py")
if not provider.is_file() or any(not (root / item).is_file() for item in needed):
    raise SystemExit("Run in project root after installing R12-R2")
original = provider.read_text(encoding="utf-8")
old = '    "homomorphism_rules", "indeterminacy_rules", "phase165_r12_r2_quotient_rules",'
new = (
    '    "homomorphism_rules", "indeterminacy_rules", "phase165_r12_r2_quotient_rules",\n'
    '    "phase165_r12_r5_structure_bridge",'
)
if old not in original and new not in original:
    raise SystemExit("Unexpected provider module tuple; refusing to modify")
if old in original and original.count(old) != 1:
    raise SystemExit("Ambiguous provider module tuple; refusing to modify")
files = (
    (package / "phase165_r12_r5_structure_bridge_audit.py", root / "phase165_r12_r5_structure_bridge_audit.py"),
    (package / "phase165_r12_r5_structure_bridge.py", root / "phase165_r12_r5_structure_bridge.py"),
    (package / "tests" / "test_phase165_r12_r5_structure_bridge.py", root / "tests" / "test_phase165_r12_r5_structure_bridge.py"),
)
for src, dst in files:
    if not dst.parent.is_dir():
        raise SystemExit("Missing target directory: " + str(dst.parent))
    if dst.exists() and src.read_bytes() != dst.read_bytes():
        raise SystemExit("Existing file differs, refusing overwrite: " + str(dst))
if new not in original:
    provider.write_text(original.replace(old, new), encoding="utf-8")
for src, dst in files:
    shutil.copy2(src, dst)
print("R12-R5 generic finite-cyclic relation bridge installed (no pi43 adapter)")
