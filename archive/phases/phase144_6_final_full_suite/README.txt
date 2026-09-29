Phase 144-6 Final Full Suite
============================

目的
----
Phase 144-6 の最後にだけ全体 pytest を実行し、
Public Route Cutover を含む既存機能全体の regression を確認する。

この package の変更
--------------------
Production code changes: none
Test code changes: none
Document changes: none

前提として確認済み
------------------
- R5-43-11D final completion audit: PASS
- Public Route Cutover production change applied
- Public Route Cutover R2 import repair applied
- Public Route Cutover R3 Web Narrative contract update applied
- Focused Public Route Cutover regression: 46 passed

Phase 144-6 の public cutover 範囲
--------------------------------
Phase 144-6 では public renderer 内の pi_6^3 route を
generic contribution-aware Narrative route に切り替える。

他の代表群を同じ public route へ追加で切り替えることは、
この final full suite package では行わない。

実行
----
repository root で:

Expand-Archive `
  -Path "$HOME\Downloads\phase144_6_final_full_suite.zip" `
  -DestinationPath "." `
  -Force

powershell -ExecutionPolicy Bypass `
  -File ".\phase144_6_final_full_suite\run_phase144_6_final_full_suite.ps1"

完了条件
--------
pytest -q が全件 PASS すること。

PASS 後
-------
Phase 144-6 の implementation/test boundary を完了と判定する。
その後、Phase 144-6 completion documentation を更新する。
