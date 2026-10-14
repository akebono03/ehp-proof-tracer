"""Guarded, idempotent R56 installer for the R55 working tree."""
from __future__ import annotations

import ast
import shutil
from pathlib import Path

root = Path.cwd()
pkg = Path(__file__).resolve().parent
partial_path = root / "phase165_r52_partial_proof.py"
template_path = root / "templates" / "index.html"
bridge_path = root / "phase165_r52_r4_flask_bridge.py"
for path in (partial_path, template_path, bridge_path, root / "phase165_r55_nk_only_goal.py"):
    if not path.is_file():
        raise SystemExit(f"Required R55 project file absent: {path}")

partial = partial_path.read_text(encoding="utf-8")
tree = ast.parse(partial)
funcs = [x for x in tree.body if isinstance(x, ast.FunctionDef) and x.name == "render_partial_proof_markdown"]
if len(funcs) != 1:
    raise SystemExit("Expected exactly one partial-renderer entry point")
node = funcs[0]
replacement = '''def render_partial_proof_markdown(result: PartialProofResult) -> str:
    """Use the existing whole-proof renderer for complete typed searches.

    Partial and failed searches retain their original fail-closed presentation.
    """
    from toda_group_proof_generic_narrative_renderer import (
        render_toda_partial_proof_narrative_markdown,
    )
    if result.status is ProofSearchStatus.COMPLETE:
        from phase165_r56_presentation_adapter import render_completed_shared_narrative
        return render_completed_shared_narrative(result)
    return render_toda_partial_proof_narrative_markdown(result)
'''
lines = partial.splitlines(keepends=True)
original = "".join(lines[node.lineno - 1:node.end_lineno])
if "render_completed_shared_narrative" in original:
    updated_partial = partial
elif "render_toda_partial_proof_narrative_markdown" in original:
    updated_partial = "".join(lines[:node.lineno - 1]) + replacement + "".join(lines[node.end_lineno:])
else:
    raise SystemExit("Unexpected partial renderer; no files modified")
ast.parse(updated_partial)

template = template_path.read_text(encoding="utf-8")
old_branch = '      {% elif view.status.value == "not_found" %}'
new_branch = ('      {% elif view.status.value == "not_found" %}\n'
              '        {% if group_proof_view and not group_proof_view.partial_result %}\n'
              '          <p>Typed proof search completed. See Group proof below.</p>\n'
              '        {% else %}')
old_end = '''        <p>
          No proof-backed result found for this query.
        </p>'''
new_end = old_end + "\n        {% endif %}"
if 'Typed proof search completed. See Group proof below.' in template:
    updated_template = template
elif template.count(old_branch) == 1 and template.count(old_end) == 1:
    updated_template = template.replace(old_branch, new_branch, 1).replace(old_end, new_end, 1)
else:
    raise SystemExit("Unexpected Jinja result branch; no files modified")

# Complete results must be marked as such for the pre-existing Jinja view.
web_adapter = root / "phase165_r52_r3_web_adapter.py"
if not web_adapter.is_file():
    raise SystemExit("Web adapter missing")
adapter = web_adapter.read_text(encoding="utf-8")
old_marker = '        partial_result=True,'
new_marker = '        partial_result=(result.status is not ProofSearchStatus.COMPLETE),'
if new_marker in adapter:
    updated_adapter = adapter
elif adapter.count(old_marker) == 1:
    updated_adapter = adapter.replace(old_marker, new_marker, 1)
    updated_adapter = updated_adapter.replace(
        'from phase165_r52_partial_proof import PartialProofResult, render_partial_proof_markdown',
        'from phase165_r52_partial_proof import PartialProofResult, ProofSearchStatus, render_partial_proof_markdown',
        1,
    )
else:
    raise SystemExit("Unexpected Web adapter; no files modified")
ast.parse(updated_adapter)

# R55 should already route n,k to the registered-goal search.
if "search_group_from_registered_goal" not in bridge_path.read_text(encoding="utf-8"):
    raise SystemExit("R55 n,k-only bridge has not been installed")
for fname in ("phase165_r56_presentation_adapter.py", "test_phase165_r56_common_renderer.py"):
    source = pkg / fname
    ast.parse(source.read_text(encoding="utf-8"))
    dst = root / fname
    if dst.exists() and dst.read_bytes() != source.read_bytes():
        raise SystemExit(f"Refusing to overwrite modified file: {fname}")

changes = [(partial_path, updated_partial), (template_path, updated_template), (web_adapter, updated_adapter)]
for path, content in changes:
    if path.read_text(encoding="utf-8") != content:
        backup = path.with_name(path.name + ".phase165_r56_backup")
        if not backup.exists():
            shutil.copy2(path, backup)
        path.write_text(content, encoding="utf-8")
for fname in ("phase165_r56_presentation_adapter.py", "test_phase165_r56_common_renderer.py"):
    shutil.copy2(pkg / fname, root / fname)

# Write complete replacement functions + changed imports for review.
p = ast.parse(updated_partial)
f = next(n for n in p.body if isinstance(n, ast.FunctionDef) and n.name == "render_partial_proof_markdown")
partial_lines = updated_partial.splitlines()
a = ast.parse(updated_adapter)
adapter_lines = updated_adapter.splitlines()
fn = next(n for n in a.body if isinstance(n, ast.FunctionDef) and n.name == "build_partial_web_group_proof_view")
first_def = min(n.lineno for n in a.body if isinstance(n, ast.FunctionDef))
(pkg / "CHANGED_CODE.md").write_text(
    "# Phase 165-R56 変更後コード\n\n"
    "## phase165_r52_partial_proof.py: render_partial_proof_markdown() 全文\n\n```python\n"
    + "\n".join(partial_lines[f.lineno - 1:f.end_lineno]) + "\n```\n\n"
    "## phase165_r52_r3_web_adapter.py: import 全文\n\n```python\n"
    + "\n".join(adapter_lines[:first_def - 1]) + "\n```\n\n"
    "## phase165_r52_r3_web_adapter.py: build_partial_web_group_proof_view() 全文\n\n```python\n"
    + "\n".join(adapter_lines[fn.lineno - 1:fn.end_lineno]) + "\n```\n\n"
    "## 新規関数とテスト\n\n"
    "新規 `phase165_r56_presentation_adapter.py` の `render_completed_shared_narrative()` と、"
    "`test_phase165_r56_common_renderer.py` のテスト全文は同梱ファイルを参照。\n\n"
    "## HTML 修正\n\n旧 Group query の失敗表示は、完成した型付き証明がある場合に抑止。"
    "未完成の場合には保持。\n",
    encoding="utf-8",
)
print("R56 installed: completed proof to shared Toda Presentation/Narrative; partial proof path retained.")
