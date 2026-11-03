# Phase 173 R4-R15R10 共通表示経路回帰監査

## 対象

GitHub `develop` HEAD `8bfa13946251c5618530641c572e8c756bb49af4` の現行コードを先に確認した。R15R9 の6行変更は GitHub に反映済み。

## 実装上の変更範囲

- 既存の本番ファイル：変更なし。
- 追加パッケージ：`phase173_r4_r15r10_common_route_audit/`。
- 新規クラス：なし。
- 追加関数：`audit.py` の `git_output`、`specialized_dimensions`、`preflight`、`inspect_partial`、`inspect_complete`、`main`。
- 新規テスト関数：`tests/test_contract.py` の4件。

## 必須回帰条件

1. 未完成群 $\pi_{12}^{4}$、$\pi_{35}^{4}$ の abstract certificate が共通 Web に1節だけ現れる。
2. 未解決 Goal があり、`generic-partial-proof` と `partial_result=True` を保つ。
3. 元の `status`、`conclusion`、`open_goals`、`references`、`proven_steps`、`diagnostics` を Web 表示によって変更しない。
4. 完成群 $\pi_6^3$、$\pi_7^4$ は `generic-complete-proof` を維持し、抽象節を追加しない。
5. 共通 Adapter と抽象群表示関数に `n`、`k` の数値定数による専用分岐を追加しない。
6. `trace` は従前どおり追加 Narrative を持たない。

## 監査で判明する設計境界

現在の `ProofNarrativeModel` に `abstract_structure` はない。共通 Web Adapter の共通フックは存在するものの、抽象群の `ProofStep` に付く出典は、従来の `model.steps` から作成した Citation 一覧へ自動的には統合されない。この差異は完了判定を変更せずに記録する。将来の共通 Model 統合に必要な検討事項であり、今回の監査では新たな Renderer・推論規則・記名生成元の等式を増やさない。

## 完了条件と次工程

- DryRun が PASS。
- 限定 pytest が PASS。
- 4群の通常 Web 実行に対する `regression_report.json` が `passed: true`。
- 本番ファイル変更がゼロ。

これは R15R10 の完了条件であって Phase 173 全体の完了条件ではない。次工程は監査結果を踏まえて共通 Narrative Model のデータ所有境界を設計し、数学的に未証明の生成元対応には文献出典付きの別の推論研究を行う。
