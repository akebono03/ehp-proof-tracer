Phase156-R5 — Reference attribution audit

目的
----
Reference statement selection ではなく、その selected statement がどの literature
reference に帰属しているかを 112 群横断で監査する。

今回確認済みの既知 defect:
  pi_6^3 の
    [R4] (5.3) / Lemma 5.2
    nu' in {eta_3, 2 iota_4, eta_4}_1
  は premise source と application theorem/lemma の attribution が混在している。

このパッケージの変更
--------------------
Production code changes: none

追加:
  phase156_r5_reference_attribution_audit/
    audit_phase156_r5_attribution.py
    test_phase156_r5_attribution.py
    run_phase156_r5_reference_attribution_audit.ps1
    README.txt

監査範囲
--------
n = 2..15
k = 0..7
合計 112 群
proof depth = 2

監査するもの
------------
selected Reference statement ごとに以下を記録する。

- Reference title / locator
- slash で結合された複合 locator の有無
- selected statement
- entry 外の consumer
- consumer の literature reference
- consumer inference rule name

分類
----
single_source
  単一 literature locator。

composite_reference
  複数 locator が一つの Reference に混在。ownership review 対象。

composite_reference_contains_consumer_reference
  複合 locator の一部が external consumer の Reference と重なる。

composite_reference_contains_consumer_rule_reference
  複合 locator の一部が external consumer の rule name に現れる。
  premise source に theorem/lemma application の帰属が混ざった可能性が高い。

実行
----
PowerShell:

cd C:\Users\user\Dropbox\Python\fitz\ehp_proof

Remove-Item `
  ".\phase156_r5_reference_attribution_audit" `
  -Recurse `
  -Force `
  -ErrorAction SilentlyContinue

Expand-Archive `
  -Path "$HOME\Downloads\phase156_r5_reference_attribution_audit.zip" `
  -DestinationPath "." `
  -Force

powershell `
  -ExecutionPolicy Bypass `
  -File ".\phase156_r5_reference_attribution_audit\run_phase156_r5_reference_attribution_audit.ps1"

完了条件
--------
- focused classifier tests が PASS
- 112 群を再現
- exceptions = 0
- pi_6^3 の既知 attribution defect を検出
- suspicious CSV に全候補を出力

この R5 では suspicious 件数が 0 であることを完了条件にしない。
まず母集団を確定し、その結果に基づいて次の repair で production metadata を修正する。

次 Phase との境界
-----------------
この監査では production code / proof data / documents は変更しない。
Reference attribution の修正は監査結果を確認してから行う。
repository-wide pytest は Phase 156 closure の最後にのみ実行する。


fixed1
------
初版の run script は audit Python file を path 指定で直接実行していたため、
sys.path が監査ディレクトリ基準となり、repository root の
toda_calculation_facade を import できなかった。

fixed1 では repository root から module execution:
  python -m phase156_r5_reference_attribution_audit_fixed1.audit_phase156_r5_attribution
に変更した。

production code / proof data の変更はない。
