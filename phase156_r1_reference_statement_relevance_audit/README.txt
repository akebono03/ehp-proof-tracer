Phase156-R1 — Reference statement relevance / minimal display audit

目的
====
Phase155 で Phase156 に繰り越した 117 件の
exact selected-statement/body duplicate を再現し、全件を一般規則で分類する。

GitHub baseline
===============
develop:
57535288615991056f9fbf2b471cc6e844545034

Phase155 final boundary:
- 10384 total tests
- 10382 routine tests
- 2 audit-only tests
- exact selected-statement/body duplicate pressure: 117
- duplicate invariant itselfは Phase156 へ deferred

変更対象
========
production:
- なし

既存 tests:
- 変更なし

追加パッケージ:
- audit_phase156_r1.py
- test_phase156_r1_audit_classifier.py
- run_phase156_r1_reference_statement_relevance_audit.ps1
- README.txt

分類
====
1. unnecessary_duplicate
   Reference attribution だけで足りる構造的重複。
   standalone exact duplicate や、同一 [Rn] の利用文で
   calculation / derivation context を持たないもの。

2. body_restatement_required
   同じ statement でも本文で calculation / derivation の流れを
   担っているとR1の構造的証拠から判断するもの。
   R1では保守的に残す側へ分類する。

3. reference_side_overfull
   一つの Reference に複数 selected statement が表示されているもの。
   R1では「Reference side の component relevance を R2 で確認すべき」
   という分類にする。

重要
====
R1の分類は consumer semantics の最終規則ではない。
R2で proof graph の consumer usage を使い、
「どの statement component が実際に必要か」を一般規則として設計する。

今回しないこと
==============
- production renderer の変更
- Reference selection の変更
- Reference statement suppression の変更
- proof graph の変更
- stable range の数学的展開
- repository-wide pytest

実行
====
PowerShell:

cd C:\Users\user\Dropbox\Python\fitz\ehp_proof

Remove-Item `
  ".\phase156_r1_reference_statement_relevance_audit" `
  -Recurse `
  -Force `
  -ErrorAction SilentlyContinue

Expand-Archive `
  -Path "$HOME\Downloads\phase156_r1_reference_statement_relevance_audit.zip" `
  -DestinationPath "." `
  -Force

powershell `
  -ExecutionPolicy Bypass `
  -File ".\phase156_r1_reference_statement_relevance_audit\run_phase156_r1_reference_statement_relevance_audit.ps1"

実行される pytest
=================
python -m pytest `
  .\phase156_r1_reference_statement_relevance_audit\test_phase156_r1_audit_classifier.py `
  -q `
  -p no:cacheprovider

全体テストは Phase156 の最後だけ行う。

完了条件
========
- 112 groups を再現
- exceptions = 0
- duplicate population = 117
- 117件すべてが3分類のいずれかに入る
- focused classifier tests PASS
- production changes = none

出力
====
phase156_r1_audit_output/
- phase156_r1_duplicate_classification.csv
- phase156_r1_group_summary.csv
- phase156_r1_classification_summary.csv
- phase156_r1_exceptions.csv
- phase156_r1_result.json
- phase156_r1_summary.txt

次 Phase との境界
================
Phase156-R2:
consumer usage（本文での実利用）から必要 statement を判定する一般規則を設計する。
R1では production behavior を変更しない。
