from pathlib import Path
import shutil

package_root = Path(__file__).resolve().parent
repo_root = package_root.parent

source = (
    package_root
    / "files"
    / "tests"
    / "test_phase160_k2_generic_transport_connection.py"
)
target = (
    repo_root
    / "tests"
    / "test_phase160_k2_generic_transport_connection.py"
)

if not target.exists():
    raise SystemExit(
        "Phase 160-R8 test file was not found; "
        "apply Phase 160-R8 before repair1"
    )

shutil.copy2(
    source,
    target,
)

print("Applied Phase 160-R8 repair1:")
print("  tests/test_phase160_k2_generic_transport_connection.py")
print("  synthetic low-dimensional fixtures replaced by real Phase 59 fixtures")
