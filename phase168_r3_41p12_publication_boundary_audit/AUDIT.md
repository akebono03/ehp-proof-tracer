# Phase 168 R3-41P12 — 文献順境界監査

## 対象

- 既存コードの確認：`web_group_proof.py`、`phase165_r55_nk_only_goal.py`、`phase166_r3t_goal_source_binding/goal_source.py`、`phase166_r3c_publication_order.py`、`phase165_r52_r16_web_citation_gate.py`、`phase168_r3_4_link_bridge.py`、`phase168_r3_3_proof_narrative_model.py`。
- 既存テストの確認：`phase166_r3t_goal_source_binding/test_connection.py`、R3-41O、R3-41N1。
- 変更対象：**新規監査パッケージのみ**。既存ソース・テストに変更なし。

## 監査方針

1. 公開 Web 経路の単一検索から、未選別 Bridge、選別済み Bridge、検索結果、Model、Renderer 出力を取得する。
2. 証明目標に対応する `citing_assertion_id` が一意に解決できるか調べる。
3. 使用された各 GIVEN に対して `precedes_citing_assertion()` を使用し、位置が実際に先行しているか検査する。
4. 目標の位置が不明な場合は `UNVERIFIABLE_TARGET` とし、証明済み扱いしない。
5. R3-41P11 の3群全文・Reference・Citation と比較する。

## 境界

GIVEN 出典と文献順を保証することは異なる。また、推論の matcher 検証は R3-41P10 の確認事項であり、本監査は再実行しない。証明書発行、Model API 変更、Renderer 変更は次段階に留保する。全体 pytest は Phase 終了時のみ実行する。
