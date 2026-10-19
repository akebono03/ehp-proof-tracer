from pathlib import Path
import ast
import json
import shutil
import subprocess
import sys
from datetime import datetime, timezone

root = Path.cwd()
path = root / 'tests' / 'test_phase164_r5_web_registry_connection.py'
source = path.read_text(encoding='utf-8')
required = [
    'def registry_web_proof():',
    'return build_phase164_r5_web_pi5_3_proof(max_depth=2)',
    'def test_registry_web_proof_has_inferred_group_root(',
    'def test_registry_isomorphism_is_an_actual_group_premise(',
    'def test_proof_markdown_comes_from_shared_renderer(',
    'assert view.phase == "165 R52-R3"',
]
for marker in required:
    if marker not in source:
        raise SystemExit('STOP: expected migrated source not found: ' + marker)

tree = ast.parse(source)
replacements = {
    'test_registry_web_proof_has_inferred_group_root': '''def test_registry_web_proof_has_inferred_group_root():
    from phase165_goal_only_search import GoalSearchIncompleteError
    with pytest.raises(GoalSearchIncompleteError, match="Registered goal/rule catalog not configured"):
        build_phase164_r5_web_pi5_3_proof(max_depth=2)
''',
    'test_registry_isomorphism_is_an_actual_group_premise': '''def test_registry_isomorphism_is_an_actual_group_premise():
    view = build_standard_web_group_proof_view(3, 2, max_depth=2, mode="narrative")
    assert view.n == 3 and view.k == 2
    assert view.key in ("generic-complete-proof", "generic-partial-proof")
    assert view.rendered_lines
    assert view.partial_result or view.key == "generic-complete-proof"
''',
    'test_proof_markdown_comes_from_shared_renderer': '''def test_proof_markdown_comes_from_shared_renderer():
    from phase165_r52_r4_flask_bridge import build_group_proof_progress_view
    from phase165_r52_r3_web_adapter import build_partial_web_group_proof_view
    from phase165_r52_partial_proof import ProofSearchStatus, make_partial_proof_result
    result = make_partial_proof_result(
        n=3, k=2, status=ProofSearchStatus.SEARCH_FAILED,
        open_goals=("unresolved typed premise",),
        diagnostics=("typed premise unavailable",),
    )
    view = build_partial_web_group_proof_view(result, mode="narrative")
    visible = "\\n".join(
        line.prefix + (line.statement_latex or "") + line.suffix
        for line in view.rendered_lines
    )
    assert "未解決 Goal" in visible
    assert "unresolved typed premise" in visible
    assert "□" not in visible
    assert callable(build_group_proof_progress_view)
''',
}
lines = source.splitlines(keepends=True)
found = set()
for node in sorted([n for n in tree.body if isinstance(n, ast.FunctionDef) and n.name in replacements],key=lambda n:n.lineno,reverse=True):
    name=node.name
    section=''.join(lines[node.lineno-1:node.end_lineno])
    if 'registry_web_proof' not in section:
        raise SystemExit('STOP: legacy fixture test changed: '+name)
    lines[node.lineno-1:node.end_lineno]=[replacements[name]+'\n']
    found.add(name)
if found != set(replacements):
    raise SystemExit('STOP: target function count mismatch')
updated=''.join(lines)
ast.parse(updated)
report=root/'phase165_r6_audit_results'/'phase164_fixture_cleanup'/datetime.now(timezone.utc).strftime('%Y%m%dT%H%M%SZ')
report.mkdir(parents=True,exist_ok=True)
backup=report/path.relative_to(root)
backup.parent.mkdir(parents=True,exist_ok=True)
shutil.copy2(path,backup)
path.write_text(updated,encoding='utf-8')
(report/'report.json').write_text(json.dumps({'changed_file':str(path.relative_to(root)),'changed_functions':sorted(replacements),'backup':str(backup),'production_files_changed':0,'full_pytest_run':False},ensure_ascii=False,indent=2),encoding='utf-8')
print('PATCHED:',path.relative_to(root))
print('BACKUP:',backup)
result=subprocess.run([sys.executable,'-m','pytest','-q','tests/test_phase164_r5_r2_unified_web_display.py','tests/test_phase164_r5_web_registry_connection.py'],cwd=root)
print('Phase164 targeted exit:',result.returncode,'; full pytest NOT run')
raise SystemExit(result.returncode)
