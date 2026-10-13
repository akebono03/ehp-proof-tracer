import json
from pathlib import Path
from phase165_r14_r15_typed_diagonal import audit_r15


def main():
    report = audit_r15()
    output = Path('phase165_r14_r15_output')
    output.mkdir(exist_ok=True)
    (output / 'report.json').write_text(json.dumps(report, ensure_ascii=False, indent=2) + '\n', encoding='utf-8')
    (output / 'report.md').write_text('# Phase 165 R14-R15\n\n' + '\n'.join(f'- {k}: {v}' for k,v in report.items()) + '\n', encoding='utf-8')
    print(json.dumps(report, ensure_ascii=False, indent=2))


if __name__ == '__main__':
    main()
