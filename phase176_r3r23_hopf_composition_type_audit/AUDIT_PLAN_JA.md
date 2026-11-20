# Phase 176 R3R23 監査計画

## 目的

Toda Proposition 2.2 の右合成公式について、左因子が合成式の場合の型付き構文制約を監査する。

## 変更一覧

新規ディレクトリ `phase176_r3r23_hopf_composition_type_audit/` のみ追加する。既存コード・既存テスト・群構造の GIVEN は変更しない。

- `audit.py`: `inspect_source`, `git_state`, `inspect_runtime`, `report_path`, `execute`, `main` を追加。
- `tests/test_audit.py`: 3つの限定テストを追加。
- `run.ps1`: DryRun と本実行を用意。
- `README.md`: 英語の説明文。
- `AUDIT_PLAN_JA.md`、`CODE_FULL_JA.md`: 日本語の監査・実装全文。

## 監査範囲

1. `expression_endpoints` と `Composition.is_type_compatible` の違い。
2. 合成の結合律を扱う既存の `GeneratorImage` 専用規則。
3. 出典付き右合成公式 `_formula_parts` の型制約。
4. 一段の合成に対する既存公式が引き続き認識されること。

## 完了条件

DryRun と本実行が PASS し、限定 pytest が PASS すること。群構造の証明完成とは別である。全体 pytest は Phase 終了時まで行わない。

## 次段階との境界

R3R24 で検討しうる一般化は、合成式の型付き正規化を出典付き公式の特殊化に適用するもの。ただし既存の `GeneratorImage` 結合律規則を無条件に Hopf 関係へ流用してはならない。
