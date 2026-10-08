# Phase 161-R4-R5 repair14 changed code

## 変更対象

### `toda_group_proof_narrative_references.py`

変更関数:

- `build_toda_group_proof_narrative_reference_entries()`

変更後関数全文:

- `output/build_toda_group_proof_narrative_reference_entries.py.txt`

import 変更なし。

## 新規テスト

- `tests/test_phase161_r4_r5_repair14_reference_locator_dedup.py`

必要 import を含む全文:

- `output/test_phase161_r4_r5_repair14_reference_locator_dedup.py.txt`

## 根本原因

Reference は最初に生成されているが、同一 Reference の判定が

```python
references.index(reference)
```

による `LiteratureReference` の完全一致だった。

そのため locator がともに `Proposition 5.1` でも metadata が異なると、

- higher eta component
- finite-dimensional aggregate

が別々の Reference entry になる。

一方、同じファイルにはすでに

```python
_same_toda_group_proof_literature_reference()
```

が存在し、locator が一致する場合は同じ文献 Reference と判定する。

## 修正

`build_toda_group_proof_narrative_reference_entries()` で既存 entry を探す際に
この semantic identity（意味上の同一性）を使う。

これにより Reference を作る最初の段階で Proposition 5.1 を1件へ統合する。

## 完了条件

初期 Reference entries で:

- `Proposition 5.1` は1件だけ
- その `proof_steps` に higher-eta component と aggregate の両方が入る

public Narrative で:

- `[R1] (5.2)`
- `[R2] Proposition 5.1`
- Proposition 5.1 一般形は Reference のみに表示
- `[R2]` は具体的 $\pi_4^3$ に付く
- $\pi_4^2$ の結論と `□` を維持

## 次 Phase との境界

今回変更しない:

- `これより, 以上より,` の prose normalization
- Web Provenance header
- $\pi_5^3$
- $\pi_6^4$
- Phase157 $\pi_6^3$ known regression
- documentation
- 全体 pytest

repair14 が通った後、repair9a〜13 のうち不要になった実験的処理は
R4 closure 前に整理する。
