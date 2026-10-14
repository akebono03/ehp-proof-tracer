from __future__ import annotations

import ast
import shutil
from pathlib import Path

ROOT = Path.cwd()
TARGET = ROOT / 'phase165_r52_r3_web_adapter.py'
COMMON = ROOT / 'web_group_proof_common.py'
LEGACY = ROOT / 'web_group_proof.py'
BACKUP = ROOT / 'phase165_r52_r3_web_adapter.py.phase165_r27_r11_r1_backup'

NEW_FUNCTION = '''def build_partial_web_group_proof_view(
    result: PartialProofResult,
    *,
    max_depth: int = 2,
    mode: str = "narrative",
) -> WebGroupProofView:
    """Adapt a verified search state to the shared Web view contract.

    Trace mode uses ProofStep entries only, while outline and narrative
    modes show the shared rendered text. Neither mode certifies open goals.
    """
    if not isinstance(result, PartialProofResult):
        raise TypeError("result must be PartialProofResult")
    if isinstance(max_depth, bool) or not isinstance(max_depth, int):
        raise TypeError("max_depth must be an int")
    if max_depth < 0:
        raise ValueError("max_depth must be nonnegative")
    if mode not in ("trace", "outline", "narrative"):
        raise ValueError("mode must be trace, outline, or narrative")

    n = result.target.sphere_dimension
    dimension = result.target.group_dimension
    k = dimension - n
    target_latex = rf"\\pi_{{{dimension}}}^{{{n}}}"

    steps = []
    for step in result.proven_steps:
        statement_latex, fallback_type_name = _group_proof_statement_latex(
            step.conclusion
        )
        steps.append(WebGroupProofStepView(
            depth=0,
            statement_latex=statement_latex,
            fallback_type_name=fallback_type_name,
            rule_name=_group_proof_rule_name(step),
            role_name="derived",
        ))

    if mode == "trace":
        rendered_lines = ()
    else:
        markdown = render_partial_proof_markdown(result)
        rendered_lines = _build_group_proof_rendered_lines(markdown)

    return WebGroupProofView(
        n=n,
        k=k,
        conclusion_latex=target_latex,
        theorem=None,
        phase="165 R52-R3",
        key="generic-partial-proof",
        steps=tuple(steps),
        max_depth=max_depth,
        mode=mode,
        rendered_lines=rendered_lines,
        partial_result=True,
    )
'''


def main() -> None:
    if not all(path.is_file() for path in (TARGET, COMMON, LEGACY)):
        raise SystemExit('R27-R10 and R27-R11 must be installed; no changes made')
    old = TARGET.read_text(encoding='utf-8-sig')
    if 'from web_group_proof_common import (' not in old:
        raise SystemExit('Shared Web adapter prerequisite missing; no changes made')
    if 'search_group_structure_automatically' not in LEGACY.read_text(encoding='utf-8-sig'):
        raise SystemExit('R27-R11 canonical search prerequisite missing; no changes made')
    tree = ast.parse(old)
    funcs = [node for node in tree.body if isinstance(node, ast.FunctionDef) and node.name == 'build_partial_web_group_proof_view']
    if len(funcs) != 1:
        raise SystemExit('Adapter function not found uniquely; no changes made')
    node = funcs[0]
    old_function = ''.join(old.splitlines(keepends=True)[node.lineno - 1:node.end_lineno])
    if old_function.strip() == NEW_FUNCTION.strip():
        print('R27-R11-R1 already installed')
        return
    if 'rendered_lines = _build_group_proof_rendered_lines(markdown)' not in old_function:
        raise SystemExit('Unexpected Web adapter function; no changes made')
    lines = old.splitlines(keepends=True)
    lines[node.lineno - 1:node.end_lineno] = [NEW_FUNCTION]
    new_text = ''.join(lines)
    compile(new_text, str(TARGET), 'exec')
    if not BACKUP.exists():
        shutil.copy2(TARGET, BACKUP)
    TARGET.write_text(new_text, encoding='utf-8')
    print('R27-R11-R1 installed: trace rendered_lines is empty; outline/narrative unchanged')


if __name__ == '__main__':
    main()
