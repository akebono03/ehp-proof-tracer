# Phase 162 R10-R6：本文と証明木の個別原因監査

## 集計

- body_rows: 47
- diagnoses: {'NO_STEP_TEXT_MATCH': 19, 'PARTIAL_EXPRESSION_ONLY': 7, 'DIRECT_STEP_CANDIDATE': 21}
- tags: {'NO_EXACT_LATEX_MATCH': 16, 'OFF_TARGET_H_MAP': 2, 'DELTA_IOTA5': 2, 'WHITEHEAD_SQUARE': 6, 'TRANSPORT_APPENDIX': 1}
- duplicate_text_groups: 6
- duplicate_math_node_groups: 27

## 優先調査項目

### OFF_TARGET_H_MAP：2 行

- 本文行 26：完全性より, $H: \pi_{3}^{2} \to \pi_{3}^{3}$ は単射.
  - 数式完全一致ノード：[]
  - 部分一致候補：[43, 69]
  - 最終結論への経路：{'43': [43, 35, 24, 13, 5, 1, 0], '69': [69, 58, 45, 38, 27, 15, 6, 2, 0]}
  - 同文の重複行：[]
  - 同数式の重複ノード：[]
- 本文行 28：完全性より, $H: \pi_{3}^{2} \to \pi_{3}^{3}$ は全射.
  - 数式完全一致ノード：[]
  - 部分一致候補：[43, 69]
  - 最終結論への経路：{'43': [43, 35, 24, 13, 5, 1, 0], '69': [69, 58, 45, 38, 27, 15, 6, 2, 0]}
  - 同文の重複行：[]
  - 同数式の重複ノード：[]

### DELTA_IOTA5：2 行

- 本文行 38：$\Delta\left(\iota_{5}\right) = \pm [\iota_{2}, \iota_{2}]$.
  - 数式完全一致ノード：[40, 61]
  - 部分一致候補：[65, 81]
  - 最終結論への経路：{'40': [40, 31, 20, 10, 4, 1, 0], '61': [61, 47, 38, 27, 15, 6, 2, 0]}
  - 同文の重複行：[38, 54]
  - 同数式の重複ノード：[40, 61]
- 本文行 54：$\Delta\left(\iota_{5}\right) = \pm [\iota_{2}, \iota_{2}]$.
  - 数式完全一致ノード：[40, 61]
  - 部分一致候補：[65, 81]
  - 最終結論への経路：{'40': [40, 31, 20, 10, 4, 1, 0], '61': [61, 47, 38, 27, 15, 6, 2, 0]}
  - 同文の重複行：[38, 54]
  - 同数式の重複ノード：[40, 61]

### WHITEHEAD_SQUARE：6 行

- 本文行 38：$\Delta\left(\iota_{5}\right) = \pm [\iota_{2}, \iota_{2}]$.
  - 数式完全一致ノード：[40, 61]
  - 部分一致候補：[65, 81]
  - 最終結論への経路：{'40': [40, 31, 20, 10, 4, 1, 0], '61': [61, 47, 38, 27, 15, 6, 2, 0]}
  - 同文の重複行：[38, 54]
  - 同数式の重複ノード：[40, 61]
- 本文行 40：$[\iota_{2}, \iota_{2}]$.
  - 数式完全一致ノード：[65, 81]
  - 部分一致候補：[40, 41, 50, 61, 62, 71]
  - 最終結論への経路：{'65': [65, 50, 41, 31, 20, 10, 4, 1, 0], '81': [81, 71, 62, 47, 38, 27, 15, 6, 2, 0]}
  - 同文の重複行：[40, 56]
  - 同数式の重複ノード：[65, 81]
- 本文行 42：これより, $H([\iota_{2}, \iota_{2}]) = \pm 2\iota_{3}$ が成り立つ.
  - 数式完全一致ノード：[50, 71]
  - 部分一致候補：[65, 81]
  - 最終結論への経路：{'50': [50, 41, 31, 20, 10, 4, 1, 0], '71': [71, 62, 47, 38, 27, 15, 6, 2, 0]}
  - 同文の重複行：[42, 58]
  - 同数式の重複ノード：[50, 71]
- 本文行 54：$\Delta\left(\iota_{5}\right) = \pm [\iota_{2}, \iota_{2}]$.
  - 数式完全一致ノード：[40, 61]
  - 部分一致候補：[65, 81]
  - 最終結論への経路：{'40': [40, 31, 20, 10, 4, 1, 0], '61': [61, 47, 38, 27, 15, 6, 2, 0]}
  - 同文の重複行：[38, 54]
  - 同数式の重複ノード：[40, 61]
- 本文行 56：$[\iota_{2}, \iota_{2}]$.
  - 数式完全一致ノード：[65, 81]
  - 部分一致候補：[40, 41, 50, 61, 62, 71]
  - 最終結論への経路：{'65': [65, 50, 41, 31, 20, 10, 4, 1, 0], '81': [81, 71, 62, 47, 38, 27, 15, 6, 2, 0]}
  - 同文の重複行：[40, 56]
  - 同数式の重複ノード：[65, 81]
- 本文行 58：これより, $H([\iota_{2}, \iota_{2}]) = \pm 2\iota_{3}$ が成り立つ.
  - 数式完全一致ノード：[50, 71]
  - 部分一致候補：[65, 81]
  - 最終結論への経路：{'50': [50, 41, 31, 20, 10, 4, 1, 0], '71': [71, 62, 47, 38, 27, 15, 6, 2, 0]}
  - 同文の重複行：[42, 58]
  - 同数式の重複ノード：[50, 71]

### TRANSPORT_APPENDIX：1 行

- 本文行 102：証明木に記録された群構造の移送について、$\pi_{4}^{3} = \mathbb{Z}/2\{\eta_{3}\}$ と $E^{n - 3}: \pi_{3 + 1}^{3} \xrightarrow{\cong} \pi_{n + 1}^{n}$ から $\pi_{n + 1}^{n} = \mathbb{Z}/2\{E^{n - 3}\eta_{3}\}$ を得る。生成元の対応は $E^{n - 3}\eta_{3} = \eta_{n}$ である。
  - 数式完全一致ノード：[4, 63, 64, 72, 73]
  - 部分一致候補：[]
  - 最終結論への経路：{'4': [4, 1, 0], '63': [63, 48, 38, 27, 15, 6, 2, 0], '64': [64, 48, 38, 27, 15, 6, 2, 0], '72': [72, 63, 48, 38, 27, 15, 6, 2, 0], '73': [73, 63, 48, 38, 27, 15, 6, 2, 0]}
  - 同文の重複行：[]
  - 同数式の重複ノード：[4, 63, 64, 72, 73]

## 数式完全一致がない項目

- 行 4：\pi_{5}^{3} = \mathbb{Z}/2\{\eta_{3}^{2}\}.
  - 部分一致候補：[0]、診断：PARTIAL_EXPRESSION_ONLY
- 行 18：$\pi_{5}^{3}$ の群構造を決定するために, 次の完全列を考える.
  - 部分一致候補：[]、診断：NO_STEP_TEXT_MATCH
- 行 21：\pi_{6}^{3} \xrightarrow{H} \pi_{6}^{5} \xrightarrow{\Delta} \pi_{4}^{2} \xrightarrow{E} \pi_{5}^{3} \xrightarrow{H} \pi_{5}^{5} \xrightarrow{\Delta} \pi_{3}^{2} \xrightarrow{E} \pi_{4}^{3} \xrightarrow{H} \pi_{4}^{5}.
  - 部分一致候補：[]、診断：NO_STEP_TEXT_MATCH
- 行 24：[R1]より, $H: \pi_{6}^{3} \to \pi_{6}^{5}$ は全射.
  - 部分一致候補：[27]、診断：PARTIAL_EXPRESSION_ONLY
- 行 26：完全性より, $H: \pi_{3}^{2} \to \pi_{3}^{3}$ は単射.
  - 部分一致候補：[43, 69]、診断：PARTIAL_EXPRESSION_ONLY
- 行 28：完全性より, $H: \pi_{3}^{2} \to \pi_{3}^{3}$ は全射.
  - 部分一致候補：[43, 69]、診断：PARTIAL_EXPRESSION_ONLY
- 行 30：完全性より, $E: \pi_{3}^{2} \to \pi_{4}^{3}$ は全射.
  - 部分一致候補：[20, 21, 89, 90]、診断：PARTIAL_EXPRESSION_ONLY
- 行 44：$\operatorname{Im}\Delta = \mathbb{Z}\{2\eta_{2}\}$.
  - 部分一致候補：[]、診断：NO_STEP_TEXT_MATCH
- 行 46：完全性より, $\ker E=\operatorname{Im}Δ=\mathbb{Z}\{2\eta_{2}\}$.
  - 部分一致候補：[]、診断：NO_STEP_TEXT_MATCH
- 行 68：完全性より, $\ker \Delta=\operatorname{Im}H=\pi_{6}^{5}$ である.
  - 部分一致候補：[]、診断：NO_STEP_TEXT_MATCH
- 行 70：これより, $\Delta: \pi_{6}^{5} \to \pi_{4}^{2}$ は零写像.
  - 部分一致候補：[]、診断：NO_STEP_TEXT_MATCH
- 行 79：\pi_{6}^{5} \xrightarrow{\Delta} \pi_{4}^{2} \xrightarrow{E} \pi_{5}^{3} \xrightarrow{H} \pi_{5}^{5}.
  - 部分一致候補：[]、診断：NO_STEP_TEXT_MATCH
- 行 84：完全性より, これより, $H: \pi_{5}^{3} \to \pi_{5}^{5}$ は零写像.
  - 部分一致候補：[17]、診断：PARTIAL_EXPRESSION_ONLY
- 行 92：(1), (2) より, $E: \pi_{4}^{2} \to \pi_{5}^{3}$ は同型.
  - 部分一致候補：[6, 7]、診断：PARTIAL_EXPRESSION_ONLY
- 行 94：$\eta_{4}=E\eta_{3}$.
  - 部分一致候補：[]、診断：NO_STEP_TEXT_MATCH
- 行 96：$\eta_{3}\eta_{3} = \eta_{3}^{2}$.
  - 部分一致候補：[]、診断：NO_STEP_TEXT_MATCH

## 全本文項目

| 行 | 原分類 | 判定 | 一致ノード | 部分候補 | 重複行 | 本文 |
|---:|---|---|---|---|---|---|
| 1 | CONNECTOR_OR_PROSE | NO_STEP_TEXT_MATCH | [] | [] | [] | 対象 |
| 4 | MATH_WITHOUT_EXACT_STEP | PARTIAL_EXPRESSION_ONLY | [] | [0] | [] | \pi_{5}^{3} = \mathbb{Z}/2\{\eta_{3}^{2}\}. |
| 7 | CONNECTOR_OR_PROSE | NO_STEP_TEXT_MATCH | [] | [] | [] | ## 使用する結果 |
| 9 | CONNECTOR_OR_PROSE | NO_STEP_TEXT_MATCH | [] | [] | [] | **[R1] (5.3).** |
| 10 | STEP_EXACT_MATH | DIRECT_STEP_CANDIDATE | [37, 44] | [] | [] | $H\left(\nu'\right) = \eta_{5}$. |
| 11 | CONNECTOR_OR_PROSE | NO_STEP_TEXT_MATCH | [] | [] | [] | **[R2] (4.5).** |
| 12 | STEP_EXACT_MATH | DIRECT_STEP_CANDIDATE | [85] | [] | [] | $E^{n - 3}: \pi_{3 + 1}^{3} \to \pi_{n + 1}^{n}$ は同型. |
| 16 | CONNECTOR_OR_PROSE | NO_STEP_TEXT_MATCH | [] | [] | [] | ## 証明 |
| 18 | MATH_WITHOUT_EXACT_STEP | NO_STEP_TEXT_MATCH | [] | [] | [] | $\pi_{5}^{3}$ の群構造を決定するために, 次の完全列を考える. |
| 21 | MATH_WITHOUT_EXACT_STEP | NO_STEP_TEXT_MATCH | [] | [] | [] | \pi_{6}^{3} \xrightarrow{H} \pi_{6}^{5} \xrightarrow{\Delta} \pi_{4}^{2} \xrightarrow{E} \pi_{5}^{3} \xrightarrow{H} \pi_{5}^{5} \xrightarro |
| 24 | MATH_WITHOUT_EXACT_STEP | PARTIAL_EXPRESSION_ONLY | [] | [27] | [] | [R1]より, $H: \pi_{6}^{3} \to \pi_{6}^{5}$ は全射. |
| 26 | MATH_WITHOUT_EXACT_STEP | PARTIAL_EXPRESSION_ONLY | [] | [43, 69] | [] | 完全性より, $H: \pi_{3}^{2} \to \pi_{3}^{3}$ は単射. |
| 28 | MATH_WITHOUT_EXACT_STEP | PARTIAL_EXPRESSION_ONLY | [] | [43, 69] | [] | 完全性より, $H: \pi_{3}^{2} \to \pi_{3}^{3}$ は全射. |
| 30 | MATH_WITHOUT_EXACT_STEP | PARTIAL_EXPRESSION_ONLY | [] | [20, 21, 89, 90] | [] | 完全性より, $E: \pi_{3}^{2} \to \pi_{4}^{3}$ は全射. |
| 32 | STEP_EXACT_MATH | DIRECT_STEP_CANDIDATE | [1] | [] | [] | $\pi_{4}^{2} = \mathbb{Z}/2\{\eta_{2}^{2}\}$. |
| 34 | STEP_EXACT_MATH | DIRECT_STEP_CANDIDATE | [19, 45] | [] | [] | $\pi_{3}^{2} = \mathbb{Z}\{\eta_{2}\}$. |
| 36 | STEP_EXACT_MATH | DIRECT_STEP_CANDIDATE | [39, 96] | [] | [] | $\pi_{5}^{5} = \mathbb{Z}\{\iota_{5}\}$. |
| 38 | STEP_EXACT_MATH | DIRECT_STEP_CANDIDATE | [40, 61] | [65, 81] | [38, 54] | $\Delta\left(\iota_{5}\right) = \pm [\iota_{2}, \iota_{2}]$. |
| 40 | STEP_EXACT_MATH | DIRECT_STEP_CANDIDATE | [65, 81] | [40, 41, 50, 61, 62, 71] | [40, 56] | $[\iota_{2}, \iota_{2}]$. |
| 42 | STEP_EXACT_MATH | DIRECT_STEP_CANDIDATE | [50, 71] | [65, 81] | [42, 58] | これより, $H([\iota_{2}, \iota_{2}]) = \pm 2\iota_{3}$ が成り立つ. |
| 44 | MATH_WITHOUT_EXACT_STEP | NO_STEP_TEXT_MATCH | [] | [] | [] | $\operatorname{Im}\Delta = \mathbb{Z}\{2\eta_{2}\}$. |
| 46 | MATH_WITHOUT_EXACT_STEP | NO_STEP_TEXT_MATCH | [] | [] | [] | 完全性より, $\ker E=\operatorname{Im}Δ=\mathbb{Z}\{2\eta_{2}\}$. |
| 48 | STEP_EXACT_MATH | DIRECT_STEP_CANDIDATE | [33, 94] | [] | [48, 62] | $\pi_{4}^{5} = 0$. |
| 50 | STEP_EXACT_MATH | DIRECT_STEP_CANDIDATE | [4, 72] | [] | [50, 66] | $\pi_{4}^{3} = \mathbb{Z}/2\{\eta_{3}\}$. |
| 52 | STEP_EXACT_MATH | DIRECT_STEP_CANDIDATE | [39, 96] | [] | [] | これより, $\pi_{5}^{5} = \mathbb{Z}\{\iota_{5}\}$. |
| 54 | STEP_EXACT_MATH | DIRECT_STEP_CANDIDATE | [40, 61] | [65, 81] | [38, 54] | $\Delta\left(\iota_{5}\right) = \pm [\iota_{2}, \iota_{2}]$. |
| 56 | STEP_EXACT_MATH | DIRECT_STEP_CANDIDATE | [65, 81] | [40, 41, 50, 61, 62, 71] | [40, 56] | $[\iota_{2}, \iota_{2}]$. |
| 58 | STEP_EXACT_MATH | DIRECT_STEP_CANDIDATE | [50, 71] | [65, 81] | [42, 58] | これより, $H([\iota_{2}, \iota_{2}]) = \pm 2\iota_{3}$ が成り立つ. |
| 60 | STEP_EXACT_MATH | DIRECT_STEP_CANDIDATE | [63] | [] | [] | [R2]より, $\pi_{n + 1}^{n} = \mathbb{Z}/2\{E^{n - 3}\eta_{3}\}$. |
| 62 | STEP_EXACT_MATH | DIRECT_STEP_CANDIDATE | [33, 94] | [] | [48, 62] | $\pi_{4}^{5} = 0$. |
| 64 | STEP_EXACT_MATH | DIRECT_STEP_CANDIDATE | [19, 45] | [] | [] | これより, $\pi_{3}^{2} = \mathbb{Z}\{\eta_{2}\}$. |
| 66 | STEP_EXACT_MATH | DIRECT_STEP_CANDIDATE | [4, 72] | [] | [50, 66] | $\pi_{4}^{3} = \mathbb{Z}/2\{\eta_{3}\}$. |
| 68 | MATH_WITHOUT_EXACT_STEP | NO_STEP_TEXT_MATCH | [] | [] | [] | 完全性より, $\ker \Delta=\operatorname{Im}H=\pi_{6}^{5}$ である. |
| 70 | MATH_WITHOUT_EXACT_STEP | NO_STEP_TEXT_MATCH | [] | [] | [] | これより, $\Delta: \pi_{6}^{5} \to \pi_{4}^{2}$ は零写像. |
| 72 | CONNECTOR_OR_PROSE | NO_STEP_TEXT_MATCH | [] | [] | [72, 86] | 完全性より, |
| 75 | CONNECTOR_OR_PROSE | NO_STEP_TEXT_MATCH | [] | [] | [] | E: \pi_{4}^{2} \to \pi_{5}^{3}\quad\text{は単射}. \qquad (1) |
| 79 | MATH_WITHOUT_EXACT_STEP | NO_STEP_TEXT_MATCH | [] | [] | [] | \pi_{6}^{5} \xrightarrow{\Delta} \pi_{4}^{2} \xrightarrow{E} \pi_{5}^{3} \xrightarrow{H} \pi_{5}^{5}. |
| 82 | STEP_EXACT_MATH | DIRECT_STEP_CANDIDATE | [49, 70] | [29, 31, 92] | [] | $\Delta: \pi_{5}^{5} \to \pi_{3}^{2}$ は単射. |
| 84 | MATH_WITHOUT_EXACT_STEP | PARTIAL_EXPRESSION_ONLY | [] | [17] | [] | 完全性より, これより, $H: \pi_{5}^{3} \to \pi_{5}^{5}$ は零写像. |
| 86 | CONNECTOR_OR_PROSE | NO_STEP_TEXT_MATCH | [] | [] | [72, 86] | 完全性より, |
| 89 | CONNECTOR_OR_PROSE | NO_STEP_TEXT_MATCH | [] | [] | [] | E: \pi_{4}^{2} \to \pi_{5}^{3}\quad\text{は全射}. \qquad (2) |
| 92 | MATH_WITHOUT_EXACT_STEP | PARTIAL_EXPRESSION_ONLY | [] | [6, 7] | [] | (1), (2) より, $E: \pi_{4}^{2} \to \pi_{5}^{3}$ は同型. |
| 94 | MATH_WITHOUT_EXACT_STEP | NO_STEP_TEXT_MATCH | [] | [] | [] | $\eta_{4}=E\eta_{3}$. |
| 96 | MATH_WITHOUT_EXACT_STEP | NO_STEP_TEXT_MATCH | [] | [] | [] | $\eta_{3}\eta_{3} = \eta_{3}^{2}$. |
| 98 | CONNECTOR_OR_PROSE | NO_STEP_TEXT_MATCH | [] | [] | [] | これより, 以上より, |
| 100 | STEP_EXACT_MATH | DIRECT_STEP_CANDIDATE | [0] | [] | [] | $\pi_{5}^{3} = \mathbb{Z}/2\{\eta_{3}^{2}\}$. |
| 102 | TRANSPORT_APPENDIX | DIRECT_STEP_CANDIDATE | [4, 63, 64, 72, 73] | [] | [] | 証明木に記録された群構造の移送について、$\pi_{4}^{3} = \mathbb{Z}/2\{\eta_{3}\}$ と $E^{n - 3}: \pi_{3 + 1}^{3} \xrightarrow{\cong} \pi_{n + 1}^{n}$ から $\pi_{n + |

## stable 移送段落

祖先中の移送経路由来。最終目標そのものへの移送かは未認証。

証明木に記録された群構造の移送について、$\pi_{4}^{3} = \mathbb{Z}/2\{\eta_{3}\}$ と $E^{n - 3}: \pi_{3 + 1}^{3} \xrightarrow{\cong} \pi_{n + 1}^{n}$ から $\pi_{n + 1}^{n} = \mathbb{Z}/2\{E^{n - 3}\eta_{3}\}$ を得る。生成元の対応は $E^{n - 3}\eta_{3} = \eta_{n}$ である。

## 解釈上の注意

- 同じ数学式の候補が複数ある場合、どれが実際に Renderer に採用されたかはこの JSON のみでは確定できない。
- 一致しない数式については、説明文中の合成式・数式フォーマットの違いも考えられる。
- 証明木から最終結論に到達する依存経路は、数学的必要性や前提の妥当性を証明しない。
