from pathlib import Path
from datetime import datetime
import ast
import shutil

package = Path(__file__).resolve().parent
project = package.parent
target = project / "phase168_r3_27_typed_statement_projection.py"
original = target.read_text(encoding="utf-8")
expected = (package / "expected_r3_27.sha256").read_text().strip()
import hashlib
if hashlib.sha256(original.encode("utf-8")).hexdigest() != expected:
    raise RuntimeError("R3-27 source differs from reviewed version; no change applied")
updated = (package / "phase168_r3_27_typed_statement_projection_FULL.py").read_text(encoding="utf-8")
ast.parse(updated)
backup = package / "backup" / datetime.now().strftime("%Y%m%dT%H%M%S")
backup.mkdir(parents=True, exist_ok=True)
shutil.copy2(target, backup / target.name)
target.write_text(updated, encoding="utf-8")
print("PATCHED:", target)
print("BACKUP:", backup / target.name)
print("FULL MODULE:", package / "phase168_r3_27_typed_statement_projection_FULL.py")
