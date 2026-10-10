# Phase 163 R4-R20 — 第1章の独立主張精査

添付 TeX を基準とする暫定審査。印刷原典照合・既存67成分との同一性確認は未実施。
既存24 IDを維持し、14候補にはIDをまだ発行しない。

## 14候補の内容と条件

- 173行 [definition_component] 誘導写像 f* と g* の定義域・値域。条件：基点付き写像 f:X→Y, g:Y→Z を固定。
- 180行 [independent_claim] 合成の結合律 (γ∘β)∘α=γ∘(β∘α)。条件：合成可能な基点付きホモトピー類 α,β,γ。
- 183行 [independent_claim] 前合成・後合成の反変／共変合成則。条件：写像 f1,f2,g1,g2 が合成可能。
- 201行 [independent_claim] reduced join の結合性を表す自然な同相。条件：基点付き空間 A,B,C。要確認：原稿の reduced join と通常の smash product の用語の違いを確認。
- 211行 [needs_mathematical_correction] 原稿は S^m∧S^n ≅ S^(m+n+1) と記載。条件：球面 S^m,S^n。要確認：通常の smash product は S^(m+n)。reduced join の記号・次元の整合性を要確認。
- 234行 [compound_claim] reduced join のホモトピー不変性・結合性・合成保存。条件：基点付き写像 f,g,h 等が定義され合成可能。要確認：0),i),ii) は分割候補。
- 260行 [compound_claim] ホモトピー類の reduced join の結合性・合成保存。条件：関連するホモトピー類が合成可能。要確認：i),ii) は分割候補。
- 294行 [compound_claim] 懸垂のホモトピー不変性・反復・合成保存。条件：n,m は反復懸垂を定義できる非負整数、写像・類は合成可能。要確認：0),i),ii) は分割候補。
- 354行 [independent_claim] [EX,Y] と π1(Y^X_0) の自然同型。条件：X locally compact（局所コンパクト）という本文条件。要確認：写像空間の位相・基点条件を確認。
- 366行 [independent_claim] 後合成 f* が [EX,Y] の加法を保存。条件：f:Y→Z、α,α′∈[EX,Y]。
- 369行 [independent_claim] E[g] による前合成が [EX,Y] の加法を保存。条件：g:W→X、α,α′∈[EX,Y]。
- 406行 [independent_claim] Ω(β∘α)=Ωβ∘Ωα。条件：合成可能な基点付きホモトピー類 α,β。
- 473行 [compound_claim] Ω0 の前合成・後合成に関する自然性（4式）。条件：本文の f:X→Y,g:EY→Z,h:Z→W、α,β,γ。要確認：4式の独立性・型を個別確認。
- 1115行 [independent_claim] E^n(Y∪β CX) と E^nY∪E^nβ CE^nX の対応。条件：β:X→Y は貼り合わせ写像、n 重懸垂が定義される。要確認：同一視の厳密性・自然性を確認。

## 未完了

残り65箇所を保留として前後文脈付きCSVに保存。数学的に内容を読んで独立性を判定する必要がある。
通常の smash product と原稿の reduced join の次元記法に注意する。
全体 pytest は Phase 終了時のみ。
