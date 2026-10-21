"""Repair R3-AI DB eta2 name to the canonical typed proof identity."""
from pathlib import Path
import ast
import shutil

ROOT = Path.cwd()
TARGET = ROOT / "phase166_r3af_goal_adapter.py"
BACKUP = ROOT / "phase166_r3ai_pi32_identity_repair_backup"

NEW_FUNCTION = '''def _generator_for_target(label: str, base_n: int, target_n: int, k: int):
    match = _SIMPLE.fullmatch(label.strip())
    if match is None:
        return None
    family, index, power = match.groups()
    if int(index) != base_n:
        return None
    if power and family != "η":
        return None
    if family == "η" and k not in (1, 2, 3):
        return None
    if family == "ν" and k != 3:
        return None
    if family == "σ" and k != 7:
        return None
    if family == "ι" and k != 0:
        return None
    # The existing pi_3^2 typed proof uses the canonical name "η₂".
    # HomotopyElement equality includes name, not only generator metadata.
    notation = (
        "η₂" if family == "η" and target_n == 2 and not power
        else family + "_" + str(target_n) + power
    )
    return HomotopyElement(
        name=notation, dimension=target_n, source=target_n + k,
        target=target_n,
        generator=(GeneratorSymbol(family=family, index=target_n)
                   if not power else None),
    )
'''

def main():
    if not TARGET.is_file():
        raise RuntimeError("Run from the repository root")
    source = TARGET.read_text(encoding="utf-8-sig")
    if '"η₂" if family == "η" and target_n == 2 and not power' in source:
        print("ALREADY_APPLIED")
        return
    if "Direct nonstable rows are eligible." not in source:
        raise RuntimeError("Phase 166 R3-AI must be installed before this repair")
    tree = ast.parse(source)
    nodes = [node for node in tree.body if isinstance(node, ast.FunctionDef)
             and node.name == "_generator_for_target"]
    if len(nodes) != 1:
        raise RuntimeError("Unexpected adapter function layout")
    node = nodes[0]
    lines = source.splitlines(keepends=True)
    rewritten = "".join(lines[:node.lineno - 1]) + NEW_FUNCTION + "\n" + "".join(lines[node.end_lineno:])
    ast.parse(rewritten)
    BACKUP.mkdir(exist_ok=True)
    shutil.copy2(TARGET, BACKUP / TARGET.name)
    TARGET.write_text(rewritten, encoding="utf-8")
    print("PATCHED:", TARGET.name)
    print("BACKUP:", BACKUP)

if __name__ == "__main__":
    main()
