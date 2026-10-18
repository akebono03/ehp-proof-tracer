"""Phase 165 R1: read-only consistency audit for the active typed proof path."""
from __future__ import annotations

import hashlib
import json
import sys
import traceback
from dataclasses import asdict, is_dataclass
from datetime import datetime, timezone
from pathlib import Path

ROOT = Path.cwd()
OUT = ROOT / 'phase165_r1_audit_results'
OUT.mkdir(exist_ok=True)


def write(name: str, content: str) -> None:
    (OUT / name).write_text(content, encoding='utf-8')


def describe(step: object) -> dict:
    rule = getattr(step, 'inference_rule', None)
    return {
        'conclusion': repr(getattr(step, 'conclusion', None)),
        'rule': str(getattr(getattr(step, 'rule', None), 'value', getattr(step, 'rule', None))),
        'inference_rule': getattr(rule, 'name', None),
        'premise_count': len(getattr(step, 'premises', ())),
        'premise_conclusions': [repr(getattr(p, 'conclusion', None)) for p in getattr(step, 'premises', ())],
    }


def ancestry(root: object) -> list:
    seen = set()
    active = set()
    result = []
    def walk(step: object) -> None:
        identifier = id(step)
        if identifier in active:
            raise ValueError('cyclic ancestry')
        if identifier in seen:
            return
        active.add(identifier)
        for premise in getattr(step, 'premises', ()):
            walk(premise)
        active.remove(identifier)
        seen.add(identifier)
        result.append(step)
    walk(root)
    return result


def collect_group(n: int, k: int) -> dict:
    from phase165_r55_nk_only_goal import search_group_from_registered_goal
    from phase165_r52_r3_web_adapter import build_partial_web_group_proof_view
    from phase165_r52_partial_proof import render_partial_proof_markdown
    from proof import ProofRule

    name = f'pi{n+k}_{n}'
    info = {'group': name, 'n': n, 'k': k, 'stages': {}, 'errors': {}}
    try:
        result = search_group_from_registered_goal(n=n, k=k)
    except Exception:
        info['errors']['search'] = traceback.format_exc()
        return info
    info['status'] = result.status.value
    info['diagnostics'] = list(result.diagnostics)
    info['open_goals'] = list(map(repr, result.open_goals))
    info['conclusion'] = repr(result.conclusion)
    info['stages']['search'] = [describe(s) for s in result.proven_steps]
    write(f'{name}_search_steps.json', json.dumps(info['stages']['search'], ensure_ascii=False, indent=2))

    roots = [s for s in result.proven_steps if s.conclusion == result.conclusion] if result.conclusion is not None else []
    info['root_count'] = len(roots)
    if len(roots) == 1:
        nodes = ancestry(roots[0])
        info['stages']['ancestry'] = [describe(s) for s in nodes]
        info['ancestry_count'] = len(nodes)
        info['given_count'] = sum(s.rule is ProofRule.GIVEN for s in nodes)
        info['inference_count'] = sum(s.rule is ProofRule.INFERENCE for s in nodes)
        write(f'{name}_ancestry.json', json.dumps(info['stages']['ancestry'], ensure_ascii=False, indent=2))
        try:
            from phase165_r56_presentation_adapter import render_completed_shared_narrative
            from phase165_r57_r10_step_narrative import has_transport_proof_ancestry
            info['has_transport_ancestry'] = has_transport_proof_ancestry(roots[0])
            from homotopy_groups import DirectSumGroup, FiniteCyclicGroup, FreeCyclicGroup
            from proof_repository import ProofRepositoryEntry
            from toda_group_result import TodaGroupResult
            from toda_group_result_proof_replay import build_complete_toda_group_result_proof_replay
            from toda_group_proof_presentation import build_toda_group_proof_presentation
            from toda_group_proof_narrative_renderer import render_toda_group_proof_narrative_markdown
            structure = result.conclusion.rhs
            if isinstance(structure, (FiniteCyclicGroup, FreeCyclicGroup)):
                generators = (structure.generator,)
                orders = (structure.order,) if isinstance(structure, FiniteCyclicGroup) else (None,)
                entry = ProofRepositoryEntry(key='phase165:typed:completed', step=roots[0], phase='165')
                group_result = TodaGroupResult(target=result.target, group_structure=structure,
                    generators=generators, generator_orders=orders, source_entry=entry, proof_step=roots[0])
                replay = build_complete_toda_group_result_proof_replay(group_result)
                presentation = build_toda_group_proof_presentation(replay)
                info['stages']['replay'] = {'type': type(replay).__name__, 'repr': repr(replay)[:20000]}
                info['stages']['presentation'] = {'type': type(presentation).__name__, 'repr': repr(presentation)[:20000]}
                write(f'{name}_replay.txt', repr(replay))
                write(f'{name}_presentation.txt', repr(presentation))
                canonical_md = render_toda_group_proof_narrative_markdown(presentation)
                write(f'{name}_canonical_renderer.md', canonical_md)
                info['stages']['canonical_markdown_sha256'] = hashlib.sha256(canonical_md.encode()).hexdigest()
            md = render_completed_shared_narrative(result)
            write(f'{name}_completed.md', md)
            info['stages']['completed_markdown_sha256'] = hashlib.sha256(md.encode()).hexdigest()
        except Exception:
            info['errors']['replay_presentation'] = traceback.format_exc()
    try:
        markdown = render_partial_proof_markdown(result)
        write(f'{name}_public.md', markdown)
        info['stages']['public_markdown_sha256'] = hashlib.sha256(markdown.encode()).hexdigest()
        info['stages']['public_markdown_length'] = len(markdown)
    except Exception:
        info['errors']['markdown'] = traceback.format_exc()
    try:
        view = build_partial_web_group_proof_view(result, max_depth=2, mode='narrative')
        info['stages']['web'] = {
            'key': view.key,
            'mode': view.mode,
            'partial_result': view.partial_result,
            'step_count': len(view.steps),
            'rendered_line_count': len(view.rendered_lines),
            'steps': [asdict(s) if is_dataclass(s) else repr(s) for s in view.steps],
            'rendered_lines': [asdict(line) if is_dataclass(line) else repr(line) for line in view.rendered_lines],
        }
        write(f'{name}_web_view.json', json.dumps(info['stages']['web'], ensure_ascii=False, indent=2))
    except Exception:
        info['errors']['web_view'] = traceback.format_exc()
    info['consistency_checks'] = {
        'root_unique_when_complete': (len(roots) == 1 if result.conclusion is not None else None),
        'public_markdown_present': info['stages'].get('public_markdown_length', 0) > 0,
        'web_steps_match_search_steps': info['stages'].get('web', {}).get('step_count') == len(result.proven_steps) if 'web' in info['stages'] else None,
        'web_has_rendered_lines': info['stages'].get('web', {}).get('rendered_line_count', 0) > 0,
    }
    return info


def main() -> int:
    report = {'phase': '165 R1', 'mode': 'READ_ONLY', 'full_pytest_run': False,
        'timestamp_utc': datetime.now(timezone.utc).isoformat(), 'cwd': str(ROOT),
        'python': sys.version, 'groups': []}
    for n, k in ((2, 1), (3, 1)):
        try:
            report['groups'].append(collect_group(n, k))
        except Exception:
            report['groups'].append({'group': f'pi{n+k}_{n}', 'fatal_error': traceback.format_exc()})
    write('audit_result.json', json.dumps(report, ensure_ascii=False, indent=2))
    for group in report['groups']:
        print(group['group'], group.get('status', 'FAILED'), group.get('consistency_checks', {}))
        for stage in group.get('errors', {}):
            print('  ERROR:', stage)
    print('Report:', OUT / 'audit_result.json')
    return 0 if all(not x.get('errors') and not x.get('fatal_error') for x in report['groups']) else 1


if __name__ == '__main__':
    raise SystemExit(main())
