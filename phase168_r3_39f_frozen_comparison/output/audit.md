# Phase 168 R3-39F — 固定基準との全文監査

監査専用。実装コード・固定基準は変更しない。

| 群 | Reference 差分行 | 本文差分行 | 基準の説明項目 |
|---|---:|---:|---|
| pi3_2 | 16 | 33 | 4/4 |
| pi4_3 | 18 | 31 | 4/4 |
| pi5_4 | 12 | 14 | 2/4 |

## pi3_2

- **一致** — H の単射を完全性から導いたことを明記 (`exactness_for_injectivity`)
- **一致** — Im Δ = ker E = 0 を明記 (`delta_image_kernel_zero`)
- **一致** — H の同型性を単射性と全射性から説明 (`hopf_iso_from_bijectivity`)
- **一致** — 基準にない一般円周公式の本文再掲がない (`no_generic_circle_in_proof`)
- 全文差分: `pi3_2_reference.diff`, `pi3_2_proof.diff`

## pi4_3

- **一致** — E の全射を完全性から導いたことを明記 (`surjectivity_from_exactness`)
- **一致** — ker E の具体的な表示 (`kernel_presentation`)
- **一致** — 準同型定理を明記 (`quotient_theorem`)
- **一致** — 基準にも存在する対角群の一般式 (`diagonal_general_in_proof`)
- 全文差分: `pi4_3_reference.diff`, `pi4_3_proof.diff`

## pi5_4

- **不足または順序差** — (4.5) への (n,m,k)=(3,4,1) の代入 (`toda45_explicit_substitution`)
- **不足または順序差** — (4.5) を引用して適用したことを明記 (`specialization_citation_in_proof`)
- **一致** — 引用する群構造を生成元の像より先に示す (`source_before_generator_image`)
- **一致** — 具体的な E 同型を表示 (`specific_map_isomorphism`)
- 全文差分: `pi5_4_reference.diff`, `pi5_4_proof.diff`

## 監査上の注意

- この項目数は固定基準の全文一致率を意味しない。
- Reference 番号の違いだけでは不合格としない。
- 不一致は数学的な誤りとは限らない。
- 全体 pytest は実行しない。
