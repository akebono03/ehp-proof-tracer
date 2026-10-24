# Phase 168 R3-41I — 共通 Renderer 固定基準監査

## 変更対象

実装ファイル、固定原文の変更なし。新規監査パッケージのみ追加する。

- `audit.py`: `digest`, `inspect_route_contract`, `summarize_comparison`, `render_report`, `run_audit`, `main` の全関数。
- `tests/test_audit.py`: 限定テスト6関数。
- `run.ps1`: Windows PowerShell 実行スクリプト。

## 実行

リポジトリ直下に ZIP を解凍し、次を実行する。

```powershell
powershell -ExecutionPolicy Bypass -File ".\phase168_r3_41i_renderer_closure_audit\run.ps1"
```

## 完了条件と区別

1. 限定 pytest PASS。
2. 3群の標準 Web Narrative を共通 Model から採取し、固定原文と全文比較する。
3. Reference ごとに本文の存在、本文中の参照番号の実際の使用状況を示す。
4. 基準の論証説明が欠ける場合は明記する。差分行数のみで数学的誤りと判定しない。
5. 実装と固定原文の SHA-256 が監査前後で同一である。
6. 全体 pytest は実行しない。

出力: `output/review_bundle.zip`。現時点での合格は「監査の正常終了」であり、「固定基準の全文品質達成」ではない。

R3-41H の有限巡回群導出経路の不足は、今回は対象外。後続の証明探索 Phase に引き継ぐ。
