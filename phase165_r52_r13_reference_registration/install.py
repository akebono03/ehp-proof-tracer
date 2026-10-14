"""Install R52-R13 only if R52-R12 wiring is exactly present."""
from pathlib import Path
import shutil

package = Path(__file__).resolve().parent
root = Path.cwd()
shared = root / "phase165_r52_r9_shared_math.py"
if not shared.is_file() or not (root / "phase165_r52_r12_component_bridge.py").is_file():
    raise SystemExit("Expected repository root with R52-R12 installed")
content = shared.read_text(encoding="utf-8")
needle = "        sources = (production, build_adopted_typed_reference_registry(adopted_tex))"
replacement = (
    "        from phase165_r52_r13_reference_registration import build_adopted_prop51_reference\n"
    "        sources = (production, build_adopted_typed_reference_registry(adopted_tex),\n"
    "                   build_adopted_prop51_reference())"
)
if replacement in content:
    print("R52-R13 shared registration already installed")
elif content.count(needle) == 1:
    backup = shared.with_name(shared.name + ".r52_r13_backup")
    if not backup.exists():
        shutil.copy2(shared, backup)
    shared.write_text(content.replace(needle, replacement), encoding="utf-8")
    print("R52-R13 shared registration installed")
else:
    raise SystemExit("Shared registration signature differs; no files modified")
for filename in (
    "phase165_r52_r13_reference_registration.py",
    "test_phase165_r52_r13_reference_registration.py",
):
    shutil.copy2(package / filename, root / filename)
