# Phase 159 pi3_2 visible dependency topological ordering repair2

## 変更対象

- `toda_group_proof_narrative_contribution_renderer.py`
  - 変更関数:
    `order_toda_group_proof_narrative_visible_step_dependencies()`
- `tests/test_phase159_pi3_2_visible_dependency_topological_order.py`
  - テストファイル全文を更新
- `audit_phase159_pi3_2_branch_continuity.py`
  - 新規監査スクリプト

## import

production code の import 変更はありません。

## 実装内容

stable topological sort の正当性は維持したまま、直前に選択した premise によって
indegree が 0 になった consumer を次の候補として優先する。

規則:

1. dependency edge は既存 `presentation.edges` のみを使う。
2. 同一 argument に属する visible step 間の edge のみ対象。
3. newly-ready consumer があれば、それを unrelated ready node より優先。
4. newly-ready consumer が複数なら元の表示順を tie-break に使う。
5. newly-ready consumer がなければ従来どおり元の表示順を使う。
6. cycle 時は既存 markdown を返す。
7. 新しい数学的 dependency は追加しない。

これにより pi_3^2 では

`pi_2^1 = 0 -> H 単射`

を同じ依存枝として連続表示する。

また E の枝は、一度 `E 同型` が選ばれれば

`E 同型 -> E 単射 -> Delta=0 -> H 全射`

と連続して進む。

`pi_3^3` と `E 同型` 自体には direct edge がないため、それらの相対順序は
従来の stable order を保持する。

## テスト

実行対象:

```powershell
python -m pytest `
  ".\tests\test_phase159_pi3_2_visible_dependency_topological_order.py" `
  ".\tests\test_phase159_r1_2_pi3_2_narrative_repair.py" `
  ".\tests\test_phase159_r1_2_hopf_injective_dependency_role.py" `
  ".\tests\test_phase159_r1_2_hopf_isomorphism_dependency_role.py" `
  -q
```

全体テストは実行しない。

## 完了条件

- focused tests が全 PASS。
- `pi_2^1=0` の直後の visible dependency branch として `H 単射` が先に来る。
- `E 同型 -> E 単射 -> Delta=0 -> H 全射` を保持する。
- `H 単射` と `H 全射` の後に `H 同型`。
- `H 同型` と `pi_3^3` の後に eta_2 定義。
- 最後に `pi_3^2 = Z{eta_2}`。
- edge のない root 同士には新しい数学的優先順位を付けない。

## 次 Phase との境界

Phase 159 では visible dependency ordering の tie-break のみ。
proof graph の再設計、argument model の再設計、全 renderer の置換、
edge のない statement 間の意味的依存推測は行わない。
