Phase153-R3-3
Representative Reference Statement Selection Rule

目的
====
Reference entry に複数の renderable statement candidate がある場合に、
どの ProofStep を代表 statement として採用するかを一般規則として実装する。

今回の変更
==========
production:
- toda_group_proof_narrative_references.py

tests:
- tests/test_phase153_r3_3_reference_statement_selection.py

追加 API
========
select_toda_group_proof_narrative_reference_statement_steps(
  entry,
  candidate_steps,
  proof_edges,
)

一般規則
========
1. candidate_steps が空なら空 tuple。
2. proof graph 上で後続 step の premise として実際に使用される candidate があれば、
   それらだけを entry 内の順序を保って採用する。
3. proof-used candidate が複数あれば、異なる証明事実を落とさないため全て保持する。
4. proof-used candidate が1つもなければ、candidate_steps の先頭を代表として採用する。

candidate_steps は R3-1/R3-2 で確認した renderable candidate を呼び出し側が渡す。
この Phase では renderer 判定そのものを selection rule に混ぜない。

実装しないこと
==============
- Reference section への statement 表示
- unresolved 12 statement types の renderer 補完
- 本文側の重複 suppress
- group-specific / theorem-specific branch

対象テスト
==========
- 新規 selection rule tests
- structured reference regression
- production reference regression
- Phase153-R2 public reference semantic fact regression

全体 pytest は Phase153 の最後にだけ実行する。

完了条件
========
- single candidate をそのまま選択できる
- multiple candidates では proof-used candidate を優先できる
- 複数の proof-used candidate を entry 順で保持できる
- proof-used candidate がなければ先頭へ fallback できる
- 既存 Reference section の表示は変わらない

次 Phase との境界
================
R3-3 は selection rule の production API 化まで。
次段階でこの API を Reference section statement renderer に接続する。
