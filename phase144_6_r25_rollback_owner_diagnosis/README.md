# Phase 144-6 R25 — R24 rollback + owner diagnosis

このパッケージは R24 で追加された production の2変更だけを rollback し、その後に残る2件の regression の ownership を診断します。

## Production rollback

対象は次の2点だけです。

1. `main.py`
   - `depth` 指定 Narrative だけ complete replay を再構築する R24 分岐を削除し、R24 前の `replay` をそのまま presentation に渡す形へ戻す。

2. `toda_group_proof_narrative_argument_multi_renderer.py`
   - R24 で削除した direct-premise の premise protection を復元する。

これ以外の production 修正は行いません。

## Diagnosis

`diagnose_phase144_6_r25.py` は production を変更しません。

`pi_6^3` について depth=2 と full/default presentation を別々に構築し、次を step identity (`id(ProofStep)`) 単位で出力します。

- Argument role 一覧
- definition block の ProofStep
- definition step を含む Argument
- definition step の contribution owner
- definition step が最終 Narrative に実際に現れるか
- `pi_5^3` を含む supporting ProofStep
- その Argument owner
- contribution owner / role / placement / provider keys
- premise / parent edge
- contribution 全体の owner 一覧
- 最終 Narrative

## Boundary

この R25 は原因診断で停止します。

診断結果を見ずに frontier, contribution selection, suppression, renderer の追加修正は行いません。
全体 pytest も実行しません。
