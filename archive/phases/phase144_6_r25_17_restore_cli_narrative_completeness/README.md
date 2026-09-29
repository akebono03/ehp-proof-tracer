# Phase 144-6 R25-17 Restore CLI Narrative Completeness

## 変更対象

- `toda_group_proof_narrative_argument_body_renderer.py`
  - 不採用 R25-16 を rollback するだけ。
- `main.py`
  - `_run_group_proof_command`
  - R24 で導入済みだった CLI Narrative completeness boundary を復元する。

## 設計

`--depth` で作られた replay は変更しない。
Trace / Outline は従来どおり depth 制限された replay を使う。

Narrative は数学的な導出文を途中で切断すると connector や結論が欠落するため、
`mode="narrative"` かつ depth 指定時には、Narrative presentation だけを full replay
から構築する。

semantic closure は R25-9B の契約どおり definition endpoint 以外を追加しない。

## Phase 境界

R25-17 focused tests が通ったら新規監査を増やさず、
Phase 144-6 最後の full pytest へ進む。
