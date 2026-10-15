"""Phase 165 Renderer R1: read-only source and route inventory."""
from __future__ import annotations

import argparse
import ast
import json
from collections import Counter
from pathlib import Path

SKIP_DIRS = {".git", ".pytest_cache", "__pycache__", ".venv", "venv", "archive", "backups"}
FOCUS_FILES = (
    "web_group_proof.py",
    "phase165_r52_r3_web_adapter.py",
    "phase165_r52_partial_proof.py",
    "phase165_r56_presentation_adapter.py",
    "toda_group_proof_narrative_renderer.py",
    "toda_group_proof_narrative_shared_components.py",
    "toda_group_proof_generic_narrative_renderer.py",
    "toda_group_proof_generic_narrative_renderer/__init__.py",
    "toda_group_proof_outline_renderer.py",
    "toda_group_proof_presentation.py",
)
ROUTE_NAMES = {
    "build_standard_web_group_proof_view",
    "build_partial_web_group_proof_view",
    "render_partial_proof_markdown",
    "render_completed_shared_narrative",
    "render_toda_group_proof_narrative_markdown",
    "render_toda_partial_proof_narrative_markdown",
    "render_toda_group_proof_generic_narrative_markdown",
}


def is_production_path(relative: Path) -> bool:
    parts = relative.parts
    if any(part in SKIP_DIRS for part in parts):
        return False
    if any("backup" in part.lower() or "snapshot" in part.lower() for part in parts):
        return False
    if parts and parts[0].startswith("phase") and len(parts) > 1:
        return False
    if relative.name.startswith("test_") or relative.name.endswith("_test.py"):
        return False
    return True


def module_name(relative: Path) -> str:
    parts = list(relative.with_suffix("").parts)
    if parts and parts[-1] == "__init__":
        parts.pop()
    return ".".join(parts)


def parse_file(path: Path, relative: Path) -> dict:
    content = path.read_text(encoding="utf-8-sig")
    tree = ast.parse(content, filename=str(relative))
    funcs = []
    imports = []
    calls = []
    for node in tree.body:
        if isinstance(node, (ast.FunctionDef, ast.AsyncFunctionDef)):
            funcs.append({"name": node.name, "line": node.lineno, "end_line": node.end_lineno})
        elif isinstance(node, ast.ImportFrom):
            imports.append({"module": node.module or "", "names": [a.name for a in node.names], "line": node.lineno, "relative_level": node.level})
        elif isinstance(node, ast.Import):
            for alias in node.names:
                imports.append({"module": alias.name, "names": [], "line": node.lineno, "relative_level": 0})
    for node in ast.walk(tree):
        if isinstance(node, ast.Call):
            name = None
            if isinstance(node.func, ast.Name):
                name = node.func.id
            elif isinstance(node.func, ast.Attribute):
                name = node.func.attr
            if name in ROUTE_NAMES:
                calls.append({"function": name, "line": node.lineno})
    duplicates = [{"name": name, "lines": [f["line"] for f in funcs if f["name"] == name]}
                  for name, count in Counter(f["name"] for f in funcs).items() if count > 1]
    return {"path": str(relative).replace("\\", "/"), "module": module_name(relative),
            "functions": funcs, "imports": imports, "route_calls": calls,
            "duplicate_top_level_functions": duplicates,
            "size_bytes": path.stat().st_size}


def gather(project: Path) -> dict:
    if not (project / "web_group_proof.py").is_file():
        raise FileNotFoundError("project root must contain web_group_proof.py")
    files = []
    failures = []
    for path in sorted(project.rglob("*.py")):
        relative = path.relative_to(project)
        if any(part in SKIP_DIRS for part in relative.parts):
            continue
        if any("backup" in part.lower() for part in relative.parts):
            continue
        if len(relative.parts) > 1 and relative.parts[0].startswith("phase"):
            continue
        try:
            files.append(parse_file(path, relative))
        except (SyntaxError, UnicodeError, OSError) as error:
            failures.append({"path": relative.as_posix(), "error": str(error)})
    focus = {name: (project / name).is_file() for name in FOCUS_FILES}
    production = [f for f in files if is_production_path(Path(f["path"]))]
    module_index = {f["module"]: f["path"] for f in production}
    renderer_files = sorted(f["path"] for f in production
                            if "renderer" in f["path"].lower() or "narrative" in f["path"].lower())
    renderer_imports = []
    for f in files:
        for imp in f["imports"]:
            if "render" in imp["module"] or "narrative" in imp["module"] or any("render" in n for n in imp["names"]):
                renderer_imports.append({"caller": f["path"], **imp,
                                         "resolved_path": module_index.get(imp["module"])})
    duplicates = [{"path": f["path"], **duplicate} for f in production
                  for duplicate in f["duplicate_top_level_functions"]]
    routes = {name: [] for name in sorted(ROUTE_NAMES)}
    for f in production:
        for fn in f["functions"]:
            if fn["name"] in routes:
                routes[fn["name"]].append({"path": f["path"], "line": fn["line"]})
    source_calls = [{"path": f["path"], **call} for f in production for call in f["route_calls"]]
    legacy = "toda_group_proof_generic_narrative_renderer"
    legacy_imports = [x for x in renderer_imports if x["module"] == legacy]
    return {"audit": "phase165-renderer-r1", "mode": "read-only", "project": str(project),
            "counts": {"all_scanned_python": len(files), "production_python": len(production),
                       "renderer_named_files": len(renderer_files), "duplicate_functions": len(duplicates),
                       "legacy_imports": len(legacy_imports), "parse_failures": len(failures)},
            "focus_exists": focus, "renderer_named_files": renderer_files,
            "duplicate_production_functions": duplicates, "public_route_definitions": routes,
            "public_route_calls": source_calls, "renderer_imports": renderer_imports,
            "legacy_imports": legacy_imports, "parse_failures": failures,
            "limitations": [
                "AST calls/imports are static evidence only; monkeypatch, reflection and dynamic import can evade scanning.",
                "Root production sources are prioritized; historical phase packages and archived scripts are excluded.",
                "R1 never deletes, renames, or edits project source files.",
                "A single implementation cannot be declared solely from renderer filename counts.",
            ]}


def report_markdown(result: dict) -> str:
    c = result["counts"]
    lines = ["# Phase 165 Renderer R1 監査結果", "", "## 件数", "",
             f"- 本番コード: {c['production_python']} Python files",
             f"- Renderer/Narrative 名称ファイル: {c['renderer_named_files']}",
             f"- トップレベル重複関数定義: {c['duplicate_functions']}",
             f"- 旧 Generic モジュールからの import: {c['legacy_imports']}",
             f"- AST 解析失敗: {c['parse_failures']}", "", "## 必須ファイルの存在", ""]
    lines += [f"- {'YES' if found else 'NO'}: `{path}`" for path, found in result["focus_exists"].items()]
    lines += ["", "## 重複関数定義", ""]
    if result["duplicate_production_functions"]:
        lines += [f"- `{x['path']}`: `{x['name']}` lines {x['lines']}" for x in result["duplicate_production_functions"]]
    else:
        lines.append("- 検出なし")
    lines += ["", "## 公開入口の定義", ""]
    for name, locs in result["public_route_definitions"].items():
        lines.append(f"- `{name}`: " + (", ".join(f"`{x['path']}:{x['line']}`" for x in locs) or "定義なし"))
    lines += ["", "## 旧 Generic モジュールへの依存", ""]
    lines.extend(f"- `{x['caller']}:{x['line']}` names={x['names']}" for x in result["legacy_imports"])
    if not result["legacy_imports"]:
        lines.append("- 検出なし（動的 import は除く）")
    lines += ["", "## 判定上の注意", ""]
    lines += [f"- {x}" for x in result["limitations"]]
    lines += ["", "## R2 以降の判断", "",
              "この監査結果をもとに、完成・未完成の公開入口、内部依存、重複定義を整理する。R1 ではコードを変更しない。", ""]
    return "\n".join(lines)


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--project", type=Path, required=True)
    parser.add_argument("--output", type=Path, required=True)
    args = parser.parse_args()
    project = args.project.resolve()
    output = args.output.resolve()
    result = gather(project)
    output.mkdir(parents=True, exist_ok=True)
    (output / "audit.json").write_text(json.dumps(result, ensure_ascii=False, indent=2), encoding="utf-8")
    (output / "review.md").write_text(report_markdown(result), encoding="utf-8")
    print(json.dumps({"audit": result["audit"], "counts": result["counts"],
                      "report": str(output / "review.md"), "full_pytest_run": False}, ensure_ascii=False, indent=2))


if __name__ == "__main__":
    main()
