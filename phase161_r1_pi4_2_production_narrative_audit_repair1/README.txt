Phase 161-R1 repair1

変更対象
========
監査 package のみ。
production source code は変更しない。

修正内容
========
初回 audit は Windows PowerShell / Python の標準出力が CP932 の場合、
eta などの Unicode を含む repr の出力で停止する可能性があった。

repair1 では、
- PYTHONUTF8=1
- PYTHONIOENCODING=utf-8
- raw object diagnostics は ascii() を使用

として監査出力を UTF-8 安全化する。

監査内容、focused tests、Phase 161 の境界は変更しない。
全体 pytest は実行しない。
