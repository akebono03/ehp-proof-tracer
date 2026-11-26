"""Read-only pin guard and limited isolated pytest runner."""
from __future__ import annotations

import argparse
import os
from pathlib import Path
import subprocess
import sys

ROOT = Path(__file__).resolve().parent.parent
BASE = '98ecbb664d5b2baf3eb5c20727ae54a078edbf78'
PREFIX = 'PHASE178_R4_'
PINS = {
    'homotopy_groups.py': '883faf1b4a067485c9127f14dbb575aaa195960e',
    'phase165_r14_r6_generic_iso.py': '8e8f5a4245f3dbbc5707b3a0042a1274e4b3e6b7',
    'phase165_r12_r11_prop42_unified.py': '79752ec035244677ff6a54debff312e87a76fbf2',
    'map_property_rules.py': '4adeebc9dedb3daf210cd8755be811aca32f1e8b',
    'phase175_r4r12r13r4_hopf_zero_public/rule.py': '74b7e8dee9032f5b0cbfc0086646bb423e73be74',
    'phase175_r4r12r13r4_hopf_zero_public/tests/test_rule.py': '44f8c403e6663569f1ff7d6eb1799d825911a4ab',
    'phase165_r52_r9_shared_math.py': 'f4383a0c248fe62903203d1863df345740581c59',
    'sources/toda/Toda_05_2.tex': '579661138928499ba04a51327f686d9b971b5314',
}
TESTS = (
    'phase178_r4_delta_surjective_zero_suspension_isolated/tests/test_rule.py',
    'phase175_r4r12r13r4_hopf_zero_public/tests/test_rule.py::test_surjectivity_rule_accepts_only_zero_map_and_exactness',
    'phase175_r4r12r13r4_hopf_zero_public/tests/test_rule.py::test_wrong_hopf_map_dimensions_are_rejected',
)


def git(*args):
    return subprocess.check_output(['git',*args],cwd=ROOT).decode('utf-8').strip()


def require(condition, message):
    if not condition:
        raise RuntimeError(message)


def preflight():
    head = git('rev-parse','HEAD')
    require(git('branch','--show-current') == 'develop','DEVELOP_REQUIRED')
    require(head == git('rev-parse','origin/develop'),'HEAD_NOT_REMOTE')
    require(git('merge-base',BASE,head) == BASE,'REVIEWED_BASE_REQUIRED')
    tracked_status = git('status','--porcelain','--untracked-files=no')
    if tracked_status:
        print(PREFIX+'TRACKED_STATUS='+tracked_status, file=sys.stderr, flush=True)
    require(not tracked_status,'TRACKED_TREE_NOT_CLEAN')
    require(not os.environ.get('PYTEST_ADDOPTS','').strip(),'PYTEST_ADDOPTS_REQUIRES_REVIEW')
    for path,sha in PINS.items():
        require(git('rev-parse','HEAD:'+path) == sha,'PIN_CHANGED:'+path)
    git('diff','--check')
    print(PREFIX+'HEAD='+head,flush=True)
    return head


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('--dry-run',action='store_true')
    args = parser.parse_args()
    try:
        head = preflight()
        if not args.dry_run:
            subprocess.run([sys.executable,'-B','-m','pytest','-q','-p','no:cacheprovider','--import-mode=importlib',*TESTS],cwd=ROOT,check=True)
            require(preflight() == head,'HEAD_CHANGED')
        print(PREFIX+'PUBLIC_CONNECTION=NOT_CHANGED')
        print(PREFIX+'FULL_PYTEST=NOT_RUN')
        print(PREFIX+'GATE='+('PASS_R4_READ_ONLY_DRYRUN' if args.dry_run else 'PASS_R4_DELTA_SURJECTIVITY_ISOLATED'))
        return 0
    except Exception as exc:
        print(PREFIX+'ERROR='+str(exc),file=sys.stderr)
        print(PREFIX+'GATE=FAIL_R4')
        return 1


if __name__ == '__main__':
    raise SystemExit(main())
