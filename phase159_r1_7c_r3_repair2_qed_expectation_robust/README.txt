Phase 159 R1-7c R3 repair2
============================

原因
----
repair1 の installer 内で backslash escaping が過剰になり、
実テスト中の r"$\square$" を検出できなかった。

repair2 は対象 test function の範囲だけを切り出し、
その内部の literal r"$\square$" を "□" に置換する。

Production code changes: none

変更対象
--------
tests/test_phase159_r1_7c_r3_known_result_direct_premise_specialization.py

変更内容
--------
r"$\square$"
↓
"□"

実行
----
cd C:\Users\oomae\Dropbox\Python\fitz\ehp_proof

Remove-Item `
  ".\phase159_r1_7c_r3_repair2_qed_expectation_robust" `
  -Recurse `
  -Force `
  -ErrorAction SilentlyContinue

Expand-Archive `
  -Path "$HOME\Downloads\phase159_r1_7c_r3_repair2_qed_expectation_robust.zip" `
  -DestinationPath "." `
  -Force

powershell `
  -ExecutionPolicy Bypass `
  -File ".\phase159_r1_7c_r3_repair2_qed_expectation_robust\run_phase159_r1_7c_r3_repair2.ps1"

完了条件
--------
- R3 focused tests が全 PASS
- pi11_4 core inference regressions が PASS
- generic ordering regressions が PASS
- pi_11^4 audit output が生成される
- full pytest は実行しない
