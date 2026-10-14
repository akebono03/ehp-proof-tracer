# Phase 165 R57-R1 入口統一・削除前監査

## 対象と変更
- `web_group_proof.py` の `build_standard_web_group_proof_view()` を関数全文置換。トップレベル import は変更しない。
- `phase165_r57_r1_renderer_inventory.json` は呼び出し元一覧を生成する監査出力。
- 新規 `test_phase165_r57_r1_single_entry.py` は3テストを含む。
- 統一済みの R55 検索と R56-R2 公開 Narrative Renderer は変更しない。

## 削除を保留した理由
`render_toda_group_proof_generic_proof_markdown` 等の低層処理を含むファイルを一括削除すると、公開 Renderer が依存する共通関数まで失う危険がある。未完成証明は現在も `render_toda_partial_proof_narrative_markdown` を使う。未完成の入力契約を公開 Renderer に接続し、すべての利用者・テストを移行してから物理削除する。

## 次の境界
未完成証明の共通 Presentation への移行、他の公開入口の完全調査、旧関数・群別分岐の物理削除は未実施。検索不成功を証明完成へ昇格させない。全体 pytest は Phase 最後のみ。
