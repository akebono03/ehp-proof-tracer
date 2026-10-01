Phase153-R3-2
Reference Statement Selection / Ownership Audit

目的
====
Phase153-R3-1 で確認した Reference section の statement candidate を、
実装前に以下の2観点で監査する。

1. selection（採用）
   各 [Rn] に statement candidate が1件なのか複数件なのか、
   unresolved rendering が混在するのかを確認する。

2. ownership（所有位置）
   Reference section に候補を表示したとき、同一 statement が現在の本文にも
   既に表示されているかを確認する。

さらに proof graph 上で、その candidate step が後続の proof step に
実際に利用されているかも記録する。

重要
====
この Phase は audit-only。
代表 statement の選択、本文からの suppress（抑制）、Reference renderer の変更は行わない。

変更対象
========
新規:
- phase153_r3_2_reference_statement_selection_ownership_audit/audit_phase153_r3_2_reference_statement_selection_ownership.py
- phase153_r3_2_reference_statement_selection_ownership_audit/run_phase153_r3_2_reference_statement_selection_ownership_audit.ps1
- phase153_r3_2_reference_statement_selection_ownership_audit/README.txt

production code: 変更なし
tests: 変更なし

監査分類
========
Selection:
- single_candidate
- single_candidate_with_unresolved
- multiple_candidates
- multiple_candidates_with_unresolved
- unresolved_only

Ownership:
- reference_only_display_candidate
- all_candidates_already_in_body
- mixed_reference_body_ownership
- no_renderable_candidate

Proof graph usage:
- all_candidates_proof_used
- mixed_proof_usage
- no_candidate_proof_dependents
- no_renderable_candidate

出力
====
- reference_entry_selection_ownership.csv
- reference_candidate_inventory.csv
- unresolved_reference_steps.csv
- selection_class_summary.csv
- ownership_class_summary.csv
- dependency_class_summary.csv
- unresolved_statement_type_summary.csv
- exception_inventory.csv
- reference_selection_ownership_summary.txt

実行
====
cd C:\Users\oomae\Dropbox\Python\fitz\ehp_proof

Remove-Item `
  ".\phase153_r3_2_reference_statement_selection_ownership_audit" `
  -Recurse `
  -Force `
  -ErrorAction SilentlyContinue

Expand-Archive `
  -Path "$HOME\Downloads\phase153_r3_2_reference_statement_selection_ownership_audit.zip" `
  -DestinationPath "." `
  -Force

powershell `
  -ExecutionPolicy Bypass `
  -File ".\phase153_r3_2_reference_statement_selection_ownership_audit\run_phase153_r3_2_reference_statement_selection_ownership_audit.ps1"

pytest
======
audit-only のためテスト追加・変更なし。
全体 pytest は Phase153 の最後にのみ実行する。

完了条件
========
- groups: 112
- exceptions: 0
- 全 Reference entry が selection class に分類される
- 全 Reference entry が ownership class に分類される
- 全 Reference entry が proof graph usage class に分類される
- unresolved statement type の内訳が得られる
- production behavior は一切変わらない

次 Phase との境界
================
R3-2 では事実の分類だけを行う。
R3-3 で、この監査結果を根拠に
「各 [Rn] に1つまたは最小集合として何を表示するか」の一般規則を確定・実装する。
本文重複の suppress は、その規則が確定してから最小限に行う。


Fixed1
======
初回 R3-2 監査では ownership と dependency の両方が
"no_renderable_candidate" という同じ分類名を使用していたにもかかわらず、
同一の Counter に加算していた。

そのため unresolved-only 28 entries が、
ownership 集計と dependency 集計の双方から加算されて 56 と表示され、
ownership partition check が失敗した。

Fixed1 では以下の Counter を分離した。
- selection_totals
- ownership_totals
- dependency_totals

分類ロジック、statement candidate 抽出、production code、既存 tests は変更しない。
