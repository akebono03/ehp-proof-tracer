# R52R1 最小修正・事前監査

## 現象と原因

R52 本監査が `R52 changed the public root expansion` で停止した。`GoalExpansion` に格納された `InferenceRule.match_guard` は Provider 呼び出しごとに別の関数オブジェクトになるため、dataclass 全体を `==` で比較すると偽陰性が生じる。R52 `audit.py` の根候補比較と `tests/test_probe.py` の3つの比較が該当する。

## 変更ファイル・対象

- `phase174_r3_r7_r52_public_kernel_source_bound_probe/audit.py`: `inspect_public_kernel_source_bound_probe` 全体。
- `phase174_r3_r7_r52_public_kernel_source_bound_probe/tests/test_probe.py`: `proposal_contract` 新規追加（最初のテストの直前）、`test_generic_wrapper_adds_only_cited_r35_kernel_obligation` 全体、新規 `test_generated_rule_closure_identity_does_not_change_root_contract`（その次）、既存の残りテストは変更なし。
- R52R1 新規監査専用ディレクトリ: `patch.py`, `run.ps1`, `tests/test_patch.py` と文書。

`match_guard` や `conclusion_builder` は再生成される callable のため比較しない。代わりに規則の型・名前・説明・前提パターン・結論パターン・文献参照・Subgoal を比較する。規則の検証自体は既存エンジンに委ねる。

GitHub `develop` HEAD `0d0b6b31582ff3e505d14fdde5eaf5e9a0b343d7`、`proof.py` の `InferenceRule` dataclass と R3 零根ルール、R52 ZIP の現行監査・テストを確認した。

## 完了条件

Source Guard、DryRun、修正済み R52 本監査、R52 の限定回帰テスト、R52R1 のパッチテストが PASS。`probe_status` が未完成ならそのまま障害を記録し、成功を偽装しない。全体 pytest は Phase 174 最終段階にのみ実施。

## 次 Phase との境界

R52R1 は監査の比較修正のみ。R53 における本番 Provider 導入や Web route の変更は含まない。
