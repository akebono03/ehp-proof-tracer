# Phase 168 R3-34 — 固定基準全文の再監査

**判定：差異あり。R3-33 の「一致」を全文一致と解釈するのは誤り。**

比較対象は同梱した固定基準と R3-33 の実出力。

## pi_3^2

- **REFERENCE_BODY_MISSING**: (5.1) の二つの一般公式が使用する結果にない
- **REFERENCE_BODY_MISSING**: Proposition 5.1 の H(η₂)=ι₃ が使用する結果にない
- **REFERENCE_NUMBERING_CHANGED**: Proposition 5.1 は基準 [R2]、現行 [R4]。番号変更だけは誤りとみなさない
- **REFERENCE_EXTRA**: Proposition 4.2 (4.4) と suspension identity が現行欄に追加された。証明上必要かを別途点検
- **PROOF_EXPLANATION_MISSING**: Δ の零写像性について ImΔ=ker E=0 の計算が省略
- **PROOF_EXPLANATION_MISSING**: H の同型性に至る「単射性と全射性より」という説明が省略
- **PROOF_SOURCE_LINK_MISSING**: 完全列、H の単射・全射・同型の根拠を本文の対応位置で明示する記述が基準より弱い

- Reference 全文差分: `pi_3^2_reference.diff`
- 証明全文差分: `pi_3^2_proof.diff`

## pi_4^3

- **REFERENCE_BODY_MISSING**: (5.1) の零群公式・対角群の一般公式が使用する結果にない
- **REFERENCE_BODY_MISSING**: Proposition 5.1 の π₃² の群構造と Δ(ι₅)=±2η₂ が使用する結果にない
- **REFERENCE_EXTRA**: eta-family notation / Proposition 4.2 の見出しが追加された。必要性と対応を点検
- **PROOF_EXPLANATION_DIFF**: ImΔ=ker E を別段落で表示しており基準と表現が異なる（欠落ではない）
- **PROOF_SOURCE_LINK_MISSING**: E の全射性など、完全性からの推論が簡略化されている

- Reference 全文差分: `pi_4^3_reference.diff`
- 証明全文差分: `pi_4^3_proof.diff`

## pi_5^4

- **REFERENCE_BODY_MISSING**: Toda (4.5) の一般的同型輸送公式が使用する結果にない
- **REFERENCE_BODY_MISSING**: Proposition 5.1 の π₄³ の群構造が使用する結果にない
- **REFERENCE_EXTRA**: eta-family notation の見出しが現行欄に追加された
- **PROOF_MISSING**: (n,m,k)=(3,4,1) への Toda (4.5) の特殊化が表示されない
- **PROOF_MISSING**: E:π₄³→π₅⁴ が同型であることが表示されない
- **PROOF_SOURCE_LINK_MISSING**: (4.5) が一覧にはあるが証明本文に [R3] が現れない
- **PROOF_ORDER_DIFF**: 生成元の像 E(η₃)=η₄ が出典・同型の説明より前に表示される
- **PROOF_EXTRA**: π₅⁴=Z/2{Eη₃} の中間式が現行に追加された（それ自体は誤りとは判定しない）

- Reference 全文差分: `pi_5^4_reference.diff`
- 証明全文差分: `pi_5^4_proof.diff`

## 判定上の注意

- Findings are qualitative comparisons of supplied source snapshots, not a proof of literature correctness.
- Current output is the supplied R3-33 capture. Re-run capture separately if repository source has changed.
- Reference numbering is not required to equal the frozen baseline.
- This audit does not run full pytest or patch source files.
