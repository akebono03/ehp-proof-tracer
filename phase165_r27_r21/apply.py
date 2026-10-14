from pathlib import Path
import ast
import shutil

ROOT = Path(__file__).resolve().parent.parent
TARGET = ROOT / 'phase165_r52_r5_auto_search.py'
BACKUP = Path(__file__).resolve().parent / 'phase165_r52_r5_auto_search.before_r27_r21.py'

OLD = '''    if discovery is None:
        from toda_calculation_facade import build_standard_toda_report
        from toda_calculation_result import TodaCalculationStatus
        from phase165_r52_r9_shared_math import search_shared_group_goal

        report = build_standard_toda_report(n=n, k=k)
        if report.status is TodaCalculationStatus.FOUND and len(report.candidates) == 1:
            group_result = report.candidates[0].source_candidate.group_result
            return search_shared_group_goal(
                n=n, k=k, group_structure=group_result.group_structure,
            )
        from phase165_r9_production_wiring import discover_goal_search_inputs
        discovery = discover_goal_search_inputs()
'''
NEW = '''    if discovery is None:
        from phase165_r9_production_wiring import discover_goal_search_inputs
        discovery = discover_goal_search_inputs()
'''

def main():
    if not TARGET.is_file():
        raise SystemExit(f'Missing target: {TARGET}')
    source = TARGET.read_text(encoding='utf-8')
    if OLD not in source:
        if NEW in source and 'from toda_calculation_facade import build_standard_toda_report' not in source:
            print('R27-R21 already installed')
            return
        raise SystemExit('R27-R21 guard failed: expected exact old discovery block')
    result = source.replace(OLD, NEW, 1)
    ast.parse(result, filename=str(TARGET))
    if not BACKUP.exists():
        shutil.copy2(TARGET, BACKUP)
    TARGET.write_text(result, encoding='utf-8', newline='')
    print('R27-R21 installed: typed search no longer borrows legacy group calculation')

if __name__ == '__main__':
    main()
