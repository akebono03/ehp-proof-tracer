# Phase 163 R4 — 部分統合用 Bridge

## 最初に変更対象を列挙

- **新規** `phase163_r4_registry_bridge.py`
  - `MigrationStatus`, `MigrationRecord`, `RegistryBridgeResult`
  - `_reference_kind`, `build_registry_bridge`
- **新規** `audit_phase163_r4.py`
  - `main`
- **新規** `tests/test_phase163_r4_registry_bridge.py`
  - 9個の `test_*` 関数
- **新規** `run.ps1`

本 ZIP 内の Python ファイルとテストファイルは関数・クラス・import を省略しない全文。ルートへのコピー方式で追加する。既存ファイルの import やクラスは変更しない。

## 現行コードで確認した対象

- `proof.py`: `ProofStep`, `LiteratureReference`。
- `proof_repository.py`: `ProofRepositoryEntry`, `ProofRepository.entries()`。
- `standard_repository.py`: 引数から4件の標準的 ProofStep 登録を生成する。
- `theorem_facts.py`: `THEOREM_FACT_REPOSITORY`、出典 locator が欠け得る。
- `toda_literature_statement_boundary.py`: `_FIXED_COMPONENTS_BY_REFERENCE` と `TodaFixedStatementComponent`。`order` は証明完了順ではない。
- R2/R3の新規 API と軽量テスト。

## 実装の正確な範囲

1. Boundary Catalog の全列挙を ID 付きで読み取り、**metadata_only** として登録。
2. Theorem Fact Repository から locator のある typed statement を独立の識別子で登録。
3. locator が不明な theorem fact は **unresolved_source** として記録し、勝手に Toda の補題などと同一視しない。
4. 引数で渡された `ProofRepository` の全エントリを、typed conclusion と既存 `ProofStepLink` で登録。出典が確認できないため `proof_internal` とし引用可能とは扱わない。
5. 同一文献の複数 component 及び文献の種類を保持し、出典情報がないのに `available_after_position` を補わない。

**未実装：** `toda_rules.py` 全件の実行時登録の列挙、標準 Repository の自動生成、数学的意味での ID 統合、Definition の網羅、出典間の正規化、既存計算経路への統合。したがって R4 全体完了ではなく **R4 の部分的橋渡し**。

## 軽量検証

```powershell
python -m pytest -q tests/test_phase163_r2_unified_registry.py tests/test_phase163_r3_registry_validation.py tests/test_phase163_r4_registry_bridge.py
python audit_phase163_r4.py
```

局所環境で **26 passed**（R2 6、R3 11、R4 9）。全体 pytest は Phase 末尾まで行わない。

## 完了条件と次工程

今回の完了条件：既存 API の変更なし、metadata と typed assertion を混同しない、未解決を未解決として出力、軽量テスト PASS。

R4 続行条件：`toda_rules.py` と各 Registry の生成経路を追加監査し、全登録実体のカバレッジを計測する。完全な数学的命題の同一性は機械的な件数だけでは確定できない。

Phase 164 までは Backward Search への接続を行わない。
