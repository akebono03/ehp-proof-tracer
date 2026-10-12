# Phase 163 R4-R80：命題本文の正式登録前チェック

登録前の条件・主張順・境界問題の監査。正式採用ではありません。

| Reference | 順序 | 候補キー | 要追加確認 |
|---|---:|---|---:|
| prop:1-6 | 1 | `proposal:prop:1-6:last_argument_additivity` | 0 |
| prop:1-6 | 2 | `proposal:prop:1-6:middle_argument_additivity` | 1 |
| prop:1-6 | 3 | `proposal:prop:1-6:first_argument_additivity` | 2 |
| thm:2.4 | 1 | `proposal:thm:2.4:odd_dimension_case` | 0 |
| thm:2.4 | 2 | `proposal:thm:2.4:even_dimension_case` | 1 |
| prop:2.5 | 1 | `proposal:prop:2.5:delta_composition` | 1 |
| prop:2.5 | 2 | `proposal:prop:2.5:whitehead_product_case` | 1 |
| prop:4.2 | 1 | `proposal:prop:4.2:ehp_exact_sequence` | 1 |

## 登録前の未解決問題

- `proposal:prop:1-6:middle_argument_additivity`: The initial variable declarations are inherited from the first item; include shared variable types in scope.
- `proposal:prop:1-6:first_argument_additivity`: The initial variable declarations are inherited from the first item; include shared variable types in scope.
- `proposal:prop:1-6:first_argument_additivity`: Extracted snippet starts with the previous item’s trailing 「が成り立つ。」; a semantic boundary adjustment is needed.
- `proposal:thm:2.4:even_dimension_case`: The even-dimensional item contains both the range-limited isomorphism and the all-degree p-component isomorphism. Consider two Assertions under the same Reference.
- `proposal:prop:2.5:delta_composition`: The equalities replacing inclusion relations have shared conditions (odd m, j<3m-1, or 2-primary components); do not omit them.
- `proposal:prop:2.5:whitehead_product_case`: The equalities replacing inclusion relations have shared conditions (odd m, j<3m-1, or 2-primary components); do not omit them.
- `proposal:prop:4.2:ehp_exact_sequence`: Equation (4.4) is embedded in Proposition 4.2. Detect duplicate Reference registration before allocating a permanent ID.

現行全 Registry との意味的重複確認・原本照合・正式な数学的検証・ID 採番は未実施。
