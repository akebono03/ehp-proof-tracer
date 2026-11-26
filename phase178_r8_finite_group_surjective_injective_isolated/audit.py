"""Read-only runner for the isolated R8 rule, allowing precisely the R7 hook."""
from __future__ import annotations

import argparse
import hashlib
import os
from pathlib import Path
import subprocess
import sys

ROOT = Path(__file__).resolve().parents[1]
BASE = 'c49f625935acc33180a8900ba1481a2852514669'
TARGET = 'phase165_r52_r9_shared_math.py'
PREFIX = 'PHASE178_R8_'
PINS = {
    'homotopy_groups.py': '883faf1b4a067485c9127f14dbb575aaa195960e',
    'proof.py': '2eb683053eaf7146bd89afbc581a386af08b8060',
    'phase165_r14_r6_generic_iso.py': '8e8f5a4245f3dbbc5707b3a0042a1274e4b3e6b7',
    'phase165_r3_recursive_search.py': '34c63d520eb102d0d1e6340148f9b7a1dd9eaace',
    'phase171_r2j_r4_r6_middle_cardinality/source.py': '5df4d3e247d1e3f9a578dd4fc9e7434c3d3f62eb',
    'phase177_r14_finite_cyclic_delta_injective_isolated/rule.py': 'fba57005273dfdf795501df5f71b3822f4ecddfe',
    'phase174_r3_r7_r32_lower_delta_kernel_audit/kernel_contract.py': 'c2357859b00ed0b446bac7a060a6d0c134fc7de5',
    'phase178_r6_finite_group_cardinality_isolated/rule.py': '8c6de74a331d75b38d592603062d99c591a040b9',
    'phase178_r6_finite_group_cardinality_isolated/tests/test_rule.py': '4c2a181164acf13ac1fb85ae8c81e3e5bdd0dffc',
    'phase178_r4_delta_surjective_zero_suspension_isolated/rule.py': '60b91c4ba674ca4680f0c3b353ceb873ecebc7ee',
}
ANCHOR = '    # Phase 177 R8: screened unsigned Prop 2.5 backward candidates.\n'
HOOK = '    # Phase 178 R7: expose the unchanged R6 finite group cardinality rule.\n    from phase178_r7_finite_group_cardinality_public.provider import (\n        build_public_finite_cardinality_provider,\n    )\n    extra_providers = tuple(extra_providers) + (\n        build_public_finite_cardinality_provider(bridge=bridge, proof_target=proof_target),\n    )\n\n'
R7_PROVIDER_SHA256 = '075790d857e08d62be17a666af88ad7dd3678b247bad125f1a028aa7467bfbbb'

TESTS = (
    'phase178_r8_finite_group_surjective_injective_isolated/tests/test_rule.py',
    'phase178_r6_finite_group_cardinality_isolated/tests/test_rule.py',
)


def git(*args):
    return subprocess.check_output(['git', *args], cwd=ROOT)


def gt(*args):
    return git(*args).decode('utf-8').strip()


def normalize(raw):
    return raw.decode('utf-8-sig').replace('\r\n', '\n')


def require(condition, message):
    if not condition:
        raise RuntimeError(message)


def preflight():
    require(Path(os.fsdecode(git('rev-parse','--show-toplevel').strip())).resolve()==ROOT, 'WRONG_ROOT')
    head = gt('rev-parse','HEAD')
    require(gt('branch','--show-current')=='develop', 'DEVELOP_REQUIRED')
    require(head==gt('rev-parse','origin/develop'), 'HEAD_NOT_REMOTE')
    require(gt('merge-base',BASE,head)==BASE, 'REVIEWED_BASE_REQUIRED')
    require(not gt('diff','--cached','--name-only'), 'STAGED_CHANGES_REFUSED')
    changed = set(gt('diff','--name-only','HEAD').splitlines())
    require(not changed-{TARGET}, 'UNRELATED_TRACKED_CHANGES:'+repr(sorted(changed)))
    require(not os.environ.get('PYTEST_ADDOPTS','').strip(), 'PYTEST_ADDOPTS_REQUIRES_REVIEW')
    for path,pin in PINS.items():
        require(gt('rev-parse','HEAD:'+path)==pin, 'PIN_CHANGED:'+path)
        require(normalize((ROOT/path).read_bytes())==normalize(git('show','HEAD:'+path)), 'DEPENDENCY_CHANGED:'+path)
    require(gt('rev-parse',BASE+':'+TARGET)=='459bc08b809fc51e89d89d4c8240b5ce0d591cdf', 'BASE_SHARED_BLOB_CHANGED')
    original = normalize(git('show',BASE+':'+TARGET))
    require(original.count(ANCHOR)==1 and HOOK not in original, 'BASE_SHARED_ANCHOR_CHANGED')
    expected = original.replace(ANCHOR, HOOK+ANCHOR, 1)
    require(normalize(git('show','HEAD:'+TARGET)) in (original,expected), 'HEAD_SHARED_UNREVIEWED')
    require(normalize((ROOT/TARGET).read_bytes())==expected, 'R7_HOOK_NOT_EXACTLY_INSTALLED')
    provider = ROOT/'phase178_r7_finite_group_cardinality_public/provider.py'
    require(hashlib.sha256(provider.read_bytes().replace(b'\r\n',b'\n')).hexdigest()==R7_PROVIDER_SHA256, 'R7_PROVIDER_CHANGED')
    git('diff','--check')
    return head,git('status','--porcelain','--untracked-files=no'),git('diff','--binary','HEAD'),(ROOT/TARGET).read_bytes()


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--dry-run',action='store_true')
    args = parser.parse_args()
    try:
        before = preflight()
        print(PREFIX+'HEAD='+before[0],flush=True)
        if not args.dry_run:
            subprocess.run([sys.executable,'-B','-m','pytest','-q','-p','no:cacheprovider',
                            '--import-mode=importlib',*TESTS],cwd=ROOT,check=True)
            require(preflight()==before,'TRACKED_STATE_CHANGED')
        print(PREFIX+'PUBLIC_CONNECTION=NOT_CHANGED')
        print(PREFIX+'FULL_PYTEST=NOT_RUN')
        print(PREFIX+'GATE='+('PASS_R8_READ_ONLY_DRYRUN' if args.dry_run else 'PASS_R8_FINITE_SURJECTIVE_INJECTIVE_ISOLATED'))
        return 0
    except Exception as exc:
        print(PREFIX+'ERROR='+str(exc),file=sys.stderr,flush=True)
        print(PREFIX+'GATE=FAIL_R8',flush=True)
        return 1


if __name__=='__main__':
    raise SystemExit(main())
