"""Idempotent guarded integration into current shared path."""
from __future__ import annotations
import ast
from pathlib import Path
import shutil

def main() -> None:
    root = Path.cwd()
    package = Path(__file__).resolve().parent
    payload = package / "phase165_r12_r20_eta_definition.py"
    target = root / payload.name
    shared = root / "phase165_r52_r9_shared_math.py"
    if not shared.is_file():
        raise FileNotFoundError(shared)
    source = root / "sources" / "toda" / "Toda_05_2.tex"
    if not source.is_file():
        raise FileNotFoundError(source)
    if target.exists() and target.read_bytes() != payload.read_bytes():
        raise RuntimeError("Conflicting R12-R20 module; refusing overwrite")
    from sys import path
    if str(package) not in path:
        path.insert(0, str(package))
    from phase165_r12_r20_eta_definition import build_cited_eta_family_definition
    build_cited_eta_family_definition(source)
    code = shared.read_text(encoding="utf8")
    hook = "build_cited_eta_family_definition"
    if hook not in code:
        needle = "        sources = (production, build_adopted_typed_reference_registry(adopted_tex),"
        if code.count(needle) != 1:
            raise RuntimeError("shared bridge source hook not unique")
        code = code.replace(needle,
            "        from phase165_r12_r20_eta_definition import build_cited_eta_family_definition\n" + needle, 1)
        needle2 = "build_adopted_toda51_zero_reference(adopted_tex))"
        if code.count(needle2) != 1:
            raise RuntimeError("shared source tuple not unique")
        code = code.replace(needle2, needle2[:-1] + ", build_cited_eta_family_definition(Path(__file__).resolve().parent / 'sources' / 'toda' / 'Toda_05_2.tex')))", 1)
        needle3 = "    from phase165_r12_r15_toda51 import expand_cited_toda51_zero"
        if code.count(needle3) != 1:
            raise RuntimeError("shared expansion hook not unique")
        code = code.replace(needle3, needle3 + "\n    from phase165_r12_r20_eta_definition import expand_cited_eta_definition", 1)
        needle4 = "        options.extend(expand_cited_toda51_zero(goal, tuple(available)))"
        if code.count(needle4) != 1:
            raise RuntimeError("shared expansion site not unique")
        code = code.replace(needle4, needle4 + "\n        options.extend(expand_cited_eta_definition(goal, tuple(available)))", 1)
    ast.parse(code)
    ast.parse(payload.read_text(encoding="utf8"))
    if not target.exists():
        shutil.copy2(payload, target)
    if code != shared.read_text(encoding="utf8"):
        backup = shared.with_name(shared.name + ".r12_r20_before.bak")
        if not backup.exists():
            shutil.copy2(shared, backup)
        shared.write_text(code, encoding="utf8")
    print("R12-R20 source-checked universal eta definition connected")

if __name__ == "__main__":
    main()
