# Phase 163 R4-R46 数学的主張の TeX 対応監査

式の直接記載と一般式の特殊化・周辺記述を区別する。TeX の引用は原本照合を意味しない。

| Reference | Assertion | 判定 | TeX 行 |
|---|---|---|---|
| toda:Proposition 5.1 | `boundary:Proposition 5.1:pi3_2_group_relation` | EXPLICIT | 192 |
| toda:Proposition 5.1 | `boundary:Proposition 5.1:eta2_hopf_relation` | EXPLICIT | 196 |
| toda:Proposition 5.1 | `boundary:Proposition 5.1:delta_iota5_relation` | EXPLICIT | 196 |
| toda:Proposition 5.1 | `boundary:Proposition 5.1:higher_eta_group_relation` | EXPLICIT | 193 |
| toda:Proposition 5.3 | `boundary:Proposition 5.3:pi4_2_group_relation` | SPECIALIZATION | 367 |
| toda:Proposition 5.3 | `boundary:Proposition 5.3:pi5_3_group_relation` | SPECIALIZATION | 367 |
| toda:Proposition 5.3 | `boundary:Proposition 5.3:pi6_4_group_relation` | SPECIALIZATION | 367 |
| toda:Proposition 5.3 | `boundary:Proposition 5.3:higher_eta_squared_group_relation` | EXPLICIT | 367 |
| toda:Proposition 5.6 | `boundary:Proposition 5.6:pi5_2_group_relation` | EXPLICIT | 695 |
| toda:Proposition 5.6 | `boundary:Proposition 5.6:pi6_3_group_relation` | EXPLICIT | 696 |
| toda:Proposition 5.6 | `boundary:Proposition 5.6:pi7_4_group_relation` | EXPLICIT | 697 |
| toda:Proposition 5.6 | `boundary:Proposition 5.6:pi8_5_group_relation` | SPECIALIZATION | 698 |
| toda:Proposition 5.6 | `boundary:Proposition 5.6:higher_nu_group_relation` | EXPLICIT | 698 |
| toda:(5.1) | `boundary:(5.1):circle_higher_homotopy_zero` | EXPLICIT | 88 |
| toda:(5.1) | `boundary:(5.1):sphere_connectivity_zero` | EXPLICIT | 89 |
| toda:(5.1) | `boundary:(5.1):stable_negative_zero` | EXPLICIT | 90 |
| toda:(5.1) | `boundary:(5.1):diagonal_identity_group` | SURROUNDING_TEXT | 93 |
| toda:(5.1) | `boundary:(5.1):stable_zero_stem` | SURROUNDING_TEXT | 94 |
| toda:(5.1) | `boundary:(5.1):diagonal_suspension_isomorphism` | NOT_LOCATED | — |
| toda:(5.3) | `boundary:(5.3):nu_prime_bracket_definition` | SURROUNDING_TEXT | 344 |
| toda:(5.3) | `boundary:(5.3):nu_prime_membership` | EXPLICIT | 348 |
| toda:(5.3) | `boundary:(5.3):nu_prime_hopf_relation` | EXPLICIT | 348 |
| toda:(5.3) | `boundary:(5.3):nu_prime_double_relation` | EXPLICIT | 348 |

## 判定の意味

- EXPLICIT: TeX に主張の直接的な記号表記を検出した。数学的完全性・原本一致の証明ではない。
- SPECIALIZATION: TeX の一般式からパラメータを代入する必要がある。
- SURROUNDING_TEXT: 参照環境の前後に記載され、環境の内部ではない。
- NOT_LOCATED: 当該参照から明示的な根拠が見つからない。
- ANCHOR_NOT_FOUND: 想定した記号形式が存在せず、保留。

## 個別の観察

- `boundary:Proposition 5.1:pi3_2_group_relation`: 命題に直接記載（EXPLICIT）
- `boundary:Proposition 5.1:eta2_hopf_relation`: 命題に直接記載（EXPLICIT）
- `boundary:Proposition 5.1:delta_iota5_relation`: 命題に直接記載（EXPLICIT）
- `boundary:Proposition 5.1:higher_eta_group_relation`: 命題に一般式として直接記載（EXPLICIT）
- `boundary:Proposition 5.3:pi4_2_group_relation`: n=2 の特殊化。文献内の別個の列挙ではない（SPECIALIZATION）
- `boundary:Proposition 5.3:pi5_3_group_relation`: n=3 の特殊化。文献内の別個の列挙ではない（SPECIALIZATION）
- `boundary:Proposition 5.3:pi6_4_group_relation`: n=4 の特殊化。文献内の別個の列挙ではない（SPECIALIZATION）
- `boundary:Proposition 5.3:higher_eta_squared_group_relation`: n>=2 の一般式に直接記載（EXPLICIT）
- `boundary:Proposition 5.6:pi5_2_group_relation`: 命題に直接記載（EXPLICIT）
- `boundary:Proposition 5.6:pi6_3_group_relation`: 命題に直接記載（EXPLICIT）
- `boundary:Proposition 5.6:pi7_4_group_relation`: 命題に直接記載（EXPLICIT）
- `boundary:Proposition 5.6:pi8_5_group_relation`: n=5 の特殊化（SPECIALIZATION）
- `boundary:Proposition 5.6:higher_nu_group_relation`: n>=5 の一般式に直接記載（EXPLICIT）
- `boundary:(5.1):circle_higher_homotopy_zero`: 式 (5.1) に直接記載（EXPLICIT）
- `boundary:(5.1):sphere_connectivity_zero`: 式 (5.1) に直接記載（EXPLICIT）
- `boundary:(5.1):stable_negative_zero`: 式 (5.1) に直接記載（EXPLICIT）
- `boundary:(5.1):diagonal_identity_group`: 番号付き (5.1) の直後の無番号表示（SURROUNDING_TEXT）
- `boundary:(5.1):stable_zero_stem`: 番号付き (5.1) の直後の無番号表示（SURROUNDING_TEXT）
- `boundary:(5.1):diagonal_suspension_isomorphism`: 式 (5.1) 自体には懸垂同型の主張を確認できない（NOT_LOCATED）
- `boundary:(5.3):nu_prime_bracket_definition`: 式 (5.3) の直前の記述（SURROUNDING_TEXT）
- `boundary:(5.3):nu_prime_membership`: 式 (5.3) に直接記載（EXPLICIT）
- `boundary:(5.3):nu_prime_hopf_relation`: 式 (5.3) に直接記載（EXPLICIT）
- `boundary:(5.3):nu_prime_double_relation`: 式 (5.3) に直接記載（EXPLICIT）
