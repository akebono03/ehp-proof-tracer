"""Minimal, guarded R12-R12 installation; no unrelated code replacement."""
from __future__ import annotations

import ast
from pathlib import Path
import shutil


def main() -> None:
    project = Path.cwd()
    package = Path(__file__).resolve().parent
    module = package / "payload" / "phase165_r12_r12_ehp_consequences.py"
    target = project / module.name
    shared_path = project / "phase165_r52_r9_shared_math.py"
    if not shared_path.is_file():
        raise FileNotFoundError(shared_path)
    if not (project / "phase165_r12_r11_prop42_unified.py").is_file():
        raise FileNotFoundError("R12-R11 installation required")
    original = shared_path.read_text(encoding="utf8")
    anchor = '    extra_providers = (build_exactness_binding_provider(bridge), build_prop42_specialization_provider(bridge)) + tuple(extra_providers)'
    new_lines = (
        '    from phase165_r12_r12_ehp_consequences import expand_ehp_exactness_consequences\n'
        '    extra_providers = (build_exactness_binding_provider(bridge), '
        'build_prop42_specialization_provider(bridge), '
        'expand_ehp_exactness_consequences) + tuple(extra_providers)'
    )
    marker = 'expand_ehp_exactness_consequences) + tuple(extra_providers)'
    if marker in original:
        changed = original
    elif original.count(anchor) == 1:
        changed = original.replace(anchor, new_lines, 1)
    else:
        raise RuntimeError("Unexpected R11 shared provider; refusing to patch")
    module_source = module.read_text(encoding="utf8")
    if target.exists() and target.read_text(encoding="utf8") != module_source:
        raise RuntimeError("Existing R12-R12 module differs; refusing overwrite")
    ast.parse(changed, filename=str(shared_path))
    ast.parse(module_source, filename=str(target))
    if original != changed:
        backup = shared_path.with_name(shared_path.name + ".r12_r12.bak")
        if not backup.exists():
            shutil.copy2(shared_path, backup)
        shared_path.write_text(changed, encoding="utf8")
        print("Updated:", shared_path.name)
    else:
        print("Already installed:", shared_path.name)
    if not target.exists():
        shutil.copy2(module, target)
        print("Added:", target.name)
    else:
        print("Already installed:", target.name)
    print("R12-R12 generic EHP consequence provider installed; full pytest NOT run")


if __name__ == "__main__":
    main()
