Phase157-R4-R3 repair1

前回の問題:
1. renderer の reference build block を3個と決め打ちしていたが、
   現行ファイルには2個しかなく apply が途中停止した。
2. generic body-usage filtering が、本文に [R] marker を持たない
   Lemma 5.13 の fixed statement を落としていた。

今回の変更:
- toda_group_proof_narrative_renderer.py
  - 現行の2つの reference build block に boundary filter を接続。
- toda_group_proof_narrative_references.py
  - representative groups について、
    generic proof graph で実際に使われている fixed reference を
    body-usage filtering 後に復元する helper を追加。
- toda_group_proof_narrative_contribution_renderer.py
  - body-usage filtering 前の fixed entries/statement lines を保持し、
    generic_used_step_ids に基づいて必要な fixed entry だけ復元。
- tests/test_phase157_r4_r3_repair1_reference_retention.py
  - pi_12^5 で Lemma 5.13 が残ること、
    Proposition 5.11 の proof-internal map facts は戻らないことを確認。

境界:
- representative 5 groups のみ。
- 112群全体への一般化は R5。
- repository-wide pytest は Phase157 closure まで実行しない。
