# Phase 165 R6 終了前の限定検証

## 変更対象
新規 `phase165_r6_final_gates/check.py`、`run.ps1`、`README.md` のみ。既存の production code、クラス、関数、テスト、baseline は変更しない。

## 内容
- 既存の R3 architecture guard、R4 golden baseline、R57 public route の3ファイルを個別に pytest。各90秒の上限。全体 pytest は行わない。
- Web route に `(n,k)=(2,1),(3,1)` を与えて公開 `WebGroupProofView` の状態・ステップ数・表示行数・テキストを記録。
- Git の変更一覧を読んで保存。直近の旧テスト撤去 report があれば歴史的件数のみ記録。
- 結果は `phase165_r6_audit_results/final_gates/report.json`。各テストログと2群のテキストが同ディレクトリに出力される。

## 実行
`powershell -ExecutionPolicy Bypass -File .\phase165_r6_final_gates\run.ps1`

## 完了条件と境界
本パッケージが PASS しても R6 完了とはしない。全体 collection error = 0 の最終確認、旧経路依存と実ブラウザー MathJax の確認は別途必要。全体 pytest は Phase 165 の最終段階だけに実施する。旧機能の削除・新機能追加は一切行わない。
