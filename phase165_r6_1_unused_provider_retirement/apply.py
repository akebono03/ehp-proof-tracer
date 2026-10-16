"""Retire inactive explicit per-group provider branch; preserve source registry."""
from __future__ import annotations
import ast
import json
from pathlib import Path
import shutil

ROOT = Path(__file__).resolve().parent.parent
TARGET = ROOT / 'phase165_r52_r7_registered_common_proof.py'
TEST = ROOT / 'phase165_r52_r7_registered_common_proof' / 'test_phase165_r52_r7_registered_common_proof.py'


def retire_provider(source: str) -> str:
    tree = ast.parse(source)
    lines = source.splitlines(keepends=True)
    classes = [x for x in tree.body if isinstance(x, ast.ClassDef) and x.name == 'RegisteredProofProvider']
    factories = [x for x in tree.body if isinstance(x, (ast.FunctionDef, ast.AsyncFunctionDef)) and x.name == 'registered_proof_providers']
    functions = [x for x in tree.body if isinstance(x, ast.FunctionDef) and x.name == 'build_registered_common_replay']
    if not (len(classes) == len(factories) == len(functions) == 1):
        if 'class RegisteredProofProvider' not in source and 'def registered_proof_providers' not in source and 'providers:' not in source:
            return source
        raise RuntimeError('unexpected production code: refuse partial removal')
    func = functions[0]
    ifnode = next((x for x in func.body if isinstance(x, ast.If) and isinstance(x.test, ast.Compare)
                   and isinstance(x.test.left, ast.Name) and x.test.left.id == 'providers'
                   and len(x.test.ops) == 1 and isinstance(x.test.ops[0], ast.Is)
                   and len(x.test.comparators) == 1 and isinstance(x.test.comparators[0], ast.Constant)
                   and x.test.comparators[0].value is None), None)
    if ifnode is None or not ifnode.orelse:
        raise RuntimeError('expected legacy provider branch is missing')
    first_body, last_body = ifnode.body[0], ifnode.body[-1]
    body = ''.join(lines[first_body.lineno - 1:last_body.end_lineno])
    body = ''.join(line[4:] if line.startswith('    ') else line for line in body.splitlines(keepends=True))
    header = ''.join(lines[func.lineno - 1:ifnode.lineno - 1])
    header = header.replace('    providers: tuple[RegisteredProofProvider, ...] | None = None,\n', '')
    header = header.replace('    providers: tuple[RegisteredProofProvider, ...] | None = None,\r\n', '')
    if 'providers:' in header:
        raise RuntimeError('unexpected signature')
    newfunc = header + body
    newfunc = newfunc.replace('    from phase165_goal_only_search import GoalSearchIncompleteError\n\n    if type(max_depth)', '    from phase165_goal_only_search import GoalSearchIncompleteError\n\n    if type(max_depth)')
    excluded = {classes[0],factories[0],func}
    result = []
    cursor = 1
    for node in sorted(excluded, key=lambda x:x.lineno):
        result.extend(lines[cursor-1:node.lineno-1])
        if node is func:
            result.append(newfunc)
        cursor=node.end_lineno+1
    result.extend(lines[cursor-1:])
    output=''.join(result)
    output=output.replace('from dataclasses import dataclass, replace', 'from dataclasses import replace')
    output=output.replace('from pathlib import Path\n', '')
    output=output.replace('from typing import Callable\n', '')
    output=output.replace('from proof import ProofStep, ProofRule, Relation', 'from proof import ProofRule')
    ast.parse(output)
    if 'RegisteredProofProvider' in output or 'registered_proof_providers' in output or 'providers:' in output:
        raise RuntimeError('legacy provider reference survived rewrite')
    return output


def retire_old_tests(source: str) -> str:
    tree = ast.parse(source)
    lines = source.splitlines(keepends=True)
    obsolete = {'test_r7_unregistered_goal_fail_closed','test_r7_duplicate_goal_provider_rejected'}
    funcs = [x for x in tree.body if isinstance(x,ast.FunctionDef) and x.name in obsolete]
    if len(funcs)!=2:
        if 'test_r7_duplicate_goal_provider_rejected' not in source:
            return source
        raise RuntimeError('unexpected legacy tests')
    for node in sorted(funcs,key=lambda x:x.lineno,reverse=True):
        del lines[node.lineno-1:node.end_lineno]
    result=''.join(lines)
    result=result.replace('from dataclasses import replace\n','')
    result=result.replace('    RegisteredProofProvider, build_registered_common_replay,\n    registered_proof_providers,\n','    build_registered_common_replay,\n')
    result=result.replace('from phase165_goal_only_search import GoalSearchIncompleteError\n','')
    result += '\n\ndef test_r7_public_replay_has_no_group_specific_provider_argument():\n    import inspect\n    from phase165_r52_r7_registered_common_proof import build_registered_common_replay\n    assert "providers" not in inspect.signature(build_registered_common_replay).parameters\n\n\ndef test_r7_group_specific_provider_inventory_retired():\n    import phase165_r52_r7_registered_common_proof as module\n    assert not hasattr(module, "RegisteredProofProvider")\n    assert not hasattr(module, "registered_proof_providers")\n'
    ast.parse(result)
    return result


def main():
    if not TARGET.is_file() or not TEST.is_file():
        raise FileNotFoundError('required existing production/test file missing')
    replacements = [(TARGET, retire_provider(TARGET.read_text(encoding='utf-8-sig'))),
                    (TEST, retire_old_tests(TEST.read_text(encoding='utf-8-sig')))]
    changed=[]
    for path, content in replacements:
        old=path.read_text(encoding='utf-8-sig')
        if old != content:
            backup=path.with_name(path.name+'.phase165_r6_1_before_retirement.bak')
            if not backup.exists(): shutil.copy2(path,backup)
            path.write_text(content,encoding='utf-8')
            changed.append(str(path.relative_to(ROOT)))
    print(json.dumps({'phase':'165 R6-1 unused provider retirement','modified':changed,'reference_registry_preserved':True,'full_pytest_run':False},ensure_ascii=False,indent=2))

if __name__=='__main__':main()
