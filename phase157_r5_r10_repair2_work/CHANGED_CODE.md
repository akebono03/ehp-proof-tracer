# Phase157 R5-R10 repair2

## 変更対象

- `web_group_proof.py`
  - `_build_group_proof_rendered_lines()` 内の separator 判定位置を display-math state より前へ移動。
- `tests/test_phase157_r5_r10_reference_proof_boundary_qed.py`
  - Reference 内の既存 `---` ではなく、`## 証明` 直前の `---` を検証。
  - separator parser の focused unit test を追加。

## Phase 境界

この repair2 では proof body relevance、statement selection、argument ordering は変更しない。
