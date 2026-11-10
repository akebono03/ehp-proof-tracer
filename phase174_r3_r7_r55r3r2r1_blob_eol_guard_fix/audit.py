"""Review the production typed proof and the absence of R55R3 narrative hooks."""
from __future__ import annotations

import argparse
import json
import os
from pathlib import Path
import tempfile

from phase174_r3_r7_r55r3r2r1_blob_eol_guard_fix.install import (
    ROOT, LEGACY_A, LEGACY_B, construct_sources, _run_git,
)


def inspect_shared_display() -> dict[str, object]:
    from phase174_r3_r7_r55r2_reference_tree_audit.audit import inspect_public_proof
    from phase174_r3_r7_r54_public_http_narrative_audit.audit import inspect_public_http_proof
    from phase168_r3_27_typed_statement_projection import typed_sentence
    from phase174_r3_r7_r25_prop27_isolated_inference.rule import typed_specialization

    if (ROOT / LEGACY_A).exists() or (ROOT / LEGACY_B).exists():
        raise RuntimeError('A bespoke R55R3 narrative package is still installed')
    reference = (ROOT / 'phase168_r3_37c_reference_projection.py').read_text(encoding='utf-8-sig')
    renderer = (ROOT / 'phase168_r3_5_model_renderer.py').read_text(encoding='utf-8-sig')
    if ('project_certified_proof_sentence' in renderer
            or 'r55r3_common_proof_display' in reference
            or 'r55r3_common_proof_display' in renderer
            or '_typed_upper_delta_transition' in renderer):
        raise RuntimeError('Obsolete R55R3 special Narrative hook remains')
    report = inspect_public_proof()
    if report['status'] != 'complete' or report['root_ancestor_steps'] != 28 or report['open_goals']:
        raise RuntimeError('The certified public root proof was changed')
    if not (report['r2']['reference_body_present']
            and report['r7']['reference_body_present']
            and report['source_proof']['upper_delta_four_distinct_inference_premises']
            and report['narrative']['r7_hopf_delta_specialization_in_proof']):
        raise RuntimeError('Certified typed formulas or literature bodies missing')
    # Stable typed formula in another legitimate (even) n, independent of
    # the n=6 public proof. No group-specific narrative is permitted.
    generalized = typed_sentence(typed_specialization(8), None)
    if generalized is None or r'\iota_{17}' not in generalized or r'\iota_{15}' not in generalized:
        raise RuntimeError('The shared theorem formatter only handles n=6')
    html = inspect_public_http_proof()
    if not html['both_http_200'] or not html['both_complete_proof']:
        raise RuntimeError('The shared HTTP proof presentation regressed')
    if any(row['repeated_intro_count'] != 1 for row in html['cases']):
        raise RuntimeError('The shared proof introduction is duplicated')
    return {
        'target': 'pi_12^7 = 0',
        'source_first_root_complete': True,
        'root_ancestor_steps': report['root_ancestor_steps'],
        'r2_r7_reference_body_count': len(report['r2']['statement_bodies']) + len(report['r7']['statement_bodies']),
        'r2_general_source_formula': report['r2']['statement_bodies'],
        'r7_general_source_formula': report['r7']['statement_bodies'],
        'r7_typed_formula_visible': report['narrative']['r7_hopf_delta_specialization_in_proof'],
        'r2_n6_zero_formula_visible': report['narrative']['r2_n6_zero_relation_in_proof'],
        'source_signed_lower_delta_displayed_as_cited': report['narrative']['unnecessary_lower_delta_plusminus_in_proof'],
        'generic_n8_prop27_formula': generalized,
        'dedicated_r55r3_narrative_remaining': False,
        'both_http_200': True,
        'both_http_complete': True,
        'new_givens': 0,
        'new_math_rules': 0,
        'full_pytest': False,
    }


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--dry-run', action='store_true')
    args = parser.parse_args()
    info = None
    if args.dry_run:
        construct_sources()
        gate = 'PASS_REVIEWED_SOURCE_PREFLIGHT'
    else:
        info = inspect_shared_display()
        gate = 'PASS_R55R3_NARRATIVE_REMOVED_SHARED_TYPED_DISPLAY'
    result = {
        'phase':'174-R3-R7-R55R3R2', 'head':_run_git('rev-parse','HEAD'),
        'observations':info, 'gate':gate,
    }
    directory = Path(os.environ.get('LOCALAPPDATA', tempfile.gettempdir())) / (
        'EHPProofTracerAudit/phase174_r3_r7_r55r3r2'
    )
    directory.mkdir(parents=True, exist_ok=True)
    path = directory / ('preflight.json' if args.dry_run else 'shared_display.json')
    path.write_text(json.dumps(result, ensure_ascii=False, indent=2) + '\n', encoding='utf-8')
    print('PHASE174_R55R3R2R1_LOCAL_HEAD=' + result['head'])
    if info:
        for key, value in info.items():
            print('PHASE174_R55R3R2R1_' + key.upper() + '=' + str(value))
    print('PHASE174_R55R3R2R1_REPORT=' + str(path))
    print('PHASE174_R55R3R2R1_GATE=' + gate)
    print('(END)')
    return 0


if __name__ == '__main__':
    raise SystemExit(main())
