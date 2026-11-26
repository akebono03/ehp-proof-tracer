"""Read-only isolated runner; permit only the reviewed R5 shared hook."""
from __future__ import annotations

import argparse
import os
from pathlib import Path
import subprocess
import sys

ROOT = Path(__file__).resolve().parents[1]
BASE = '4863d0d2d985b48a7eac69a702d9374a3c685165'
PREFIX = 'PHASE178_R6_'
TARGET = 'phase165_r52_r9_shared_math.py'
PINS = {
    'homotopy_groups.py': '883faf1b4a067485c9127f14dbb575aaa195960e',
    'expression.py': '7f7cd97468cd753643369f54774ee9892968c345',
    'proof.py': '2eb683053eaf7146bd89afbc581a386af08b8060',
    'phase165_r3_recursive_search.py': '34c63d520eb102d0d1e6340148f9b7a1dd9eaace',
    'phase171_r2j_r4_r6_middle_cardinality/source.py': '5df4d3e247d1e3f9a578dd4fc9e7434c3d3f62eb',
    'phase171_r2j_r4_r6_middle_cardinality/tests/test_audit.py': 'd9ffa7934e6c13259fbade74812b8c321c9264b4',
    'phase175_r4r7_prop25_typed_composition/rule.py': 'e957752baf93f75352d106e53205730af9a02b4d',
    'phase177_r14_finite_cyclic_delta_injective_isolated/rule.py': 'fba57005273dfdf795501df5f71b3822f4ecddfe',
    'phase177_r14_finite_cyclic_delta_injective_isolated/tests/test_rule.py': '385c4daaa7c43ac74082e20e314235144addd427',
}
ANCHOR = '    # Phase 177 R8: screened unsigned Prop 2.5 backward candidates.\n'
HOOK = (
    '    # Phase 178 R5: expose the unchanged R4 Delta-E surjectivity rule.\n'
    '    from phase178_r4_delta_surjective_zero_suspension_isolated.rule import (\n'
    '        expand_delta_surjective_from_zero_suspension,\n'
    '    )\n'
    '    extra_providers = tuple(extra_providers) + (\n'
    '        expand_delta_surjective_from_zero_suspension,\n'
    '    )\n\n'
)
TESTS = (
    'phase178_r6_finite_group_cardinality_isolated/tests/test_rule.py',
    'phase171_r2j_r4_r6_middle_cardinality/tests/test_audit.py::test_generic_cardinality_product_without_middle_group_presentation',
    'phase171_r2j_r4_r6_middle_cardinality/tests/test_audit.py::test_mixed_source_and_inference_steps_produce_real_inference',
    'phase177_r14_finite_cyclic_delta_injective_isolated/tests/test_rule.py::test_order_supports_mixed_and_many_summands',
)


def git(*args):
    return subprocess.check_output(['git',*args],cwd=ROOT)


def gt(*args):
    return git(*args).decode('utf-8').strip()


def normalize(raw):
    return raw.decode('utf-8-sig').replace('\r\n','\n')


def require(condition,message):
    if not condition:
        raise RuntimeError(message)


def preflight():
    require(Path(os.fsdecode(git('rev-parse','--show-toplevel').strip())).resolve()==ROOT,'WRONG_ROOT')
    head=gt('rev-parse','HEAD')
    require(gt('branch','--show-current')=='develop','DEVELOP_REQUIRED')
    require(head==gt('rev-parse','origin/develop'),'HEAD_NOT_REMOTE')
    require(gt('merge-base',BASE,head)==BASE,'REVIEWED_BASE_REQUIRED')
    require(not gt('diff','--cached','--name-only'),'STAGED_CHANGES_REFUSED')
    changed=set(gt('diff','--name-only','HEAD').splitlines())
    require(not changed-{TARGET},'UNRELATED_TRACKED_CHANGES:'+repr(sorted(changed)))
    require(not os.environ.get('PYTEST_ADDOPTS','').strip(),'PYTEST_ADDOPTS_REQUIRES_REVIEW')
    for path,pin in PINS.items():
        require(gt('rev-parse','HEAD:'+path)==pin,'PIN_CHANGED:'+path)
        require(normalize((ROOT/path).read_bytes())==normalize(git('show','HEAD:'+path)),'DEPENDENCY_CHANGED:'+path)
    require(gt('rev-parse',BASE+':'+TARGET)=='f4383a0c248fe62903203d1863df345740581c59','BASE_SHARED_BLOB_CHANGED')
    original=normalize(git('show',BASE+':'+TARGET))
    require(original.count(ANCHOR)==1 and HOOK not in original,'BASE_SHARED_ANCHOR_CHANGED')
    expected=original.replace(ANCHOR,HOOK+ANCHOR,1)
    require(normalize(git('show','HEAD:'+TARGET)) in (original,expected),'HEAD_SHARED_UNREVIEWED')
    require(normalize((ROOT/TARGET).read_bytes())==expected,'R5_HOOK_NOT_EXACTLY_INSTALLED')
    git('diff','--check')
    return head,git('status','--porcelain','--untracked-files=no'),git('diff','--binary','HEAD'),(ROOT/TARGET).read_bytes()


def main():
    parser=argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--dry-run',action='store_true')
    args=parser.parse_args()
    try:
        before=preflight()
        print(PREFIX+'HEAD='+before[0],flush=True)
        if not args.dry_run:
            subprocess.run([sys.executable,'-B','-m','pytest','-q','-p','no:cacheprovider',
                            '--import-mode=importlib',*TESTS],cwd=ROOT,check=True)
            require(preflight()==before,'TRACKED_STATE_CHANGED')
        print(PREFIX+'PUBLIC_CONNECTION=NOT_CHANGED')
        print(PREFIX+'FULL_PYTEST=NOT_RUN')
        print(PREFIX+'GATE='+('PASS_R6_READ_ONLY_DRYRUN' if args.dry_run else 'PASS_R6_FINITE_GROUP_CARDINALITY_ISOLATED'))
        return 0
    except Exception as exc:
        print(PREFIX+'ERROR='+str(exc),file=sys.stderr,flush=True)
        print(PREFIX+'GATE=FAIL_R6',flush=True)
        return 1


if __name__=='__main__':
    raise SystemExit(main())
