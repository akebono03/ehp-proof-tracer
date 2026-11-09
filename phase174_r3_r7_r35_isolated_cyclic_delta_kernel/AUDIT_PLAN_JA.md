# Phase 174 R3-R7-R35 — 一般的巡回核の隔離推論監査

## 変更対象

既存ファイル・クラス・関数・import・テストへの変更はありません。リポジトリ直下に新設する
`phase174_r3_r7_r35_isolated_cyclic_delta_kernel/` のみが対象です。

- `rule.py`：新規 `expression_coordinates()`、`conditional_inputs()`、
  `cyclic_delta_kernel_rule()`、`expand_cyclic_delta_kernel()`。
- `audit.py`：新規 `git()`、`blob_sha()`、`same_reviewed_blob()`、
  `verify_checkout()`、`inspect_isolated_frontier()`、`report()`、`main()`。
- `tests/test_rule.py`：一般推論の正例と異常系、検証済み前提の要求を確認。
- `tests/test_audit.py`：実際の R34 の出典付き生成元と Source Guard を確認。
- `tests/test_static_contract.py`：本番コード・出典の独立した静的監査。
- `run.ps1`：DryRun／通常監査／限定 pytest。

## 数学的契約

証明済みの独立した前提として $A=\mathbb Z\{g\}$、
$B=\mathbb Z/m\{h\}$、$f(g)=\pm h$ を持つ準同型 $f:A\to B$ に対して、
$\ker f=\langle mg\rangle$ を INFERENCE（推論）により導けます。

ここでは $f$ が Toda EHP の $\Delta$ 型であることも確認しますが、
$(q,n)$ や生成元名に専用の分岐は設けません。`Composition`（合成式）の始域と終域は
各因子の型から再帰的に決定します。

## 公開の境界

R34 の2件の出典付き GIVEN と、別の先行文献に由来する対角群の一般表示から
導く **独立の INFERENCE ProofStep** が必要です。

この Phase では共通 Provider を変更しません。監査で参照する `GoalExpansion` は
証明ではなく逆向き探索の提案です。テスト専用の `ProofStep` はユーザーの公開証明には
挿入しません。

## Gate と次工程

期待 Gate：
`PASS_R35_ISOLATED_COMPOSITE_KERNEL_RULE_AUDITED_PUBLIC_WIRING_PENDING`

R35 が PASS した後、R35R1 または次の工程で共通 Provider への接続、
対角群の具体化に対応する一般推論の検証、実際の核の ProofStep を確認します。
$\pi_{12}^7=0$ はまだ未証明です。全体 pytest は Phase 174 の最後にだけ実行します。
