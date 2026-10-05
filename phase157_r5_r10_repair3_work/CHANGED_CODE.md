# Phase157 R5-R10 repair3

## 変更対象

### `toda_group_proof_narrative_renderer.py`

変更する関数:

- `_finalize_toda_group_proof_narrative_markdown`
- `render_toda_group_proof_narrative_markdown`

変更内容:

- `## 証明` の直前を常に空行 + `---` + 空行に正規化する。
- `pi_6^3` を含む generic multi-argument route に
  `_wrap_phase150_rc4_generic_public_narrative()` を共通適用する。
- QED `$\square$` は既存 finalizer の規則を維持する。

### `tests/test_phase157_r5_r10_reference_proof_boundary_qed.py`

- `pi_6^3` で `使用する結果` / `証明` が明示されることを追加確認。
- Proof 直前の separator を確認。
- Web adapter で heading / separator / QED を確認。

## Phase 境界

Reference selection、statement relevance、argument ordering の修正は R10 には含めない。
