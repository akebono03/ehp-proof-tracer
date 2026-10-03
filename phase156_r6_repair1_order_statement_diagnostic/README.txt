Phase 156-R6 repair1 — ORDER statement diagnostic

Production changes: none.

目的
====
repair1 後、canonical equation (2) は復元したが、
既存テストが期待する

$\operatorname{ord}\left(\eta_{3}^{3}\right) = 2$

が見つからなくなった。

depth 2 / 3 の pi_6^3 について ORDER block の各 ProofStep を列挙し、

- statement type
- lhs / rhs の有無
- lhs / rhs の型と repr
- repository raw LaTeX
- generic Narrative rendering
- public Narrative 内の ord 行

を表示する。

この結果から、canonical relation normalization が
ORDER statement に誤適用されているか、
または別 renderer が表示を変えているかを確定する。

pytest / repository-wide pytest は実行しない。
