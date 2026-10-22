# Phase 168 R2-8②：pytest 収集衝突の修正

## 原因

R2-8①と R2-8② の双方に `tests/test_audit.py` があり、同時収集時に `import file mismatch` が発生した。監査本体が実行される前の収集エラーであり、数学的照合の失敗ではない。

## 変更ファイル・位置

- `phase168_r2_8_2_structured_generator_audit/run.ps1`：スクリプト全文を更新。既存の R2-8② 用 `tests/test_audit.py` だけを削除し、固有名のテストと R2-8① テストを `--import-mode=importlib` で実行する。
- `phase168_r2_8_2_structured_generator_audit/tests/test_phase168_r2_8_2_structured_comparison.py`：旧テスト4関数を変更なしで移設。
- `phase168_r2_8_2_structured_generator_audit/README.md`・`AUDIT.md`：全文更新。

既存 production code と R2-8① のテストは変更しない。`audit.py` も変更しない。不要な __pycache__ 全体削除は行わない。

## 実行する限定テスト

```powershell
python -m pytest -q --import-mode=importlib phase168_r2_8_2_structured_generator_audit/tests/test_phase168_r2_8_2_structured_comparison.py phase168_r2_8_1_citation_mismatch_audit/tests/test_audit.py
```

その後に `python -m phase168_r2_8_2_structured_generator_audit.audit` を実行して9対象の JSON を生成する。Phase 168 終了までは全体テストを実行しない。

## 完了条件と次の境界

8件の限定テストが通り、`output/structured_comparison.json` が生成されること。R2-8③の生成元同一性判定や命題の特殊化はこの修正に含めない。
