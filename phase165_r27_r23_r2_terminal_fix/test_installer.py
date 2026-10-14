import ast
import importlib.util
from pathlib import Path

ROOT = Path(__file__).resolve().parent
spec = importlib.util.spec_from_file_location('r23_r2_apply', ROOT / 'apply.py')
module = importlib.util.module_from_spec(spec)
spec.loader.exec_module(module)

SOURCE = '''import argparse
from toda_calculation_facade import (\n  build_standard_toda_report,\n)

def _run_group_proof_command(n, k, max_depth=2, mode="narrative"):
    return build_standard_toda_report(n=n, k=k)

def main(argv=None):
    raw_argv = argv if argv is not None else []
    if raw_argv and raw_argv[0] == "explore":
        return 0
    if raw_argv and raw_argv[0] == "group-proof":
        return _run_group_proof_command(3, 1)
    parser = build_argument_parser()
    args = parser.parse_args(raw_argv)
    query = TodaGroupQuery(n=args.n, k=args.k)
    if args.n < 2:
        print('boundary')
        return 0
    report = build_standard_toda_report(n=args.n, k=args.k)
    print(report.reports)
    return 0
'''

def test_r23_r2_nonstandard_main_layout_can_migrate():
    result = module.transform(SOURCE)
    ast.parse(result)
    assert 'return _run_group_query_command(' in result
    assert 'build_standard_toda_report(' not in result
    assert 'raw_argv[0] == "explore"' in result


def test_r23_r2_transform_idempotent():
    once = module.transform(SOURCE)
    twice = module.transform(once)
    assert once == twice


def test_r23_r2_missing_parser_is_guarded():
    bad = SOURCE.replace('parser = build_argument_parser()', 'parser = None')
    try:
        module.transform(bad)
    except RuntimeError as error:
        assert 'not unique' in str(error)
    else:
        raise AssertionError('Expected layout guard')


def test_r23_r2_terminal_branch_accepts_local_declarations():
    source = SOURCE.replace(
        '    report = build_standard_toda_report(n=args.n, k=args.k)',
        '    report: object = build_standard_toda_report(n=args.n, k=args.k)',
    )
    updated = module.transform(source)
    ast.parse(updated)
    assert 'build_standard_toda_report(' not in updated
    assert 'return _run_group_query_command(' in updated


def test_r23_r2_terminal_branch_accepts_try_statements():
    source = SOURCE.replace(
        '    report = build_standard_toda_report(n=args.n, k=args.k)',
        '    try:\n        report = build_standard_toda_report(n=args.n, k=args.k)\n    except Exception:\n        return 1',
    )
    updated = module.transform(source)
    ast.parse(updated)
    assert 'build_standard_toda_report(' not in updated
