Phase 153-R3-1
112 Groups Reference Statement Coverage Audit

目的
====
Reference section の各 [R1], [R2], ... について、現行の semantic information と
renderer だけを利用した場合に数学的 statement を表示できるかを、112 groups 全体で監査する。

この package は audit-only であり、production code は変更しない。

監査範囲
========
n = 2..15
k = 0..7
合計 112 groups
proof replay depth = 2
semantic closure を使用

分類
====
1. reference_only
   現行情報から数学的 statement 候補を抽出できない reference entry。

2. reference_plus_statement
   現行の narrative LaTeX renderer または generic semantic renderer から
   数学的 statement 候補を取得できる reference entry。

3. unresolved_rendering
   reference は存在するが、statement renderer が rule-name / type-name /
   raw repr / raw str fallback に落ちる entry。

4. statement_duplicates_body
   Reference section に statement を表示すると、現在の本文にも同じ statement が
   正規化後の完全一致で存在するケース。
   R3 の実装段階で本文側の重複整理候補となる。

変更対象
========
新規:
- phase153_r3_1_reference_statement_coverage_audit/audit_phase153_r3_1_reference_statement_coverage.py
- phase153_r3_1_reference_statement_coverage_audit/run_phase153_r3_1_reference_statement_coverage_audit.ps1
- phase153_r3_1_reference_statement_coverage_audit/README.txt

変更しない:
- toda_group_proof_narrative_references.py
- toda_group_proof_narrative_renderer.py
- toda_group_proof_generic_narrative_renderer.py
- tests/*
- README.md
- design.md
- development_log.md
- roadmap.md
- proof_records.md

実行
====
PowerShell で ehp_proof repository root に移動してから以下を実行する。

cd C:\Users\oomae\Dropbox\Python\fitz\ehp_proof

Remove-Item `
  ".\phase153_r3_1_reference_statement_coverage_audit" `
  -Recurse `
  -Force `
  -ErrorAction SilentlyContinue

Expand-Archive `
  -Path "$HOME\Downloads\phase153_r3_1_reference_statement_coverage_audit.zip" `
  -DestinationPath "." `
  -Force

powershell `
  -ExecutionPolicy Bypass `
  -File ".\phase153_r3_1_reference_statement_coverage_audit\run_phase153_r3_1_reference_statement_coverage_audit.ps1"

pytest
======
R3-1 は audit-only なので pytest は追加・変更しない。
全体 pytest も Phase153 の最後まで実行しない。

完了条件
========
- groups: 112
- exceptions: 0
- 全 reference entry が以下のいずれかに分類される:
  reference_only
  reference_plus_statement
  unresolved_rendering
- statement candidate が body duplicate / no exact body duplicate に分類される
- production behavior に変更がない

次 Phase との境界
================
R3-1 では監査結果を確定するだけ。
Reference section renderer の実装変更、statement の採用規則、本文重複の抑制は
R3-2 以降で行う。
