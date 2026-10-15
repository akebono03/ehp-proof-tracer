"""Phase 165 Renderer R5: read-only structural audit of the installed local tree."""
from __future__ import annotations

import ast
from collections import Counter
from datetime import datetime, timezone
import json
from pathlib import Path
import re

PACKAGE = Path(__file__).resolve().parent
PROJECT = PACKAGE.parent
OUTPUT = PACKAGE / "audit_output"
OLD_NAME = "toda_group_proof_generic_narrative_renderer"
CANONICAL = "toda_group_proof_narrative_renderer.py"

FOCUS = (
    CANONICAL,
    "phase165_renderer_narrative_model.py",
    "phase165_r52_partial_proof.py",
    "phase165_r52_r3_web_adapter.py",
    "phase165_r56_presentation_adapter.py",
    "web_group_proof.py",
    "toda_group_proof_narrative_shared_components.py",
    "phase165_r57_r2_partial_narrative.py",
    "phase165_r57_r10_step_narrative.py",
)
ENTRY_NAMES = (
    "render_narrative_proof_model",
    "render_toda_group_proof_narrative_markdown",
    "render_toda_partial_proof_narrative_markdown",
    "render_partial_proof_markdown",
    "render_completed_shared_narrative",
    "build_partial_web_group_proof_view",
    "build_standard_web_group_proof_view",
)


def allowed_file(path: Path) -> bool:
    relative = path.relative_to(PROJECT)
    if any(part.startswith(".") or part == "__pycache__" for part in relative.parts):
        return False
    if relative.parts[0].startswith("phase165_renderer_r"):
        return False
    if relative.parts[0].startswith("phase165_renderer_single_implementation_cleanup"):
        return False
    return True


def source_of(path: Path) -> str:
    return path.read_text(encoding="utf-8-sig")


def public_defs(path: Path) -> dict[str, list[int]]:
    tree = ast.parse(source_of(path), filename=str(path))
    definitions: dict[str, list[int]] = {}
    for node in tree.body:
        if isinstance(node, (ast.FunctionDef, ast.AsyncFunctionDef)):
            definitions.setdefault(node.name, []).append(node.lineno)
    return definitions


def find_old_imports(text: str) -> list[int]:
    """Locate old import statements, not narrative strings or documentation."""
    matches = []
    for n, line in enumerate(text.splitlines(), 1):
        if re.match(r"^\s*(?:from\s+" + OLD_NAME + r"\b|import\s+" + OLD_NAME + r"\b)", line):
            matches.append(n)
    return matches


def audit(project: Path = PROJECT) -> dict:
    global PROJECT
    original_project = PROJECT
    PROJECT = project
    try:
        focused = {name: project / name for name in FOCUS}
        missing = [name for name, path in focused.items() if not path.is_file()]
        if missing:
            raise RuntimeError("required files missing: " + ", ".join(missing))
        sources = {name: source_of(path) for name, path in focused.items()}
        definitions = {name: public_defs(path) for name, path in focused.items()}
        canonical = definitions[CANONICAL]
        counts = {name: len(canonical.get(name, ())) for name in (
            "render_narrative_proof_model", "render_toda_group_proof_narrative_markdown",
            "render_toda_partial_proof_narrative_markdown",
        )}
        old_alias = (project / OLD_NAME / "__init__.py").exists() or (project / (OLD_NAME + ".py")).exists()
        old_imports = []
        scoped = []
        renderer_files = []
        for path in project.rglob("*.py"):
            if not allowed_file(path):
                continue
            scoped.append(path)
            rel = str(path.relative_to(project)).replace("\\", "/")
            if "render" in path.name or "narrative" in path.name:
                renderer_files.append(rel)
            content = source_of(path)
            for n in find_old_imports(content):
                old_imports.append({"file": rel, "line": n})
        partial_tree = ast.parse(sources["phase165_r52_partial_proof.py"])
        wrappers = [n for n in partial_tree.body if isinstance(n, ast.FunctionDef) and n.name == "render_partial_proof_markdown"]
        partial_wrapper = ast.get_source_segment(sources["phase165_r52_partial_proof.py"], wrappers[0]) if len(wrappers) == 1 else ""
        web_source = sources["web_group_proof.py"]
        adapter_source = sources["phase165_r52_r3_web_adapter.py"]
        model_source = sources["phase165_renderer_narrative_model.py"]
        dispatcher_tree = ast.parse(sources[CANONICAL])
        dispatcher_nodes = [n for n in dispatcher_tree.body if isinstance(n, ast.FunctionDef) and n.name == "render_narrative_proof_model"]
        dispatcher_source = ast.get_source_segment(sources[CANONICAL], dispatcher_nodes[0]) if len(dispatcher_nodes) == 1 else ""
        checks = {
            "no_legacy_alias": not old_alias,
            "no_legacy_imports": not old_imports,
            "one_public_complete_narrative_definition": counts["render_toda_group_proof_narrative_markdown"] == 1,
            "one_shared_model_dispatcher": counts["render_narrative_proof_model"] == 1,
            "one_partial_narrative_definition": counts["render_toda_partial_proof_narrative_markdown"] == 1,
            "partial_public_uses_model_dispatcher": "build_narrative_proof_model" in partial_wrapper and "render_narrative_proof_model" in partial_wrapper,
            "web_entry_uses_shared_adapter": "build_partial_web_group_proof_view" in web_source,
            "web_adapter_uses_public_narrative": "render_partial_proof_markdown(result)" in adapter_source,
            "dispatcher_preserves_complete_and_incomplete": all(token in dispatcher_source for token in (
                "ProofSearchStatus.COMPLETE", "render_completed_shared_narrative", "render_toda_partial_proof_narrative_markdown",
            )),
            "model_preserves_proven_steps_and_open_goals": all(token in model_source for token in ("proven_steps", "open_goals")),
        }
        # Discovery, not a falsified proof of uniqueness: these helpers need follow-up ownership review.
        potential_alternates = []
        for name in renderer_files:
            path = project / name
            if path == focused[CANONICAL] or path.name.endswith("test.py"):
                continue
            if name.startswith("audit_") or name.startswith("test_") or name.startswith("tests/"):
                continue
            if "narrative" not in name and "proof" not in name:
                continue
            try:
                tree = ast.parse(source_of(path), filename=name)
            except SyntaxError:
                continue
            entry_funcs = [node.name for node in tree.body if isinstance(node, ast.FunctionDef)
                           and node.name.startswith("render_") and ("narrative" in node.name or "proof" in node.name)]
            if entry_funcs:
                potential_alternates.append({"path": name, "functions": entry_funcs[:25]})
        status = "STATIC_PASS_REVIEW_REQUIRED" if all(checks.values()) else "STATIC_FAIL"
        return {
            "audit": "phase165-renderer-r5", "status": status,
            "timestamp_utc": datetime.now(timezone.utc).isoformat(),
            "checks": checks,
            "counts": {
                "scanned_python": len(scoped), "renderer_named_files": len(renderer_files),
                "legacy_import_statements": len(old_imports),
                "canonical_public_complete_definitions": counts["render_toda_group_proof_narrative_markdown"],
                "canonical_dispatchers": counts["render_narrative_proof_model"],
                "candidate_helper_renderers": len(potential_alternates),
            },
            "old_imports": old_imports,
            "focus_public_definitions": {name: {key: positions for key, positions in defs.items() if key in ENTRY_NAMES}
                                         for name, defs in definitions.items()},
            "potential_alternative_narrative_helpers": potential_alternates,
            "limitations": [
                "AST and source inspection alone cannot prove that no dynamic import, monkeypatch or untested path exists.",
                "Helper render functions are not necessarily separate public renderers; manual ownership classification remains required.",
                "This audit does not certify mathematical correctness or arbitrary-goal backward search completeness.",
            ],
        }
    finally:
        PROJECT = original_project


def main() -> None:
    OUTPUT.mkdir(parents=True, exist_ok=True)
    data = audit()
    (OUTPUT / "audit.json").write_text(json.dumps(data, ensure_ascii=False, indent=2), encoding="utf-8")
    lines = ["# Phase 165 Renderer R5 最終監査", "", f"判定: **{data['status']}**", "", "## 静的チェック", ""]
    for key, value in data["checks"].items():
        lines.append(f"- {'PASS' if value else 'FAIL'}: `{key}`")
    lines += ["", "## 件数", ""]
    for key, value in data["counts"].items():
        lines.append(f"- {key}: {value}")
    lines += ["", "## 旧 import 残存", ""]
    lines += [f"- `{item['file']}:{item['line']}`" for item in data["old_imports"]] or ["- なし"]
    lines += ["", "## 補助 Renderer 候補（存在だけで重複と判定しない）", ""]
    for item in data["potential_alternative_narrative_helpers"]:
        lines.append(f"- `{item['path']}`: {', '.join(item['functions'])}")
    lines += ["", "## 監査上の限界", ""] + [f"- {item}" for item in data["limitations"]]
    (OUTPUT / "review.md").write_text("\n".join(lines) + "\n", encoding="utf-8")
    print(json.dumps({"status": data["status"], "counts": data["counts"],
                      "check_failures": [key for key, value in data["checks"].items() if not value],
                      "report": str(OUTPUT / "review.md"), "full_pytest_run": False},
                     ensure_ascii=False, indent=2))
    if not all(data["checks"].values()):
        raise SystemExit(2)


if __name__ == "__main__":
    main()
