# Phase 174 R3-R7-R21：Hopf–Δ 推論の前提監査

## 変更対象

既存の Python コード、既存テスト、DB、Renderer、GIVEN、推論規則の変更は **なし**。
新設 `phase174_r3_r7_r21_delta_hopf_chain_audit/` の以下のみ。

- `audit.py`: Git HEAD・出典・数学的依存順・公開未完成状態の読み取り専用監査
- `tests/test_audit.py`: 独立した前提・出典順・改変拒否のテスト
- `tests/test_public.py`: 誤った公開完成を拒否するテスト
- `run.ps1`: DryRun → 必要な限定 pytest → 本監査
- `README.md`: 英語の実行案内
- `CODE_FULL_JA.md`: 新設コードの全文

## 数学的依存関係

Toda の採用 TeX の Proposition 5.9 の証明では、$E\pi_{10}^5=0$、
$0\to\pi_{11}^6\xrightarrow{H}\pi_{11}^{11}\xrightarrow{\Delta}\pi_9^5$ の完全列、
$\ker\Delta=\langle 2\iota_{11}\rangle$ が使われる。
それによって $H$ は単射で、像は $2\mathbb Z$ になる。
Proposition 2.7 の $H(\Delta(\iota_{13}))=\pm 2\iota_{11}$ と合わせると、
$\Delta(\iota_{13})$ が $\pi_{11}^6$ を生成するという帰結の出典構造を確認できる。

しかしこれは **出典内での証明の構成** の確認であり、公開 Proof Search 内の
`TodaDeltaImageUpToSignStatement` の検証済み ProofStep が得られたことは意味しない。

## 完了条件

- HEAD の一致、Source Guard PASS、限定テスト PASS
- 独立した Hopf 前提と循環のない依存順を確認
- `SIGNED_DELTA_WITNESSES=0` / `VERIFIED_STEPS=0` を保持
- 新規 GIVEN 0、新規数学規則 0、全体 pytest 未実施

## R22 との境界

R21 では数学的推論規則の実装をしない。次段階では型付きの
`H`, `Δ`, 生成元、および exactness（完全性）の必要な一般表現と、
出典から独立した検証済み前提への変換経路を監査する。
