# Phase 169 R10EQ-R1 — 任意の安定元の共通 Definition

## 目的

`HyoujiGen.csv` の生成元の名前ごとに反復懸垂の文献記録を追加する構造をやめ、安定元の代表という一つの定義に基づき `GeneratorImage` を導出する。生成元名による条件分岐を追加しない。ここで安定範囲は $n\ge k+2$ とする。

安定ホモトピー群 $G_k=\operatorname{colim}_n\pi_{n+k}^n$ の同一元 $x$ の代表を $x_n$ とすると、$E(x_n)=x_{n+1}$ は代表の選び方に関する定義的同一性である。一方 Toda (4.5) が与える $E$ の同型性や、$x_n$ が生成元であること、群の位数は別に立証する。

## 型と名前の区別

`kinds=0` の登録は、プロジェクト内で「同じ安定元の添字付き表現」として**採用する表記規約**と明示する。この規約によって、安定範囲の同一 ID・型・次元の連続した表現のみを定義として接続する。CSV が群構造や任意の異なる名前同士の等式を証明するわけではない。

任意の未登録の元 $x\in\pi_{n+k}^n$ に対しても、`IteratedSuspension(x, 1)` を明示すれば $E(x)$ という定義的表示が利用できる。これは任意の元に適用できるが、勝手に付けた別名 `y` との一致までは主張しない。

和・整数倍・合成については、型付きの各項の対応を再帰的に検証する。ただし既存の引用付き・合成元推論経路がある場合はそれらを優先し、過去の Proof Tree の形を不必要に変えない。

## 変更対象

- 既存 `phase165_r52_r9_shared_math.py` の `shared_expansion_provider()` **関数全体のみ**を置換。モジュール import は変更しない。
- 新規 `phase169_r10eq_r1_universal_stable_definition/definition.py` に `typed_element_span()`、`is_defined_stable_suspension()`、`is_defined_stable_image()`、`expand_defined_stable_element_image()` を追加。
- 新規 `patch.py`, `audit.py`, `tests/test_r10eq_stable_definition.py`, `tests/test_r10eq_live.py`, `run.ps1`。

## 証明上の境界

新しい規則は前提のない `INFERENCE` として Definition の式変形を表す。これは外部文献を偽装した `GIVEN` ではない。Replay 検証では、結論の写像・両端の型・安定範囲・同じ登録 ID または明示された懸垂の定義を再確認する。

既存の群構造輸送には、出典を持つ以前の群構造と Toda (4.5) の証明が引き続き必要。新規規則は `GeneratorImage` 以外の結論を作らない。

## 検証と完了条件

限定 pytest と実検索で $\pi_{41}^{30}$、$\pi_{44}^{30}$ を検査し、両者の `complete` と Trust Boundary PASS を確認する。さらに39件すべての登録行、未登録元の明示的懸垂、合成・和・整数倍、不正な添字・型・名前の拒否を限定テストする。全体 pytest は Phase 最終段階まで実行しない。

## 次段階との境界

今回の作業は数学的 Definition と型付き探索のみ。完成 Proof Tree の表示で、出典に依存しない Definition の導出が適切に省略・統合されるかは次段階で別途監査する。現行の `R10EP` 表示修正とは独立。
