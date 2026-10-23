from __future__ import annotations

import ast
from pathlib import Path
import shutil

package = Path(__file__).resolve().parent
project = package.parent
target = project / "phase168_r3_37c_reference_projection.py"
replacement = (package / target.name).read_text(encoding="utf-8")
ast.parse(replacement)
old = target.read_text(encoding="utf-8")
if old == replacement:
    print("ALREADY_APPLIED:", target)
elif (
    'def project_reference_bodies(registry, assertion_ids):' in old
    and 'r"$\\cdots\\xrightarrow{\\Delta}\\pi_q^p"' in old
    and "Toda51BelowDiagonalZeroStatement" not in old
):
    backup = package / "backup" / target.name
    backup.parent.mkdir(parents=True, exist_ok=True)
    shutil.copy2(target, backup)
    target.write_text(replacement, encoding="utf-8")
    print("PATCHED:", target)
    print("BACKUP:", backup)
else:
    raise SystemExit("UNEXPECTED_SOURCE: current file differs from reviewed R3-37D; no modifications made")
print("FULL_FUNCTION:", package / target.name)
