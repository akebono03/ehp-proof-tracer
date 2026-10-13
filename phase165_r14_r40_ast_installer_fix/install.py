"""Install R40 common proof route without depending on literal source layout.

Only the R39 n=2,k=1 override and R40 common-replay selection are touched.
"""
from __future__ import annotations

import ast
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
WEB = ROOT / "web_group_proof.py"
COMMON = ROOT / "phase164_r5_r2_common_replay.py"


def _function(source: str, name: str) -> ast.FunctionDef:
    matches = [node for node in ast.parse(source).body
               if isinstance(node, ast.FunctionDef) and node.name == name]
    if len(matches) != 1:
        raise RuntimeError(f"expected one {name} function")
    return matches[0]


def _is_r39_branch(node: ast.stmt) -> bool:
    if not isinstance(node, ast.If):
        return False
    body = ast.unparse(ast.Module(body=node.body, type_ignores=[]))
    return ("build_phase165_pi32_web_view" in body
            and "phase165_r14_r39_web_connection" in body
            and "n == 2" in ast.unparse(node.test)
            and "k == 1" in ast.unparse(node.test))


def _replace_line_span(source: str, start: int, end: int, content: str) -> str:
    lines = source.splitlines(keepends=True)
    return "".join(lines[:start - 1] + [content] + lines[end:])


def _change_web(source: str) -> str:
    fn = _function(source, "build_standard_web_group_proof_view")
    r39_nodes = [node for node in fn.body if _is_r39_branch(node)]
    if len(r39_nodes) > 1:
        raise RuntimeError("multiple R39 Web routes; manual review needed")
    if r39_nodes:
        node = r39_nodes[0]
        return _replace_line_span(source, node.lineno, node.end_lineno, "")
    if "build_phase165_pi32_web_view" in ast.unparse(fn):
        raise RuntimeError("R39 view call not in expected direct branch")
    return source


def _change_common(source: str) -> str:
    fn = _function(source, "build_phase164_r5_r2_common_replay")
    signature = "build_phase165_r40_pi32_common_replay"
    if signature in ast.unparse(fn):
        return source
    branch = (
        "    if n == 2 and k == 1:\n"
        "        from phase165_r14_r40_replay import build_phase165_r40_pi32_common_replay\n"
        "        return build_phase165_r40_pi32_common_replay(group_result, max_depth)\n\n"
    )
    # Place directly after the function docstring, independent of later branches.
    if fn.body and isinstance(fn.body[0], ast.Expr) and isinstance(fn.body[0].value, ast.Constant) and isinstance(fn.body[0].value.value, str):
        line = fn.body[0].end_lineno
    elif fn.body:
        line = fn.body[0].lineno - 1
    else:
        raise RuntimeError("empty common replay function")
    lines = source.splitlines(keepends=True)
    lines.insert(line, branch)
    return "".join(lines)


def main() -> None:
    updates = []
    for path, change, backup in (
        (WEB, _change_web, "web_group_proof.phase165_r40_backup.py"),
        (COMMON, _change_common, "phase164_r5_r2_common_replay.phase165_r40_backup.py"),
    ):
        original = path.read_text(encoding="utf-8")
        changed = change(original)
        compile(changed, str(path), "exec")
        updates.append((path, original, changed, backup))
    # Both proposed edits must compile before either existing project file changes.
    for path, original, changed, backup in updates:
        if original != changed:
            backup_path = path.with_name(backup)
            if not backup_path.exists():
                backup_path.write_text(original, encoding="utf-8")
            path.write_text(changed, encoding="utf-8")
    print("R39 display override removed; R38 ProofStep routed to shared renderer")


if __name__ == "__main__":
    main()
