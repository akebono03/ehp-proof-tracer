"""Check the distribution and the exact installer anchors before touching production."""
from __future__ import annotations

import ast
from pathlib import Path
from phase169_r3k_narrative_localization.apply import HERE, ROOT, TARGET, HELPER_SOURCE, patch_function


def main() -> None:
    required = (
        HERE / "apply.py", HERE / "audit.py", HERE / "run.ps1",
        HERE / "phase169_r3k_narrative_projection.py",
        HERE / "tests/test_phase169_r3k_narrative_localization.py",
        ROOT / "phase168_r3_41l_reasoned_prose/tests/test_phase168_r3_41l_reasoned_prose.py",
        ROOT / "phase169_r3j_narrative_boundary_audit/audit.py",
        ROOT / "phase169_r3j_narrative_boundary_audit/tests/test_r3j_narrative_boundary_audit.py",
    )
    for path in required:
        if not path.exists():
            raise RuntimeError("R3K_MISSING: " + str(path))
    source = TARGET.read_text(encoding="utf-8-sig").replace("\r\n", "\n")
    revised, function = patch_function(source)
    ast.parse(revised)
    ast.parse(HELPER_SOURCE.read_text(encoding="utf-8"))
    if len(function.splitlines()) < 180:
        raise RuntimeError("R3K full renderer function is too small")
    print("R3K_PREFLIGHT_OK=True",flush=True)


if __name__ == "__main__":
    main()
