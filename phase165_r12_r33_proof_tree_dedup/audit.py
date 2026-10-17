"""Run the established R12-R32 Web-path audit after tree deduplication."""
import json
from pathlib import Path

from r32_audit_support import run_diagnostic


def main():
    from phase165_r12_r33_proof_tree_dedup import same_completed_proof_tree
    report = run_diagnostic()
    report['phase'] = '165 R12-R33'
    report['mode'] = 'PROOF_TREE_DEDUP_WEB_AUDIT'
    report['tree_comparator_available'] = callable(same_completed_proof_tree)
    report['status'] = 'AUDIT_COMPLETE' if report['tree_comparator_available'] else 'AUDIT_BLOCKED'
    target = Path(__file__).resolve().parent / 'audit_result.json'
    target.write_text(json.dumps(report, ensure_ascii=False, indent=2), encoding='utf8')
    print(json.dumps({k: v for k, v in report.items() if k != 'root_derivations'},
                     ensure_ascii=False, indent=2))
    print('Detailed proof trees:', target)


if __name__ == '__main__':
    main()
