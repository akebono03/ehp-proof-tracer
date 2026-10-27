# Phase 169 R10E9 — η 合成生成元の型付き別名接続

## R10E8 の実測値

- `π_23^15`: `complete`、未解決なし、推論による生成元像10件。
- `π_24^15`: `partial`、GeneratorImage 2件・Relation 2件が残存。生成元像の推論22件。
- Web 表示の `π_22^13` も同じ 9-stem の η・ε 合成生成元を含み、未完成。

## 原因仮説と変更境界

`phase165_r12_r21_eta_generator_chain.py` の `_eta_pair()` は、引用から作った `TodaEtaFamilyDefinitionStatement.element` と DB の Unicode 添字を持つ `HomotopyElement` を `==` で比較している。同じ型付き η 元であっても、表示名が異なるため候補が得られない場合がある。

既存の `phase165_r12_r28_presentation_connection._matching_eta_name()` は、系列、添字、始域、終域、次元および既知の2形式の表記を照合する。これを `_eta_pair()` の照合に再利用する。推論規則、文献からの GIVEN、合成の2因子要求はすべてそのままとする。

## 変更一覧

- **変更ファイル**: `phase165_r12_r21_eta_generator_chain.py`
- **変更関数**: `_eta_pair()` 全体を置換。既存 import は変更しない。既存クラスは変更しない。
- **追加**: `phase169_r10e9_eta_composite_alias_fix/patch.py`, `audit.py`, `tests/test_r10e9_eta_composite_alias.py`, `run.ps1`, `README.md`, 本ファイル。
- **追加位置**: プロジェクト直下の新規監査パッケージ。既存の別関数・別 Phase の機能は変更しない。

`patch.py` の `OLD_FUNCTION` と `NEW_FUNCTION` に変更前後の関数全文を収録する。変更後は `_eta_pair_FULL.py` と対象モジュール全文を `output/` に出力する。参照する既存 import は変更しないため、既存 import 領域は対象モジュール全文にそのまま保持する。

## 完了条件

1. 変更対象モジュールの Git blob・既存差分・LF/CRLF を監査して安全に置換。
2. Unicode 添字の η に対し、引用からの特殊化2件と懸垂像の実推論を検証。
3. 無関係の記号・型・次元・写像の偽装を拒否。
4. 別の公理に依存せず、`η∘ε` の合成像が既存の「2因子とも INFERENCE」という規則に依存することを検証。
5. `π_22^13`, `π_24^15` を再探索し、未解決条件をそのまま記録。`π_23^15` を対照群として再探索。
6. 限定 pytest のみ実施。全体 pytest は Phase 169 終了時。

## 次 Phase との境界

R10E9 は証明木に対する生成元像の連結に限定する。Web Renderer の整形、Reference の表示方式、Trust Boundary の総合監査、文章の固定基準比較は次段階。`complete` の判定は検索結果に従い、監査コードから合成しない。
