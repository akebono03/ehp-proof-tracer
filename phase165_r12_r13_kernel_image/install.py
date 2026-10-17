"""Guarded installer for R12-R13. Local uncommitted changes are preserved."""
from __future__ import annotations

import ast
from pathlib import Path
import shutil


def main() -> None:
    project = Path.cwd()
    package = Path(__file__).resolve().parent
    payload = package / "payload" / "phase165_r12_r13_kernel_image.py"
    target = project / payload.name
    shared_path = project / "phase165_r52_r9_shared_math.py"
    for required in (shared_path, project / "phase165_r12_r12_ehp_consequences.py", project / "phase165_r12_r11_prop42_unified.py"):
        if not required.is_file():
            raise FileNotFoundError(required)
    original = shared_path.read_text(encoding="utf8")
    anchor = "    extra_providers = (build_exactness_binding_provider(bridge), "
    marker = "    from phase165_r12_r13_kernel_image import build_concrete_kernel_provider"
    if marker in original:
        changed = original
    else:
        if original.count(anchor) != 1:
            raise RuntimeError("Unexpected shared provider structure; refusing to modify")
        insertion = (
            "    from phase165_r12_r13_kernel_image import build_concrete_kernel_provider\n"
            "    extra_providers = (build_concrete_kernel_provider(bridge),) + tuple(extra_providers)\n"
        )
        changed = original.replace(anchor, insertion + anchor, 1)
    new_module = payload.read_text(encoding="utf8")
    ast.parse(new_module, filename=str(payload))
    ast.parse(changed, filename=str(shared_path))
    if target.is_file() and target.read_text(encoding="utf8") != new_module:
        raise RuntimeError("Existing R12-R13 module differs; refusing to overwrite")
    if changed != original:
        backup = shared_path.with_name(shared_path.name + ".r12_r13.bak")
        if not backup.exists():
            shutil.copy2(shared_path, backup)
        shared_path.write_text(changed, encoding="utf8")
        print("Updated:", shared_path.name)
    else:
        print("Already connected:", shared_path.name)
    if not target.exists():
        shutil.copy2(payload, target)
        print("Added:", target.name)
    print("R12-R13 generic concrete kernel provider installed. Full pytest NOT run.")


if __name__ == "__main__":
    main()
