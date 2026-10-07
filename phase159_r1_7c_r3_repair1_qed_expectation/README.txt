Phase 159 R1-7c R3 repair1
============================

原因
----
R3 production output は正しい。

実際の末尾:
□

R3 の新規 test だけが旧表現:
$\square$

を期待していた。

Phase 158-R5-6 では public Narrative の terminal QED contract は
literal "□" に統一済みであり、GitHub 現行 tests でも

rendered.rstrip().endswith("□")

が使用されている。

変更
----
Production code changes: none

変更ファイル:
tests/test_phase159_r1_7c_r3_known_result_direct_premise_specialization.py

変更 test function:
test_phase159_r1_7c_r3_pi11_4_renders_i11_decomposition_specialization()

変更前:
  assert body.rstrip().endswith(
    r"$\square$"
  )

変更後:
  assert body.rstrip().endswith(
    "□"
  )

Phase boundary
--------------
- R3 の direct-premise specialization logic は変更しない。
- pi_11^4 public Narrative の4段階の証明構造は変更しない。
- repository-wide pytest は実行しない。
