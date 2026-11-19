"""Phase 176 R3R4: read-only zero-image and Hopf-subgroup dependency audit.

Existing proof rules, database results and referenced sources are observed only.
No proof is created, admitted or registered by this module.
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
PACKAGE = 'phase176_r3r4_zero_image_and_hopf_lift_frontier'
REVIEWED_HEAD = 'bc40f11670ddc592cb4388b45fc40c255b87ebf6'
MARKER = 'PHASE176_R3R4_WORKER_JSON='
SOURCES = (
    'phase175_r3_pi73_hopf_lift/rule.py',
    'phase175_r3_pi73_hopf_lift/tests/test_rule.py',
    'phase174_r3_r7_r6_cyclic_generator_zero_image/rule.py',
    'phase174_r3_r7_r5_zero_image_hopf_injective/rule.py',
    'phase175_r3r9_lemma57_explicit_public/rule.py',
    'phase165_r52_r9_shared_math.py',
    'phase165_r55_nk_only_goal.py',
    'phase176_r3_n3_rule_sufficiency_audit/audit.py',
    'sources/toda/Toda_05_2.tex',
)
SOURCE_CONTRACT = {
    'phase175_r3_pi73_hopf_lift/rule.py': (
        'def hopf_lift_inputs(', 'codomain.rhs.order != goal.order',
    ),
    'phase174_r3_r7_r6_cyclic_generator_zero_image/rule.py': (
        'def expand_zero_image_from_cyclic_generator(',
        'def cyclic_generator_zero_image_inputs(',
    ),
    'phase175_r3r9_lemma57_explicit_public/rule.py': (
        'def exact_lemma57_zero_image_goal(',
        'def expand_cited_lemma57_explicit_zero(',
    ),
    'sources/toda/Toda_05_2.tex': (
        r'\label{lemma:5.7}', r"E(\eta_2\circ\nu')=0",
        r'\label{prop:5.9}',
    ),
}


def git(*args: str, check: bool = True) -> tuple[int, str]:
    result = subprocess.run(('git',) + args, cwd=ROOT, capture_output=True,
                            text=True, encoding='utf-8', errors='replace', check=False)
    if check and result.returncode:
        raise RuntimeError('GIT_FAILED: ' + ' '.join(args) + ': ' + result.stderr.strip())
    return result.returncode, result.stdout.strip()


def verify_sources(root: Path = ROOT) -> dict[str, str]:
    missing = [p for p in SOURCES if not (root / p).is_file()]
    if missing:
        raise RuntimeError('SOURCE_FILES_MISSING: ' + repr(missing))
    for file, anchors in SOURCE_CONTRACT.items():
        text = ''.join((root / file).read_text(encoding='utf-8-sig').split())
        absent = [a for a in anchors if ''.join(a.split()) not in text]
        if absent:
            raise RuntimeError('SOURCE_ANCHORS_MISSING: ' + file + ': ' + repr(absent))
    return {p: hashlib.sha256((root / p).read_bytes()).hexdigest() for p in SOURCES}


def preflight() -> dict[str, object]:
    if Path(git('rev-parse', '--show-toplevel')[1]).resolve() != ROOT.resolve():
        raise RuntimeError('REPOSITORY_ROOT_MISMATCH')
    if git('branch', '--show-current')[1] != 'develop':
        raise RuntimeError('DEVELOP_BRANCH_REQUIRED')
    if git('merge-base', '--is-ancestor', REVIEWED_HEAD, 'HEAD', check=False)[0]:
        raise RuntimeError('R3R3_HEAD_NOT_ANCESTOR')
    if git('status', '--porcelain', '--untracked-files=no')[1]:
        raise RuntimeError('TRACKED_WORKTREE_CHANGES_REQUIRE_REVIEW')
    hashes = verify_sources(ROOT)
    return {
        'head': git('rev-parse', 'HEAD')[1],
        'origin_develop': git('rev-parse', '--verify', 'origin/develop', check=False)[1] or None,
        'source_sha256': hashes,
        'historical_source_guards': 'FOUR_KNOWN_FAILURES_NOT_PASSING',
        'full_pytest': 'NOT_RUN',
    }


def describe(value: object, limit: int = 1400) -> dict[str, str]:
    return {'type': type(value).__module__ + '.' + type(value).__name__,
            'repr': repr(value)[:limit]}


def proposal_summary(options: tuple[object, ...]) -> dict[str, object]:
    return {
        'count': len(options),
        'status': 'UNVERIFIED_PROPOSALS',
        'options': [
            {
                'rule': getattr(item.rule, 'name', type(item.rule).__name__),
                'subgoals': [describe(x) for x in item.subgoals],
            }
            for item in options[:12]
        ],
        'truncated': len(options) > 12,
    }


def safe_provider(provider: object, goal: object) -> dict[str, object]:
    try:
        return proposal_summary(tuple(provider(goal)))
    except Exception as exc:
        return {'status': 'PROVIDER_ERROR',
                'error': type(exc).__name__ + ': ' + str(exc)}


def observe() -> dict[str, object]:
    from homotopy_groups import TodaPrimaryGroup, TodaHopfInvariantMap
    from phase165_r12_r2_quotient_rules import CyclicStructureStatement
    from phase165_r14_r6_generic_iso import MapInjective
    from phase165_r55_nk_only_goal import search_group_from_registered_goal
    from phase165_r52_r9_shared_math import build_shared_typed_bridge, shared_expansion_provider
    from phase169_r10e4_ordered_db_prior.db_prior import exact_prior_database_result
    from phase174_r3_r7_r5_zero_image_hopf_injective.rule import (
        hopf_injectivity_from_zero_image_inputs,
    )
    from phase174_r3_r7_r6_cyclic_generator_zero_image.rule import (
        cyclic_generator_zero_image_inputs,
        expand_zero_image_from_cyclic_generator,
    )
    from phase175_r3r9_lemma57_explicit_public.rule import (
        exact_lemma57_zero_image_goal,
    )
    from proof import Relation, RelationType

    result = search_group_from_registered_goal(n=3, k=5)
    cyclic = [x for x in result.open_goals if isinstance(x, CyclicStructureStatement)]
    if len(cyclic) != 1 or cyclic[0].group != TodaPrimaryGroup(8, 3) or cyclic[0].order != 2:
        raise RuntimeError('CYCLIC_GOAL_DRIFT')
    goal = cyclic[0]
    h = TodaHopfInvariantMap(goal.group, TodaPrimaryGroup(8, 5))
    injectivity = MapInjective(h)
    injectivity_inputs = hopf_injectivity_from_zero_image_inputs(injectivity)
    if injectivity_inputs is None or len(injectivity_inputs) != 2:
        raise RuntimeError('HOPF_INJECTIVITY_INPUT_DRIFT')
    zero_image_goal = injectivity_inputs[0]
    preceding_prior = exact_prior_database_result(2, 5)
    if (not isinstance(preceding_prior, Relation)
            or preceding_prior.relation_type is not RelationType.EQUALITY
            or preceding_prior.lhs != TodaPrimaryGroup(7, 2)):
        raise RuntimeError('PRECEDING_PRIOR_GROUP_DRIFT')
    isolated = expand_zero_image_from_cyclic_generator(zero_image_goal, preceding_prior)
    generator_inputs = cyclic_generator_zero_image_inputs(zero_image_goal, preceding_prior)
    if generator_inputs is None:
        raise RuntimeError('ZERO_IMAGE_GENERATOR_INPUT_DRIFT')
    lemma57_compatible = exact_lemma57_zero_image_goal(generator_inputs[1])
    bridge = build_shared_typed_bridge()
    ordinary = shared_expansion_provider(bridge, proof_target=result.open_goals[-1])
    return {
        'target': [3, 5],
        'search_status': result.status.value,
        'open_goals': len(result.open_goals),
        'cyclic_goal': describe(goal),
        'hopf_injectivity_goal': describe(injectivity),
        'hopf_injectivity_inputs': [describe(x) for x in injectivity_inputs],
        'zero_image_goal': describe(zero_image_goal),
        'preceding_group_prior_is_a_candidate_not_a_proof': describe(preceding_prior),
        'isolated_zero_image_candidates': proposal_summary(tuple(isolated)),
        'zero_image_generator_subgoals': [describe(x) for x in generator_inputs],
        'generator_image_matches_explicit_lemma57_directly': lemma57_compatible,
        'shared_zero_image_candidates': safe_provider(ordinary, zero_image_goal),
        'shared_generator_zero_candidates': safe_provider(ordinary, generator_inputs[1]),
        'shared_hopf_injective_candidates': safe_provider(ordinary, injectivity),
        'blockers': (
            'ISOLATED_CYCLIC_ZERO_IMAGE_RULE_NOT_AUTOMATICALLY_CONNECTED',
            'GENERATOR_SUSPENSION_ZERO_NEEDS_COMPOSITION_TRANSPORT_FROM_LEMMA57',
            'IMAGE_SUBGROUP_ORDER_TWO_NEEDS_TYPED_KERNEL_AND_HOPF_IMAGE_PROOFS',
            'NO_SOURCE_OR_INFERRED_PROOF_ADMITTED_BY_AUDIT',
        ),
        'new_given': 0, 'new_mathematical_rules': 0,
        'proof_complete': False,
    }


def worker(timeout: int) -> dict[str, object]:
    env = dict(os.environ, PYTHONDONTWRITEBYTECODE='1', PYTHONIOENCODING='utf-8')
    try:
        p = subprocess.run(
            (sys.executable, '-B', '-m', PACKAGE + '.audit', '--worker'),
            cwd=ROOT, env=env, capture_output=True, text=True,
            encoding='utf-8', errors='replace', timeout=timeout, check=False,
        )
    except subprocess.TimeoutExpired as exc:
        raise RuntimeError('R3R4_WORKER_TIMEOUT') from exc
    lines = [line[len(MARKER):] for line in p.stdout.splitlines() if line.startswith(MARKER)]
    if p.returncode or len(lines) != 1:
        raise RuntimeError('R3R4_WORKER_FAILED: code=' + str(p.returncode)
                           + ' stderr=' + p.stderr[-4000:])
    result = json.loads(lines[0])
    if result.get('proof_complete') is not False or result.get('new_given') != 0:
        raise RuntimeError('AUDIT_MUST_NOT_CLAIM_COMPLETION')
    return result


def report_path() -> Path:
    path = Path(os.environ.get('LOCALAPPDATA') or tempfile.gettempdir()) / 'EHPProofTracerAudit' / PACKAGE
    path.mkdir(parents=True, exist_ok=True)
    return path / 'report.json'


def run(dry_run: bool, timeout: int) -> int:
    report: dict[str, object] = {
        'phase': '176_R3R4', 'dry_run': dry_run,
        'timestamp_utc': datetime.now(timezone.utc).isoformat(),
        'gate': 'FAIL_R3R4', 'mode': 'READ_ONLY_ZERO_IMAGE_AND_HOPF_LIFT_FRONTIER',
        'new_given': 0, 'new_mathematical_rules': 0,
        'full_pytest': 'NOT_RUN', 'proof_complete': False,
    }
    try:
        report['preflight'] = preflight()
        if not dry_run:
            report['observed'] = worker(timeout)
        report['gate'] = 'PASS_R3R4_READ_ONLY_DRYRUN' if dry_run else 'PASS_R3R4_ZERO_IMAGE_FRONTIER_AUDIT'
    except Exception as exc:
        report['error'] = type(exc).__name__ + ': ' + str(exc)
        report['traceback'] = traceback.format_exc()[-8000:]
    path = report_path()
    path.write_text(json.dumps(report, ensure_ascii=False, indent=2) + '\n', encoding='utf-8')
    print('PHASE176_R3R4_GATE=' + report['gate'])
    print('PHASE176_R3R4_REPORT=' + str(path))
    print('PHASE176_R3R4_HEAD=' + str(report.get('preflight', {}).get('head', 'UNVERIFIED')))
    if 'observed' in report:
        found = report['observed']
        print('PHASE176_R3R4_GROUP=(3,5) STATUS=' + found['search_status'] + ' OPEN=' + str(found['open_goals']))
        print('PHASE176_R3R4_ISOLATED_ZERO_IMAGE_PROPOSALS=' + str(found['isolated_zero_image_candidates']['count']))
        print('PHASE176_R3R4_SHARED_ZERO_IMAGE_PROPOSALS=' + str(found['shared_zero_image_candidates'].get('count', 'ERROR')))
        print('PHASE176_R3R4_LEMMA57_DIRECT_MATCH=' + str(found['generator_image_matches_explicit_lemma57_directly']).lower())
    if 'error' in report:
        print('PHASE176_R3R4_ERROR=' + report['error'])
    print('PHASE176_R3R4_FULL_PYTEST=NOT_RUN')
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
            print(MARKER + json.dumps(observe(), ensure_ascii=False))
            return 0
        except Exception:
            traceback.print_exc()
            return 1
    return run(args.dry_run, args.timeout)


if __name__ == '__main__':
    raise SystemExit(main())
