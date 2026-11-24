# 変更一覧・確認の記録

## 変更一覧

- `phase165_r52_r9_shared_math.py::shared_expansion_provider()` — 変更対象。既存 `available` の出典選別結果から Provider を組み立て、`expand()` の R3R37 の直後に候補を追加する。
- `phase176_r3r39_public_equality_transport/source.py` — 新規。`right_hopf_transport_backward_plan()`、`build_public_right_hopf_transport_provider()`、後者の内側の `expand()` を追加。
- `phase176_r3r39_public_equality_transport/apply.py` — 新規。原状のアンカー検証・最小変更適用・共有関数全文ファイル生成。
- `phase176_r3r39_public_equality_transport/audit.py` — 新規。`source_guard()`、`probe()`、`main()` を追加。
- `phase176_r3r39_public_equality_transport/tests/test_source.py` — 新規。既存規則の6段階、型チェック、出典重複拒否、Provider 順序・再生テスト。
- `phase176_r3r39_public_equality_transport/run.ps1` — 新規。DryRun、本実行、限定 pytest を実行。

変更されないもの：既存の数学規則、Prop 2.2 と Toda (5.3)/(5.5) の既存 GIVEN、群構造 Goal、Web Renderer。

## 完了条件

DryRun、本実行の Source-first 監査、共有 DFS の6段階 Proof Tree 検証、限定 pytest、`git diff --check` のすべてが PASS すること。根の群構造 complete は対象外。

## 次工程との境界

$$H(\nu'\eta_6^2)=\eta_5\eta_6\eta_7$$

までの移送が共有 DFS で確認できた後、Toda (5.5) の $4\nu_5$ との結合・等式輸送を別工程で行う。根の群全体を巡回位数2と証明する工程はさらに後である。
