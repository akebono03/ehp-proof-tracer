# Phase157 R5-R10 repair8

## Production code

変更なし。

## テスト変更

### `tests/test_phase144_6_r3_production_references.py`

古い `(5.2)` 必須契約を Phase157 の reference relevance 契約へ更新。

### `tests/test_phase156_r5_repair9_test_contract_after_boundary_collapse.py`

nu-prime bracket definition の「出力全体から消える」契約を廃止し、

- Reference には存在する
- Proof body には重複しない

という現在の境界契約へ変更。

### `tests/test_phase153_r11_generic_reference_attribution_filtering.py`

`Proposition 5.6` という locator 自体を禁止するのではなく、

- root result `pi_6^3 = Z/4{nu'}` は Reference に自己参照されない
- earlier fixed group result `pi_5^2 = ...` は Reference として許可される

ことを確認する。

## Phase 境界

R10 の production 実装は追加変更しない。
focused test が通れば R10 完了とし、R11 の proof body relevance へ進む。
