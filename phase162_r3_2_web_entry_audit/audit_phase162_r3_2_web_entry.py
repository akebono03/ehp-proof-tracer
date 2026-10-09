from pathlib import Path
import ast
import json
import sys

ROOT = Path(__file__).resolve().parent.parent
TARGETS = (
    "phase162_web_narrative_integration.py",
    "web_app.py",
    "web_group_proof.py",
    "templates/index.html",
    "phase162_r3_narrative_connection.py",
    "phase162_r2_existing_proof_connection.py",
)
NEEDLES = (
    "懸垂同型の検証済み証明",
    "validated",
    "verified",
    "phase162",
    "narrative",
    "render_template",
    "group_proof_view",
    "reference",
)
def audit_file(path: Path) -> dict:
    if not path.is_file():
        return {"path": str(path.relative_to(ROOT)), "exists": False}
    text = path.read_text(encoding="utf-8-sig")
    lines = text.splitlines()
    matches = []
    for i, line in enumerate(lines):
        if any(x.lower() in line.lower() for x in NEEDLES):
            start = max(0, i - 2)
            end = min(len(lines), i + 3)
            matches.append({"line": i + 1, "context": [
                {"number": j + 1, "text": lines[j]} for j in range(start, end)
            ]})
    parsed = None
    if path.suffix == ".py":
        try:
            parsed = [
                {"name": node.name, "line": node.lineno}
                for node in ast.walk(ast.parse(text))
                if isinstance(node, (ast.FunctionDef, ast.AsyncFunctionDef, ast.ClassDef))
                and any(x in node.name.lower() for x in ("phase162", "narrative", "proof"))
            ]
        except SyntaxError as error:
            parsed = {"syntax_error": str(error)}
    return {
        "path": str(path.relative_to(ROOT)),
        "exists": True,
        "line_count": len(lines),
        "matched_context": matches[:70],
        "definitions": parsed,
    }

def main() -> None:
    if not (ROOT / "proof.py").exists():
        raise SystemExit("Run from a bundle extracted directly in the repository root.")
    report = {
        "purpose": "R3-2 local verified panel entrypoint audit; read only; no code changed",
        "repository_root": str(ROOT),
        "files": [audit_file(ROOT / target) for target in TARGETS],
    }
    output = ROOT / "phase162_r3_2_web_entry_audit.json"
    output.write_text(json.dumps(report, ensure_ascii=False, indent=2), encoding="utf-8")
    print(f"Wrote {output}")
    local = ROOT / "phase162_web_narrative_integration.py"
    if not local.exists():
        print("Local Phase 162 integration source not found. No modifications were made.")
    else:
        print("Local Phase 162 integration source found. No modifications were made.")
    print("Full suite not run.")

if __name__ == "__main__":
    main()
