from pathlib import Path
import shutil

package_root = Path(__file__).resolve().parent
repo_root = package_root.parent

required_files = (
    repo_root / "stable_rules.py",
    repo_root / "toda_stable_transport.py",
)
for required in required_files:
    if not required.exists():
        raise SystemExit(
            f"required Phase 160 file not found: {required.name}"
        )

copies = (
    (
        package_root / "files" / "toda_stable_group_transport.py",
        repo_root / "toda_stable_group_transport.py",
    ),
    (
        package_root / "files" / "tests" / "test_phase160_generic_finite_cyclic_transport.py",
        repo_root / "tests" / "test_phase160_generic_finite_cyclic_transport.py",
    ),
)

for source, destination in copies:
    destination.parent.mkdir(parents=True, exist_ok=True)
    shutil.copy2(source, destination)

print("Applied Phase 160-R4 files:")
print("  toda_stable_group_transport.py")
print("  tests/test_phase160_generic_finite_cyclic_transport.py")
