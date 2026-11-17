# Phase 175 R4R8 — 監査計画

## 対象と境界

Toda Proposition 2.5 と (5.8) の符号付き関係を、先行した R4R7 の一般推論規則に結びつけるための独立した前提を監査する。**本 Phase は監査のみ**。数式を直接 GIVEN に登録せず、実証されていない前提を ProofStep に昇格させない。

## 監査する数学的条件

- 先行完成群構造 $\pi_7^4=\mathbb Z\{\nu_4\}\oplus\mathbb Z/4\{E\nu'\}$ と $\pi_8^5=\mathbb Z/8\{\nu_5\}$ の DB 上の型を確認する。先行完成証明は再探索しない。
- E の生成元像 $E\nu_4=\nu_5$ と $E(E\nu')=2\nu_5$ を証明済みとは仮定しない。
- これらの像が別途証明されれば、整数計算から $\ker E=\mathbb Z\{2\nu_4-E\nu'\}$ を得る。これは**条件付きの代数計算**であって公開の証明ステップではない。
- $\Delta:\pi_9^9\to\pi_7^4$ と $E:\pi_7^4\to\pi_8^5$ の EHP 完全性を型のみ確認し、証明済みとして扱わない。
- $\pi_9^9=\mathbb Z\{\iota_9\}$、像の完全性、生成元像から $\Delta(\iota_9)=\pm(2\nu_4-E\nu')$ を得る一般推論は今後の義務。符号は残す。
- R4R7 のもう一方の前提 $\iota_9\circ E^2\eta_7=\eta_9$ も独立して証明を要する。

## 証明境界

先行 DB の直接的な結論登録禁止、専用 Narrative 不追加、Source-first と First Successful Proof Search を維持。公開 Proof Search に規則を接続しない。先行完成証明の再探索なし。全体 pytest は Phase 終了時のみ。

## 最終 Gate

`PASS_R4R8_SIGNED_DELTA_KERNEL_FRONTIER_RECORDED_NOT_PUBLIC`
