# Phase 164 R4-R1 — 変更一覧

## 新規ファイル（既存の Production コードは変更しない）

1. `phase164_r4_r1_source_crosswalk.py` — リポジトリ直下に追加。`SOURCE_TARGETS`、`_ancestors`、`source_crosswalk`、`audit_current_repository`、`write_reports`、`main`。完全な import と実装は同梱ファイルに収録。
2. `tests/test_phase164_r4_r1_source_crosswalk.py` — `tests/` に追加。全テスト関数、必要な import を全文収録。
3. 配布用 `run.ps1`、`README.md`、`CHANGED_CODE.md`。

## 実行 pytest

```powershell
python -B -m pytest -q tests/test_phase164_r4_r1_source_crosswalk.py tests/test_phase164_r4_real_registry_audit.py tests/test_phase164_r3_registry_search_connection.py tests/test_phase164_r2_citation_eligibility.py
```

## 完了条件

- 2つの実際の文献由来 `ProofStep` の根拠候補となる source Statement ID を一意に特定。
- 誤った ID・原本転記の改竄・不足前提を拒否。
- 推論祖先の存在を確認し、数学的内容の同値性・原本版の確認・引用資格の許可は主張しない。
- 全体 pytest は行わない。

## 次の境界

R4-R2 以降では必要に応じて各出典の構造化主張を独立照合する。R4-R1 では `SOURCE_ARCHIVE` を `FIXED_STATEMENT` として昇格させず、ProofStep を生成しない。
