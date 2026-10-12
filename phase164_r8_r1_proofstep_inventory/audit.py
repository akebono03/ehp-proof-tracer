"""Phase 164 R8-R1: read-only production ProofStep construction inventory."""
from __future__ import annotations
import ast
import json
from collections import Counter
from pathlib import Path

SKIP_DIRS = {".git", ".venv", "venv", "__pycache__", ".pytest_cache", "node_modules", "build", "dist"}
RELEVANT = ("proof", "toda", "repository", "generator", "operation", "phase161", "phase162", "phase163", "phase164")
CALL_NAMES = {"ProofStep", "apply_inference_match", "apply_inference_rule", "replace", "copy", "deepcopy"}

def _name(node):
    if isinstance(node, ast.Name):
        return node.id
    if isinstance(node, ast.Attribute):
        return node.attr
    return None

def inventory(root: Path) -> dict:
    root = Path(root)
    if not (root / "proof.py").is_file():
        raise FileNotFoundError("Run from the project root containing proof.py")
    counts = Counter()
    sites = []
    parsed = 0
    errors = []
    for path in sorted(root.rglob("*.py")):
        rel = path.relative_to(root)
        if any(part in SKIP_DIRS or part.startswith("phase164_r8_r1_proofstep_inventory") for part in rel.parts):
            continue
        if "tests" in rel.parts or path.name.startswith("test_"):
            continue
        try:
            tree = ast.parse(path.read_text(encoding="utf-8-sig"), filename=str(rel))
        except (SyntaxError, UnicodeError) as exc:
            errors.append({"file": str(rel), "error": str(exc)})
            continue
        parsed += 1
        class Walker(ast.NodeVisitor):
            def __init__(self):
                self.context = []
            def visit_FunctionDef(self, node):
                self.context.append(node.name)
                self.generic_visit(node)
                self.context.pop()
            visit_AsyncFunctionDef = visit_FunctionDef
            def visit_ClassDef(self, node):
                self.context.append(node.name)
                self.generic_visit(node)
                self.context.pop()
            def visit_Call(self, node):
                name = _name(node.func)
                if name in CALL_NAMES:
                    if name == "ProofStep":
                        role = "direct_constructor"
                    elif name.startswith("apply_inference"):
                        role = "inference_application"
                    elif name == "replace":
                        role = "dataclass_replace_review"
                    else:
                        role = "copy_review"
                    # A replace() call is only a candidate until its target is typed.
                    counts[role] += 1
                    sites.append({"file": str(rel).replace("\\", "/"), "line": node.lineno,
                                  "function": ".".join(self.context) or "<module>",
                                  "call": name, "role": role})
                self.generic_visit(node)
        Walker().visit(tree)
    examples = {}
    for role in sorted(counts):
        examples[role] = [x for x in sites if x["role"] == role][:15]
    key_paths = {
        "generator_replay": "repository_generator_known_group_proof_replay.py",
        "operation_replay": "repository_operation_query_proof_replay.py",
        "backward_reconstruction": "phase161_r5_backward_proof_reconstruction.py",
        "core_proof": "proof.py",
        "group_calculation": "toda_calculation.py",
    }
    key_status = {}
    for key, name in key_paths.items():
        content = (root / name).read_text(encoding="utf-8-sig") if (root / name).is_file() else ""
        key_status[key] = {"exists": bool(content), "direct_constructors": sum(x["file"] == name and x["role"] == "direct_constructor" for x in sites),
                           "inference_calls": sum(x["file"] == name and x["role"] == "inference_application" for x in sites)}
    return {"phase": "164 R8-R1", "mode": "READ_ONLY_PROOFSTEP_PRODUCTION_INVENTORY",
            "parsed_production_modules": parsed, "syntax_errors": errors,
            "counts": dict(counts), "key_paths": key_status, "sites": sites, "examples": examples,
            "production_modified": False, "full_pytest_run": False,
            "next": "Review direct constructors and inference applications before introducing common Factory; replay must reuse identity"}

def write_report(data: dict, output: Path) -> None:
    output.mkdir(parents=True, exist_ok=True)
    (output / "audit.json").write_text(json.dumps(data, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    lines = ["# Phase 164 R8-R1 — ProofStep 生成経路の棚卸し", "", "- モード: 読み取り専用", "- 全体 pytest: 未実施",
             f'- 解析した本番 Python ファイル数: {data["parsed_production_modules"]}',
             f'- 構文エラー: {len(data["syntax_errors"])}', "", "## 呼び出し分類", ""]
    for role, count in sorted(data["counts"].items()):
        lines.append(f"- {role}: {count}件")
    lines += ["", "## 代表経路", ""]
    for name, details in data["key_paths"].items():
        lines.append(f'- {name}: file={details["exists"]}, direct={details["direct_constructors"]}, inference={details["inference_calls"]}')
    lines += ["", "## 生成サイト例（各分類先頭15件）", ""]
    for role, entries in data["examples"].items():
        lines.append(f"### {role}")
        for entry in entries:
            lines.append(f'- `{entry["file"]}:{entry["line"]}` — `{entry["function"]}` / `{entry["call"]}`')
    lines += ["", "## 判断の境界", "", "- `ProofStep(...)` は直接生成候補である。", "- `apply_inference_match(...)` は規則に基づく推論生成であり、単純なコンストラクタと統合しない。", "- Replay は既存 ProofStep の identity（同一性）保持が必要であり、新規生成対象ではない。", "- `dataclasses.replace` は他のデータクラスも対象とするため個別に確認する。", "- 本結果は静的棚卸しであり、R8 の実装完了判定ではない。", ""]
    (output / "report.md").write_text("\n".join(lines), encoding="utf-8")

if __name__ == "__main__":
    data = inventory(Path.cwd())
    write_report(data, Path.cwd() / "phase164_r8_r1_output")
    print((Path.cwd() / "phase164_r8_r1_output" / "report.md").read_text(encoding="utf-8"))
