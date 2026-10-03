# Phase157 R11-R11 repair4

## 変更対象

### toda_group_proof_narrative_references.py

変更関数:
- select_toda_group_proof_narrative_reference_statement_steps()

変更:
- used candidate 判定を ProofStep identity のみに依存させない。
- proof edge で実際に使われた premise と同じ conclusion を持つ candidate も used とみなす。

### toda_group_proof_narrative_contribution_renderer.py

新規関数:
- `_phase157_r11_reference_statement_match_key()`
  - 追加位置: `suppress_toda_group_proof_narrative_reference_body_duplicates()` の直前。

変更関数:
- `suppress_toda_group_proof_narrative_reference_body_duplicates()`

変更:
- standalone statement 比較時に `\tag{N}` と末尾句読点を無視。
- 表示では tag を保持して `[R#]より` を付ける。

### tests/test_phase157_r11_reference_reason_punctuation.py

- tagged Hopf derivation expectation に更新。
- (5.3) の double relation / Hopf relation が双方 Reference に残る regression test を追加。

## Phase 境界

R11 の Reference usage / proof dependency 表示だけ。
全体 pytest は Phase157 closure まで実行しない。
