from pathlib import Path
import ast
import shutil

ROOT = Path.cwd()
BACKUP = ROOT / "phase166_r3ai_zero_web_display_backup"

def replace_exact(path, old, new):
    file = ROOT / path
    source = file.read_text(encoding="utf-8-sig")
    if new in source:
        print("ALREADY_APPLIED:", path)
        return
    if source.count(old) != 1:
        raise RuntimeError("Unexpected version: " + path)
    updated = source.replace(old, new, 1)
    ast.parse(updated, filename=path)
    BACKUP.mkdir(exist_ok=True)
    shutil.copy2(file, BACKUP / file.name)
    file.write_text(updated, encoding="utf-8")
    print("PATCHED:", path)

def main():
    replace_exact(
        "phase165_r55_nk_only_goal.py",
        "    if bridge is None:\n        bridge = build_shared_typed_bridge()",
        '''    if bridge is None and goal is None:
        from phase166_r3af_goal_adapter import database_zero_group_goal_candidates
        zero_candidates = database_zero_group_goal_candidates(n=n, k=k)
        if len(zero_candidates) == 1:
            return make_partial_proof_result(
                n=n, k=k, status=ProofSearchStatus.NOT_SEARCHED,
                open_goals=zero_candidates,
                diagnostics=("零群の型付き Goal を取得済み。共通証明探索への接続は未実装。",),
            )
    if bridge is None:
        bridge = build_shared_typed_bridge()''',
    )
    replace_exact(
        "toda_group_proof_narrative_renderer.py",
        '                       if getattr(goal, "lhs", None) == result.target)',
        '''                       if (getattr(goal, "lhs", None) == result.target
                           or getattr(goal, "group", None) == result.target))''',
    )
    replace_exact(
        "phase165_r52_r3_web_adapter.py",
        '    target_latex = rf"\\pi_{{{dimension}}}^{{{n}}}"',
        '''    target_latex = rf"\\pi_{{{dimension}}}^{{{n}}}"
    if result.status is not ProofSearchStatus.COMPLETE:
        from homotopy_groups import TodaPrimaryGroupZeroStatement
        if any(
            isinstance(item, TodaPrimaryGroupZeroStatement)
            and item.group == result.target
            for item in result.open_goals
        ):
            target_latex += " = 0"''',
    )
if __name__ == "__main__":
    main()
