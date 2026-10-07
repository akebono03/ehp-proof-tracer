Phase 159 R1-7c R3 repair4 repair2
====================================

目的
----
前回の Phase157 failure は単なる heading 表記差ではなく、
current pi_6^3 public Reference から Equation 5.3 heading 自体が
見えないことが判明した。

この package は修正を行わない audit-only package。

確認するもの
------------
1. current pi_6^3 final public Narrative
2. final Reference headings
3. 5.3 / nu-prime を含む final lines
4. raw Reference entries
5. fixed-statement-boundary filter 後の entries
6. 各 proof step の:
   - inference rule
   - conclusion type
   - boundary classification
   - reference locator
   - component key
7. repair4 pruner を pi_6^3 に直接適用した結果
8. repair4 pruner が pi_6^3 で本当に no-op か

変更
----
Production code changes: none
Test code changes: none

出力
----
phase159_r1_7c_r3_repair4_repair2_pi6_reference_diagnosis/
audit_output/pi6_reference_diagnosis.txt

この診断結果を見てから、
- stale test repair
- existing Reference pipeline regression repair
のどちらかを決める。

repository-wide pytest は実行しない。
