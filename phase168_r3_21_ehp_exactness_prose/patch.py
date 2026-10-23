from pathlib import Path
import ast
import shutil

ROOT = Path(__file__).resolve().parent.parent
PACKAGE = Path(__file__).resolve().parent
TARGET = ROOT / "phase168_r3_5_model_renderer.py"
NEW = (PACKAGE / "render_model_backed_narrative_markdown_FULL.py").read_text(encoding="utf-8")


def main():
    if not TARGET.is_file():
        raise SystemExit("ERROR: target renderer missing")
    source = TARGET.read_text(encoding="utf-8-sig")
    nodes = [x for x in ast.parse(source).body if isinstance(x, ast.FunctionDef) and x.name == "render_model_backed_narrative_markdown"]
    if len(nodes) != 1:
        raise SystemExit("ERROR: expected exactly one renderer function")
    node = nodes[0]
    lines = source.splitlines(keepends=True)
    old = "".join(lines[node.lineno - 1:node.end_lineno])
    if old.strip() == NEW.strip():
        print("ALREADY_PATCHED:", TARGET)
        return
    if "build_narrative_body_lines(result, model)" not in old:
        raise SystemExit("ERROR: unexpected renderer implementation; no changes applied")
    backup = PACKAGE / "backup" / TARGET.name
    backup.parent.mkdir(parents=True, exist_ok=True)
    shutil.copy2(TARGET, backup)
    updated = "".join(lines[:node.lineno - 1]) + NEW.rstrip() + "\n" + "".join(lines[node.end_lineno:])
    ast.parse(updated)
    TARGET.write_text(updated, encoding="utf-8")
    print("PATCHED:", TARGET)
    print("BACKUP:", backup)
    print("FULL_FUNCTION:", PACKAGE / "render_model_backed_narrative_markdown_FULL.py")


if __name__ == "__main__":
    main()
