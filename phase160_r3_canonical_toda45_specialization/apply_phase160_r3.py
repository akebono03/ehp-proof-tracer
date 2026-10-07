from pathlib import Path
import shutil

package_root = Path(__file__).resolve().parent
repo_root = package_root.parent

required = repo_root / "stable_rules.py"
if not required.exists():
    raise SystemExit(
        "stable_rules.py was not found in repository root"
    )

stable_text = required.read_text(encoding="utf-8")
required_names = (
    "canonical_toda_stable_base",
    "toda_primary_group_stem",
    "toda_stable_transport_exponent",
)
missing = [
    name for name in required_names
    if f"def {name}(" not in stable_text
]
if missing:
    raise SystemExit(
        "Phase 160-R2 is required before R3. Missing: "
        + ", ".join(missing)
    )

copies = (
    (
        package_root / "files" / "toda_stable_transport.py",
        repo_root / "toda_stable_transport.py",
    ),
    (
        package_root / "files" / "tests" / "test_phase160_canonical_toda45_specialization.py",
        repo_root / "tests" / "test_phase160_canonical_toda45_specialization.py",
    ),
)

for source, destination in copies:
    destination.parent.mkdir(parents=True, exist_ok=True)
    shutil.copy2(source, destination)

print("Applied Phase 160-R3 files:")
print("  toda_stable_transport.py")
print("  tests/test_phase160_canonical_toda45_specialization.py")
