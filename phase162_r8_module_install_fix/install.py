"""Install the missing Phase 162 Web replay module at the repository root."""
from pathlib import Path
import ast
import shutil

bundle = Path(__file__).resolve().parent
repo = bundle.parent
source = bundle / "phase162_pi5_3_web_replay.py"
destination = repo / "phase162_pi5_3_web_replay.py"
web_file = repo / "web_group_proof.py"

if not source.is_file() or not web_file.is_file():
    raise FileNotFoundError("Run this bundle inside the EHP Proof Tracer repository")
source_text = source.read_text(encoding="utf-8")
ast.parse(source_text)
web_text = web_file.read_text(encoding="utf-8-sig")
if "from phase162_pi5_3_web_replay import" not in web_text:
    raise RuntimeError("R8 Web route is not installed; do not install an unused module")
if destination.exists():
    current_text = destination.read_text(encoding="utf-8-sig")
    if current_text == source_text:
        print("Already installed:", destination)
    else:
        backup = repo / "phase162_pi5_3_web_replay.py.phase162_r8_install_before.bak"
        if not backup.exists():
            shutil.copy2(destination, backup)
        shutil.copy2(source, destination)
        print("Updated:", destination)
        print("Backup:", backup)
else:
    shutil.copy2(source, destination)
    print("Installed:", destination)
