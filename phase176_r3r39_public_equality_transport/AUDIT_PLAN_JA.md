# Phase 176 R3R39 — 等式移送の共有探索接続

## 対象・境界

GitHub `akebono03/ehp-proof-tracer` の `develop`（2026-11-24、`8033d70c`）にある R3R38、R3R35、R3R37 を確認した。今回の変更対象は既存 `phase165_r52_r9_shared_math.py` の `shared_expansion_provider()` のみと、新規ディレクトリ `phase176_r3r39_public_equality_transport/` のコード・テストである。既存数学規則の定義、出典レジストリ、根の群構造、Web Narrative は変更しない。

既存関数の変更は、閉包 Provider の構築と、その返す `GoalExpansion` を共有 `expand()` に追加する二箇所である。実行後、既存関数の全文を `SHARED_FUNCTION_FULL_JA.md` に生成する。

## 数学的動機

局所検証済みの以下を、共有 Proof Search で独立に証明する。

$$
H(\alpha\circ E\beta)=\delta\circ E\beta,\qquad E\beta=\gamma.
$$

候補 $\beta=\delta\circ\gamma_1$ は、$\gamma=\gamma_1\circ\gamma_2$ の場合の**探索候補**であり、定理・GIVEN ではない。真に $E\beta=\gamma$ が成り立つことは既存 R3R35 の GeneratorImage の独立推論で検証する。一般式の対象は次の等式である。

$$
H(\alpha\circ\gamma)=\delta\circ\gamma.
$$

6段階の既存規則：左合成保存、$H$ の等式保存、対称律、左合成保存、推移律、推移律。それぞれ単独の `GoalExpansion` として共有 DFS の ProofStep に保存する。

## Source-first と順序

出典選別を通過した `TodaProp22RightFormula()` と $H(\alpha)=\delta$ が重複なく存在するときのみ候補を提示する。Proposition 2.2 の引用と Hopf 値の出典の欠如・重複では候補0件。`shared_expansion_provider()` の既存 `retain_ordered_root_expansions()` を通し、証明の再生は `reconstruct_registered_goal()` に委ねる。Provider 自体は GIVEN も ProofStep も作らない。

## 限定 Gate

- DryRun で従来ファイルの存在・AST・唯一のパッチ位置を検証し、変更しない。
- 本実行で旧 Provider・局所推論を残して共有関数に最小2箇所の接続を入れる。
- 群構造ではなく中間 Hopf 等式について、実際の Source-screened Context と共有 DFS を使用し、6段階が Proof Tree に残ることを検証する。
- 限定 pytest と `git diff --check` のみ実行する。全体 pytest は実行しない。
- 次工程は Toda (5.5)、合成の括弧付け、最終 Hopf 像に限る。群構造の complete 判定は行わない。

## 事前確認

- GitHub `develop` HEAD: `8033d70c5ee67626b278918be15484c688ed146e`。
- 直近独立テスト: R3R38R1、23 passed（ユーザー環境）。
- 今回作成した ZIP の実環境 Gate は利用者の実行前には **未検証**。PASS と記録してよいのは実行結果を確認した後のみ。
