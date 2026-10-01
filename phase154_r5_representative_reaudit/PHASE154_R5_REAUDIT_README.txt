Phase 154-R5 Representative Re-audit

目的
----
R5 Fix1 / Repair1 / Repair2 / Repair3 後に、5代表群で
Reference ↔ proof body linkage の残存問題がないか横断監査する。

対象
----
- pi6_3
- pi10_4
- pi11_4
- pi12_5
- pi16_9

条件
----
- Narrative
- depth 2

production changes
------------------
なし。

監査項目
--------
1. linked marker:
   [R#]より、...

2. neutral marker:
   [R#]を用いる。

3. neutral marker のうち、Proof graph 上で一意な visible non-root consumer
   が存在するもの:
   residual linkage candidate

4. incomplete marker:
   [R#] を含むが、linked / neutral の完全な文になっていない行

判定
----
- neutral marker はそれだけでは欠陥としない。
- unique visible non-root consumer がない neutral marker は正常。
- residual linkage candidate が 1件でもあれば R5 はまだ閉じない。
- incomplete marker が 1件でもあれば R5 はまだ閉じない。

R5 完了条件
-----------
- residual_linkage_candidates = 0
- incomplete_reference_marker_lines = 0

focused pytest
--------------
R5 Fix1 / Repair1 / Repair2 と R2/R4/R8 の current-contract tests を実行する。

全体テスト
----------
実行しない。Phase 154 の最後にのみ実行する。

次の境界
--------
R5 完了なら Phase 154-R6 punctuation normalization へ進む。
