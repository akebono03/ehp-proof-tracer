"""Focused, public Web audit for general reference formatting and proof status."""
from __future__ import annotations

import argparse
import json
from pathlib import Path

from phase165_r52_partial_proof import ProofSearchStatus
from phase165_r55_nk_only_goal import search_group_from_registered_goal
from phase165_r52_r9_shared_math import build_shared_typed_bridge
from phase168_r3_4_link_bridge import build_linked_proof_narrative_model
from phase168_r3_5_model_renderer import render_model_backed_narrative_markdown
from phase169_r10e4_ordered_db_prior.db_prior import exact_prior_database_result
from web_group_proof import build_standard_web_group_proof_view


def inspect_complete(n: int, k: int) -> dict[str, object]:
    """Use the real typed search and inspect source-backed Reference output."""
    bridge = build_shared_typed_bridge()
    contexts: list[object] = []
    result = search_group_from_registered_goal(
        n=n, k=k, bridge=bridge, context_sink=contexts.append,
    )
    if result.status is not ProofSearchStatus.COMPLETE or not contexts:
        raise RuntimeError(f'Expected a completed source-first proof n={n}, k={k}')
    model = build_linked_proof_narrative_model(result, contexts[-1])
    markdown = render_model_backed_narrative_markdown(result, model)
    view = build_standard_web_group_proof_view(
        n=n, k=k, mode='narrative', citation_source='model',
    )
    if view.key != 'generic-complete-proof' or view.partial_result:
        raise RuntimeError('A completed proof changed status')
    prop44 = [c for c in model.citations if
              (c.reference.locator or c.reference.label) == 'Proposition 4.4']
    lemma54 = [c for c in model.citations if
               (c.reference.locator or c.reference.label) == 'Lemma 5.4']
    prop_correct = all(
        any(r'\xrightarrow{\;\cong\;}' in s and r'\alpha\circ\gamma' in s
            for s in c.statement_bodies)
        for c in prop44
    ) and 'Steenrod1951' not in markdown
    lemma_correct = all(
        any(r'H(\nu_4)=\iota_7' in s and r"2E\nu_4=E^2\nu'" in s
            for s in c.statement_bodies)
        for c in lemma54
    )
    prior_rendered = any(
        any(segment.kind == 'inline_math' and r'\pi_{' in segment.value
            for segment in line.segments)
        and any('先行データベース結果' in segment.value for segment in line.segments)
        for line in view.rendered_lines
    )
    row = {
        'n': n, 'k': k,
        'source_reference_count': len(model.citations),
        'prop44_body_present': bool(prop44) and prop_correct,
        'lemma54_body_present': bool(lemma54) and lemma_correct,
        'prior_db_tex_rendered': prior_rendered,
        'named_complete': True,
        'open_goals': len(result.open_goals),
    }
    row['passed'] = all((row['prop44_body_present'], row['lemma54_body_present'],
                         row['prior_db_tex_rendered'], not result.open_goals))
    print(f'PHASE173_R4_R15R12_N={n}_K={k} ' +
          f'PROP44={row["prop44_body_present"]} LEMMA54={row["lemma54_body_present"]} '
          f'DB_TEX={prior_rendered} COMPLETE={row["named_complete"]}', flush=True)
    return row


def inspect_partial(k: int) -> dict[str, object]:
    """Do not promote abstract-only results into named-generator proofs."""
    goal = exact_prior_database_result(4, k)
    if goal is None:
        raise RuntimeError('Registered target is missing')
    result = search_group_from_registered_goal(n=4, k=k, goal=goal)
    view = build_standard_web_group_proof_view(
        n=4, k=k, goal=goal, mode='narrative', citation_source='model',
    )
    headings = [line.prefix for line in view.rendered_lines if line.kind == 'heading']
    passed = (
        result.abstract_structure is not None
        and result.conclusion is None
        and result.status in (ProofSearchStatus.PARTIAL, ProofSearchStatus.SEARCH_FAILED)
        and bool(result.open_goals)
        and view.key == 'generic-partial-proof' and view.partial_result
        and headings.count('証明済みの抽象群構造') == 1
    )
    row = {'k': k, 'open_goals': len(result.open_goals), 'named_pending': passed,
           'abstract_heading_count': headings.count('証明済みの抽象群構造'),
           'passed': passed}
    print(f'PHASE173_R4_R15R12_K={k} NAMED_PENDING={passed} '
          f'OPEN_GOALS={len(result.open_goals)}', flush=True)
    return row


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--output', type=Path, required=True)
    args = parser.parse_args()
    completed = [inspect_complete(4, k) for k in (3, 4, 7)]
    partial = [inspect_partial(k) for k in (8, 31)]
    passed = all(row['passed'] for row in completed + partial)
    data = {
        'phase': '173-R4-R15R12',
        'head_reviewed': 'e2996ec2ff496203f94daa9bc22550c5e69a6b11',
        'completed': completed,
        'partial': partial,
        'full_pytest_performed': False,
        'proof_search_changed': False,
        'passed': passed,
    }
    args.output.parent.mkdir(parents=True, exist_ok=True)
    args.output.write_text(json.dumps(data, ensure_ascii=False, indent=2) + '\n', encoding='utf-8')
    print('PHASE173_R4_R15R12_AUDIT=' + ('PASS' if passed else 'FAIL'), flush=True)
    return 0 if passed else 1


if __name__ == '__main__':
    raise SystemExit(main())
