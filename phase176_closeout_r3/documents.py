"""Retain R2's verified full-suite record and explicitly record recovery."""
from phase176_closeout_r2.documents import sections as r2_sections


def sections(report, r2_report_sha256):
    """Build the recovery edition from the verified R2 evidence, not a new test."""
    result = r2_sections(report)
    for name, text in result.items():
        if name == 'README.md':
            extra = (
                'R2 passed the repaired active suite but its closeout gate failed during '
                'document publication with a Windows PermissionError. R3 verified the saved '
                'R2 evidence and recovered all five complete documents without rerunning '
                'the full suite. The R2 failure record remains unchanged. '
                f'R2 report SHA-256: `{r2_report_sha256}`.\n'
            )
        else:
            extra = (
                'R2 は修正後の全体 pytest に合格したが、文書生成・適用時の Windows '
                'PermissionError により終了 Gate は FAIL となった。R3 は保存済みの '
                'R2 合格証拠を検証し、全体 pytest を再実行せず主要5文書の全文更新を復旧した。'
                'R2 の失敗記録は変更せず保持する。'
                f'R2 report SHA-256：`{r2_report_sha256}`。\n'
            )
        result[name] = text.rstrip() + '\n\n' + extra
    return result
