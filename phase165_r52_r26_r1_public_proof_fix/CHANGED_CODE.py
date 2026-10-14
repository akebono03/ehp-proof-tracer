"""R26-R1: Switch only Proposition 5.1's pi3^2 lookup to shared typed proof."""
from __future__ import annotations
import ast
import json
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
TARGET = ROOT / 'toda_prop56_zero_bootstrap.py'
MARKER = 'phase165_r52_r26_r1_shared_pi32_lookup'


def install() -> dict[str, object]:
    source = TARGET.read_text(encoding='utf-8')
    if MARKER in source:
        return {'phase': '165 R52-R26-R1', 'status': 'ALREADY_INSTALLED', 'production_modified': False, 'full_pytest_run': False}
    tree = ast.parse(source)
    funcs = [node for node in tree.body if isinstance(node, ast.FunctionDef) and node.name == '_build_prop51_step']
    if len(funcs) != 1:
        raise RuntimeError('Expected one _build_prop51_step function; aborting without changes')
    func = funcs[0]
    lines = source.splitlines(keepends=True)
    original = ''.join(lines[func.lineno - 1:func.end_lineno])
    needle = '''    phase49[\n      "result"\n    ].steps,'''
    start = '  pi3_2_step = _find_unique_step(\n'
    if original.count(start) != 1:
        raise RuntimeError('Expected one pi3_2_step assignment; aborting without changes')
    setup = '''  # phase165_r52_r26_r1_shared_pi32_lookup\n  # The pi3^2 proof is regenerated using common typed inference rules.\n  # This does not reintroduce any pi3^2-specific rule or GIVEN result.\n  from pathlib import Path\n  from hopf_facts import ETA_2\n  from phase165_r14_r38_direct_registry import build_adopted_typed_reference_registry\n  from phase165_r52_r9_shared_math import build_shared_typed_bridge, search_shared_group_goal\n  from phase165_r52_partial_proof import ProofSearchStatus\n  adopted_path = Path(__file__).resolve().with_name("phase165_r14_r39_toda51.tex")\n  adopted_bridge = build_shared_typed_bridge(\n    sources=(build_adopted_typed_reference_registry(adopted_path),),\n  )\n  pi32_search = search_shared_group_goal(\n    n=2, k=1, group_structure=FreeCyclicGroup(ETA_2), bridge=adopted_bridge,\n  )\n  if pi32_search.status is not ProofSearchStatus.COMPLETE:\n    raise ValueError("shared pi_3^2 proof is incomplete")\n  if not any(step.rule is ProofRule.INFERENCE for step in pi32_search.proven_steps):\n    raise ValueError("shared pi_3^2 result has no inferred ProofStep")\n\n'''
    # The same Phase 49 expression appears again in eta2_hopf_step.
    # Replace only the first argument of the pi3_2_step call.
    begin = original.index(start)
    end_marker = '  eta2_hopf_step = _find_unique_step(\n'
    end = original.find(end_marker, begin + len(start))
    if end < 0:
        raise RuntimeError('Expected eta2_hopf_step immediately after pi3_2_step')
    pi32_block = original[begin:end]
    if pi32_block.count(needle) != 1:
        raise RuntimeError('The pi3_2_step lookup has an unexpected shape')
    replaced_block = pi32_block.replace(needle, '    pi32_search.proven_steps,', 1)
    modified = original[:begin] + setup + replaced_block + original[end:]

    ast.parse(modified)
    backup = TARGET.with_name(TARGET.name + '.phase165_r52_r26_r1_backup')
    if not backup.exists():
        backup.write_text(source, encoding='utf-8')
    lines[func.lineno - 1:func.end_lineno] = [modified]
    new_source = ''.join(lines)
    ast.parse(new_source)
    TARGET.write_text(new_source, encoding='utf-8')
    (Path(__file__).parent / 'MODIFIED_FUNCTION.md').write_text(
        '# _build_prop51_step() — full installed function\n\n```python\n'
        + modified + '\n```\n', encoding='utf-8',
    )
    return {'phase': '165 R52-R26-R1', 'status': 'INSTALLED', 'changed_file': TARGET.name,
            'changed_function': '_build_prop51_step', 'backup': backup.name,
            'production_modified': True, 'full_pytest_run': False}


if __name__ == '__main__':
    print(json.dumps(install(), indent=2, ensure_ascii=False))
