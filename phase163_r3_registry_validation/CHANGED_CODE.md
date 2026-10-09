# Phase 163 R3 — 命題同一性・引用順序・依存関係

## 変更対象

- **新規** `phase163_r3_registry_validation.py`（プロジェクトルートへ追加）
  - `CitationDecision`, `IdentityDecision` — 判定 Enum
  - `CitationAssessment`, `DependencyAudit` — 結果 dataclass
  - `compare_assertion_identity()` — 主張同一性の保守的判定
  - `audit_dependencies()` — 未登録依存・循環依存の検出
  - `assess_citation()` — 引用利用可能性の3値判定
- **新規** `tests/test_phase163_r3_registry_validation.py`（既存 `tests` 内へ追加）
  - 11 個の軽量テスト。新規テスト関数の全文は当該ファイルに収録。
- **新規** `phase163_r3_registry_validation/run.ps1`（配布用実行ファイル）
- `proof.py`、既存 Registry、Renderer、R2 のデータ構造とテストは**変更しない**。
- `README.md`、`docs/design.md`、`docs/development_log.md`、`docs/roadmap.md`、`docs/proof_records.md` は**変更しない**。

## 既存コード・関連テストの確認

- GitHub `akebono03/ehp-proof-tracer` の現行 `proof.py`、`proof_repository.py`、`theorem_facts.py`、`toda_literature_statement_boundary.py` を確認。
- Phase 163 R2 配布済み `unified_statement_registry.py` と `tests/test_phase163_r2_unified_registry.py` の全文を確認。
- GitHub では R2 の新規ファイルが見つからないため、ローカルで R2 を適用済みであることを R3 実行前提とする。

## 判定契約と限界

- `IdentityDecision.SAME`: 同じ `assertion_id`。`DIFFERENT`: 型・由来、または内容が明示的に異なる場合。その他は `UNKNOWN`。**文字列が等しくても異なる ID を勝手に同一視しない**。
- 引用は `ALLOWED`, `DENIED`, `UNKNOWN` の3値。使用可は**同一の明示された `source_id`** かつ **引用先の証明完了位置が引用元の掲載位置より厳密に早い**場合に限る。
- `PROOF_INTERNAL` を外部文献から引用すること、自己引用、まだ利用可能でない文献内主張を拒否。
- 依存グラフに未登録 ID や循環があれば未確認。循環検出は登録済み主張の依存辺だけを対象とする。
- 文献間の先後関係、同じ掲載位置内の適用可能性、複数命題同時証明の正当性、数学的同値性は現時点で推定しない。
- R2 データ構造の公開列挙 API が未定義のため、監査は R2 の内部参照辞書を**読み取りのみ**で利用する。R4 の API 統合時に再検討する。
- 既存の Backward Search や Renderer とは未接続。新規コードを読みに行く既存経路はない。

## テスト

```powershell
python -m pytest -q tests/test_phase163_r2_unified_registry.py tests/test_phase163_r3_registry_validation.py
```

作成環境では **17 passed**（R2: 6、R3: 11）。全体 pytest は Phase 163 終了時まで実施しない。

## 完了条件

- 文献 ID と Assertion ID を区別したまま同一性を保守的に評価する。
- 証明完了位置が未確認なら引用可を推測しない。
- 自己引用・proof-internal の外部使用を防ぐ。
- 循環依存と未登録依存を検出する。
- R2 と R3 の軽量テストが PASS し、既存 API を変更しない。

## 次 Phase との境界

R4 は既存の分散 Registry を統一台帳に照合・移行する作業。一般的な Backward Search への組込みは Phase 164 に残す。R1 の数学的に異なる全命題数は依然として未確定。

## コードの全文

新規モジュールおよびテストは ZIP 内に**そのまま置き換え可能な全文**として収録。既存コードへの差分パッチはない。
