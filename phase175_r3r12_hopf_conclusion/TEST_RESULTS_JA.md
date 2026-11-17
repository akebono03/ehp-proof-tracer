# Phase 175 R3R12R5 — 限定テスト・実行記録

## 変更前の確認

- R3R12R4 の Windows DryRun・本実行 Gate：PASS。
- 限定 pytest：52 passed。
- 公開証明：complete、generic-complete-proof、Trust True、Reference 7件、Lemma 5.4 非使用、最終結論1件。

## 今回の表示修正

一般 Hopf lift の検証済み写像を用いて、次の2つを同じ書式で表示する。

- `よって, $H: \pi_{7}^{3}\to \pi_{7}^{5}$ は全射.`
- `よって, $H: \pi_{7}^{3}\to \pi_{7}^{5}$ は同型.`

写像の数字はテストでの実例であり、生成コードに固定しない。

## 作成環境での検証

- インストーラー限定 pytest：**6 passed**。
- Python 構文検査：PASS。
- 既存の前提検証と書式を利用する表示テスト：実際の Windows リポジトリでの本実行対象。
- ZIP 整合性：梱包後に検査。

## 未実施の検証

Windows における限定統合 pytest・Web Group query はユーザー本実行で確認する。全体 pytest は Phase 175 終了時まで実施しない。

期待最終 Gate：`PASS_R3R12R5_VERIFIED_HOPF_MAP_DOMAIN_CODOMAIN`。
