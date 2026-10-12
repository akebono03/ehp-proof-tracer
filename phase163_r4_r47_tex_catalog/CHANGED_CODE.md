# Phase 163 R4-R47 変更一覧

## 新規ファイル

- `phase163_r4_r47_tex_catalog.py` — 独立した TeX 環境登録カタログの生成・検証・保存。
  - `require`, `digest`、`build_catalog`、`enforce_compatible`、`write_catalog`、`main` を新規追加。
  - 既存の `UnifiedStatementRegistry` のクラス・メソッドや import は変更しない。
- `tests/test_phase163_r4_r47_tex_catalog.py` — 限定テスト9件。import を含む全文。
- `run.ps1` — 既存 R4-R42〜44 出力を参照して限定 pytest と登録処理を実行。
- `README.md` — 英語の実行説明・制約。
- `CHANGED_CODE.md` — 本ファイル。

## 生成するファイル（プロジェクトの実行時）

- `phase163_r4_r47_output/catalog.json` — TeX 本文、章・掲載順、既存参照、登録状態の保存先。
- `phase163_r4_r47_output/catalog.csv` — 検査・閲覧用一覧。
- `phase163_r4_r47_output/report.md` — 日本語の実行報告。

## 限定テスト

`python -m pytest -q phase163_r4_r47_tex_catalog/tests/test_phase163_r4_r47_tex_catalog.py`

ローカルの単体テスト結果：9 passed。さらにアップロードされた5章の TeX と既存監査結果から108件の生成、繰り返し保存の整合性を検証した。ユーザー環境の Registry 接続と書き込み完了は `run.ps1` の結果で判定する。

## 完了条件

1. TeX 抽出108環境の取りこぼしがない。
2. 既存23 Reference と67 Assertion の識別子を維持する。
3. 66件の新規参照番号は候補に留め、番号未解決19件に架空の文献番号を与えない。
4. `TEX_REGISTERED` と `STRUCTURED`、`SOURCE_VERIFIED` を独立管理する。
5. SHA-256 や ID の矛盾、無断の再番号付けを検出する。
6. 既存 Registry、証明探索、TeX 原稿を変更しない。

## 次工程との境界

今回の登録先は独立 JSON カタログであり、本番 Registry への新規 Reference/Assertion 追加は行わない。R4-R48 以降で未抽出の定義等の範囲を監査し、参照番号の確定や統合方式を段階的に扱う。全体 pytest は Phase 163 最終時のみ実施する。
