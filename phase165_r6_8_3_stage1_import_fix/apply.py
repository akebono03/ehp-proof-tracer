from pathlib import Path
import ast
import shutil

path = Path.cwd() / "probes" / "probe_phase54_capabilities.py"
if not path.is_file():
    raise SystemExit(f"MISSING: {path}")
source = path.read_text(encoding="utf-8")
old = "from probes.probe_phase50_capabilities import (\n  print_separator,\n)"
new = "from probes.probe_phase49_capabilities import (\n  print_separator,\n)"
if old in source:
    changed = source.replace(old, new, 1)
    ast.parse(changed)
    backup = path.with_suffix(path.suffix + ".r6_8_3_import.bak")
    if not backup.exists():
        shutil.copy2(path, backup)
    path.write_text(changed, encoding="utf-8")
    print("APPLIED: Phase 54 no longer imports the retired Phase 50 module")
elif new in source and old not in source:
    print("ALREADY APPLIED: Phase 54 imports print_separator from Phase 49")
else:
    raise SystemExit("BLOCKED: Phase 54 import differs from inspected source")
