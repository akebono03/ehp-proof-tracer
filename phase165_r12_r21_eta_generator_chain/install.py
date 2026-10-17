"""Install additive R12-R21 shared expansion hook with AST and idempotence gates."""
from __future__ import annotations
import ast
from pathlib import Path
import shutil


def main() -> None:
    repo = Path.cwd()
    here = Path(__file__).resolve().parent
    shared = repo / "phase165_r52_r9_shared_math.py"
    if not shared.is_file():
        raise FileNotFoundError(shared)
    for name in ("phase165_r12_r20_eta_definition.py", "sources/toda/Toda_05_2.tex"):
        if not (repo / name).is_file():
            raise RuntimeError("R12-R20 is required: " + name)
    from sys import path
    if str(repo) not in path:
        path.insert(0, str(repo))
    from phase165_r52_r9_shared_math import build_shared_typed_bridge
    from phase165_r12_r20_eta_definition import TodaEtaFamilyGeneralDefinition
    bridge = build_shared_typed_bridge()
    cited = [x for x in bridge.proof_links if x.step is not None and isinstance(x.step.conclusion, TodaEtaFamilyGeneralDefinition)]
    if len(cited) != 1:
        raise RuntimeError("R12-R20 unique cited eta definition is missing")
    code = shared.read_text(encoding="utf8")
    anchor = "        options.extend(expand_cited_eta_definition(goal, tuple(available)))"
    import_line = "    from phase165_r12_r21_eta_generator_chain import expand_cited_eta_generator"
    hook_line = "        options.extend(expand_cited_eta_generator(goal))"
    if hook_line not in code:
        if code.count(anchor) != 1:
            raise RuntimeError("shared eta definition hook ambiguous")
        code = code.replace(anchor, anchor + "\n" + hook_line, 1)
        import_anchor = "    from phase165_r12_r20_eta_definition import expand_cited_eta_definition"
        if code.count(import_anchor) != 1:
            raise RuntimeError("shared eta definition import ambiguous")
        code = code.replace(import_anchor, import_anchor + "\n" + import_line, 1)
    elif import_line not in code:
        raise RuntimeError("hook exists without import")
    ast.parse(code)
    for name in ("phase165_r12_r21_eta_generator_chain.py", "phase165_r12_r19_generator_connection.py"):
        source = here / name
        ast.parse(source.read_text(encoding="utf8"))
        target = repo / name
        if target.exists() and target.read_bytes() != source.read_bytes():
            raise RuntimeError("conflicting existing module: " + name)
    for name in ("phase165_r12_r21_eta_generator_chain.py", "phase165_r12_r19_generator_connection.py"):
        source = here / name
        target = repo / name
        if not target.exists():
            shutil.copy2(source, target)
    if code != shared.read_text(encoding="utf8"):
        backup = shared.with_name(shared.name + ".r12_r21_before.bak")
        if not backup.exists():
            shutil.copy2(shared, backup)
        shared.write_text(code, encoding="utf8")
    print("R12-R21 shared eta generator expansions connected")


if __name__ == "__main__":
    main()
