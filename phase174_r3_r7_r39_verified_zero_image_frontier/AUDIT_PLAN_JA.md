# Phase 174 R3-R7-R39 監査計画

## 変更対象

新規ディレクトリ `phase174_r3_r7_r39_verified_zero_image_frontier/` の `source_guard.py`、`audit.py`、`run.ps1`、3個の限定テスト、文書だけ。既存実装の変更なし。

## 証明義務

1. Toda (5.9) の一般的な消滅関係の出典付き GIVEN を Source-first で検証する。
2. `n=6` の特殊化 $\nu_6\eta_9=0$ を元の GIVEN から INFERENCE で導く。
3. 安定な生成元の懸垂、合成、結合律に関する既存規則を順に照合する。
4. $E(\nu_5\eta_8^2)=0$ の生成元像だけを実際の `ProofStep` として導出する。
5. 先行 DB prior の $\pi_{10}^{5}=\mathbb Z/2\{\nu_5\eta_8^2\}$ は別に照合し、独立した Toda の文献命題とは扱わない。
6. R6 は巡回群表示に INFERENCE を要求するため、DB prior の GIVEN がそのまま通らないことを照合する。
7. 群全体の零像、上側 Δ 全射性、最終群の完成を宣言しない。

## Gate

`PASS_R39_CITED_GENERATOR_ZERO_PROVED_DB_PRESENTATION_BARRIER`。

## 次 Phase との境界

R40 では、巡回群表示の独立した INFERENCE を確保できるか、もしくは厳密に再検証された採用済み DB prior を前提として認める **別の一般推論規則** が数学的・安全設計上許容されるかを監査する。R39 では規則変更を行わない。
