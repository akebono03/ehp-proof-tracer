# Phase 175 R4R12R13R1 — 読み取り専用監査

## 対象

Toda (5.8) の式 $\Delta(\iota_9)=\pm(2\nu_4-E\nu')$ から始める一般推論経路について、既存 Provider の候補を監査する。

## 数学的義務

1. $\pi_9^9\cong\mathbb Z$ と $\pi_7^4\cong\mathbb Z\oplus\mathbb Z/4$ の証明済み構造を正しく参照する。
2. 生成元の像の自由成分が $\pm 2$ であることから $\Delta$ の単射性を、一般規則で導出する。
3. $\pi_8^4\xrightarrow E\pi_9^5\xrightarrow H\pi_9^9\xrightarrow\Delta\pi_7^4$ の二つの完全性窓を、独立した引用付き前提として使用する。
4. $\Delta$ の単射性から $H=0$、続いて $E$ の全射性を一般規則で導出する。
5. $E(\nu_4\eta_7)=\nu_5\eta_8$ の二因子を再帰的 Proof Search で証明する。

このパッケージでは 1～5 の完成は主張しない。まず候補の有無と出典文字列・次数型を確認する。

## 禁止事項

直接 GIVEN の追加、既存完成証明の再探索、専用 Narrative、全体 pytest、候補を証明と同一視すること。

## 次の境界

監査 report に従って、欠落する一般推論の最小実装と限定テストを次の変更として扱う。
