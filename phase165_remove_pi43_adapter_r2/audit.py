"""Read-only audit of the retired pi4^3-specific adapter."""
from __future__ import annotations
import ast
import json
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
OLD_MODULE = 'phase165_r52_r23_existing_rule_adapter'
OLD_FUNCTION = 'expand_existing_pi43_rules'


def audit_repository(root: Path) -> dict[str, object]:
    """Audit root-level importable Python modules; do not alter production files."""
    shared = root / 'phase165_r52_r9_shared_math.py'
    if not shared.is_file():
        raise FileNotFoundError(shared)
    targets: list[dict[str, str | int]] = []
    unreadable: list[str] = []
    for path in sorted(root.glob('*.py')):
        try:
            code = path.read_text(encoding='utf-8-sig')
            tree = ast.parse(code, filename=str(path))
        except (SyntaxError, UnicodeError):
            unreadable.append(path.name)
            continue
        for node in ast.walk(tree):
            if isinstance(node, ast.ImportFrom) and node.module == OLD_MODULE:
                targets.append({'file': path.name, 'line': node.lineno, 'kind': 'module_import'})
            elif isinstance(node, ast.Import):
                if any(x.name == OLD_MODULE for x in node.names):
                    targets.append({'file': path.name, 'line': node.lineno, 'kind': 'module_import'})
            elif isinstance(node, ast.Name) and node.id == OLD_FUNCTION:
                targets.append({'file': path.name, 'line': node.lineno, 'kind': 'function_name'})
    shared_code = shared.read_text(encoding='utf-8-sig')
    shared_tree = ast.parse(shared_code)
    provider = next((n for n in shared_tree.body if isinstance(n, ast.FunctionDef) and n.name == 'shared_expansion_provider'), None)
    if provider is None:
        raise RuntimeError('Shared expansion provider is missing')
    provider_source = ast.get_source_segment(shared_code, provider) or ''
    catalog_connectors = {
        'generic_backward': 'build_generic_backward_expansion_provider' in provider_source,
        'verified_witness_inverse': 'reverse_rules_from_witnesses' in provider_source,
        'seeded_goals': 'generate_seeded_backward_goals' in provider_source,
    }
    adapter_exists = (root / (OLD_MODULE + '.py')).exists()
    status = ('REMOVED' if not adapter_exists and not targets and all(catalog_connectors.values())
              else 'REVIEW_REQUIRED')
    return {'phase': '165 Adapter Removal R2', 'status': status,
            'adapter_file_exists': adapter_exists, 'active_root_references': targets,
            'unparsed_root_files': unreadable, 'generic_connectors': catalog_connectors,
            'full_pytest_run': False}


def main() -> None:
    result = audit_repository(ROOT)
    out = Path(__file__).resolve().parent / 'audit_result.json'
    out.write_text(json.dumps(result, ensure_ascii=False, indent=2) + '\n', encoding='utf-8')
    print(json.dumps(result, ensure_ascii=False, indent=2))
    if result['status'] != 'REMOVED':
        raise SystemExit(1)


if __name__ == '__main__':
    main()
