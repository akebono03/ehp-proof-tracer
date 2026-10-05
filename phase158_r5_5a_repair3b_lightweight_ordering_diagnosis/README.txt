Phase 158-R5-5a repair3b — lightweight ordering ownership diagnosis

目的
----
repair3 の ordering ownership diagnosis は focused test 3件を PASS したが、
本診断時の巨大な object repr 出力が重かった。

repair3b では診断対象と層を維持しつつ、
TodaGroupProofNarrativeArgument などの再帰的 repr を完全に廃止する。

変更対象
--------
新規追加のみ:

- phase158_r5_5a_repair3b_lightweight_ordering_diagnosis/audit_phase158_r5_5a_repair3b.py
- phase158_r5_5a_repair3b_lightweight_ordering_diagnosis/test_phase158_r5_5a_repair3b.py
- phase158_r5_5a_repair3b_lightweight_ordering_diagnosis/run_phase158_r5_5a_repair3b.ps1
- phase158_r5_5a_repair3b_lightweight_ordering_diagnosis/README.txt

Production code changes
-----------------------
なし。

既存 test code changes
----------------------
なし。

診断対象
--------
- pi_7^4
- pi_15^8

Public scope
------------
実際の Web と同じ:

build_standard_web_group_proof_view(
  n,
  k,
  max_depth=2,
  mode="narrative",
)

出力する情報
------------
1. public body の表示行
2. semantic block:
   - block index
   - role
   - dependency block indices
   - contained statement types
   - generic rendered text
3. generic block proof order
4. lightweight narrative argument:
   - argument index
   - role
   - supporting block indices
   - conclusion block index
   - child argument indices
   - supporting/conclusion statement types
5. presentation edge:
   - premise block
   - parent block
   - premise index
   - premise/parent statement type

削除する重い出力
----------------
TodaGroupProofNarrativeArgument の repr 全体を出力しない。

ProofStep / block / presentation object の再帰的 repr も出力しない。

Phase boundary
--------------
audit/diagnosis のみ。

production renderer、presentation、proof data、semantic model は変更しない。
R5-5b の実装修正を先取りしない。

pytest
------
focused lightweight diagnosis tests のみ。

repository-wide pytest は Phase 158 の最後にのみ実行する。

完了条件
--------
1. focused tests が PASS する。
2. pi_7^4 と pi_15^8 の診断が最後まで完了する。
3. object の巨大な recursive repr を出力しない。
4. public body / semantic block / proof order / argument / edge を照合できる。
5. production code を変更しない。
