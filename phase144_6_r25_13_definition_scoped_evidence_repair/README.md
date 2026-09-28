# Phase 144-6 R25-13

## 変更対象

- `toda_group_proof_narrative_argument_multi_renderer.py`
- 関数 `render_toda_group_proof_narrative_multi_argument_markdown`

## 原因

`extract_toda_group_proof_narrative_argument_method_evidence` で取得した method evidence を、全 argument role の `local_body_blocks` に無条件で再投入していた。

この再投入は depth=2 で欠落していた definition を回復するためには必要だが、`ESTABLISH_ORDER` 等にも適用すると、本来 argument body の frontier 外にある evidence step まで contribution 候補に戻る。

## 修正

method evidence による `local_body_blocks` の拡張を `ESTABLISH_DEFINITION` の場合だけに限定する。

`semantic closure`、argument extraction、contribution renderer、既存 API は変更しない。

## Focused tests

- R25-13 ownership-boundary test
- Phase 144-6 R25-9b depth=2 nu-prime definition regression
- Phase 144-6 pi6 generic production route
- Phase 144-6 R5-43-11D final-completion focused audit

Phase 全体の pytest はここでは実行しない。
