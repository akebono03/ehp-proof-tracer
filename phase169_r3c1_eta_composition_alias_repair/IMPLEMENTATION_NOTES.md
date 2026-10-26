# Phase 169 R3C1 — 変更一覧と完了条件

## 修正対象

- `phase165_r12_r21_eta_generator_chain.py` のみ本番変更。R3C の実行失敗により元のコードへ復元された状態から適用する。
- import：`from expression import Composition, HomotopyElement` の追加。変更後の import 全文は `imports_full.py` および `full_files/` を参照。
- 新規 `_composition_eta_suspensions()`：既存 `suspension_to_generator_image_rule()` の直後に追加。今回の修正の中心となる関数全文は `full_functions/`。
- 新規 `composition_eta_suspension_image_rule()`：前述の新規関数の直後に追加。関数全文は `full_functions/`。
- 既存 `expand_cited_eta_generator()`：関数全文を置換。R3C 提案版と内容は同じだが、復元後の現行コードから見ると変更に当たる。関数全文は `full_functions/`。
- 既存の `_eta_pair()`, `eta_definition_to_suspension_rule()`, `suspension_to_generator_image_rule()`, `proof_has_cited_eta_general_ancestor()` は変更しない。
- 本番ファイル全体は `full_files/phase165_r12_r21_eta_generator_chain.py` に収録。
- `tests/test_phase169_r3c1_eta_alias_repair.py` を新規追加（テスト5件、import・補助関数全文）。R3C の既存テスト7件を新パッケージにも同梱。
- 実行・適用・復元用 `run.ps1`, `apply.py`, `restore.py`, `audit.py` は新規。既存本番テストやドキュメントは書き換えない。

## 修正理由

R3C の模擬テストは Toda の定義値だけを用いていたが、実際の DB 目標では η₂ の Unicode 下付き文字表記を用いるため、正規形とのオブジェクト比較が不一致となった。既存の `_matching_eta_name`（η の family/index/dimension/source/target に加え正規名を検証）により実際の四因子を検査し、証明上の前提は正規の η 系列の `GeneratorSuspension` に結び付ける。

## 限定 pytest

新規5件＋従来のR3Cテスト7件＋既存関連テストのみ。全体 pytest は実施しない。

## 完了条件

1. 実DBの π₄², π₅³ から得た GeneratorImage に対し2つの型付き懸垂前提が生成される。
2. 前提は引用された一般η系列定義からの `INFERENCE` として導出され、未証明 GIVEN は追加されない。
3. 実際の引用済みコンテキストで `image_search_status=proved` を確認する。監査に失敗した場合には本番変更を復元。
4. π₄² は完全を維持し、π₅³ の群構造全体や EHP 同型性を誤って完了扱いにしない。

次の R3D は EHP の同型性証明の不足前提を扱う。その他の機能を追加しない。
