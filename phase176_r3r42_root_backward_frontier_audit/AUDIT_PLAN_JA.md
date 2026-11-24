# Phase 176 R3R42 — 根の逆向き探索境界監査

対象：$\pi_8^3=\mathbb Z/2\{\nu'\eta_6^2\}$。

## 背景と目的

R3R41 は $H(\nu'\eta_6^2)=4\nu_5$ の独立した共有探索を確認した。しかし Web の群構造 Goal からその等式まで到達したことは、まだ確認されていない。

`found 0` は検証に成功した導出の数であり、候補生成数と必ずしも同じではない。過去の R3R17〜R3R20 の独立した候補検査とは区別して、今回は実際の Web narrative 入口を一回呼び出す。

## 観測箇所

- 実際の Web Group query から渡された root、引用 context、探索結果。
- Root Order Gate の入力・出力（実際に呼び出された場合のみ）。
- DFS に返された候補の個数、順序、全 subgoal、各 Goal の呼び出しの有無。
- 探索が受理した ProofStep、未解決 Goal、表示側の step 数と診断。
- 独立した候補検査として、既存の巡回群規則、Hopf 単射性、R3R41 の登録表記と標準表記それぞれの Goal を確認する。実際の Web 探索結果には追加しない。

## 完了条件

`PASS_R3R42_PUBLIC_ROOT_FRONTIER_RECORDED` と `PASS_R3R42_FRONTIER_AUDIT_FOCUSED_TESTS`。候補数を決め打ちしない。根が未完成でも観測できれば監査成功であり、証明成功とは区別する。Source-first、First Successful Proof Search、Root Order Gate の実装は変更しない。

本番ファイル、DB、GIVEN、数学規則、Renderer は変更しない。今回の pytest は監査機構の限定テストのみで、全体 pytest は実施しない。次工程は監査結果から最初の不足規則・候補接続を決める。
