# Phase 175 R4R14 — π₁₀⁶ 証明フロンティア監査

## 対象

- `phase174_r3_r7_r12_toda59_annihilator_source/source.py`: (5.9) 出典証拠
- `phase174_r3_r7_r12_toda59_annihilator_source/rule.py`: 添字6の型付き特殊化
- `phase174_r3_r7_r13_cited_annihilator_bridge/registry.py`: 一般出典 GIVEN の登録
- `phase165_r52_r9_shared_math.py`: 共有 Proof Search 接続
- `phase174_r3_r7_r3_ehp_zero_rule/rule.py`: Δ 全射を経由する既存の零群規則
- `phase165_r55_nk_only_goal.py`: 群検索 API

## 数学的確認

Toda (5.9) は $\nu_n\eta_{n+3}=0$ ($n\ge 6$) の一般的な出典であり、添字6の個別関係は推論として導かれる。$\pi_{10}^{6}=0$ を直接 GIVEN として登録しない。

候補経路は $\pi_9^5=\mathbb Z/2\{\nu_5\eta_8\}$ と $E(\nu_5\eta_8)=\nu_6\eta_9=0$、さらに EHP 完全性と $\pi_{10}^{11}=0$ を利用する。現行コードにこの推論の全体があるかを次の作業で精査する。本監査自体は数学規則を追加しない。

## 完了条件

- 現行出典・推論コードの blob が一致する。
- (5.9) の出典 GIVEN がちょうど1件存在する。
- 添字6への特殊化が公開 Provider に到達する。
- 現行 EHP の未解決前提を報告する。
- 限定 pytest が PASS する。
- 全体 pytest、本番コード更新を行わない。

## 次工程との境界

本監査による `PARTIAL_FRONTIER_CONFIRMED` は群の証明完成を意味しない。既存規則再利用または必要最小限の追加規則は監査結果を見て判断する。
