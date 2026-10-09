# Phase 162 R10-R5: 証明本文の由来監査

## 概要

- nodes: 97
- presentation_edges: 109
- body_lines: 47
- line_origins: {'CONNECTOR_OR_PROSE': 10, 'MATH_WITHOUT_EXACT_STEP': 16, 'STEP_EXACT_MATH': 20, 'TRANSPORT_APPENDIX': 1}
- duplicate_conclusions: 27
- matched_steps: 24
- unmatched_steps: 73

## 本文の行と候補 ProofStep

| 行 | 分類 | 候補ノード | 本文 |
|---:|---|---|---|
| 1 | CONNECTOR_OR_PROSE | [] | 対象 |
| 4 | MATH_WITHOUT_EXACT_STEP | [] | \pi_{5}^{3} = \mathbb{Z}/2\{\eta_{3}^{2}\}. |
| 7 | CONNECTOR_OR_PROSE | [] | ## 使用する結果 |
| 9 | CONNECTOR_OR_PROSE | [] | **[R1] (5.3).** |
| 10 | STEP_EXACT_MATH | [37, 44] | $H\left(\nu'\right) = \eta_{5}$. |
| 11 | CONNECTOR_OR_PROSE | [] | **[R2] (4.5).** |
| 12 | STEP_EXACT_MATH | [85] | $E^{n - 3}: \pi_{3 + 1}^{3} \to \pi_{n + 1}^{n}$ は同型. |
| 16 | CONNECTOR_OR_PROSE | [] | ## 証明 |
| 18 | MATH_WITHOUT_EXACT_STEP | [] | $\pi_{5}^{3}$ の群構造を決定するために, 次の完全列を考える. |
| 21 | MATH_WITHOUT_EXACT_STEP | [] | \pi_{6}^{3} \xrightarrow{H} \pi_{6}^{5} \xrightarrow{\Delta} \pi_{4}^{2} \xrightarrow{E} \pi_{5}^{3} \xrightarrow{H} \pi_{5}^{5} \xrightarrow{\Delta} \pi_{3}^{2 |
| 24 | MATH_WITHOUT_EXACT_STEP | [] | [R1]より, $H: \pi_{6}^{3} \to \pi_{6}^{5}$ は全射. |
| 26 | MATH_WITHOUT_EXACT_STEP | [] | 完全性より, $H: \pi_{3}^{2} \to \pi_{3}^{3}$ は単射. |
| 28 | MATH_WITHOUT_EXACT_STEP | [] | 完全性より, $H: \pi_{3}^{2} \to \pi_{3}^{3}$ は全射. |
| 30 | MATH_WITHOUT_EXACT_STEP | [] | 完全性より, $E: \pi_{3}^{2} \to \pi_{4}^{3}$ は全射. |
| 32 | STEP_EXACT_MATH | [1] | $\pi_{4}^{2} = \mathbb{Z}/2\{\eta_{2}^{2}\}$. |
| 34 | STEP_EXACT_MATH | [19, 45] | $\pi_{3}^{2} = \mathbb{Z}\{\eta_{2}\}$. |
| 36 | STEP_EXACT_MATH | [39, 96] | $\pi_{5}^{5} = \mathbb{Z}\{\iota_{5}\}$. |
| 38 | STEP_EXACT_MATH | [40, 61] | $\Delta\left(\iota_{5}\right) = \pm [\iota_{2}, \iota_{2}]$. |
| 40 | STEP_EXACT_MATH | [65, 81] | $[\iota_{2}, \iota_{2}]$. |
| 42 | STEP_EXACT_MATH | [50, 71] | これより, $H([\iota_{2}, \iota_{2}]) = \pm 2\iota_{3}$ が成り立つ. |
| 44 | MATH_WITHOUT_EXACT_STEP | [] | $\operatorname{Im}\Delta = \mathbb{Z}\{2\eta_{2}\}$. |
| 46 | MATH_WITHOUT_EXACT_STEP | [] | 完全性より, $\ker E=\operatorname{Im}Δ=\mathbb{Z}\{2\eta_{2}\}$. |
| 48 | STEP_EXACT_MATH | [33, 94] | $\pi_{4}^{5} = 0$. |
| 50 | STEP_EXACT_MATH | [4, 72] | $\pi_{4}^{3} = \mathbb{Z}/2\{\eta_{3}\}$. |
| 52 | STEP_EXACT_MATH | [39, 96] | これより, $\pi_{5}^{5} = \mathbb{Z}\{\iota_{5}\}$. |
| 54 | STEP_EXACT_MATH | [40, 61] | $\Delta\left(\iota_{5}\right) = \pm [\iota_{2}, \iota_{2}]$. |
| 56 | STEP_EXACT_MATH | [65, 81] | $[\iota_{2}, \iota_{2}]$. |
| 58 | STEP_EXACT_MATH | [50, 71] | これより, $H([\iota_{2}, \iota_{2}]) = \pm 2\iota_{3}$ が成り立つ. |
| 60 | STEP_EXACT_MATH | [63] | [R2]より, $\pi_{n + 1}^{n} = \mathbb{Z}/2\{E^{n - 3}\eta_{3}\}$. |
| 62 | STEP_EXACT_MATH | [33, 94] | $\pi_{4}^{5} = 0$. |
| 64 | STEP_EXACT_MATH | [19, 45] | これより, $\pi_{3}^{2} = \mathbb{Z}\{\eta_{2}\}$. |
| 66 | STEP_EXACT_MATH | [4, 72] | $\pi_{4}^{3} = \mathbb{Z}/2\{\eta_{3}\}$. |
| 68 | MATH_WITHOUT_EXACT_STEP | [] | 完全性より, $\ker \Delta=\operatorname{Im}H=\pi_{6}^{5}$ である. |
| 70 | MATH_WITHOUT_EXACT_STEP | [] | これより, $\Delta: \pi_{6}^{5} \to \pi_{4}^{2}$ は零写像. |
| 72 | CONNECTOR_OR_PROSE | [] | 完全性より, |
| 75 | CONNECTOR_OR_PROSE | [] | E: \pi_{4}^{2} \to \pi_{5}^{3}\quad\text{は単射}. \qquad (1) |
| 79 | MATH_WITHOUT_EXACT_STEP | [] | \pi_{6}^{5} \xrightarrow{\Delta} \pi_{4}^{2} \xrightarrow{E} \pi_{5}^{3} \xrightarrow{H} \pi_{5}^{5}. |
| 82 | STEP_EXACT_MATH | [49, 70] | $\Delta: \pi_{5}^{5} \to \pi_{3}^{2}$ は単射. |
| 84 | MATH_WITHOUT_EXACT_STEP | [] | 完全性より, これより, $H: \pi_{5}^{3} \to \pi_{5}^{5}$ は零写像. |
| 86 | CONNECTOR_OR_PROSE | [] | 完全性より, |
| 89 | CONNECTOR_OR_PROSE | [] | E: \pi_{4}^{2} \to \pi_{5}^{3}\quad\text{は全射}. \qquad (2) |
| 92 | MATH_WITHOUT_EXACT_STEP | [] | (1), (2) より, $E: \pi_{4}^{2} \to \pi_{5}^{3}$ は同型. |
| 94 | MATH_WITHOUT_EXACT_STEP | [] | $\eta_{4}=E\eta_{3}$. |
| 96 | MATH_WITHOUT_EXACT_STEP | [] | $\eta_{3}\eta_{3} = \eta_{3}^{2}$. |
| 98 | CONNECTOR_OR_PROSE | [] | これより, 以上より, |
| 100 | STEP_EXACT_MATH | [0] | $\pi_{5}^{3} = \mathbb{Z}/2\{\eta_{3}^{2}\}$. |
| 102 | TRANSPORT_APPENDIX | [4, 63, 64, 72, 73] | 証明木に記録された群構造の移送について、$\pi_{4}^{3} = \mathbb{Z}/2\{\eta_{3}\}$ と $E^{n - 3}: \pi_{3 + 1}^{3} \xrightarrow{\cong} \pi_{n + 1}^{n}$ から $\pi_{n + 1}^{n} = \mathbb{Z} |

## 証明木の全ノード

| ノード | 深さ | 規則 | 前提 | 親 | 文献 | 数式 | 本文行 |
|---:|---:|---|---|---|---|---|---|
| 0 | 0 | inference | [1, 2, 3] | [] | Proposition 5.3 | \pi_{5}^{3} = \mathbb{Z}/2\{\eta_{3}^{2}\} | [100] |
| 1 | 1 | inference | [4, 5] | [0] | (5.2) | \pi_{4}^{2} = \mathbb{Z}/2\{\eta_{2}^{2}\} | [32] |
| 2 | 1 | inference | [6, 7] | [0] | Proposition 5.3 | E: \pi_{4}^{2} \xrightarrow{\cong} \pi_{5}^{3} | [] |
| 3 | 1 | inference | [8, 9] | [0] | None | E\eta_{2}\eta_{3} = \eta_{3}\eta_{4} | [] |
| 4 | 2 | inference | [10, 11] | [1] | None | \pi_{4}^{3} = \mathbb{Z}/2\{\eta_{3}\} | [50, 66, 102] |
| 5 | 2 | inference | [12, 13, 14] | [1] | (5.2) | Toda52CompositionIsomorphismStatement | [] |
| 6 | 2 | inference | [15, 16] | [2] | Proposition 5.3 | E: \pi_{4}^{2} \to \pi_{5}^{3} \text{ is injective} | [] |
| 7 | 2 | inference | [17, 18] | [2] | Proposition 5.3 | E: \pi_{4}^{2} \to \pi_{5}^{3} \text{ is surjective} | [] |
| 8 | 2 | given | [] | [3] | None | TodaEtaFamilyDefinitionStatement | [] |
| 9 | 2 | given | [] | [3] | None | TodaEtaFamilyDefinitionStatement | [] |
| 10 | 3 | inference | [19, 20, 21] | [4] | None | \pi_{4}^{3} = \mathbb{Z}/2\{E\eta_{2}\} | [] |
| 11 | 3 | inference | [22] | [4] | None | \eta_{3} = E\eta_{2} | [] |
| 12 | 3 | inference | [23] | [5] | None | \pi_{i - 1}^{1} = 0 | [] |
| 13 | 3 | inference | [24, 25, 26] | [5, 14] | Proposition 4.4 | \left(\beta, γ\right) \mapsto E\beta + \eta_{2}γ\quad\text{は同型写像} | [] |
| 14 | 3 | inference | [13] | [5] | Proposition 4.4 | γ \mapsto \eta_{2}γ | [] |
| 15 | 3 | inference | [27, 28] | [6] | Proposition 5.3 | TodaDeltaZeroStatement | [] |
| 16 | 3 | given | [] | [6] | None | \pi_{6}^{5} \xrightarrow{\Delta} \pi_{4}^{2} \xrightarrow{E} \pi_{5}^{3} \text{ is exact} | [] |
| 17 | 3 | inference | [29, 30] | [7] | Proposition 5.3 | H: \pi_{5}^{3} \to \pi_{5}^{5} \text{ is the zero map} | [] |
| 18 | 3 | given | [] | [7] | None | \pi_{4}^{2} \xrightarrow{E} \pi_{5}^{3} \xrightarrow{H} \pi_{5}^{5} \text{ is exact} | [] |
| 19 | 4 | given | [] | [10] | None | \pi_{3}^{2} = \mathbb{Z}\{\eta_{2}\} | [34, 64] |
| 20 | 4 | inference | [31, 32] | [10] | None | \ker\left(E: \pi_{3}^{2} \to \pi_{4}^{3}\right) = \mathbb{Z}\{2\eta_{2}\} | [] |
| 21 | 4 | inference | [33, 34] | [10] | None | E: \pi_{3}^{2} \to \pi_{4}^{3} \text{ is surjective} | [] |
| 22 | 4 | given | [] | [11] | None | TodaEtaFamilyDefinitionStatement | [] |
| 23 | 4 | given | [] | [12] | None | i \ge 3 | [] |
| 24 | 4 | inference | [35, 36] | [13, 25] | None | H(\eta_{2}) = \iota_{3} | [] |
| 25 | 4 | inference | [24] | [13] | None | H\left(\eta_{2}\right) = \iota_{3} | [] |
| 26 | 4 | given | [] | [13] | None | (\beta, γ) \mapsto E\beta + \eta_{2}γ | [] |
| 27 | 4 | inference | [37, 38] | [15] | Proposition 5.3 | H: \pi_{6}^{3} \to \pi_{6}^{5} \text{ is surjective} | [] |
| 28 | 4 | given | [] | [15] | None | \pi_{6}^{3} \xrightarrow{H} \pi_{6}^{5} \xrightarrow{\Delta} \pi_{4}^{2} \text{ is exact} | [] |
| 29 | 4 | inference | [38] | [17] | Proposition 5.1 | \Delta: \pi_{5}^{5} \to \pi_{3}^{2} \text{ is injective} | [] |
| 30 | 4 | given | [] | [17] | None | \pi_{5}^{3} \xrightarrow{H} \pi_{5}^{5} \xrightarrow{\Delta} \pi_{3}^{2} \text{ is exact} | [] |
| 31 | 5 | inference | [39, 40, 41] | [20] | None | \operatorname{Im}\left(\Delta: \pi_{5}^{5} \to \pi_{3}^{2}\right) = \mathbb{Z}\{2\eta_{2}\} | [] |
| 32 | 5 | given | [] | [20] | None | \pi_{5}^{5} \xrightarrow{\Delta} \pi_{3}^{2} \xrightarrow{E} \pi_{4}^{3} \text{ is exact} | [] |
| 33 | 5 | given | [] | [21] | None | \pi_{4}^{5} = 0 | [48, 62] |
| 34 | 5 | given | [] | [21] | None | \pi_{3}^{2} \xrightarrow{E} \pi_{4}^{3} \xrightarrow{H} \pi_{4}^{5} \text{ is exact} | [] |
| 35 | 5 | inference | [42, 43] | [24] | None | H: \pi_{3}^{2} \xrightarrow{\cong} \pi_{3}^{3} | [] |
| 36 | 5 | given | [] | [24] | None | \pi_{3}^{3} = \mathbb{Z}\{\iota_{3}\} | [] |
| 37 | 5 | inference | [44] | [27] | (5.3) | H\left(\nu'\right) = \eta_{5} | [10] |
| 38 | 5 | inference | [45, 46, 47, 48] | [27, 29] | Proposition 5.1 | TodaProp51FiniteDimensionalStatement | [] |
| 39 | 6 | given | [] | [31] | None | \pi_{5}^{5} = \mathbb{Z}\{\iota_{5}\} | [36, 52] |
| 40 | 6 | inference | [49] | [31] | None | \Delta\left(\iota_{5}\right) = \pm [\iota_{2}, \iota_{2}] | [38, 54] |
| 41 | 6 | inference | [50, 51, 52, 53] | [31] | None | [\iota_{2}, \iota_{2}] = \pm 2\eta_{2} | [] |
| 42 | 6 | inference | [54, 55] | [35] | None | TodaHopfInvariantInjectiveStatement | [] |
| 43 | 6 | inference | [56, 57] | [35] | None | H: \pi_{3}^{2} \to \pi_{3}^{3} \text{ is surjective} | [] |
| 44 | 6 | given | [] | [37] | (5.3) | H\left(\nu'\right) = \eta_{5} | [10] |
| 45 | 6 | inference | [58, 59, 60] | [38, 82] | None | \pi_{3}^{2} = \mathbb{Z}\{\eta_{2}\} | [34, 64] |
| 46 | 6 | inference | [60] | [38, 62] | None | H\left(\eta_{2}\right) = \iota_{3} | [] |
| 47 | 6 | inference | [61, 62] | [38] | None | \Delta\left(\iota_{5}\right) = \pm 2\eta_{2} | [] |
| 48 | 6 | inference | [63, 64] | [38] | None | \pi_{n + 1}^{n} = \mathbb{Z}/2\{\eta_{n}\} | [] |
| 49 | 7 | given | [] | [40] | None | \Delta: \pi_{5}^{5} \to \pi_{3}^{2} | [82] |
| 50 | 7 | inference | [65] | [41] | Proposition 2.7 | H([\iota_{2}, \iota_{2}]) = \pm 2\iota_{3} | [42, 58] |
| 51 | 7 | given | [] | [41] | None | H(\eta_{2}) = \iota_{3} | [] |
| 52 | 7 | given | [] | [41] | None | H\left(\eta_{2}\right) = \iota_{3} | [] |
| 53 | 7 | given | [] | [41] | None | TodaHopfInvariantInjectiveStatement | [] |
| 54 | 7 | given | [] | [42] | None | \pi_{2}^{1} = 0 | [] |
| 55 | 7 | given | [] | [42] | None | \pi_{2}^{1} \xrightarrow{E} \pi_{3}^{2} \xrightarrow{H} \pi_{3}^{3} \text{ is exact} | [] |
| 56 | 7 | inference | [66, 67] | [43] | None | TodaDeltaZeroStatement | [] |
| 57 | 7 | given | [] | [43] | None | \pi_{3}^{2} \xrightarrow{H} \pi_{3}^{3} \xrightarrow{\Delta} \pi_{1}^{1} \text{ is exact} | [] |
| 58 | 7 | inference | [68, 69] | [45, 60] | None | H: \pi_{3}^{2} \xrightarrow{\cong} \pi_{3}^{3} | [] |
| 59 | 7 | given | [] | [45, 60] | None | \pi_{3}^{3} = \mathbb{Z}\{\iota_{3}\} | [] |
| 60 | 7 | inference | [58, 59] | [45, 46, 62] | None | H(\eta_{2}) = \iota_{3} | [] |
| 61 | 7 | inference | [70] | [47, 92] | None | \Delta\left(\iota_{5}\right) = \pm [\iota_{2}, \iota_{2}] | [38, 54] |
| 62 | 7 | inference | [71, 60, 46, 68] | [47, 92] | None | [\iota_{2}, \iota_{2}] = \pm 2\eta_{2} | [] |
| 63 | 7 | inference | [72, 73] | [48] | (4.5) | \pi_{n + 1}^{n} = \mathbb{Z}/2\{E^{n - 3}\eta_{3}\} | [60, 102] |
| 64 | 7 | inference | [74, 75] | [48] | None | E^{n - 3}\eta_{3} = \eta_{n} | [102] |
| 65 | 8 | given | [] | [50] | None | [\iota_{2}, \iota_{2}] | [40, 56] |
| 66 | 8 | inference | [76] | [56] | None | E: \pi_{1}^{1} \to \pi_{2}^{2} \text{ is injective} | [] |
| 67 | 8 | given | [] | [56] | None | \pi_{3}^{3} \xrightarrow{\Delta} \pi_{1}^{1} \xrightarrow{E} \pi_{2}^{2} \text{ is exact} | [] |
| 68 | 8 | inference | [77, 78] | [58, 62] | None | TodaHopfInvariantInjectiveStatement | [] |
| 69 | 8 | inference | [79, 80] | [58] | None | H: \pi_{3}^{2} \to \pi_{3}^{3} \text{ is surjective} | [] |
| 70 | 8 | given | [] | [61] | None | \Delta: \pi_{5}^{5} \to \pi_{3}^{2} | [82] |
| 71 | 8 | inference | [81] | [62] | Proposition 2.7 | H([\iota_{2}, \iota_{2}]) = \pm 2\iota_{3} | [42, 58] |
| 72 | 8 | inference | [82, 75] | [63] | None | \pi_{4}^{3} = \mathbb{Z}/2\{\eta_{3}\} | [50, 66, 102] |
| 73 | 8 | inference | [83, 84, 85] | [63] | (4.5) | E^{n - 3}: \pi_{3 + 1}^{3} \xrightarrow{\cong} \pi_{n + 1}^{n} | [102] |
| 74 | 8 | given | [] | [64] | None | TodaEtaFamilyDefinitionStatement | [] |
| 75 | 8 | inference | [86] | [64, 72] | None | \eta_{3} = E\eta_{2} | [] |
| 76 | 9 | given | [] | [66] | None | E: \pi_{1}^{1} \xrightarrow{\cong} \pi_{2}^{2} | [] |
| 77 | 9 | given | [] | [68] | None | \pi_{2}^{1} = 0 | [] |
| 78 | 9 | given | [] | [68] | None | \pi_{2}^{1} \xrightarrow{E} \pi_{3}^{2} \xrightarrow{H} \pi_{3}^{3} \text{ is exact} | [] |
| 79 | 9 | inference | [87, 88] | [69] | None | TodaDeltaZeroStatement | [] |
| 80 | 9 | given | [] | [69] | None | \pi_{3}^{2} \xrightarrow{H} \pi_{3}^{3} \xrightarrow{\Delta} \pi_{1}^{1} \text{ is exact} | [] |
| 81 | 9 | given | [] | [71] | None | [\iota_{2}, \iota_{2}] | [40, 56] |
| 82 | 9 | inference | [45, 89, 90] | [72] | None | \pi_{4}^{3} = \mathbb{Z}/2\{E\eta_{2}\} | [] |
| 83 | 9 | given | [] | [73] | None | 3 \ge 1 + 2 | [] |
| 84 | 9 | given | [] | [73] | None | n \ge 3 | [] |
| 85 | 9 | given | [] | [73] | None | E^{n - 3}: \pi_{3 + 1}^{3} \to \pi_{n + 1}^{n} | [12] |
| 86 | 9 | given | [] | [75] | None | TodaEtaFamilyDefinitionStatement | [] |
| 87 | 10 | inference | [91] | [79] | None | E: \pi_{1}^{1} \to \pi_{2}^{2} \text{ is injective} | [] |
| 88 | 10 | given | [] | [79] | None | \pi_{3}^{3} \xrightarrow{\Delta} \pi_{1}^{1} \xrightarrow{E} \pi_{2}^{2} \text{ is exact} | [] |
| 89 | 10 | inference | [92, 93] | [82] | None | \ker\left(E: \pi_{3}^{2} \to \pi_{4}^{3}\right) = \mathbb{Z}\{2\eta_{2}\} | [] |
| 90 | 10 | inference | [94, 95] | [82] | None | E: \pi_{3}^{2} \to \pi_{4}^{3} \text{ is surjective} | [] |
| 91 | 11 | given | [] | [87] | None | E: \pi_{1}^{1} \xrightarrow{\cong} \pi_{2}^{2} | [] |
| 92 | 11 | inference | [96, 61, 62] | [89] | None | \operatorname{Im}\left(\Delta: \pi_{5}^{5} \to \pi_{3}^{2}\right) = \mathbb{Z}\{2\eta_{2}\} | [] |
| 93 | 11 | given | [] | [89] | None | \pi_{5}^{5} \xrightarrow{\Delta} \pi_{3}^{2} \xrightarrow{E} \pi_{4}^{3} \text{ is exact} | [] |
| 94 | 11 | given | [] | [90] | None | \pi_{4}^{5} = 0 | [48, 62] |
| 95 | 11 | given | [] | [90] | None | \pi_{3}^{2} \xrightarrow{E} \pi_{4}^{3} \xrightarrow{H} \pi_{4}^{5} \text{ is exact} | [] |
| 96 | 12 | given | [] | [92] | None | \pi_{5}^{5} = \mathbb{Z}\{\iota_{5}\} | [36, 52] |

## 同じ数式を持つ複数ノード

- [4, 72]: `\pi_{4}^{3} = \mathbb{Z}/2\{\eta_{3}\}`
- [10, 82]: `\pi_{4}^{3} = \mathbb{Z}/2\{E\eta_{2}\}`
- [11, 75]: `\eta_{3} = E\eta_{2}`
- [19, 45]: `\pi_{3}^{2} = \mathbb{Z}\{\eta_{2}\}`
- [20, 89]: `\ker\left(E: \pi_{3}^{2} \to \pi_{4}^{3}\right) = \mathbb{Z}\{2\eta_{2}\}`
- [21, 90]: `E: \pi_{3}^{2} \to \pi_{4}^{3} \text{ is surjective}`
- [24, 25, 46, 51, 52, 60]: `H(\eta_{2}) = \iota_{3}`
- [31, 92]: `\operatorname{Im}\left(\Delta: \pi_{5}^{5} \to \pi_{3}^{2}\right) = \mathbb{Z}\{2\eta_{2}\}`
- [32, 93]: `\pi_{5}^{5} \xrightarrow{\Delta} \pi_{3}^{2} \xrightarrow{E} \pi_{4}^{3} \text{ is exact}`
- [33, 94]: `\pi_{4}^{5} = 0`
- [34, 95]: `\pi_{3}^{2} \xrightarrow{E} \pi_{4}^{3} \xrightarrow{H} \pi_{4}^{5} \text{ is exact}`
- [35, 58]: `H: \pi_{3}^{2} \xrightarrow{\cong} \pi_{3}^{3}`
- [36, 59]: `\pi_{3}^{3} = \mathbb{Z}\{\iota_{3}\}`
- [37, 44]: `H\left(\nu'\right) = \eta_{5}`
- [39, 96]: `\pi_{5}^{5} = \mathbb{Z}\{\iota_{5}\}`
- [40, 61]: `\Delta\left(\iota_{5}\right) = \pm [\iota_{2}, \iota_{2}]`
- [41, 62]: `[\iota_{2}, \iota_{2}] = \pm 2\eta_{2}`
- [43, 69]: `H: \pi_{3}^{2} \to \pi_{3}^{3} \text{ is surjective}`
- [49, 70]: `\Delta: \pi_{5}^{5} \to \pi_{3}^{2}`
- [50, 71]: `H([\iota_{2}, \iota_{2}]) = \pm 2\iota_{3}`
- [54, 77]: `\pi_{2}^{1} = 0`
- [55, 78]: `\pi_{2}^{1} \xrightarrow{E} \pi_{3}^{2} \xrightarrow{H} \pi_{3}^{3} \text{ is exact}`
- [57, 80]: `\pi_{3}^{2} \xrightarrow{H} \pi_{3}^{3} \xrightarrow{\Delta} \pi_{1}^{1} \text{ is exact}`
- [65, 81]: `[\iota_{2}, \iota_{2}]`
- [66, 87]: `E: \pi_{1}^{1} \to \pi_{2}^{2} \text{ is injective}`
- [67, 88]: `\pi_{3}^{3} \xrightarrow{\Delta} \pi_{1}^{1} \xrightarrow{E} \pi_{2}^{2} \text{ is exact}`
- [76, 91]: `E: \pi_{1}^{1} \xrightarrow{\cong} \pi_{2}^{2}`

## stable 移送追加段落

証明木に記録された群構造の移送について、$\pi_{4}^{3} = \mathbb{Z}/2\{\eta_{3}\}$ と $E^{n - 3}: \pi_{3 + 1}^{3} \xrightarrow{\cong} \pi_{n + 1}^{n}$ から $\pi_{n + 1}^{n} = \mathbb{Z}/2\{E^{n - 3}\eta_{3}\}$ を得る。生成元の対応は $E^{n - 3}\eta_{3} = \eta_{n}$ である。

## 注意

Exact LaTeX matching finds candidate origins, not proof of semantic relevance. Non-matches may reflect formatting or multi-line LaTeX.
