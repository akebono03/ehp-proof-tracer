"""Phase 176 R3: read-only, observed-rule sufficiency audit for (n,k)=(3,5).

No proofs, registry assertions or expansion rules are added by this module.
"""
from __future__ import annotations

import argparse
from datetime import datetime, timezone
import hashlib
import json
import os
from pathlib import Path
import subprocess
import sys
import tempfile
import traceback

ROOT = Path(__file__).resolve().parents[1]
PACKAGE = 'phase176_r3_n3_rule_sufficiency_audit'
REVIEWED_R2_HEAD = '28987939b67e42e6f770e138295d88e299aa19ce'
MARKER = 'PHASE176_R3_WORKER_JSON='
TARGET = (3, 5)
SOURCE_FILES = (
    'phase165_r55_nk_only_goal.py',
    'phase165_r52_r9_shared_math.py',
    'phase165_r52_r2_search_adapter.py',
    'phase176_r2_n3_source_frontier_audit/audit.py',
    'sources/toda/Toda_05_2.tex',
    'sources/toda/Toda_02_2.tex',
)
SOURCE_ANCHORS = {
    'Lemma 5.7': ('sources/toda/Toda_05_2.tex', r'\label{lemma:5.7}', r"E(\eta_2\circ\nu')=0"),
    '(5.5)': ('sources/toda/Toda_05_2.tex', r'\textbf{(5.5).}', r'4\nu_{n}=\eta_n^{3}'),
    '(5.3)': ('sources/toda/Toda_05_2.tex', r'\textbf{(5.3).}', r"H(\nu')=\eta_5"),
    'Proposition 5.6': ('sources/toda/Toda_05_2.tex', r'\label{prop:5.6}'),
    'Proposition 5.8': ('sources/toda/Toda_05_2.tex', r'\label{prop:5.8}'),
    'Proposition 5.9 proof': ('sources/toda/Toda_05_2.tex', r'\label{prop:5.9}', r'\ker\Delta'),
    'Proposition 2.2': ('sources/toda/Toda_02_2.tex', r'\label{prop:2.2}', r'H(\alpha\circ E\beta)'),
}


def git(*args: str, check: bool = True) -> tuple[int, str]:
    command = subprocess.run(('git',) + args, cwd=ROOT, capture_output=True,
                             text=True, encoding='utf-8', errors='replace', check=False)
    if check and command.returncode:
        raise RuntimeError('GIT_READ_FAILED ' + ' '.join(args) + ': ' + command.stderr.strip())
    return command.returncode, command.stdout.strip()


def check_source_anchors(root: Path) -> dict[str, dict[str, object]]:
    checked: dict[str, dict[str, object]] = {}
    for label, (name, *anchors) in SOURCE_ANCHORS.items():
        path = root / name
        if not path.is_file():
            raise RuntimeError('SOURCE_MISSING: ' + name)
        text = ''.join(path.read_text(encoding='utf-8-sig').split())
        missing = [anchor for anchor in anchors if ''.join(anchor.split()) not in text]
        checked[label] = {'source': name, 'present': not missing, 'missing': missing}
    return checked


def preflight() -> dict[str, object]:
    if Path(git('rev-parse', '--show-toplevel')[1]).resolve() != ROOT.resolve():
        raise RuntimeError('REPOSITORY_ROOT_MISMATCH')
    if git('branch', '--show-current')[1] != 'develop':
        raise RuntimeError('DEVELOP_REQUIRED')
    if git('merge-base', '--is-ancestor', REVIEWED_R2_HEAD, 'HEAD', check=False)[0]:
        raise RuntimeError('R2_HEAD_NOT_ANCESTOR')
    if git('status', '--porcelain', '--untracked-files=no')[1]:
        raise RuntimeError('TRACKED_CHANGES_REQUIRE_REVIEW')
    for name in SOURCE_FILES:
        if not (ROOT / name).is_file():
            raise RuntimeError('REVIEWED_SOURCE_MISSING: ' + name)
    anchors = check_source_anchors(ROOT)
    if not all(item['present'] for item in anchors.values()):
        raise RuntimeError('SOURCE_ANCHORS_MISSING: ' + repr(anchors))
    hashes = {name: hashlib.sha256((ROOT / name).read_bytes()).hexdigest() for name in SOURCE_FILES}
    return {'head': git('rev-parse', 'HEAD')[1],
            'origin_develop': git('rev-parse', '--verify', 'origin/develop', check=False)[1] or None,
            'source_sha256': hashes, 'source_anchors': anchors,
            'historical_guards': 'FOUR_KNOWN_FAILURES_NOT_PASSING', 'full_pytest': 'NOT_RUN'}


def safe_detail(value: object, limit: int = 2000) -> dict[str, object]:
    """Record structural details, not a claim that a value was proved."""
    return {'type': type(value).__module__ + '.' + type(value).__name__,
            'str': str(value)[:limit], 'repr': repr(value)[:limit]}


def describe_expansion(item: object) -> dict[str, object]:
    """An expansion is only a proposal, never a verified ProofStep."""
    record = {'type': type(item).__name__, 'repr': repr(item)[:2500]}
    for attr in ('rule_name', 'name', 'inference_rule', 'premises', 'subgoals', 'goals'):
        if hasattr(item, attr):
            try:
                value = getattr(item, attr)
                record[attr] = repr(value)[:2000]
            except Exception as exc:
                record[attr + '_error'] = type(exc).__name__
    return record


def summarize_proposals(goal: object, provider: object) -> dict[str, object]:
    """Call the existing provider once; do not consume or certify its proposals."""
    try:
        proposals = tuple(provider(goal))
    except Exception as exc:
        return {'status': 'provider_error', 'error': type(exc).__name__ + ': ' + str(exc)}
    return {'status': 'inspected', 'proposal_count': len(proposals),
            'proposals': [describe_expansion(item) for item in proposals[:12]],
            'truncated': len(proposals) > 12}


def observe() -> dict[str, object]:
    from phase165_r55_nk_only_goal import search_group_from_registered_goal
    from phase165_r52_r9_shared_math import build_shared_typed_bridge, shared_expansion_provider
    from phase165_r52_partial_proof import ProofSearchStatus
    from proof import ProofRule

    # The ordinary public registered-goal search remains the source of truth.
    result = search_group_from_registered_goal(n=3, k=5)
    record: dict[str, object] = {
        'target': [3, 5], 'status': result.status.value,
        'open_goal_count': len(result.open_goals),
        'open_goals': [dict(index=i + 1, **safe_detail(goal)) for i, goal in enumerate(result.open_goals)],
        'diagnostics': list(result.diagnostics),
        'references': list(result.references),
        'proven_step_count': len(result.proven_steps),
        'proven_steps': [
            {'conclusion': safe_detail(step.conclusion, 1000), 'rule': str(step.rule),
             'inference_rule': getattr(step.inference_rule, 'name', None),
             'premise_count': len(step.premises)}
            for step in result.proven_steps[:60]
        ],
        'conclusion_claimed': result.conclusion is not None,
        'new_given': 0, 'new_rules': 0,
    }
    if result.status is ProofSearchStatus.COMPLETE:
        raise RuntimeError('R3_EXPECTED_UNFINISHED_TARGET_DRIFT: review before continuing')
    if not result.open_goals:
        raise RuntimeError('UNFINISHED_WITHOUT_OPEN_GOALS')

    # Inventory current cited source witnesses. This does not add a source.
    bridge = build_shared_typed_bridge()
    provenance = {}
    for assertion in bridge.registry._assertions.values():
        ref = bridge.registry._references.get(assertion.reference_id)
        label = str(getattr(ref, 'locator', '') or getattr(ref, 'label', '') or '')
        if any(token in label.lower() for token in (
            '5.7', '5.5', '5.3', '5.6', '5.8', '2.2', '4.2', '4.4')):
            provenance[assertion.assertion_id] = {
                'locator': label, 'origin': str(assertion.origin),
                'content_type': type(assertion.content).__name__,
                'content': str(assertion.content)[:1200],
            }
    linked = {link.assertion_id for link in bridge.proof_links
              if link.step is not None and link.step.rule is ProofRule.GIVEN}
    for aid in provenance:
        provenance[aid]['linked_given'] = aid in linked
    record['relevant_registry_assertions'] = provenance
    record['total_registry_assertions'] = len(bridge.registry._assertions)
    record['total_linked_given'] = len(linked)

    # Count root-level proposals for all *actual* open goals, without asserting
    # that each belongs to a particular mathematical dependency.
    provider = shared_expansion_provider(bridge, proof_target=result.open_goals[-1])
    record['open_goal_proposals'] = [
        {'goal_index': i + 1, **summarize_proposals(goal, provider)}
        for i, goal in enumerate(result.open_goals)
    ]
    return record


def worker(timeout: int) -> dict[str, object]:
    env = dict(os.environ, PYTHONDONTWRITEBYTECODE='1', PYTHONIOENCODING='utf-8')
    try:
        process = subprocess.run((sys.executable, '-B', '-m', PACKAGE + '.audit', '--worker'),
                                 cwd=ROOT, env=env, capture_output=True, text=True,
                                 encoding='utf-8', errors='replace', check=False, timeout=timeout)
    except subprocess.TimeoutExpired as exc:
        raise RuntimeError('WORKER_TIMEOUT') from exc
    matched = [line[len(MARKER):] for line in process.stdout.splitlines() if line.startswith(MARKER)]
    if process.returncode or len(matched) != 1:
        raise RuntimeError('WORKER_FAILED: exit=' + str(process.returncode)
                           + ' stderr=' + process.stderr[-4000:]
                           + ' stdout=' + process.stdout[-1500:])
    row = json.loads(matched[0])
    if row.get('target') != [3, 5]:
        raise RuntimeError('WORKER_TARGET_MISMATCH')
    return row


def report_path() -> Path:
    folder = Path(os.environ.get('LOCALAPPDATA') or tempfile.gettempdir()) / 'EHPProofTracerAudit' / PACKAGE
    folder.mkdir(parents=True, exist_ok=True)
    return folder / 'report.json'


def execute(dry_run: bool, timeout: int) -> int:
    report: dict[str, object] = {
        'phase': '176_R3', 'dry_run': dry_run,
        'mode': 'READ_ONLY_RULE_SUFFICIENCY_AUDIT',
        'timestamp_utc': datetime.now(timezone.utc).isoformat(),
        'gate': 'FAIL_R3', 'new_given': 0, 'new_rules': 0, 'full_pytest': 'NOT_RUN',
        'mathematical_proof_complete': False,
    }
    try:
        report['preflight'] = preflight()
        if not dry_run:
            report['observed'] = worker(timeout)
        report['gate'] = 'PASS_R3_READ_ONLY_DRYRUN' if dry_run else 'PASS_R3_OPEN_GOAL_AND_PROVIDER_INVENTORY'
    except Exception as exc:
        report['error'] = type(exc).__name__ + ': ' + str(exc)
        report['traceback'] = traceback.format_exc()[-7000:]
    path = report_path()
    path.write_text(json.dumps(report, ensure_ascii=False, indent=2, default=str) + '\n', encoding='utf-8')
    print('PHASE176_R3_GATE=' + report['gate'])
    print('PHASE176_R3_REPORT=' + str(path))
    print('PHASE176_R3_HEAD=' + report.get('preflight', {}).get('head', 'UNVERIFIED'))
    if 'observed' in report:
        data = report['observed']
        print('PHASE176_R3_GROUP=(3,5) STATUS=' + data['status']
              + ' OPEN=' + str(data['open_goal_count']))
        for row in data['open_goal_proposals']:
            print('PHASE176_R3_GOAL=' + str(row['goal_index'])
                  + ' PROPOSALS=' + str(row.get('proposal_count', row.get('status'))))
    if 'error' in report:
        print('PHASE176_R3_ERROR=' + report['error'])
    print('PHASE176_R3_FULL_PYTEST=NOT_RUN')
    print('(END)')
    return 0 if report['gate'].startswith('PASS_') else 1


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--dry-run', action='store_true')
    parser.add_argument('--worker', action='store_true')
    parser.add_argument('--timeout', type=int, default=120)
    args = parser.parse_args()
    if args.worker:
        try:
            print(MARKER + json.dumps(observe(), ensure_ascii=False, default=str))
            return 0
        except Exception:
            traceback.print_exc()
            return 1
    return execute(args.dry_run, args.timeout)


if __name__ == '__main__':
    raise SystemExit(main())
