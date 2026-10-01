Phase153-R3-11
Reference/Body Ownership Repair

目的
====
Phase153-R3-8 で確認した exact body duplicate 149件を、
Reference/body ownership の一般規則で解消する。

R3-8 classification
====================
- embedded_without_reference_marker: 146
- standalone_line: 3
- total: 149

変更対象
========
production:
- toda_group_proof_narrative_contribution_renderer.py

変更する関数:
- suppress_toda_group_proof_narrative_reference_body_duplicates

tests:
- tests/test_phase153_r3_11_reference_body_ownership_repair.py

一般規則
========
selected Reference statement は Reference section が primary owner。

本文側:
1. exact standalone duplicate
   -> 削除する。

2. 同じ [Rn] marker と exact selected statement を含む行
   -> 既存どおり "[Rn]を用いる。" へ compact する。

3. [Rn] marker を持たないが exact selected statement を含む行
   -> statement substring だけを [Rn] へ置換する。
   -> 接続語、理由文、後続文は保持する。

4. similar / semantic-equivalent だが文字列が異なる文
   -> suppress しない。

例
==
before:
  この結果として、$E: A \xrightarrow{\cong} B$を得る。

after:
  この結果として、[R2]を得る。

今回しないこと
==============
- semantic-equivalence 判定
- paraphrase suppression
- Reference selection rule
- Reference renderer
- proof graph
- full pytest

完了条件
========
112 groups 全体について:
- exact selected-statement duplicates in public proof body = 0
- Reference section の statement は保持
- nonidentical statement は保持
- R3-3〜R3-10 targeted regression tests PASS

次 Phase との境界
================
R3-11 は exact ownership repair まで。
次は 112-group Reference regression re-audit を行い、
R3 closure 条件を確認する。
