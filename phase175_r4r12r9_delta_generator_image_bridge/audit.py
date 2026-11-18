"""Phase 175 R4R12R9: source-first map-equality to generator-image bridge."""
from __future__ import annotations

import argparse
from datetime import datetime, timezone
import json
from pathlib import Path
import subprocess
import traceback

from . import installer

PACKAGE = 'phase175_r4r12r9_delta_generator_image_bridge'
PRIOR_COMMIT = 'b7bbb1032ef6c0568cb0cbf1c0116c2b183716e4'
REVIEWED_MERGE_COMMIT = '3ec001a59044aeb056ec7190c43c6066eaf5abae'


def git(root: Path, *args: str) -> str:
    result = subprocess.run(['git', *args], cwd=root, capture_output=True,
                            text=True, encoding='utf-8', errors='replace')
    if result.returncode != 0:
        raise RuntimeError('R9_GIT_FAILURE ' + ' '.join(args) + ': ' + result.stderr)
    return result.stdout.strip()


def verify(root: Path) -> dict[str, object]:
    if Path(git(root, 'rev-parse', '--show-toplevel')).resolve() != root:
        raise RuntimeError('R9_WRONG_ROOT')
    if git(root, 'branch', '--show-current') != 'develop':
        raise RuntimeError('R9_WRONG_BRANCH')
    head = git(root, 'rev-parse', 'HEAD')
    if head not in (PRIOR_COMMIT, REVIEWED_MERGE_COMMIT):
        raise RuntimeError('R9_HEAD_NEEDS_REVIEW: ' + head)
    if head == REVIEWED_MERGE_COMMIT:
        # GitHub compare: b7bbb103..3ec001a is exactly one reviewed merge
        # commit with zero file changes; check this locally, not by title.
        if git(root, 'rev-list', '--count', PRIOR_COMMIT + '..' + head) != '1':
            raise RuntimeError('R9_UNREVIEWED_MERGE_COUNT')
        if git(root, 'diff', '--name-only', PRIOR_COMMIT, head):
            raise RuntimeError('R9_UNREVIEWED_MERGE_FILES')
        if git(root, 'merge-base', PRIOR_COMMIT, head) != PRIOR_COMMIT:
            raise RuntimeError('R9_UNREVIEWED_MERGE_ANCESTRY')
    dirty = set(git(root, 'diff', '--name-only').splitlines())
    dirty.update(git(root, 'diff', '--cached', '--name-only').splitlines())
    if dirty - {str(installer.TARGET), '.pytest_cache/v/cache/nodeids'}:
        raise RuntimeError('R9_UNREVIEWED_TRACKED_CHANGES ' + repr(sorted(dirty)))
    return {'head': head, 'dirty': sorted(dirty)}


def audit(root: Path, dry_run: bool) -> dict[str, object]:
    folder = root / PACKAGE / 'output'
    folder.mkdir(parents=True, exist_ok=True)
    state = verify(root)
    # Validate the previously cited source independently of any new inference.
    from phase175_r4r12r8_delta_generator_source_audit.audit import inspect_source
    source_file = root / 'sources/toda/Toda_05_2.tex'
    source_evidence = inspect_source(source_file.read_text(encoding='utf-8-sig'))
    prior_version = git(root, 'rev-parse', PRIOR_COMMIT + ':sources/toda/Toda_05_2.tex')
    working_version = git(root, 'hash-object', 'sources/toda/Toda_05_2.tex')
    if prior_version != working_version:
        raise RuntimeError('R9_UNREVIEWED_TODA_SOURCE_BLOB')
    from phase165_r14_r6_generic_iso import GeneratorImage
    from phase175_r4r12_public_two_summand_quotient.provider import expand_public_two_summand_quotient
    from phase169_r10e4_ordered_db_prior.db_prior import exact_prior_database_result
    from phase165_r12_r2_quotient_rules import CyclicStructureStatement
    from .rule import expand_proved_delta_equality_image

    root_goal = exact_prior_database_result(5, 4)
    cyclic = CyclicStructureStatement(root_goal.lhs, root_goal.rhs.generator, 2)
    routes = expand_public_two_summand_quotient(cyclic, proof_target=root_goal)
    if len(routes) != 2:
        raise RuntimeError('R9_QUOTIENT_ROUTES_DRIFT')
    orientation1 = routes[1]
    target = orientation1.subgoals[2]
    if not isinstance(target, GeneratorImage):
        raise RuntimeError('R9_DELTA_GOAL_TYPE_DRIFT')
    options = expand_proved_delta_equality_image(target)
    # No result is promoted unless its *separate proof goal* is solved.
    if len(options) != 1 or len(options[0].subgoals) != 1:
        raise RuntimeError('R9_GENERAL_BRIDGE_NOT_MATCHED')
    # This pass deliberately does not attempt or claim recursive proof success.
    changed = installer.install(root, dry_run=dry_run, output=folder)
    shared_counts = None
    if not dry_run:
        from phase165_r52_r9_shared_math import build_shared_typed_bridge, shared_expansion_provider
        shared = shared_expansion_provider(build_shared_typed_bridge(), proof_target=root_goal)
        delta_proposals = tuple(shared(target))
        equality_proposals = tuple(shared(options[0].subgoals[0]))
        bridge_options = tuple(p for p in delta_proposals if p.rule.name == options[0].rule.name)
        if len(bridge_options) != 1:
            raise RuntimeError('R9_BRIDGE_NOT_VISIBLE_IN_SHARED_SEARCH')
        shared_counts = {'delta_image_bridge_candidates': len(bridge_options),
                         'delta_equality_candidates': len(equality_proposals),
                         'delta_equality_rules': [p.rule.name for p in equality_proposals]}
    return {'phase': PACKAGE, 'dry_run': dry_run, 'git': state,
            'source': source_evidence, 'install': changed, 'shared': shared_counts, 'generator_image_candidate_count': len(options),
            'equality_subgoal': repr(options[0].subgoals[0]),
            'new_given': 0, 'new_math_rules_other_than_generic_bridge': 0,
            'recursive_search_executed': False, 'group_proof_complete': False,
            'full_pytest_executed': False,
            'gate': 'PASS_R4R12R9_GENERIC_BRIDGE_CONNECTED_PROOF_PENDING'}


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--dry-run', action='store_true')
    parser.add_argument('--root', type=Path, default=Path.cwd())
    args = parser.parse_args()
    root = args.root.resolve()
    destination = root / PACKAGE / 'output' / ('preflight.json' if args.dry_run else 'audit_report.json')
    try:
        result = audit(root, args.dry_run)
        destination.write_text(json.dumps(result, indent=2, ensure_ascii=False) + '\n', encoding='utf-8')
        print('PHASE175_R4R12R9_GATE=' + str(result['gate']))
        print('PHASE175_R4R12R9_GROUP_COMPLETE=False')
        print('PHASE175_R4R12R9_REPORT=' + str(destination))
        return 0
    except Exception as exc:
        destination.parent.mkdir(parents=True, exist_ok=True)
        destination.write_text(json.dumps({'gate':'FAIL_R4R12R9', 'error':str(exc),
                                           'traceback':traceback.format_exc()},ensure_ascii=False,indent=2),encoding='utf-8')
        print('PHASE175_R4R12R9_GATE=FAIL_R4R12R9')
        print('PHASE175_R4R12R9_ERROR=' + str(exc))
        return 1


if __name__ == '__main__':
    raise SystemExit(main())
