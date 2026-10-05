# Phase157 R5-R10 repair4

## 変更対象

### `toda_group_proof_narrative_renderer.py`

変更する関数:

- `_phase153_r3_10_connect_public_reference_section`
- `_wrap_phase150_rc4_generic_public_narrative`

変更内容:

- specialized route の wrapper が `## 証明` の直前に `---` を必ず出力。
- generic route の wrapper が `## 証明` の直前に `---` を必ず出力。
- generic wrapper が `pi_6^3` の legacy intro
  `使用する結果を先にまとめる.` を受理して正式な section heading に置換。

### `tests/test_phase157_r5_r10_reference_proof_boundary_qed.py`

- 代表群で Reference/Proof の境界を確認。
- `pi_6^3` の legacy intro が public output に残らないことを確認。
- Web adapter の separator / heading / QED を確認。

## Phase 境界

proof body relevance、Reference selection、argument ordering は変更しない。
