# Phase 165 R57-R9 変更対象・コード全文

## 変更対象

本番コードのファイル・クラス・関数・メソッド：**なし**。

新規ファイル：`phase165_r57_r9_renderer_comparison/audit.py`（実行時のみ Renderer を差し替える監査）、`test_phase165_r57_r9_renderer_comparison.py`、`run.ps1`。

既存 API、既存テスト、数学的推論規則、Renderer の実装は変更しない。両 Python ファイルの全文は ZIP 内に省略せず収録した。

## pytest

```powershell
python -m pytest -q .\phase165_r57_r9_renderer_comparison\test_phase165_r57_r9_renderer_comparison.py
```

## 完了条件

本番 Web 入口から `π₅⁴` の `PartialProofResult` を取得し、同一結果に対する旧専用分岐あり・なしの Narratives と ProofStep 監査記録を生成する。

## 次段階との境界

実行中の専用表示分岐は本段階で削除しない。ProofStep の来歴と共通 Renderer の文章が数学的に同等と確認されるまでは削除禁止。
