from pathlib import Path
import json
from phase165_r14_r24_delta_connection import audit_r24


def main():
    report = audit_r24(Path(__file__).with_name('toda_51_complete.tex'))
    output = Path('phase165_r14_r24_output')
    output.mkdir(exist_ok=True)
    (output / 'report.json').write_text(json.dumps(report, ensure_ascii=False, indent=2) + '\n', encoding='utf-8')
    (output / 'prop42_source_review.md').write_text(
        '# Proposition 4.2 原文候補（数学的認証前）\n\n'
        + '\n\n'.join(
            '## ' + c['assertion_id'] + '\n\n```tex\n' + c['source_text'] + '\n```'
            for c in report['prop42_source_candidates']
        ) + '\n', encoding='utf-8'
    )
    print(json.dumps({k: v for k, v in report.items() if k != 'prop42_source_candidates'}, ensure_ascii=False, indent=2))


if __name__ == '__main__':
    main()
