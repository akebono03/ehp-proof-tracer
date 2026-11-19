# Phase 176 R2 — n=3, k=5 Source Frontier Audit

## 対象

`π_8^3 = \mathbb Z/2\{\nu'\eta_6^2\}` の未完成証明について、Toda Chapter V の Proposition 5.9 の証明本文に明示された出典を確認する。現行 Proof Search と Web 表示も観測するが、証明を生成したり、推論規則を追加したりしない。

## 数学的依存関係

1. Toda (5.2) および Proposition 5.8 によって `π_7^2` の生成元を把握する。
2. Lemma 5.7 による $E(\eta_2\circ\nu')=0$ と合成の性質によって、$E\pi_7^2=0$ を示す。
3. EHP 完全列 (4.4) から $0\to\pi_8^3\xrightarrow{H}\pi_8^5\xrightarrow{\Delta}\pi_6^2$ が完全となり、$H$ の単射と $\operatorname{im}H=\ker\Delta$ を得る。
4. Proposition 5.6 で $\pi_8^5=\mathbb Z/8\{\nu_5\}$ を使用する。Lemma 5.7 の $\Delta(\nu_5)=\pm(\eta_2\circ\nu')$、(5.2)、Proposition 5.6、(5.5) から、$\ker\Delta=\langle4\nu_5\rangle=\langle\eta_5^3\rangle$ を確認する。ここには $\Delta(\nu_5)$ が位数4の生成元を与えることの型付き根拠が必要。
5. Proposition 2.2 と (5.3)、連続する $\eta$ の suspension 定義により $H(\nu'\circ\eta_6^2)=\eta_5^3$ を示す。
6. $H$ が単射、像が2元巡回群であり、その生成元が指定元の像であることから、群の巡回構造と生成元を導く。結論を直接 GIVEN として登録しない。

## 原文監査と実行境界

監査対象：`sources/toda/Toda_05_2.tex`、`sources/toda/Toda_02_2.tex`。固定アンカー検査は本文同一性の全検証ではない。参照文字列があるだけで ProofStep が証明済みになるわけではない。現行の `search_group_from_registered_goal`、`build_standard_web_group_proof_view` の結果を別 worker で記録する。

この Phase では `README.md`、`docs/design.md`、`docs/development_log.md`、`docs/roadmap.md`、`docs/proof_records.md` を変更しない。Source-first、First Successful Proof Search、既存の Source Guard 4件未解決を維持する。全体 pytest は実施しない。
