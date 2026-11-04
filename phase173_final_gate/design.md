# Phase 173 最終 Gate — 設計と判定条件

## 変更対象

本 ZIP は新規 `phase173_final_gate/` ディレクトリだけを追加する。既存のクラス・関数・import、数学的 `ProofStep`、推論規則、Web Renderer、Git index、主要5文書を変更しない。

- `gate.py`: 新規 `git()`、`validate_snapshot()`、`parse_pytest_summary()`、`write_report()`、`main()`。
- `run.ps1`: リポジトリ整合性と単一の Phase 末尾全体 pytest を管理。
- `tests/test_gate_contract.py`: 新規5テスト関数（パラメータを含め10ケース）。
- `README.md`: 英語の実行説明。

## 監査結果と残す境界

2026-11-04 に提出された4群の Web 表示文字列を確認した。

- `(n,k)=(4,8)`: $\pi_{12}^{4}\cong\mathbb Z/2$ の抽象群構造は検証済み、$\varepsilon_4$ を記名した群の証明は未完成、内部未解決 Goal 3件を表示上1件に集約。
- `(4,9)`: $\pi_{13}^{4}\cong(\mathbb Z/2)^3$ の抽象群構造は検証済み、記名生成元の証明は未完成、未解決 Goal 2件を表示上1件に集約。
- `(5,3)`: $\pi_8^5$ の記名群構造は未証明、証明ステップなし。
- `(4,4)`: $\pi_8^4$ は完成証明であり、Reference と `□` を保持。

R15R17-R3R5 では Flask の HTTP 出力4件が PASS したが、MathJax の pixel-level 表示は独立に検証されていない。文字列確認を画像検査と混同しない。

## Phase 終了テスト

`-DryRun` は全体 pytest を実行せず、Source Guard と限定テストのみ実行する。通常実行時、GitHub `develop` と一致するクリーンな追跡ファイル状態、監査済み15ファイルの Blob 同一性を検証した後、現行 `tests/` を **1回のみ**実行する。Phase 155 の退避済み audit-only テストは現行 `tests/conftest.py` の選別仕様どおり除外する。終了コード0と `N passed` の末尾サマリーを両方検査する。

テストの出力・判定結果は `%LOCALAPPDATA%/EHPProofTracerRecovery/phase173_final_gate/` に書き込み、Git worktree 内には保存しない。成功後に同じ HEAD で Gate を再実行しても、全体 pytest を重複実行しない。成功が出るまでは正式な Phase 終了を宣言しない。

## 次工程との境界

Phase 173 の正式 Closeout は、全体 pytest PASS の実測ログを確認し、文書5件へ結果を反映してから判定する。次 Phase の数学的導出・未完成群の証明一般化は今回の Gate に含めない。
