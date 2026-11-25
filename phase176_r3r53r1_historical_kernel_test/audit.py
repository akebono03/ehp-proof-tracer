"""Compare the reviewed pre-R53 projection and current renderer on one real proof."""
from __future__ import annotations

import ast
import json
import os
from pathlib import Path
import re
import subprocess
import tempfile
from unittest.mock import patch

from phase176_r3r46r1_prior_group_availability.apply import normalize, pinned
from phase176_r3r53_common_kernel_renderer.apply import ROOT, PIN, TARGET, updated_source

EXPECTED = r'\ker(E:\pi_{3}^{2}\to \pi_{4}^{3})=\langle 2\eta_{2}\rangle'
HISTORICAL = r'\ker E=\mathbb{Z}\{2\eta_{2}\}'
ROOT_MATH = r'\pi_{4}^{3} = \mathbb{Z}/2\{\eta_{3}\}'


def old_projection(module):
    """Load only the old function from the pinned Git blob, without editing disk."""
    raw = subprocess.check_output(['git','cat-file','blob',PIN], cwd=ROOT)
    source, _ = normalize(raw)
    if not pinned(source, PIN) or updated_source(raw) == raw:
        raise RuntimeError('UNVERIFIED_OLD_PROJECTION')
    nodes = [node for node in ast.parse(source).body if isinstance(node, ast.FunctionDef)
             and node.name == 'typed_sentence']
    if len(nodes) != 1:
        raise RuntimeError('OLD_PROJECTION_NOT_UNIQUE')
    namespace = dict(vars(module))
    exec(compile(ast.Module(body=nodes, type_ignores=[]), '<reviewed R3R52 typed_sentence>', 'exec'), namespace)
    return namespace['typed_sentence']


def observe():
    from phase165_r52_partial_proof import ProofSearchStatus
    from phase165_r52_r9_shared_math import build_shared_typed_bridge
    from phase165_r55_nk_only_goal import search_group_from_registered_goal
    from phase168_r3_4_link_bridge import build_linked_proof_narrative_model
    from phase168_r3_5_model_renderer import render_model_backed_narrative_markdown
    import phase168_r3_27_typed_statement_projection as projection
    from phase165_r12_r2_quotient_rules import KernelMultipleStatement, QuotientIsomorphismStatement
    from phase165_r12_r13_kernel_image import SuspensionKernelFreeCyclicStatement
    from homotopy_groups import TodaPrimaryGroup, TodaSuspensionMap
    from proof import ProofRule
    from toda_conclusion_latex_renderer import render_repository_conclusion_latex
    from phase176_r3r50_strict_nu_prime_connection.audit import walk_tree

    raw = TARGET.read_bytes()
    if updated_source(raw) != raw:
        raise RuntimeError('R3R53_NOT_APPLIED')
    # Exactly the same search/model route as the historical integration test.
    bridge = build_shared_typed_bridge()
    result = search_group_from_registered_goal(n=3, k=1, bridge=bridge)
    if result.status is not ProofSearchStatus.COMPLETE or result.open_goals:
        raise RuntimeError('HISTORICAL_PI43_PROOF_NOT_COMPLETE')
    roots = [s for s in result.proven_steps if s.conclusion == result.conclusion]
    if not roots:
        raise RuntimeError('HISTORICAL_PI43_ROOT_MISSING')
    tree = walk_tree(roots[-1])
    model = build_linked_proof_narrative_model(result, bridge)
    snapshot = tuple((id(s), repr(s.conclusion), tuple(id(p) for p in s.premises)) for s in tree)
    baseline = old_projection(projection)
    with patch.object(projection, 'typed_sentence', baseline):
        before = render_model_backed_narrative_markdown(result, model)
    after = render_model_backed_narrative_markdown(result, model)
    mapping = TodaSuspensionMap(TodaPrimaryGroup(3,2), TodaPrimaryGroup(4,3))
    kernels = [s for s in tree if type(s.conclusion) is KernelMultipleStatement
               and s.conclusion.map == mapping and s.conclusion.domain == mapping.source_group
               and s.conclusion.multiple == 2 and s.rule is ProofRule.INFERENCE]
    matching = [s for s in kernels if render_repository_conclusion_latex(s.conclusion) == EXPECTED]
    free_kernels = [repr(s.conclusion) for s in tree if type(s.conclusion) is SuspensionKernelFreeCyclicStatement]
    quotient_steps = [s for s in tree if type(s.conclusion) is QuotientIsomorphismStatement
                      and s.conclusion.map == mapping and s.conclusion.multiple == 2]
    unchanged = snapshot == tuple((id(s), repr(s.conclusion), tuple(id(p) for p in s.premises)) for s in tree)
    report = {
        'status': result.status.value, 'open_goals': [repr(g) for g in result.open_goals],
        'root': repr(result.conclusion), 'root_tree_steps': len(tree),
        'old_assertion_in_pre_r53': HISTORICAL in before,
        'old_assertion_in_current': HISTORICAL in after,
        'common_kernel_in_current': EXPECTED in after,
        'common_kernel_in_pre_r53': EXPECTED in before,
        'matching_kernel_steps': len(matching),
        'free_kernel_statements': free_kernels,
        'quotient_steps': len(quotient_steps), 'proof_tree_unchanged': unchanged,
        'old_kernel_math': [m for m in re.findall(r'\$([^$\n]+)\$',before) if r'\ker' in m],
        'new_kernel_math': [m for m in re.findall(r'\$([^$\n]+)\$',after) if r'\ker' in m],
        'new_root_visible': ROOT_MATH in after,
        'new_math_rules': 0, 'new_given_registrations': 0, 'full_pytest': 'NOT_RUN',
    }
    # Preserve evidence even if the premise or current display is unexpected.
    folder = Path(os.environ.get('LOCALAPPDATA') or tempfile.gettempdir()) / 'EHPProofTracerAudit' / 'phase176_r3r53r1_historical_kernel_test'
    folder.mkdir(parents=True, exist_ok=True)
    (folder/'pre_r53_pi43.md').write_text(before, encoding='utf-8')
    (folder/'current_pi43.md').write_text(after, encoding='utf-8')
    ok = (bool(matching) and bool(quotient_steps) and unchanged and EXPECTED in after
          and ROOT_MATH in after and '準同型定理' in after
          and after.count('次の完全列を考える') == 1)
    report['gate'] = ('PASS_R3R53R1_HISTORICAL_EXPECTATION_VERIFIED' if ok
                      else 'FAIL_R3R53R1_HISTORICAL_PROOF_OR_DISPLAY_UNEXPECTED')
    (folder/'report.json').write_text(json.dumps(report,ensure_ascii=False,indent=2)+'\n',encoding='utf-8')
    for k,v in report.items():
        print('PHASE176_R3R53R1_'+k.upper()+'='+json.dumps(v,ensure_ascii=False))
    print('REPORT='+str(folder/'report.json'))
    if not ok:
        raise RuntimeError(report['gate'])
    return report
