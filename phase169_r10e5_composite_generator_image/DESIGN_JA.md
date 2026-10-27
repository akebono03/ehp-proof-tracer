# Phase 169 R10E5 — 合成生成元の懸垂像

## 目標

Phase 169 R10E4-R4 は先行 DB 結果の採用と Toda (4.5) により、7-stem の巡回群や零群について完成証明を生成した。一方、`π_20^14=Z/2{ν_14^2}` は `GeneratorImage` を未解決として残した。

今回の Phase では、`E(f∘g)=Ef∘Eg` という懸垂関手の合成保存性を、Proof Tree の型付き INFERENCE として追加する。DB に保存された合成生成元の表記から像の証明を作ることはしない。

## 変更範囲

既存ファイル `phase165_r52_r9_shared_math.py` の `shared_expansion_provider()` のみ変更。既存の import 部分は変更しない。新規の `phase169_r10e5_composite_generator_image/rule.py` を追加し、`component_image_obligations`、`composite_generator_image_rule`、`expand_composite_generator_image` を定義する。

`_endpoints()` は内部の型付き補助関数。新規関数の全文は同梱した `rule.py` に、変更した既存関数とファイルの全文は `run.ps1` 実行時に `output/` に保存する。

## 証明の条件

`GeneratorImage` が合成 `f∘g` についての1回の懸垂を表すとき、その源・標的の球面次数を確認する。左右の因子についてそれぞれ別の `GeneratorImage` を subgoal として要求し、両者が `ProofRule.INFERENCE` である場合にだけ元の像を結論づける。

`ν` や `σ` などの系列 ID はこの合成規則で特別扱いしない。個別の因子の像を証明できるかは既存の引用付き系列定義に委ねる。既存の η 合成の経路を優先するため、同じ目標への候補の二重生成を避ける。

## 未対応の範囲

加法、係数倍、基底変換を含むすべての生成元について証明を追加する Phase ではない。未登録の μ・ε 等の定義が必要な場合は、検索状態を未完成のままとする。DB の先行順序・由来・Trust Boundary を変更しない。

## テストと完了条件

新規限定テストで型付き2因子、合成の多重化、次数不一致の拒否、GIVEN 偽装の拒否、二重パッチ防止を確認する。既存の R10E4・R10E2・R10E1・R7・Phase168 の関係する限定テストと探索監査を実行する。全体 pytest は Phase169 の最後にだけ実行する。
