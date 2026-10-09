# Phase 162 R10-R3 — 97ノード分類とReference欠落監査

実 Web replay を対象にした読み取り専用結果。分類は排他的、tags は非排他的。

## 排他的分類

- CITED_BOUNDARY: **2** — nodes [41, 42]
- FIXED_STATEMENT: **5** — nodes [37, 39, 77, 82, 97]
- OTHER_GIVEN: **42** — nodes [1, 2, 3, 5, 7, 8, 9, 12, 14, 15, 18, 21, 23, 24, 26, 28, 30, 33, 36, 43, 44, 46, 48, 50, 53, 57, 59, 63, 65, 67, 68, 71, 74, 75, 76, 79, 84, 86, 89, 91, 94, 95]
- PROOF_INTERNAL: **11** — nodes [38, 40, 78, 83, 85, 87, 88, 90, 92, 93, 96]
- UNCLASSIFIED_INFERENCE: **37** — nodes [4, 6, 10, 11, 13, 16, 17, 19, 20, 22, 25, 27, 29, 31, 32, 34, 35, 45, 47, 49, 51, 52, 54, 55, 56, 58, 60, 61, 62, 64, 66, 69, 70, 72, 73, 80, 81]

合計 **97**

## 出典抽出の監査

- 文献抽出結果: {'Proposition 2.7': 2, 'Proposition 4.4': 2, '(5.2)': 2, '(5.3)': 1, '(4.5)': 2, 'Proposition 5.1': 2, 'Proposition 5.3': 7}
- foundational_reference のみで抽出不可: [41]

### Reference の段階別結果

- 生の抽出: [{'number': 1, 'locator': 'Proposition 5.3', 'rule_names': ['Toda Proposition 5.3 n=3 pi_5^3 finite-cyclic transport', 'Toda Proposition 5.3 n=3 suspension isomorphism', 'Toda Proposition 5.3 n=3 Delta zero implies suspension injective', 'Toda Proposition 5.3 n=3 Hopf zero implies suspension surjective', 'Toda Proposition 5.3 n=3 Hopf surjective implies Delta zero', 'Toda Proposition 5.3 n=3 Delta injectivity implies Hopf zero', 'Toda Proposition 5.3 n=3 Hopf eta_5 surjectivity'], 'step_count': 7}, {'number': 2, 'locator': '(5.2)', 'rule_names': ['Toda 5.2 pi_4^2 finite-cyclic transport', 'Toda 5.2 eta_2 composition isomorphism'], 'step_count': 2}, {'number': 3, 'locator': 'Proposition 4.4', 'rule_names': ['Toda Proposition 4.4 eta_2 n=2 specialization', 'Toda Proposition 4.4 eta_2 second-summand restriction'], 'step_count': 2}, {'number': 4, 'locator': 'Proposition 5.1', 'rule_names': ['Toda Proposition 5.1 n=3 Delta injectivity', 'Toda Proposition 5.1 finite-dimensional integration'], 'step_count': 2}, {'number': 5, 'locator': '(5.3)', 'rule_names': ['phase162_verified_literature_citation'], 'step_count': 1}, {'number': 6, 'locator': 'Proposition 2.7', 'rule_names': ['Toda Proposition 2.7 iota_2 Whitehead-square Hopf invariant up to sign', 'Toda Proposition 2.7 iota_2 Whitehead-square Hopf invariant up to sign'], 'step_count': 2}, {'number': 7, 'locator': '(4.5)', 'rule_names': ['Toda 4.5 pi_4^3 finite-cyclic transport', 'Toda 4.5 stable-range iterated suspension isomorphism'], 'step_count': 2}]
- 固定命題の選別後: [{'number': 1, 'locator': '(5.2)', 'rule_names': ['Toda 5.2 eta_2 composition isomorphism'], 'step_count': 1}, {'number': 2, 'locator': 'Proposition 4.4', 'rule_names': ['Toda Proposition 4.4 eta_2 n=2 specialization'], 'step_count': 1}, {'number': 3, 'locator': 'Proposition 5.1', 'rule_names': ['Toda Proposition 5.1 finite-dimensional integration'], 'step_count': 1}, {'number': 4, 'locator': '(4.5)', 'rule_names': ['Toda 4.5 stable-range iterated suspension isomorphism'], 'step_count': 1}]
- 実際の表示ラベル: ['(4.5).']

### 引用境界の各ノード

- {'key': 'literature:(5.3):nu_prime_hopf_relation', 'proof_rule': 'inference', 'inference_rule': 'phase162_verified_literature_citation', 'fixed_classification': 'proof_internal', 'extractor_locator': '(5.3)', 'premise_count': 1}
- {'key': 'literature:(5.3):nu_prime_hopf_relation', 'proof_rule': 'given', 'inference_rule': None, 'fixed_classification': None, 'extractor_locator': None, 'premise_count': 0}

### Web に表示された Reference

```text
**[R1] (4.5).**
$E^{n - 3}: \pi_{3 + 1}^{3} \to \pi_{n + 1}^{n}$ は同型.

---
```

## 重複・写像の候補

- 同じ結論のノード群: [[1, 55], [2, 63], [3, 57], [4, 58], [5, 59], [6, 60], [7, 34, 54], [8, 35, 56], [9, 25, 45], [10, 61], [11, 64], [12, 65], [13, 66], [14, 67], [15, 68], [16, 69], [17, 70], [18, 71, 94], [19, 72], [20, 73], [23, 43], [24, 44], [26, 46], [27, 47], [28, 48], [29, 49], [30, 50], [31, 51], [32, 52], [33, 53], [41, 42]]
- 写像の性質に関するノード: [9, 14, 16, 22, 23, 25, 26, 27, 29, 31, 32, 37, 39, 43, 45, 46, 47, 49, 51, 52, 67, 69, 77, 83, 85, 87, 88, 90, 92, 93]

## 全97ノード

| ID | 分類 | 型 | 推論規則 | 参照 | 前提 → 利用先 | tags |
|---:|---|---|---|---|---|---|
| 1 | OTHER_GIVEN | Relation | - | - | [] → [17] |  |
| 2 | OTHER_GIVEN | Relation | - | - | [] → [11] |  |
| 3 | OTHER_GIVEN | TodaDeltaMap | - | - | [] → [4] | MAP_FIELDS |
| 4 | UNCLASSIFIED_INFERENCE | TodaDeltaImageUpToSignStatement | Toda Delta iota_5 Whitehead-square relation | - | [3] → [11] | MAP_FIELDS |
| 5 | OTHER_GIVEN | WhiteheadProduct | - | - | [] → [6] |  |
| 6 | UNCLASSIFIED_INFERENCE | TodaProp27HopfInvariantUpToSignStatement | Toda Proposition 2.7 iota_2 Whitehead-square Hopf invariant up to sign | Proposition 2.7 | [5] → [10] | EXTRACTABLE_REFERENCE |
| 7 | OTHER_GIVEN | TodaPi32Eta2DefinitionStatement | - | - | [] → [10] | MAP_FIELDS |
| 8 | OTHER_GIVEN | Relation | - | - | [] → [10] |  |
| 9 | OTHER_GIVEN | TodaHopfInvariantInjectiveStatement | - | - | [] → [10] | MAP_FIELDS, MAP_PROPERTY |
| 10 | UNCLASSIFIED_INFERENCE | TodaPi32WhiteheadSquareUpToSignStatement | Toda pi_3^2 Whitehead square equals twice eta_2 up to sign | - | [6, 7, 8, 9] → [11] |  |
| 11 | UNCLASSIFIED_INFERENCE | TodaDeltaImageFreeCyclicStatement | Toda pi_4^3 Delta image generated by twice eta_2 | - | [2, 4, 10] → [13] | MAP_FIELDS |
| 12 | OTHER_GIVEN | TodaProp42ExactnessStatement | - | - | [] → [13] |  |
| 13 | UNCLASSIFIED_INFERENCE | TodaSuspensionKernelFreeCyclicStatement | Toda pi_4^3 exactness Delta image equals E kernel | - | [11, 12] → [17] | MAP_FIELDS |
| 14 | OTHER_GIVEN | TodaPrimaryGroupZeroStatement | - | - | [] → [16] | MAP_PROPERTY |
| 15 | OTHER_GIVEN | TodaProp42ExactnessStatement | - | - | [] → [16] |  |
| 16 | UNCLASSIFIED_INFERENCE | TodaSuspensionSurjectiveStatement | Toda pi_4^3 E-H exactness zero-right suspension surjectivity | - | [14, 15] → [17] | MAP_FIELDS, MAP_PROPERTY |
| 17 | UNCLASSIFIED_INFERENCE | Relation | Toda pi_4^3 finite cyclic quotient calculation | - | [1, 13, 16] → [20] |  |
| 18 | OTHER_GIVEN | TodaEtaFamilyDefinitionStatement | - | - | [] → [19] |  |
| 19 | UNCLASSIFIED_INFERENCE | Relation | Toda eta_3 notation suspension bridge | - | [18] → [20] |  |
| 20 | UNCLASSIFIED_INFERENCE | Relation | Toda pi_4^3 eta_3 generator notation | - | [17, 19] → [40] |  |
| 21 | OTHER_GIVEN | ScalarGreaterEqualStatement | - | - | [] → [22] |  |
| 22 | UNCLASSIFIED_INFERENCE | TodaPrimaryGroupZeroStatement | Toda pi_(i-1)^1 zero for i at least 3 | - | [21] → [39] | MAP_PROPERTY |
| 23 | OTHER_GIVEN | TodaPrimaryGroupZeroStatement | - | - | [] → [25] | MAP_PROPERTY |
| 24 | OTHER_GIVEN | TodaProp42ExactnessStatement | - | - | [] → [25] |  |
| 25 | UNCLASSIFIED_INFERENCE | TodaHopfInvariantInjectiveStatement | Toda EHP exactness zero-left Hopf injectivity | - | [23, 24] → [32] | MAP_FIELDS, MAP_PROPERTY |
| 26 | OTHER_GIVEN | TodaSuspensionIsomorphismStatement | - | - | [] → [27] | MAP_FIELDS, MAP_PROPERTY |
| 27 | UNCLASSIFIED_INFERENCE | TodaSuspensionInjectiveStatement | Toda suspension isomorphism implies injectivity | - | [26] → [29] | MAP_FIELDS, MAP_PROPERTY |
| 28 | OTHER_GIVEN | TodaProp42ExactnessStatement | - | - | [] → [29] |  |
| 29 | UNCLASSIFIED_INFERENCE | TodaDeltaZeroStatement | Toda EHP exactness injective-right Delta zero | - | [27, 28] → [31] | MAP_FIELDS, MAP_PROPERTY |
| 30 | OTHER_GIVEN | TodaProp42ExactnessStatement | - | - | [] → [31] |  |
| 31 | UNCLASSIFIED_INFERENCE | TodaHopfInvariantSurjectiveStatement | Toda EHP exactness zero-Delta Hopf surjectivity | - | [29, 30] → [32] | MAP_FIELDS, MAP_PROPERTY |
| 32 | UNCLASSIFIED_INFERENCE | TodaHopfInvariantIsomorphismStatement | Toda Hopf invariant injective and surjective implies isomorphism | - | [25, 31] → [34] | MAP_FIELDS, MAP_PROPERTY |
| 33 | OTHER_GIVEN | Relation | - | - | [] → [34] |  |
| 34 | UNCLASSIFIED_INFERENCE | TodaPi32Eta2DefinitionStatement | Toda pi_3^2 define eta_2 as unique Hopf preimage | - | [32, 33] → [35, 37] | MAP_FIELDS, SHARED_PREMISE |
| 35 | UNCLASSIFIED_INFERENCE | Relation | Toda pi_3^2 eta_2 Hopf relation | - | [34] → [37] |  |
| 36 | OTHER_GIVEN | TodaProp44DecompositionMap | - | - | [] → [37] | MAP_FIELDS |
| 37 | FIXED_STATEMENT | TodaProp44IsomorphismStatement | Toda Proposition 4.4 eta_2 n=2 specialization | Proposition 4.4 | [34, 35, 36] → [38, 39] | EXTRACTABLE_REFERENCE, FIXED_CLASSIFICATION, MAP_FIELDS, MAP_PROPERTY, SHARED_PREMISE |
| 38 | PROOF_INTERNAL | TodaProp44SecondSummandRestrictionStatement | Toda Proposition 4.4 eta_2 second-summand restriction | Proposition 4.4 | [37] → [39] | EXTRACTABLE_REFERENCE |
| 39 | FIXED_STATEMENT | Toda52CompositionIsomorphismStatement | Toda 5.2 eta_2 composition isomorphism | (5.2) | [22, 37, 38] → [40] | EXTRACTABLE_REFERENCE, FIXED_CLASSIFICATION, MAP_FIELDS, MAP_PROPERTY |
| 40 | PROOF_INTERNAL | Relation | Toda 5.2 pi_4^2 finite-cyclic transport | (5.2) | [20, 39] → [97] | EXTRACTABLE_REFERENCE |
| 41 | CITED_BOUNDARY | Relation | - | - | [] → [42] | H_NU_PRIME |
| 42 | CITED_BOUNDARY | Relation | phase162_verified_literature_citation | (5.3) | [41] → [83] | H_NU_PRIME, EXTRACTABLE_REFERENCE |
| 43 | OTHER_GIVEN | TodaPrimaryGroupZeroStatement | - | - | [] → [45] | MAP_PROPERTY |
| 44 | OTHER_GIVEN | TodaProp42ExactnessStatement | - | - | [] → [45] |  |
| 45 | UNCLASSIFIED_INFERENCE | TodaHopfInvariantInjectiveStatement | Toda EHP exactness zero-left Hopf injectivity | - | [43, 44] → [52, 61] | MAP_FIELDS, MAP_PROPERTY, SHARED_PREMISE |
| 46 | OTHER_GIVEN | TodaSuspensionIsomorphismStatement | - | - | [] → [47] | MAP_FIELDS, MAP_PROPERTY |
| 47 | UNCLASSIFIED_INFERENCE | TodaSuspensionInjectiveStatement | Toda suspension isomorphism implies injectivity | - | [46] → [49] | MAP_FIELDS, MAP_PROPERTY |
| 48 | OTHER_GIVEN | TodaProp42ExactnessStatement | - | - | [] → [49] |  |
| 49 | UNCLASSIFIED_INFERENCE | TodaDeltaZeroStatement | Toda EHP exactness injective-right Delta zero | - | [47, 48] → [51] | MAP_FIELDS, MAP_PROPERTY |
| 50 | OTHER_GIVEN | TodaProp42ExactnessStatement | - | - | [] → [51] |  |
| 51 | UNCLASSIFIED_INFERENCE | TodaHopfInvariantSurjectiveStatement | Toda EHP exactness zero-Delta Hopf surjectivity | - | [49, 50] → [52] | MAP_FIELDS, MAP_PROPERTY |
| 52 | UNCLASSIFIED_INFERENCE | TodaHopfInvariantIsomorphismStatement | Toda Hopf invariant injective and surjective implies isomorphism | - | [45, 51] → [54, 55] | MAP_FIELDS, MAP_PROPERTY, SHARED_PREMISE |
| 53 | OTHER_GIVEN | Relation | - | - | [] → [54, 55] | SHARED_PREMISE |
| 54 | UNCLASSIFIED_INFERENCE | TodaPi32Eta2DefinitionStatement | Toda pi_3^2 define eta_2 as unique Hopf preimage | - | [52, 53] → [55, 56, 61] | MAP_FIELDS, SHARED_PREMISE |
| 55 | UNCLASSIFIED_INFERENCE | Relation | Toda pi_3^2 free cyclic generator transport | - | [52, 53, 54] → [70, 82] | SHARED_PREMISE |
| 56 | UNCLASSIFIED_INFERENCE | Relation | Toda pi_3^2 eta_2 Hopf relation | - | [54] → [61, 82] | SHARED_PREMISE |
| 57 | OTHER_GIVEN | TodaDeltaMap | - | - | [] → [58] | MAP_FIELDS |
| 58 | UNCLASSIFIED_INFERENCE | TodaDeltaImageUpToSignStatement | Toda Delta iota_5 Whitehead-square relation | - | [57] → [62, 64] | MAP_FIELDS, SHARED_PREMISE |
| 59 | OTHER_GIVEN | WhiteheadProduct | - | - | [] → [60] |  |
| 60 | UNCLASSIFIED_INFERENCE | TodaProp27HopfInvariantUpToSignStatement | Toda Proposition 2.7 iota_2 Whitehead-square Hopf invariant up to sign | Proposition 2.7 | [59] → [61] | EXTRACTABLE_REFERENCE |
| 61 | UNCLASSIFIED_INFERENCE | TodaPi32WhiteheadSquareUpToSignStatement | Toda pi_3^2 Whitehead square equals twice eta_2 up to sign | - | [60, 54, 56, 45] → [62, 64] | SHARED_PREMISE |
| 62 | UNCLASSIFIED_INFERENCE | TodaDeltaImageUpToSignStatement | Toda Delta iota_5 twice eta_2 up-to-sign bridge | - | [58, 61] → [82] | MAP_FIELDS |
| 63 | OTHER_GIVEN | Relation | - | - | [] → [64] |  |
| 64 | UNCLASSIFIED_INFERENCE | TodaDeltaImageFreeCyclicStatement | Toda pi_4^3 Delta image generated by twice eta_2 | - | [63, 58, 61] → [66] | MAP_FIELDS |
| 65 | OTHER_GIVEN | TodaProp42ExactnessStatement | - | - | [] → [66] |  |
| 66 | UNCLASSIFIED_INFERENCE | TodaSuspensionKernelFreeCyclicStatement | Toda pi_4^3 exactness Delta image equals E kernel | - | [64, 65] → [70] | MAP_FIELDS |
| 67 | OTHER_GIVEN | TodaPrimaryGroupZeroStatement | - | - | [] → [69] | MAP_PROPERTY |
| 68 | OTHER_GIVEN | TodaProp42ExactnessStatement | - | - | [] → [69] |  |
| 69 | UNCLASSIFIED_INFERENCE | TodaSuspensionSurjectiveStatement | Toda pi_4^3 E-H exactness zero-right suspension surjectivity | - | [67, 68] → [70] | MAP_FIELDS, MAP_PROPERTY |
| 70 | UNCLASSIFIED_INFERENCE | Relation | Toda pi_4^3 finite cyclic quotient calculation | - | [55, 66, 69] → [73] |  |
| 71 | OTHER_GIVEN | TodaEtaFamilyDefinitionStatement | - | - | [] → [72] |  |
| 72 | UNCLASSIFIED_INFERENCE | Relation | Toda eta_3 notation suspension bridge | - | [71] → [73, 80] | SHARED_PREMISE |
| 73 | UNCLASSIFIED_INFERENCE | Relation | Toda pi_4^3 eta_3 generator notation | - | [70, 72] → [78] |  |
| 74 | OTHER_GIVEN | ScalarGreaterEqualStatement | - | - | [] → [77] |  |
| 75 | OTHER_GIVEN | ScalarGreaterEqualStatement | - | - | [] → [77] |  |
| 76 | OTHER_GIVEN | TodaIteratedSuspensionMap | - | - | [] → [77] | MAP_FIELDS |
| 77 | FIXED_STATEMENT | Toda45IsomorphismStatement | Toda 4.5 stable-range iterated suspension isomorphism | (4.5) | [74, 75, 76] → [78] | EXTRACTABLE_REFERENCE, FIXED_CLASSIFICATION, MAP_FIELDS, MAP_PROPERTY |
| 78 | PROOF_INTERNAL | Relation | Toda 4.5 pi_4^3 finite-cyclic transport | (4.5) | [73, 77] → [81] | EXTRACTABLE_REFERENCE |
| 79 | OTHER_GIVEN | TodaEtaFamilyDefinitionStatement | - | - | [] → [80] |  |
| 80 | UNCLASSIFIED_INFERENCE | Relation | Toda higher eta-family iterated suspension bridge | - | [79, 72] → [81] |  |
| 81 | UNCLASSIFIED_INFERENCE | Relation | Toda higher eta-family finite-cyclic generator bridge | - | [78, 80] → [82] |  |
| 82 | FIXED_STATEMENT | TodaProp51FiniteDimensionalStatement | Toda Proposition 5.1 finite-dimensional integration | Proposition 5.1 | [55, 56, 62, 81] → [83, 88] | EXTRACTABLE_REFERENCE, FIXED_CLASSIFICATION, SHARED_PREMISE |
| 83 | PROOF_INTERNAL | TodaHopfInvariantSurjectiveStatement | Toda Proposition 5.3 n=3 Hopf eta_5 surjectivity | Proposition 5.3 | [42, 82] → [85] | EXTRACTABLE_REFERENCE, MAP_FIELDS, MAP_PROPERTY |
| 84 | OTHER_GIVEN | TodaProp42ExactnessStatement | - | - | [] → [85] |  |
| 85 | PROOF_INTERNAL | TodaDeltaZeroStatement | Toda Proposition 5.3 n=3 Hopf surjective implies Delta zero | Proposition 5.3 | [83, 84] → [87] | EXTRACTABLE_REFERENCE, MAP_FIELDS, MAP_PROPERTY |
| 86 | OTHER_GIVEN | TodaProp42ExactnessStatement | - | - | [] → [87] |  |
| 87 | PROOF_INTERNAL | TodaSuspensionInjectiveStatement | Toda Proposition 5.3 n=3 Delta zero implies suspension injective | Proposition 5.3 | [85, 86] → [93] | EXTRACTABLE_REFERENCE, MAP_FIELDS, MAP_PROPERTY |
| 88 | PROOF_INTERNAL | TodaDeltaInjectiveStatement | Toda Proposition 5.1 n=3 Delta injectivity | Proposition 5.1 | [82] → [90] | EXTRACTABLE_REFERENCE, MAP_FIELDS, MAP_PROPERTY |
| 89 | OTHER_GIVEN | TodaProp42ExactnessStatement | - | - | [] → [90] |  |
| 90 | PROOF_INTERNAL | TodaHopfInvariantZeroStatement | Toda Proposition 5.3 n=3 Delta injectivity implies Hopf zero | Proposition 5.3 | [88, 89] → [92] | EXTRACTABLE_REFERENCE, MAP_FIELDS, MAP_PROPERTY |
| 91 | OTHER_GIVEN | TodaProp42ExactnessStatement | - | - | [] → [92] |  |
| 92 | PROOF_INTERNAL | TodaSuspensionSurjectiveStatement | Toda Proposition 5.3 n=3 Hopf zero implies suspension surjective | Proposition 5.3 | [90, 91] → [93] | EXTRACTABLE_REFERENCE, MAP_FIELDS, MAP_PROPERTY |
| 93 | PROOF_INTERNAL | TodaSuspensionIsomorphismStatement | Toda Proposition 5.3 n=3 suspension isomorphism | Proposition 5.3 | [87, 92] → [97] | EXTRACTABLE_REFERENCE, MAP_FIELDS, MAP_PROPERTY |
| 94 | OTHER_GIVEN | TodaEtaFamilyDefinitionStatement | - | - | [] → [96] |  |
| 95 | OTHER_GIVEN | TodaEtaFamilyDefinitionStatement | - | - | [] → [96] |  |
| 96 | PROOF_INTERNAL | Relation | Toda Proposition 5.3 n=3 eta-square suspension bridge | - | [94, 95] → [97] |  |
| 97 | FIXED_STATEMENT | Relation | Toda Proposition 5.3 n=3 pi_5^3 finite-cyclic transport | Proposition 5.3 | [40, 93, 96] → [] | EXTRACTABLE_REFERENCE, FIXED_CLASSIFICATION, ROOT |

## 判定上の注意

- ROOT に到達可能なノードでも、文章化する必要があるとは限らない。
- 出典の抽出失敗と文献の真偽は別問題。
- 外見上不要な写像が実際にどの推論の前提かはJSONの premises / consumers で確認する。
