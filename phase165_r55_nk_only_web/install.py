"""Guarded R55 installer: update default search routing and remove R54 input form."""
from pathlib import Path
import ast
import shutil

root = Path.cwd()
pkg = Path(__file__).resolve().parent
bridge_path = root / "phase165_r52_r4_flask_bridge.py"
template_path = root / "templates" / "index.html"
if not bridge_path.is_file() or not template_path.is_file():
    raise SystemExit("Run from the repository root containing the Flask bridge and template")
bridge = bridge_path.read_text(encoding="utf-8")
html = template_path.read_text(encoding="utf-8")
old_line = "        result = search_group_structure_automatically(n=n, k=k)"
new_lines = ("        from phase165_r55_nk_only_goal import search_group_from_registered_goal\n"
             "        result = search_group_from_registered_goal(n=n, k=k)")
if old_line in bridge:
    if bridge.count(old_line) != 1:
        raise SystemExit("Unexpected Flask bridge structure")
    bridge = bridge.replace(old_line, new_lines, 1)
elif new_lines not in bridge:
    raise SystemExit("Flask bridge is different from expected R54 baseline")
form_start = '      <form method="post" id="phase165-explicit-group-goal">'
if form_start in html:
    if html.count(form_start) != 1:
        raise SystemExit("Multiple R54 forms found")
    begin = html.index(form_start)
    end = html.find("      </form>", begin)
    if end < 0:
        raise SystemExit("R54 form closing tag absent")
    html = html[:begin] + html[end + len("      </form>\n"):]
if 'id="phase165-explicit-group-goal"' in html:
    raise SystemExit("Generator field removal incomplete")

ast.parse(bridge)
for filename in ("phase165_r55_nk_only_goal.py", "test_phase165_r55_nk_only_goal.py"):
    ast.parse((pkg / filename).read_text(encoding="utf-8"))
    dest = root / filename
    if dest.exists() and dest.read_bytes() != (pkg / filename).read_bytes():
        raise SystemExit(f"Refusing to overwrite modified file: {filename}")
for path, content in ((bridge_path, bridge), (template_path, html)):
    if path.read_text(encoding="utf-8") != content:
        backup = path.with_name(path.name + ".phase165_r55_backup")
        if not backup.exists():
            shutil.copy2(path, backup)
        path.write_text(content, encoding="utf-8")
for filename in ("phase165_r55_nk_only_goal.py", "test_phase165_r55_nk_only_goal.py"):
    shutil.copy2(pkg / filename, root / filename)

# Full replaceable function and imports, collected after installation.
source = bridge_path.read_text(encoding="utf-8")
parsed = ast.parse(source)
lines = source.splitlines()
function = next(node for node in parsed.body if isinstance(node, ast.FunctionDef)
                and node.name == "build_group_proof_progress_view")
first_def = min(node.lineno for node in parsed.body if isinstance(node, ast.FunctionDef))
imports = "\n".join(lines[:first_def - 1])
full_function = "\n".join(lines[function.lineno - 1:function.end_lineno])
(pkg / "CHANGED_CODE.md").write_text(
    "# R55 変更後コード\n\n## `phase165_r52_r4_flask_bridge.py` の import 全文\n\n"
    "```python\n" + imports + "\n```\n\n"
    "## `build_group_proof_progress_view()` 全文\n\n"
    "```python\n" + full_function + "\n```\n\n"
    "## 新規ファイル\n\n"
    "`phase165_r55_nk_only_goal.py` と `test_phase165_r55_nk_only_goal.py` は ZIP に全文収録。"
    "テンプレートの R54 生成元フォームは削除。旧 POST endpoint は互換性のため非表示で保持。\n",
    encoding="utf-8",
)
print("R55: n,k-only typed registry goal selection enabled; R54 generator input form hidden.")
