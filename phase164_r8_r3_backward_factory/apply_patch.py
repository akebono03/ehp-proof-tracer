"""Fail-closed, minimal Phase 164 R8-R3 patch for the existing backward builder."""
from pathlib import Path
import ast
import shutil

ROOT = Path(__file__).resolve().parent.parent
TARGET = ROOT / 'phase161_r5_backward_proof_reconstruction.py'
BACKUP = ROOT / 'phase161_r5_backward_proof_reconstruction.phase164_r8_r3_backup.py'

OLD_IMPORT = 'from phase161_r4_literature_premise_matching import (\n    expand_phase161_r4_literature_goal,\n    match_phase161_r4_existing_premises,\n)\n'
NEW_IMPORT = OLD_IMPORT + 'from phase164_r8_proofstep_factory import derive_inference_proof_step\n'
OLD_PROOF_IMPORT = '    apply_inference_match,\n'
OLD_USE = 'result = apply_inference_match(matches[0])'
NEW_USE = 'result = derive_inference_proof_step(matches[0])'
OLD_LITERATURE_USE = 'result = apply_inference_match(inference_matches[0])'
NEW_LITERATURE_USE = 'result = derive_inference_proof_step(inference_matches[0])'


def write_changed_code(changed):
    parsed = ast.parse(changed)
    target = next(node for node in parsed.body if isinstance(node, ast.FunctionDef) and node.name == 'reconstruct_phase161_r5_goal')
    lines = changed.splitlines()
    changed_function = '\n'.join(lines[target.lineno - 1:target.end_lineno])
    imports = '\n'.join(lines[:next(i for i, line in enumerate(lines) if line.startswith('@dataclass'))]).strip()
    output = Path(__file__).with_name('CHANGED_CODE.md')
    output.write_text(
        '# Phase 164 R8-R3 — 変更コード全文\n\n'
        '変更ファイル: `phase161_r5_backward_proof_reconstruction.py`\n\n'
        '変更対象: import 全体と `reconstruct_phase161_r5_goal` 全体。\n'
        '追加テストは `tests/test_phase164_r8_r3_backward_factory.py` に全文収録。\n'
        '変更なし: `proof.py`, `hopf_rules.py`, `map_facts.py`, Factory 本体。\n\n'
        '## import 全文\n\n```python\n' + imports + '\n```\n\n'
        '## 関数全文\n\n```python\n' + changed_function + '\n```\n',
        encoding='utf-8',
    )


def apply():
    if not TARGET.is_file():
        raise FileNotFoundError(TARGET)
    if not (ROOT / 'phase164_r8_proofstep_factory.py').is_file():
        raise FileNotFoundError('R8-R2 factory is not installed')
    raw = TARGET.read_bytes()
    source = raw.decode('utf-8')
    newline = '\r\n' if b'\r\n' in raw else '\n'
    canonical = source.replace('\r\n', '\n')
    already = NEW_IMPORT in canonical and NEW_USE in canonical and NEW_LITERATURE_USE in canonical
    if already:
        print('Already installed: phase161_r5_backward_proof_reconstruction.py')
        return
    if canonical.count(OLD_IMPORT) != 1 or canonical.count(OLD_PROOF_IMPORT) != 1 or canonical.count(OLD_USE) != 1 or canonical.count(OLD_LITERATURE_USE) != 1:
        raise ValueError('Unexpected local code: refusing unsafe modification')
    parsed = ast.parse(canonical)
    functions = [n for n in parsed.body if isinstance(n, (ast.FunctionDef, ast.AsyncFunctionDef)) and n.name == 'reconstruct_phase161_r5_goal']
    if len(functions) != 1:
        raise ValueError('Target reconstruction function not found exactly once')
    uses = [n for n in ast.walk(functions[0]) if isinstance(n, ast.Call) and isinstance(n.func, ast.Name) and n.func.id == 'apply_inference_match']
    if len(uses) != 2:
        raise ValueError('Unexpected inference call count: refusing patch')
    changed = canonical.replace(OLD_IMPORT, NEW_IMPORT, 1).replace(OLD_PROOF_IMPORT, '', 1).replace(OLD_USE, NEW_USE, 1).replace(OLD_LITERATURE_USE, NEW_LITERATURE_USE, 1)
    ast.parse(changed)
    if not BACKUP.exists():
        shutil.copy2(TARGET, BACKUP)
    TARGET.write_bytes(changed.replace('\n', newline).encode('utf-8'))
    write_changed_code(changed)
    print('Updated: phase161_r5_backward_proof_reconstruction.py; backup:', BACKUP.name)


if __name__ == '__main__':
    apply()
