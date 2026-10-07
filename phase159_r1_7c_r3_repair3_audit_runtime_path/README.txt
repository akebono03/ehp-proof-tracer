Phase 159 R1-7c R3 repair3
============================

原因
----
R3 production と focused tests は成功している。

失敗したのは audit script の runtime import path のみ。

package subdirectory 内の audit script を直接実行すると、Python の
sys.path[0] は package directory になるため、repository root にある
toda_calculation_facade.py を import できない。

GitHub の既存 audit script では repository root を

REPOSITORY_ROOT = Path(__file__).resolve().parents[1]

で求めて sys.path に追加する方式が使われている。

変更
----
Production code changes: none

変更対象:
phase159_r1_7c_r3_known_result_direct_premise_specialization/
audit_phase159_r1_7c_r3.py

追加:
- import sys
- REPOSITORY_ROOT
- repository root の sys.path.insert(0, ...)

テスト変更:
なし

実行
----
cd C:\Users\oomae\Dropbox\Python\fitz\ehp_proof

Remove-Item `
  ".\phase159_r1_7c_r3_repair3_audit_runtime_path" `
  -Recurse `
  -Force `
  -ErrorAction SilentlyContinue

Expand-Archive `
  -Path "$HOME\Downloads\phase159_r1_7c_r3_repair3_audit_runtime_path.zip" `
  -DestinationPath "." `
  -Force

powershell `
  -ExecutionPolicy Bypass `
  -File ".\phase159_r1_7c_r3_repair3_audit_runtime_path\run_phase159_r1_7c_r3_repair3.ps1"

完了条件
--------
- R3 focused tests 5件 PASS
- directly affected regressions 24件 PASS
- audit script が import error なしで実行
- pi_11^4_after_r3.md が生成される
- full pytest は実行しない
