# Phase 168 R2-8⑦ 実装・監査

- 変更対象：`phase165_r52_r16_web_citation_gate.py` の `screen_shared_proof_context()` 全体、および `phase168_r2_toda52_transport.py` の import と `_toda52_rule()` 全体。
- 追加：`phase168_r2_8_7_reference_binding/patch.py`、限定テスト3件、実行スクリプト。
- 出典：登録済み `assertion.reference_id` から引いた `LiteratureEntry.locator` を利用。文献順で許可された固定命題だけが GIVEN の対象。
- 旧い GIVEN リンクを選択する場合にも、許可された登録レコードに対応する出典を付与。既に文献参照が設定されている場合はそれを保持。
- Toda (5.2) の推論規則は原典照合済みの `Toda52UniversalStatement` を検査している。該当する (5.2) を `literature_reference` に結び付ける。
- 探索成功と Reference の表示成功を混同しない。`reference_trace.json` で `extracted_locator` と最終 Reference entries の両方を確認する。
- 共通 Renderer の文献除外規則や Narrative の抽象表現は今回変更しない。後続 R2-8⑧ で必要性を判断。
- 全体 pytest は Phase 168 の終了時のみ。
