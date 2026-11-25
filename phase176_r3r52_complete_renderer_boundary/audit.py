"""Read-only observation of the actual completed Web proof and its projections."""
from __future__ import annotations

import argparse
import ast
from collections import Counter
import json
import os
from pathlib import Path
import re
import subprocess
import tempfile
from unittest.mock import patch

from phase176_r3r46r1_prior_group_availability.apply import normalize, pinned

ROOT = Path(__file__).resolve().parents[1]
PACKAGE = Path(__file__).resolve().parent.name
PINS = {
    'web_group_proof.py': '2c66da9c8e80a13812a63b6adda34c9414d8413c',
    'web_group_proof_common.py': '6d42e2d5d74e009bc4f8c903f0f4014ba6a9c863',
    'phase165_r52_r3_web_adapter.py': 'dda215780c0468cf421592aff86c79b1f5482eed',
    'toda_conclusion_latex_renderer.py': 'b73f204b2e187a6873d1650406b7eafeecfda312',
    'phase168_r3_27_typed_statement_projection.py': 'f324c9cfd19a8710daf0bc6c99926b07c6e3b3b5',
    'phase168_r3_5_model_renderer.py': 'f77616cf4ccc734954754e6e5d3a8d8b550dfef1',
    'phase168_r3_41p13_trust_boundary/verification.py': '547464846ce574d227092a4aacb895d2e2dfefca',
    'phase168_r3_3_proof_narrative_model.py': '6a298aae5f7cbc8ec1be5b02a931b6b7a72e9d52',
    'phase168_r3_4_link_bridge.py': 'c3a6233a57c41e61e6649ee33c7a336d7aa1c664',
    'phase176_r3r51_verified_db_subgroup_lift/audit.py': '620445025b13ebd678ee324dc0ca02fd53be5b80',
}


def git(*args):
    return subprocess.check_output(['git', *args], cwd=ROOT)


def preflight():
    from phase176_r3r51_verified_db_subgroup_lift.apply import planned_changes
    if any(a != b for a, b in planned_changes().values()):
        raise RuntimeError('R3R51_NOT_APPLIED')
    for name, pin in PINS.items():
        source, _ = normalize((ROOT / name).read_bytes())
        if not pinned(source, pin):
            raise RuntimeError('UNREVIEWED_RENDERER:' + name)
        ast.parse(source, filename=name)
    return git('rev-parse', 'HEAD').decode('ascii').strip()


def kernel_style(value):
    """Classify only the right side of a displayed kernel equality."""
    if not isinstance(value, str) or r'\ker' not in value or '=' not in value:
        return 'not_kernel'
    rhs = value.split('=', 1)[1]
    if r'\langle' in rhs and r'\rangle' in rhs:
        return 'subgroup'
    if r'\mathbb{Z}' in rhs:
        return 'integer_braces'
    return 'other'


def display_audit(markdown):
    """Report rendered equality repetitions without modifying the proof or text."""
    equations = []
    for line in markdown.splitlines():
        for math in re.findall(r'\$([^$\n]+)\$', line):
            if math.count('=') != 1 or r'\ker' in math:
                continue
            lhs, rhs = math.split('=')
            if lhs.strip() and rhs.strip():
                equations.append(math.strip())
    counts = Counter(equations)
    return {'apparent_identity_equations': [v for v in equations
                                             if v.split('=')[0].strip() == v.split('=')[1].strip()],
            'repeated_equations': {k: v for k, v in counts.items() if v > 1},
            'english_exactness_present': 'is exact' in markdown}


def observe():
    from phase176_r3r49_hopf_image_frontier.audit import capture_web
    from phase176_r3r50_strict_nu_prime_connection.audit import walk_tree
    from phase176_r3r43r1_finite_cyclic_subgroup_lift_isolated.rule import (
        RULE_NAME, finite_cyclic_subgroup_lift_inputs,
    )
    from phase165_r12_r2_quotient_rules import CyclicStructureStatement, KernelMultipleStatement
    from phase169_r10e4_ordered_db_prior.db_prior import verified_db_step
    from phase176_r3r48_cited_finite_delta_kernel.rule import RULE_NAME as KERNEL_RULE
    from proof import ProofRule, find_inference_matches_for_rule
    from toda_conclusion_latex_renderer import render_repository_conclusion_latex
    from web_group_proof_common import _group_proof_statement_latex
    import phase165_r52_r3_web_adapter as adapter
    import phase168_r3_5_model_renderer as renderer
    import phase168_r3_27_typed_statement_projection as projection
    import phase168_r3_41p13_trust_boundary as trust

    captures, verified, markdowns, projections = [], [], [], []
    original_adapter = adapter.build_partial_web_group_proof_view
    original_verify = trust.verify_proof_tree_for_narrative
    original_render = renderer.render_model_backed_narrative_markdown
    original_sentence = projection.typed_sentence

    def observed_adapter(result, **kwargs):
        view = original_adapter(result, **kwargs)
        captures.append((result, kwargs.get('narrative_model'), view))
        return view

    def observed_verify(*args, **kwargs):
        value = original_verify(*args, **kwargs)
        verified.append((args, kwargs, value))
        return value

    def observed_render(result, model):
        value = original_render(result, model)
        markdowns.append((model, value))
        return value

    def observed_sentence(statement, step):
        value = original_sentence(statement, step)
        if type(statement) is KernelMultipleStatement:
            projections.append((step, value))
        return value

    # All observers call through unchanged. No proof step or rendered text is injected.
    with patch.object(adapter, 'build_partial_web_group_proof_view', observed_adapter), \
         patch.object(trust, 'verify_proof_tree_for_narrative', observed_verify), \
         patch.object(renderer, 'render_model_backed_narrative_markdown', observed_render), \
         patch.object(projection, 'typed_sentence', observed_sentence):
        invocation, result, calls, key = capture_web()
    if len(captures) != 1 or len(verified) != 1 or len(markdowns) != 1:
        raise RuntimeError('UNEXPECTED_PUBLIC_RENDER_OR_TRUST_CALL_COUNT')
    rendered_result, model, view = captures[0]
    bridge, root = invocation['bridge'], invocation['goal']
    if (rendered_result is not result or verified[0][0][0] is not result
            or verified[0][0][1] is not bridge
            or model is not markdowns[0][0] or model.root_index is None):
        raise RuntimeError('SEARCH_TRUST_RENDER_IDENTITY_MISMATCH')
    if result.status.value != 'complete' or key != 'generic-complete-proof' or result.open_goals:
        raise RuntimeError('ROOT_NOT_COMPLETE')
    root_step = model.steps[model.root_index]
    if root_step.conclusion != root or root_step.rule is not ProofRule.INFERENCE:
        raise RuntimeError('ROOT_NOT_INFERRED')
    tree = walk_tree(root_step)
    if {id(s) for s in tree} != {id(s) for s in result.proven_steps}:
        raise RuntimeError('ACCEPTED_STEP_ANCESTRY_MISMATCH')
    inference_count, given_count = verified[0][2]
    if inference_count + given_count != len(tree):
        raise RuntimeError('TRUST_COUNT_MISMATCH')
    goal = CyclicStructureStatement(root.lhs, root.rhs.generator, root.rhs.order)
    lifts = [s for s in tree if s.conclusion == goal and s.rule is ProofRule.INFERENCE
             and s.inference_rule is not None and s.inference_rule.name == RULE_NAME]
    if len(lifts) != 1:
        raise RuntimeError('LIFT_NOT_UNIQUE')
    lift = lifts[0]
    parents = lift.premises
    if len(parents) != 5 or any(parents[i].rule is not ProofRule.INFERENCE for i in (0,1,3,4)):
        raise RuntimeError('LIFT_PREMISE_RULES_CHANGED')
    if not verified_db_step(parents[2], proof_target=root, bridge=bridge):
        raise RuntimeError('LIFT_DB_PRIOR_NOT_VERIFIED')
    inputs = tuple(s.conclusion for s in parents)
    if finite_cyclic_subgroup_lift_inputs(goal, *inputs[1:]) != inputs:
        raise RuntimeError('LIFT_TYPED_INPUTS_CHANGED')
    if not find_inference_matches_for_rule(lift.inference_rule, parents):
        raise RuntimeError('LIFT_REPLAY_FAILED')
    kernel = parents[3]
    if type(kernel.conclusion) is not KernelMultipleStatement or kernel.inference_rule.name != KERNEL_RULE:
        raise RuntimeError('KERNEL_INFERENCE_CHANGED')
    db_rows, cited_rows, other_givens = [], [], []
    for s in tree:
        if s.rule is not ProofRule.GIVEN:
            continue
        if s.conclusion in (root, goal):
            raise RuntimeError('ROOT_AS_GIVEN')
        if verified_db_step(s, proof_target=root, bridge=bridge):
            db_rows.append(repr(s.conclusion))
            continue
        links = [link.assertion_id for link in bridge.proof_links if link.step is s]
        if links:
            cited_rows.append({'statement': repr(s.conclusion), 'assertion_ids': links})
        else:
            # The real public trust gate has already accepted this tree. Report
            # any other allowed provenance rather than assume it is a DB row.
            other_givens.append(repr(s.conclusion))
    direct = render_repository_conclusion_latex(kernel.conclusion)
    trace_math, fallback = _group_proof_statement_latex(kernel.conclusion)
    if fallback is not None or direct != trace_math or kernel_style(direct) != 'subgroup':
        raise RuntimeError('R3R47_COMMON_KERNEL_DISPLAY_REGRESSION')
    rendered = [v for s,v in projections if s is kernel]
    markdown = markdowns[0][1]
    web_kernel_math = list(dict.fromkeys(
        value for line in view.rendered_lines
        for value in (line.statement_latex, *(seg.value for seg in line.segments
                      if seg.kind in ('inline_math', 'display_math')))
        if kernel_style(value) != 'not_kernel'
    ))
    styles = [kernel_style(v) for v in rendered]
    if 'integer_braces' not in styles or not any(kernel_style(v) == 'integer_braces' for v in web_kernel_math):
        raise RuntimeError('EXPECTED_COMPLETE_KERNEL_DISPLAY_DEFECT_NOT_REPRODUCED')
    # Display-only comparison using a real accepted prefix, not a new search.
    from phase165_r52_partial_proof import make_partial_proof_result, ProofSearchStatus
    from phase168_r3_4_link_bridge import build_linked_proof_narrative_model
    cut = next(i for i, s in enumerate(result.proven_steps) if s is lift)
    prefix = result.proven_steps[:cut]
    if not any(s is kernel for s in prefix):
        raise RuntimeError('KERNEL_NOT_IN_ACCEPTED_PREFIX')
    if any(s.conclusion == root for s in prefix):
        raise RuntimeError('ROOT_ALREADY_IN_PREFIX')
    partial = make_partial_proof_result(n=3, k=5, status=ProofSearchStatus.PARTIAL,
                                        proven_steps=prefix, open_goals=(root,))
    partial_model = build_linked_proof_narrative_model(partial, bridge)
    partial_markdown = original_render(partial, partial_model)
    if direct not in partial_markdown:
        raise RuntimeError('PARTIAL_PREFIX_SUBGROUP_DISPLAY_NOT_FOUND')
    citation_rows = [{'number': c.number, 'locator': c.reference.locator or c.reference.label,
                      'step_indices': list(c.step_indices), 'assertion_ids': list(c.assertion_ids),
                      'statement_bodies': list(c.statement_bodies)} for c in model.citations]
    report = {'gate':'PASS_R3R52_COMPLETE_PROOF_RENDERER_BOUNDARY_AUDITED',
              'status':result.status.value, 'web_key':key, 'root_group_proved':True,
              'accepted_step_count':len(result.proven_steps), 'root_tree_steps':len(tree),
              'open_goals':[], 'trust_boundary_called_and_passed':True,
              'trust_inference_count':inference_count, 'trust_given_count':given_count,
              'baseline_62_steps_preserved':len(tree)==62,
              'partial_prefix_projection_subgroup':True,
              'partial_prefix_is_new_search':False, 'partial_prefix_step_count':len(prefix),
              'lift_replayed':True, 'codomain_prior_verified':True,
              'lift_premise_rules':[s.rule.value for s in parents],
              'verified_db_givens':db_rows, 'linked_source_givens':cited_rows,
              'other_trust_accepted_givens':other_givens,
              'citation_rows':citation_rows, 'kernel_direct_latex':direct,
              'kernel_complete_projection':rendered, 'kernel_web_math':web_kernel_math,
              'kernel_display_defect_reproduced':True,
              'diagnosis':'COMPLETE_TYPED_SENTENCE_USES_LEGACY_INTEGER_BRACES',
              'display_findings':display_audit(markdown), 'new_math_rules':0,
              'new_given_registrations':0, 'full_pytest':'NOT_RUN'}
    # Persist a structured proof ancestry index without manufacturing any edges.
    indices = {id(s): i for i,s in enumerate(tree)}
    report['proof_ancestry'] = [{'index':i, 'rule':s.rule.value,
        'inference_rule':getattr(s.inference_rule,'name',None), 'conclusion':repr(s.conclusion),
        'premises':[indices[id(p)] for p in s.premises]} for i,s in enumerate(tree)]
    return report, markdown, partial_markdown


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('--dry-run', action='store_true')
    args = parser.parse_args()
    head = preflight()
    print('PHASE176_R3R52_HEAD='+head)
    if args.dry_run:
        print('PHASE176_R3R52_GATE=PASS_R3R52_DRYRUN')
        return 0
    before = (git('diff','--binary','HEAD'), git('status','--porcelain'))
    report, markdown, partial_markdown = observe()
    after = (git('diff','--binary','HEAD'), git('status','--porcelain'))
    if before != after:
        raise RuntimeError('AUDIT_CHANGED_REPOSITORY')
    report['repository_unchanged'] = True
    report['head'] = head
    folder = Path(os.environ.get('LOCALAPPDATA') or tempfile.gettempdir()) / 'EHPProofTracerAudit' / PACKAGE
    folder.mkdir(parents=True, exist_ok=True)
    path = folder / 'report.json'
    path.write_text(json.dumps(report, ensure_ascii=False, indent=2)+'\n', encoding='utf-8')
    (folder / 'actual_narrative.md').write_text(markdown, encoding='utf-8')
    (folder / 'partial_prefix_narrative.md').write_text(partial_markdown, encoding='utf-8')
    for k,v in report.items():
        if k not in ('proof_ancestry','citation_rows','linked_source_givens','verified_db_givens'):
            print('PHASE176_R3R52_'+k.upper()+'='+json.dumps(v, ensure_ascii=False))
    print('PHASE176_R3R52_CITATION_COUNT='+str(len(report['citation_rows'])))
    print('REPORT='+str(path))
    print('NARRATIVE='+str(folder / 'actual_narrative.md'))
    return 0


if __name__ == '__main__':
    raise SystemExit(main())
