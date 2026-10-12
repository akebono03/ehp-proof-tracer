# Phase 164 R2 — 変更対象と境界

## 新規ファイル

- `phase164_r2_citation_eligibility.py`（プロジェクト直下）
  - `EligibilityStatus`（新規 Enum）
  - `EligibilityResult`（新規 dataclass）
  - `assess_phase164_r2_citation`（新規関数）
- `tests/test_phase164_r2_citation_eligibility.py`（既存 tests ディレクトリ）
  - `make_bridge` と局所テスト関数一式
- `phase164_r2_citation_eligibility/run.ps1`（配布 ZIP 内）

新規関数・クラスの追加位置はすべて各新規ファイル内。既存ファイル・クラス・関数・import の変更はありません。新規 Python ファイルは ZIP 内に import を含め全文収録しています。コードの省略はありません。

## 実行する pytest

```powershell
python -B -m pytest -q tests/test_phase164_r2_citation_eligibility.py tests/test_phase163_r2_unified_registry.py tests/test_phase163_r3_registry_validation.py tests/test_phase163_r4_registry_bridge.py
```

## 完了条件

引用資格の自動承認が禁止され、明示検証・構造化・祖先依存・掲載順の条件が成立した場合に限り ALLOWED。既存局所テストを壊さない。Phase 164 全体 pytest は R5 のみ。

## 次の境界

R3 で `usable` の判定済み主張のみを既存 Backward Search に接続する。R2 は ProofStep 生成、証明再構築、Renderer を変更しない。
