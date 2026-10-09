# Phase 163 R4-R2 変更説明

## 変更対象

- 新規 `phase163_r4_r2_coverage_audit.py`: `call_name`、`literal_keyword`、`inspect_source`、`scan_root`、`summarize`、`audit`。クラス追加なし。
- 新規 `tests/test_phase163_r4_r2_coverage_audit.py`: 5個の軽量テスト。
- 新規 `run.ps1`: コピー・focused pytest・監査報告作成。
- 既存ファイル `proof.py`、`toda_rules.py`、各 Repository、Renderer は変更しない。

## 追加位置

プロジェクト直下に Python ファイルを追加。テストは `tests/` に新規追加。
いずれも import と関数本体を省略せず、ZIP 内のファイルが全文となる。

## 監査条件と制限

- AST によるルート直下 Python ファイルの候補抽出。実際の登録数や数学的全命題数には換算しない。
- R4 の既存 Bridge を読み取り、状態別の数を別集計する。
- 文献境界の `metadata_only` を構造化された数学的主張として数えない。
- 定義候補、事実 Entry、`ProofRepositoryEntry`、Factory の静的候補を列挙する。
- 同一性・汎用/特殊化・出典・定義文献・利用可能時点は引き続き未検証。
- `sites.csv` の `mapping_status=not_verified` は未照合を表し、未登録と断定しない。
- R4-R2 は対象の完全な統合ではなく、欠落を可視化する監査である。

## 実行

```powershell
cd C:\Users\user\Dropbox\Python\fitz\ehp_proof
Expand-Archive -Path "$HOME\Downloads\phase163_r4_r2_coverage_audit.zip" -DestinationPath "." -Force
powershell -ExecutionPolicy Bypass -File ".\phase163_r4_r2_coverage_audit\run.ps1"
```

Focused tests: `python -m pytest -q tests/test_phase163_r4_r2_coverage_audit.py tests/test_phase163_r4_registry_bridge.py`.

完了条件: 実行が成功し、`phase163_r4_r2_output/report.md`、`sites.csv`、`summary.json` が保存され、エラーと未検証事項が表示されること。

Phase 境界: この監査で全命題同一性・引用可能性・R4 完全移行は確定しない。全体 pytest は Phase 163 最終段階でのみ実施する。
