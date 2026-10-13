"""Install R52-R4 after verifying the expected current Flask code and template."""
from __future__ import annotations
import ast
from pathlib import Path
import shutil

ROOT = Path.cwd()
BUNDLE = Path(__file__).resolve().parent
APP = ROOT / "web_app.py"
TEMPLATE = ROOT / "templates" / "index.html"


def replace_once(text: str, old: str, new: str, label: str) -> str:
    if new in text:
        return text
    if old in text:
        if text.count(old) != 1:
            raise RuntimeError(f"ambiguous insertion anchor: {label}")
        return text.replace(old, new, 1)
    raise RuntimeError(f"unexpected current source at {label}; refusing to patch")


def main() -> None:
    for item in (APP, TEMPLATE):
        if not item.is_file():
            raise FileNotFoundError(str(item))
    for name in (
        "phase165_r52_partial_proof.py",
        "phase165_r52_r2_search_adapter.py",
        "phase165_r52_r3_web_adapter.py",
    ):
        if not (ROOT / name).is_file():
            raise FileNotFoundError(f"Missing R52 dependency: {name}")

    app = APP.read_text(encoding="utf-8-sig")
    html = TEMPLATE.read_text(encoding="utf-8-sig")
    app = replace_once(
        app,
        "from web_group_proof import (",
        "from phase165_r52_r4_flask_bridge import (\n"
        "  build_group_proof_progress_view,\n"
        ")\nfrom web_group_proof import (".replace("\\n", "\n"),
        "web_app imports",
    )
    app = replace_once(
        app,
        '        elif form_kind == "operation":',
        """        elif form_kind == "group_proof_progress":
          n = _parse_integer_form_value(n_value, "n")
          k = _parse_integer_form_value(k_value, "k")
          group_proof_view = build_group_proof_progress_view(
            n=n, k=k,
          )
        elif form_kind == "operation":""",
        "web_app progress route",
    )
    html = replace_once(
        html,
        '    <section\n      id="operation-query"',
        """    <section
      id="group-proof-progress-query"
      aria-labelledby="group-proof-progress-heading"
    >
      <h2 id="group-proof-progress-heading">Group proof progress</h2>
      <p>Show current typed proof-search status for any valid n and k.
         Without a registered typed goal this is NOT_SEARCHED, not a proof.</p>
      <form method="post">
        <input type="hidden" name="form_kind" value="group_proof_progress">
        <label for="progress-n">n</label>
        <input id="progress-n" name="n" type="number" step="1" required value="{{ n_value }}">
        <label for="progress-k">k</label>
        <input id="progress-k" name="k" type="number" step="1" required value="{{ k_value }}">
        <button type="submit">Show proof progress</button>
      </form>
    </section>

    <section
      id="operation-query""",
        "progress form",
    )
    html = replace_once(
        html,
        """        <h3>
          Conclusion
        </h3>""",
        """        <h3>
          {% if group_proof_view.partial_result %}Proof target{% else %}Conclusion{% endif %}
        </h3>""",
        "partial conclusion label",
    )
    ast.parse(app)
    # Confirm one newly inserted route and no duplicate independent forms.
    if app.count('elif form_kind == "group_proof_progress"') != 1:
        raise RuntimeError("progress route count incorrect")
    if html.count('name="form_kind" value="group_proof_progress"') != 1:
        raise RuntimeError("progress form count incorrect")
    source = (BUNDLE / "phase165_r52_r4_flask_bridge.py").read_text(encoding="utf-8")
    test = (BUNDLE / "test_phase165_r52_r4_flask_connection.py").read_text(encoding="utf-8")
    ast.parse(source)
    ast.parse(test)
    targets = {
        APP: app,
        TEMPLATE: html,
        ROOT / "phase165_r52_r4_flask_bridge.py": source,
        ROOT / "test_phase165_r52_r4_flask_connection.py": test,
    }
    for path, content in targets.items():
        if path.exists() and path not in (APP, TEMPLATE):
            current = path.read_text(encoding="utf-8-sig")
            if current != content:
                raise RuntimeError(f"Existing R4 file differs; refusing overwrite: {path}")
    # Prepare a complete copy of the changed index function for inspection.
    tree = ast.parse(app)
    create = next(node for node in tree.body if isinstance(node, ast.FunctionDef) and node.name == "create_app")
    index = next(node for node in create.body if isinstance(node, ast.FunctionDef) and node.name == "index")
    lines = app.splitlines(keepends=True)
    (BUNDLE / "index_FULL_AFTER_INSTALL.py.txt").write_text(
        "".join(lines[index.lineno-1:index.end_lineno]), encoding="utf-8"
    )
    (BUNDLE / "web_app_IMPORTS_AFTER_INSTALL.py.txt").write_text(
        "".join(lines[:create.lineno-1]), encoding="utf-8"
    )
    for path in (APP, TEMPLATE):
        backup = path.with_suffix(path.suffix + ".phase165_r52_r4_backup")
        if not backup.exists():
            shutil.copy2(path, backup)
    for path, content in targets.items():
        if not path.exists() or path.read_text(encoding="utf-8-sig") != content:
            path.write_text(content, encoding="utf-8")
        print(f"Verified: {path.relative_to(ROOT)}")


if __name__ == "__main__":
    main()
