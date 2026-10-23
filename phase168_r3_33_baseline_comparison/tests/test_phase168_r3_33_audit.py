from __future__ import annotations

import importlib.util
from pathlib import Path

PACKAGE = Path(__file__).resolve().parents[1]
SPEC = importlib.util.spec_from_file_location('phase168_r3_33_audit', PACKAGE / 'audit.py')
AUDIT = importlib.util.module_from_spec(SPEC)
assert SPEC.loader is not None
SPEC.loader.exec_module(AUDIT)


def test_audit_recognizes_order_missing_and_duplicated_phrases():
    case = {'milestones': (('first', 'ABC'), ('second', 'DEF'), ('third', 'GHI'))}
    output = AUDIT.analyze_markdown('使用する結果\n証明\nDEF ABC', case)
    statuses = [x['status'] for x in output['milestones']]
    assert statuses == ['IN_ORDER', 'OUT_OF_ORDER_OR_DUPLICATE', 'MISSING_OR_DIFFERENT_EXPRESSION']


def test_baseline_files_preserved_and_expected_cases_present():
    assert [case['name'] for case in AUDIT.CASES] == ['pi_3^2', 'pi_4^3', 'pi_5^4']
    for case in AUDIT.CASES:
        text = (PACKAGE / 'baselines' / case['baseline']).read_text(encoding='utf-8')
        assert '証明' in text
        assert '以上より' in text
    pi54 = next(c for c in AUDIT.CASES if c['name'] == 'pi_5^4')
    assert ('toda45_specialization', '(n,m,k)=(3,4,1)') in pi54['milestones']
