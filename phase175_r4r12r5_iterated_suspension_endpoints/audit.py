"""R4R12R5: typed suspension-endpoint repair and public candidate audit."""
from __future__ import annotations

import argparse
from datetime import datetime, timezone
import json
import os
from pathlib import Path
import sys
import tempfile
import traceback

from phase175_r4r12r5_iterated_suspension_endpoints import installer

DRY_GATE = 'PASS_R4R12R5_ENDPOINT_REPAIR_DRYRUN'
FINAL_GATE = 'PASS_R4R12R5_TWO_SUMMAND_ROOT_CANDIDATES_NOT_PROVED'


def run(root: Path, *, dry_run: bool) -> int:
    base = Path(os.environ.get('LOCALAPPDATA') or tempfile.gettempdir())
    folder = base/'EHPProofTracerAudit'/'phase175_r4r12r5_iterated_suspension_endpoints'/datetime.now(timezone.utc).strftime('%Y%m%dT%H%M%S_%fZ')
    folder.mkdir(parents=True,exist_ok=False)
    report = {'phase':'175-R4R12R5','dry_run':dry_run,'gate':'FAIL_R4R12R5',
              'new_given':0,'new_mathematical_rules':0,'pi95_proof_complete':False,
              'full_pytest_executed':False,'prior_proof_search_executed':False}
    try:
        report['install'] = installer.install(root,dry_run=dry_run,output=folder)
        if not dry_run:
            from phase175_r4r12_public_two_summand_quotient.audit import inspect_public_root
            report['public'] = inspect_public_root()
            if report['public'].get('public_root_candidates',0) < 1:
                raise RuntimeError('R4R12R5_ROOT_CANDIDATES_ABSENT')
        report['gate'] = DRY_GATE if dry_run else FINAL_GATE
    except Exception as exc:
        report['error']=type(exc).__name__+': '+str(exc)
        report['traceback']=traceback.format_exc()[-6000:]
    (folder/'report.json').write_text(json.dumps(report,indent=2,ensure_ascii=False)+'\n',encoding='utf-8')
    print('PHASE175_R4R12R5_GATE='+str(report['gate']))
    print('PHASE175_R4R12R5_REPORT='+str(folder/'report.json'))
    print('PHASE175_R4R12R5_NEW_GIVEN=0')
    print('PHASE175_R4R12R5_NEW_MATHEMATICAL_RULES=0')
    print('PHASE175_R4R12R5_PI95=NOT_COMPLETE')
    print('PHASE175_R4R12R5_FULL_PYTEST=NOT_RUN')
    if isinstance(report.get('public'),dict):
        print('PHASE175_R4R12R5_PUBLIC_CANDIDATES='+str(report['public'].get('public_root_candidates')))
        print('PHASE175_R4R12R5_OBLIGATIONS_EACH='+str(report['public'].get('each_candidate_proof_obligations')))
    if 'error' in report:
        print('PHASE175_R4R12R5_ERROR='+str(report['error']))
        return 1
    return 0


def main(argv: list[str] | None=None) -> int:
    parser=argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--root',type=Path,default=Path.cwd())
    parser.add_argument('--dry-run',action='store_true')
    args=parser.parse_args(argv)
    return run(args.root.resolve(),dry_run=args.dry_run)


if __name__=='__main__':
    sys.exit(main())
