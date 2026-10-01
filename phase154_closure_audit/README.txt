Phase 154 Closure Audit

目的
----
Phase 154 で扱った Narrative prose refinement の全カテゴリを、
Phase 最終 full regression の前にまとめて監査する。

production 変更
---------------
なし。

既存 test 変更
--------------
なし。

母集団
------
- n = 2..15
- k = 0..7
- 112 groups
- Narrative depth = 2
- public Narrative renderer

Phase 154 categories
--------------------
1. transition repetition
   接続語・導出 transition の重複再発を確認。

2. semantic duplication
   同じ final reason の重複や、
   `である.を用いる.` のような壊れた sentence composition を確認。

3. internal fallback leakage
   inference-rule name / statement type-name fallback が
   public Narrative に露出していないことを確認。

4. English prose
   `\text{ is injective}` / `\text{ is exact}` 等が
   public Narrative に残っていないことを確認。

5. Reference ↔ proof-body linkage
   - Reference numbering contiguous
   - duplicate title なし
   - root Reference を外部 Reference として表示しない
   - body marker が displayed Reference に解決
   - marker-bearing route で unused Reference なし

6. Argument / Contribution ordering
   - Reference section は Proof section より前
   - section heading の重複なし
   - Phase 149 ordering regression を再実行

7. punctuation
   - Japanese comma `、` = 0
   - Japanese period `。` = 0
   - all 112 groups に ASCII comma prose が存在
   - all 112 groups に ASCII period prose が存在

focused regression
------------------
Phase 154 R2 / R4 / R5 / R6 の全 current tests を実行する。

boundary regression
-------------------
Phase 154 の前提になっている:
- Phase 149 ordering
- Phase 150 reason prose

の focused tests も再実行する。

full test suite
---------------
この package では実行しない。

全体 test は Phase 154 の最後にだけ実行する。

audit output
------------
- audit_output/summary.txt
- audit_output/violations.csv
- audit_output/exceptions.csv

完了条件
--------
- Phase 154 focused regression PASS
- ordering / reason regression PASS
- scanned groups = 112
- rendered groups = 112
- exceptions = 0
- violations = 0
- 7 categories の violation count がすべて 0
- groups with ASCII comma prose = 112
- groups with ASCII period prose = 112

PASS 後
-------
1. Phase 154 documentation closure
2. Phase 154 final full regression

FAIL の場合
-----------
production をその場では変更しない。

`violations.csv` / `exceptions.csv` を基に、
Phase 154 closure repair として原因を1カテゴリずつ最小修正する。
