Phase 158-R5-4 repair1
=========================

目的
----
R5-4 audit package の実行環境だけを修正する。

原因
----
audit_phase158_r5_4.py を audit subdirectory から直接実行したため、
repository root が Python sys.path に入らず、
toda_calculation_facade を import できなかった。

また PowerShell は native command の non-zero exit code だけでは
$ErrorActionPreference = "Stop" によって停止しないため、
Python 失敗後も summary.txt の読み込みへ進んでいた。

修正
----
1. audit script 冒頭で repository root を sys.path に追加。
2. python 実行後に $LASTEXITCODE を検査。
3. summary.txt の存在を検査してから Get-Content。

変更しないもの
--------------
Production code: 変更なし
Test code: 変更なし
pytest: 実行しない
R5-4 の監査内容: 変更なし
