# Phase157 R5-R10 repair9

## Production code

変更なし。

## テスト変更

### `tests/test_phase144_6_r3_production_references.py`

public Reference では `Lemma 5.4` が Phase157 relevance pruning により除外されることを確認する。

### `tests/test_phase156_r5_repair12_reference_frontier.py`

内部 frontier のテストは変更しない。

public Reference の期待値のみ:

- `(5.3)`
- `Proposition 5.3`
- `Proposition 5.6`

へ更新する。

### `tests/test_phase156_r5_repair13_root_reference_frontier.py`

repair12 と同様に、内部 frontier 契約は維持し、
public Reference のみ Phase157 の relevance 契約へ更新する。

## Phase 境界

focused test が通れば R10 完了。
R11 で proof body relevance の本体へ進む。
