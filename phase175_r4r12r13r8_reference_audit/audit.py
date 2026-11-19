"""Phase 175 R13R8 read-only audit of citation projection and line endings."""
from __future__ import annotations

import argparse
import ast
import json
import subprocess
from pathlib import Path

ROOT_FILES = (
    'phase168_r3_3_proof_narrative_model.py',
    'phase168_r3_37c_reference_projection.py',
    'phase168_r3_5_model_renderer.py',
    'toda_group_proof_narrative_references.py',
    'toda_group_proof_narrative_contribution_renderer.py',
)
TARGET_LOCATORS = ('(5.11)', '(5.8)')


def git(root: Path, *args: str) -> dict[str, object]:
    result = subprocess.run(['git', *args], cwd=root, capture_output=True, text=True, encoding='utf-8', errors='replace', check=False)
    return {'returncode': result.returncode, 'stdout': result.stdout.strip(), 'stderr': result.stderr.strip()}


def inspect_module(path: Path) -> dict[str, object]:
    raw = path.read_bytes()
    text = raw.decode('utf-8-sig')
    module = ast.parse(text, filename=str(path))
    functions = [node.name for node in module.body if isinstance(node, (ast.FunctionDef, ast.AsyncFunctionDef))]
    return {
        'path': path.name, 'size_bytes': len(raw), 'crlf': raw.count(b'\r\n'),
        'bare_lf': raw.count(b'\n') - raw.count(b'\r\n'),
        'functions': functions, 'locator_mentions': {x: text.count(x) for x in TARGET_LOCATORS},
    }


def collect(root: Path) -> dict[str, object]:
    paths = {name: root / name for name in ROOT_FILES}
    missing = [name for name, path in paths.items() if not path.is_file()]
    modules = {name: inspect_module(path) for name, path in paths.items() if path.is_file()}
    model_source = paths[ROOT_FILES[0]].read_text(encoding='utf-8-sig') if not missing or paths[ROOT_FILES[0]].exists() else ''
    projection_source = paths[ROOT_FILES[1]].read_text(encoding='utf-8-sig') if paths[ROOT_FILES[1]].exists() else ''
    renderer_source = paths[ROOT_FILES[2]].read_text(encoding='utf-8-sig') if paths[ROOT_FILES[2]].exists() else ''
    bridge = {
        'model_has_statement_bodies': 'statement_bodies=' in model_source,
        'model_has_assertion_id_fallback': 'project_cited_proof_step_reference_bodies(' in model_source,
        'projection_limits_fallback_to_verified_sources': 'project_verified_cited_toda_given_reference_body(' in projection_source,
        'renderer_outputs_statement_bodies': 'for sentence in citation.statement_bodies:' in renderer_source,
        'renderer_has_step_citation_mapping': 'model.step_citation_numbers' in renderer_source,
    }
    prior = root / 'phase175_r4r12r13r7_typed_nu_prime_notation'
    relevant = sorted(str(p.relative_to(root)) for p in prior.rglob('*.py')) if prior.is_dir() else []
    status = git(root, 'status', '--short')
    changed = git(root, 'diff', '--numstat')
    head = git(root, 'rev-parse', 'HEAD')
    branch = git(root, 'branch', '--show-current')
    return {
        'phase': '175_R4R12R13R8', 'mode': 'READ_ONLY_SOURCE_AUDIT',
        'repo_root': str(root), 'head': head, 'branch': branch, 'status': status,
        'diff_numstat': changed, 'missing': missing, 'modules': modules,
        'citation_pipeline': bridge, 'r13r7_python_files': relevant,
        'findings': [
            'R3/R7 numbered references with empty bodies require verification against actual cited ProofStep and registry links.',
            'Do not generate statements from locators alone or add a narrative-only citation.',
            'Web render and proof search must be checked in the user environment before declaring R13R8 complete.',
        ],
        'gate': 'AUDIT_READY_NOT_FIX_COMPLETE' if not missing and all(bridge.values()) else 'SOURCE_OR_PIPELINE_GAP',
    }


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument('--root', type=Path, default=Path.cwd())
    parser.add_argument('--output', type=Path, default=None)
    args = parser.parse_args()
    root = args.root.resolve()
    report = collect(root)
    payload = json.dumps(report, indent=2, ensure_ascii=False) + '\n'
    if args.output is None:
        print(payload, end='')
    else:
        output = args.output.resolve()
        output.parent.mkdir(parents=True, exist_ok=True)
        output.write_text(payload, encoding='utf-8')
        print('PHASE175_R13R8_REPORT=' + str(output))
        print('PHASE175_R13R8_GATE=' + report['gate'])
    return 0 if report['gate'] == 'AUDIT_READY_NOT_FIX_COMPLETE' else 2


if __name__ == '__main__':
    raise SystemExit(main())
