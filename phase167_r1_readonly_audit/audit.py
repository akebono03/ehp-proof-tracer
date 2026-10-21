"""Phase 167 R1 read-only audit. No production imports or writes to repository."""
from __future__ import annotations
import ast
import json
from pathlib import Path
import sys

ROOT = Path(__file__).resolve().parent.parent
REQUIRED = {
    'adapter': ('phase165_r56_presentation_adapter.py', 'render_completed_shared_narrative'),
    'proofstep_renderer': ('phase165_r57_r10_step_narrative.py', 'render_completed_from_proofsteps'),
    'reference_renderer': ('toda_group_proof_narrative_references.py', 'render_toda_group_proof_narrative_reference_entries_markdown'),
    'public_renderer': ('toda_group_proof_narrative_renderer.py', 'render_toda_group_proof_narrative_markdown'),
}

def functions(path: Path):
    tree = ast.parse(path.read_text(encoding='utf-8-sig'), filename=str(path))
    return {n.name: n for n in tree.body if isinstance(n, (ast.FunctionDef, ast.AsyncFunctionDef))}

def audit(repo: Path):
    checked = {}
    for key, (filename, name) in REQUIRED.items():
        path = repo / filename
        if not path.is_file():
            checked[key] = {'file': filename, 'status': 'missing'}
            continue
        names = functions(path)
        node = names.get(name)
        checked[key] = {'file': filename, 'function': name, 'status': 'found' if node else 'missing_function', 'line': getattr(node, 'lineno', None)}
    ref_file = repo / 'toda_group_proof_narrative_references.py'
    adapter_file = repo / 'phase165_r56_presentation_adapter.py'
    proof_file = repo / 'phase165_r57_r10_step_narrative.py'
    ref = ref_file.read_text(encoding='utf-8-sig') if ref_file.exists() else ''
    adapter = adapter_file.read_text(encoding='utf-8-sig') if adapter_file.exists() else ''
    proof = proof_file.read_text(encoding='utf-8-sig') if proof_file.exists() else ''
    saved = repo / 'phase165_r1_audit_results/pi4_3_public.md'
    narrative = saved.read_text(encoding='utf-8-sig') if saved.exists() else None
    steps_file = repo / 'phase165_r2_order_audit_results/pi4_3_steps.json'
    steps = json.loads(steps_file.read_text(encoding='utf-8-sig')) if steps_file.exists() else {}
    names = [step.get('inference_name') for step in steps.get('steps', [])]
    return {
        'mode': 'READ_ONLY', 'repository': str(repo),
        'functions': checked,
        'source_checks': {
            'reference_5_1_branch': 'entry.reference.locator == "(5.1)"' in ref,
            'reference_5_1_component_keys': 'component_keys' in ref,
            'adapter_has_conditional_alternate_renderer': 'render_completed_from_proofsteps(result, root)' in adapter,
            'alternate_renderer_includes_given_statements': '_render_generic_narrative_step(step)' in proof,
            'alternate_renderer_exposes_rule_names': 'f"{prefix}{rule}' in proof,
        },
        'saved_artifact_checks': {
            'artifact_present': narrative is not None,
            'reference_5_1_heading': '**[R1] (5.1).**' in (narrative or ''),
            'reference_5_1_formula_present_in_section': ('\\pi_{n}^{n}' in (narrative or '').split('## 証明')[0]),
            'rule_name_in_body': 'infinite cyclic quotient structure' in (narrative or ''),
            'eta_generator_image_occurrences': (narrative or '').count('E(\\eta_{2})') + (narrative or '').count('E\\eta_{2}'),
            'saved_step_count': len(steps.get('steps', [])),
            'has_quotient_rule': 'infinite cyclic quotient structure' in names,
            'has_first_iso_rule': 'first isomorphism theorem for generated kernel' in names,
        },
        'limits': [
            'Saved artifacts do not establish the current Web response.',
            'Static source inspection does not prove which conditional renderer runs.',
            'No production modules were imported and no pytest was invoked.',
        ],
    }

def main():
    if len(sys.argv) != 2:
        raise SystemExit('Usage: python audit.py <repository-root>')
    report = audit(Path(sys.argv[1]).resolve())
    output = Path(__file__).resolve().parent / 'r1_report.json'
    output.write_text(json.dumps(report, ensure_ascii=False, indent=2), encoding='utf-8')
    print(json.dumps(report, ensure_ascii=False, indent=2))
    print('REPORT:', output)

if __name__ == '__main__':
    main()
