# Phase 162 R9 — π₅³ 証明木と表示の出所監査

**監査のみ。証明木・Renderer・Web のコードは変更しない。**

- Root preserved: True
- Unique ancestor ProofSteps: 123
- Presentation nodes: 123
- Narrative paragraphs: 45
- Report meanings: 'tree matches' are exact rendered fragments, not proof validity judgments.

## 1. 最終結論からの直接依存

- `root` depth=0, `INFERENCE`, `Relation`, premises=3: `\pi_{5}^{3} = \mathbb{Z}/2\{\eta_{3}^{2}\}`
- `root/1` depth=1, `INFERENCE`, `Relation`, premises=2: `\pi_{4}^{2} = \mathbb{Z}/2\{\eta_{2}^{2}\}`
- `root/1/1` depth=2, `INFERENCE`, `Relation`, premises=2: `\pi_{4}^{3} = \mathbb{Z}/2\{\eta_{3}\}`
- `root/1/2` depth=2, `INFERENCE`, `Toda52CompositionIsomorphismStatement`, premises=3: `Toda52CompositionIsomorphismStatement`
- `root/2` depth=1, `INFERENCE`, `TodaSuspensionIsomorphismStatement`, premises=2: `TodaSuspensionIsomorphismStatement`
- `root/2/1` depth=2, `INFERENCE`, `TodaSuspensionInjectiveStatement`, premises=2: `E: \pi_{4}^{2} \to \pi_{5}^{3} \text{ is injective}`
- `root/2/2` depth=2, `INFERENCE`, `TodaSuspensionSurjectiveStatement`, premises=2: `E: \pi_{4}^{2} \to \pi_{5}^{3} \text{ is surjective}`
- `root/3` depth=1, `INFERENCE`, `Relation`, premises=2: `E\eta_{2}\eta_{3} = \eta_{3}\eta_{4}`
- `root/3/1` depth=2, `GIVEN`, `TodaEtaFamilyDefinitionStatement`, premises=0: `TodaEtaFamilyDefinitionStatement`
- `root/3/2` depth=2, `GIVEN`, `TodaEtaFamilyDefinitionStatement`, premises=0: `TodaEtaFamilyDefinitionStatement`

## 2. 問題のある文章の出所候補

### unrelated_H_pi3
- 概要: H(π3²→π3³): unrelated map
- 本文段落番号: []
- 証明木の数式に同一断片を含むノード数: 0
- 該当する最初の経路: []

### unrelated_E_pi3
- 概要: E(π3²→π4³): ancillary suspension
- 本文段落番号: []
- 証明木の数式に同一断片を含むノード数: 0
- 該当する最初の経路: []

### wrong_kernel_context
- 概要: ker E / Im Δ claim: inspect map context
- 本文段落番号: []
- 証明木の数式に同一断片を含むノード数: 0
- 該当する最初の経路: []

### symbolic_stable
- 概要: symbolic stable family in pi5³ output
- 本文段落番号: []
- 証明木の数式に同一断片を含むノード数: 0
- 該当する最初の経路: []

### stable_tail
- 概要: stable transport appended narrative
- 本文段落番号: [44]
- 証明木の数式に同一断片を含むノード数: 0
- 該当する最初の経路: []

### eta_tautology
- 概要: eta3 tautology
- 本文段落番号: []
- 証明木の数式に同一断片を含むノード数: 0
- 該当する最初の経路: []

### eta_composition
- 概要: eta3 eta3 expression
- 本文段落番号: []
- 証明木の数式に同一断片を含むノード数: 0
- 該当する最初の経路: []

### delta_iota5
- 概要: delta(iota5) repetitions
- 本文段落番号: []
- 証明木の数式に同一断片を含むノード数: 0
- 該当する最初の経路: []

## 3. Stable transport の抽出元

- `extract_suspension_transport_facts(root)` 結果: FOUND
- `source_group_step`: path=root/2/1/1/1/2/4/1/1; `\pi_{4}^{3} = \mathbb{Z}/2\{\eta_{3}\}`
- `isomorphism_step`: path=root/2/1/1/1/2/4/1/2; `None`
- `transported_group_step`: path=root/2/1/1/1/2/4/1; `\pi_{n + 1}^{n} = \mathbb{Z}/2\{E^{n - 3}\eta_{3}\}`
- `generator_bridge_step`: path=root/2/1/1/1/2/4/2; `E^{n - 3}\eta_{3} = \eta_{n}`
- `render_suspension_transport_link` returned text: False

## 4. 証明木の全ノード（経路・型・式）

- `root` [INFERENCE] Relation: `\pi_{5}^{3} = \mathbb{Z}/2\{\eta_{3}^{2}\}`
- `root/1` [INFERENCE] Relation: `\pi_{4}^{2} = \mathbb{Z}/2\{\eta_{2}^{2}\}`
- `root/1/1` [INFERENCE] Relation: `\pi_{4}^{3} = \mathbb{Z}/2\{\eta_{3}\}`
- `root/1/1/1` [INFERENCE] Relation: `\pi_{4}^{3} = \mathbb{Z}/2\{E\eta_{2}\}`
- `root/1/1/1/1` [GIVEN] Relation: `\pi_{3}^{2} = \mathbb{Z}\{\eta_{2}\}`
- `root/1/1/1/2` [INFERENCE] TodaSuspensionKernelFreeCyclicStatement: `TodaSuspensionKernelFreeCyclicStatement`
- `root/1/1/1/2/1` [INFERENCE] TodaDeltaImageFreeCyclicStatement: `TodaDeltaImageFreeCyclicStatement`
- `root/1/1/1/2/1/1` [GIVEN] Relation: `\pi_{5}^{5} = \mathbb{Z}\{\iota_{5}\}`
- `root/1/1/1/2/1/2` [INFERENCE] TodaDeltaImageUpToSignStatement: `\Delta\left(\iota_{5}\right) = \pm [\iota_{2}, \iota_{2}]`
- `root/1/1/1/2/1/2/1` [GIVEN] TodaDeltaMap: `TodaDeltaMap`
- `root/1/1/1/2/1/3` [INFERENCE] TodaPi32WhiteheadSquareUpToSignStatement: `TodaPi32WhiteheadSquareUpToSignStatement`
- `root/1/1/1/2/1/3/1` [INFERENCE] TodaProp27HopfInvariantUpToSignStatement: `TodaProp27HopfInvariantUpToSignStatement`
- `root/1/1/1/2/1/3/1/1` [GIVEN] WhiteheadProduct: `[\iota_{2}, \iota_{2}]`
- `root/1/1/1/2/1/3/2` [GIVEN] TodaPi32Eta2DefinitionStatement: `TodaPi32Eta2DefinitionStatement`
- `root/1/1/1/2/1/3/3` [GIVEN] Relation: `H\left(\eta_{2}\right) = \iota_{3}`
- `root/1/1/1/2/1/3/4` [GIVEN] TodaHopfInvariantInjectiveStatement: `TodaHopfInvariantInjectiveStatement`
- `root/1/1/1/2/2` [GIVEN] TodaProp42ExactnessStatement: `\pi_{5}^{5} \xrightarrow{\Delta} \pi_{3}^{2} \xrightarrow{E} \pi_{4}^{3} \text{ is exact}`
- `root/1/1/1/3` [INFERENCE] TodaSuspensionSurjectiveStatement: `E: \pi_{3}^{2} \to \pi_{4}^{3} \text{ is surjective}`
- `root/1/1/1/3/1` [GIVEN] TodaPrimaryGroupZeroStatement: `\pi_{4}^{5} = 0`
- `root/1/1/1/3/2` [GIVEN] TodaProp42ExactnessStatement: `\pi_{3}^{2} \xrightarrow{E} \pi_{4}^{3} \xrightarrow{H} \pi_{4}^{5} \text{ is exact}`
- `root/1/1/2` [INFERENCE] Relation: `\eta_{3} = E\eta_{2}`
- `root/1/1/2/1` [GIVEN] TodaEtaFamilyDefinitionStatement: `TodaEtaFamilyDefinitionStatement`
- `root/1/2` [INFERENCE] Toda52CompositionIsomorphismStatement: `Toda52CompositionIsomorphismStatement`
- `root/1/2/1` [INFERENCE] TodaPrimaryGroupZeroStatement: `\pi_{i - 1}^{1} = 0`
- `root/1/2/1/1` [GIVEN] ScalarGreaterEqualStatement: `ScalarGreaterEqualStatement`
- `root/1/2/2` [INFERENCE] TodaProp44IsomorphismStatement: `TodaProp44IsomorphismStatement`
- `root/1/2/2/1` [INFERENCE] TodaPi32Eta2DefinitionStatement: `TodaPi32Eta2DefinitionStatement`
- `root/1/2/2/1/1` [INFERENCE] TodaHopfInvariantIsomorphismStatement: `TodaHopfInvariantIsomorphismStatement`
- `root/1/2/2/1/1/1` [INFERENCE] TodaHopfInvariantInjectiveStatement: `TodaHopfInvariantInjectiveStatement`
- `root/1/2/2/1/1/1/1` [GIVEN] TodaPrimaryGroupZeroStatement: `\pi_{2}^{1} = 0`
- `root/1/2/2/1/1/1/2` [GIVEN] TodaProp42ExactnessStatement: `\pi_{2}^{1} \xrightarrow{E} \pi_{3}^{2} \xrightarrow{H} \pi_{3}^{3} \text{ is exact}`
- `root/1/2/2/1/1/2` [INFERENCE] TodaHopfInvariantSurjectiveStatement: `H: \pi_{3}^{2} \to \pi_{3}^{3} \text{ is surjective}`
- `root/1/2/2/1/1/2/1` [INFERENCE] TodaDeltaZeroStatement: `TodaDeltaZeroStatement`
- `root/1/2/2/1/1/2/1/1` [INFERENCE] TodaSuspensionInjectiveStatement: `E: \pi_{1}^{1} \to \pi_{2}^{2} \text{ is injective}`
- `root/1/2/2/1/1/2/1/1/1` [GIVEN] TodaSuspensionIsomorphismStatement: `TodaSuspensionIsomorphismStatement`
- `root/1/2/2/1/1/2/1/2` [GIVEN] TodaProp42ExactnessStatement: `\pi_{3}^{3} \xrightarrow{\Delta} \pi_{1}^{1} \xrightarrow{E} \pi_{2}^{2} \text{ is exact}`
- `root/1/2/2/1/1/2/2` [GIVEN] TodaProp42ExactnessStatement: `\pi_{3}^{2} \xrightarrow{H} \pi_{3}^{3} \xrightarrow{\Delta} \pi_{1}^{1} \text{ is exact}`
- `root/1/2/2/1/2` [GIVEN] Relation: `\pi_{3}^{3} = \mathbb{Z}\{\iota_{3}\}`
- `root/1/2/2/2` [INFERENCE] Relation: `H\left(\eta_{2}\right) = \iota_{3}`
- `root/1/2/2/3` [GIVEN] TodaProp44DecompositionMap: `TodaProp44DecompositionMap`
- `root/1/2/3` [INFERENCE] TodaProp44SecondSummandRestrictionStatement: `TodaProp44SecondSummandRestrictionStatement`
- `root/2` [INFERENCE] TodaSuspensionIsomorphismStatement: `TodaSuspensionIsomorphismStatement`
- `root/2/1` [INFERENCE] TodaSuspensionInjectiveStatement: `E: \pi_{4}^{2} \to \pi_{5}^{3} \text{ is injective}`
- `root/2/1/1` [INFERENCE] TodaDeltaZeroStatement: `TodaDeltaZeroStatement`
- `root/2/1/1/1` [INFERENCE] TodaHopfInvariantSurjectiveStatement: `H: \pi_{6}^{3} \to \pi_{6}^{5} \text{ is surjective}`
- `root/2/1/1/1/1` [INFERENCE] Relation: `H\left(\nu'\right) = \eta_{5}`
- `root/2/1/1/1/1/1` [INFERENCE] Relation: `H\left(\nu'\right) = E^{2}\eta_{3}`
- `root/2/1/1/1/1/1/1` [INFERENCE] Toda53NuPrimeBracketSpecializationStatement: `Toda53NuPrimeBracketSpecializationStatement`
- `root/2/1/1/1/1/1/1/1` [GIVEN] TodaBracketMembershipStatement: `\nu' \in \{\eta_{3}, 2\iota_{4}, \eta_{4}\}_{1}`
- `root/2/1/1/1/1/1/2` [INFERENCE] Relation: `2\eta_{3} = 0`
- `root/2/1/1/1/1/1/2/1` [INFERENCE] Relation: `\pi_{4}^{3} = \mathbb{Z}/2\{\eta_{3}\}`
- `root/2/1/1/1/1/1/2/1/1` [INFERENCE] Relation: `\pi_{4}^{3} = \mathbb{Z}/2\{E\eta_{2}\}`
- `root/2/1/1/1/1/1/2/1/1/1` [GIVEN] Relation: `\pi_{3}^{2} = \mathbb{Z}\{\eta_{2}\}`
- `root/2/1/1/1/1/1/2/1/1/2` [INFERENCE] TodaSuspensionKernelFreeCyclicStatement: `TodaSuspensionKernelFreeCyclicStatement`
- `root/2/1/1/1/1/1/2/1/1/2/1` [INFERENCE] TodaDeltaImageFreeCyclicStatement: `TodaDeltaImageFreeCyclicStatement`
- `root/2/1/1/1/1/1/2/1/1/2/1/1` [GIVEN] Relation: `\pi_{5}^{5} = \mathbb{Z}\{\iota_{5}\}`
- `root/2/1/1/1/1/1/2/1/1/2/1/2` [INFERENCE] TodaDeltaImageUpToSignStatement: `\Delta\left(\iota_{5}\right) = \pm [\iota_{2}, \iota_{2}]`
- `root/2/1/1/1/1/1/2/1/1/2/1/2/1` [GIVEN] TodaDeltaMap: `TodaDeltaMap`
- `root/2/1/1/1/1/1/2/1/1/2/1/3` [INFERENCE] TodaPi32WhiteheadSquareUpToSignStatement: `TodaPi32WhiteheadSquareUpToSignStatement`
- `root/2/1/1/1/1/1/2/1/1/2/1/3/1` [INFERENCE] TodaProp27HopfInvariantUpToSignStatement: `TodaProp27HopfInvariantUpToSignStatement`
- `root/2/1/1/1/1/1/2/1/1/2/1/3/1/1` [GIVEN] WhiteheadProduct: `[\iota_{2}, \iota_{2}]`
- `root/2/1/1/1/1/1/2/1/1/2/1/3/2` [GIVEN] TodaPi32Eta2DefinitionStatement: `TodaPi32Eta2DefinitionStatement`
- `root/2/1/1/1/1/1/2/1/1/2/1/3/3` [GIVEN] Relation: `H\left(\eta_{2}\right) = \iota_{3}`
- `root/2/1/1/1/1/1/2/1/1/2/1/3/4` [GIVEN] TodaHopfInvariantInjectiveStatement: `TodaHopfInvariantInjectiveStatement`
- `root/2/1/1/1/1/1/2/1/1/2/2` [GIVEN] TodaProp42ExactnessStatement: `\pi_{5}^{5} \xrightarrow{\Delta} \pi_{3}^{2} \xrightarrow{E} \pi_{4}^{3} \text{ is exact}`
- `root/2/1/1/1/1/1/2/1/1/3` [INFERENCE] TodaSuspensionSurjectiveStatement: `E: \pi_{3}^{2} \to \pi_{4}^{3} \text{ is surjective}`
- `root/2/1/1/1/1/1/2/1/1/3/1` [GIVEN] TodaPrimaryGroupZeroStatement: `\pi_{4}^{5} = 0`
- `root/2/1/1/1/1/1/2/1/1/3/2` [GIVEN] TodaProp42ExactnessStatement: `\pi_{3}^{2} \xrightarrow{E} \pi_{4}^{3} \xrightarrow{H} \pi_{4}^{5} \text{ is exact}`
- `root/2/1/1/1/1/1/2/1/2` [INFERENCE] Relation: `\eta_{3} = E\eta_{2}`
- `root/2/1/1/1/1/1/2/1/2/1` [GIVEN] TodaEtaFamilyDefinitionStatement: `TodaEtaFamilyDefinitionStatement`
- `root/2/1/1/1/1/2` [INFERENCE] Relation: `E^{2}\eta_{3} = \eta_{5}`
- `root/2/1/1/1/1/2/1` [GIVEN] TodaEtaFamilyDefinitionStatement: `TodaEtaFamilyDefinitionStatement`
- `root/2/1/1/1/1/2/2` [GIVEN] TodaEtaFamilyDefinitionStatement: `TodaEtaFamilyDefinitionStatement`
- `root/2/1/1/1/2` [INFERENCE] TodaProp51FiniteDimensionalStatement: `TodaProp51FiniteDimensionalStatement`
- `root/2/1/1/1/2/1` [INFERENCE] Relation: `\pi_{3}^{2} = \mathbb{Z}\{\eta_{2}\}`
- `root/2/1/1/1/2/1/1` [INFERENCE] TodaHopfInvariantIsomorphismStatement: `TodaHopfInvariantIsomorphismStatement`
- `root/2/1/1/1/2/1/1/1` [INFERENCE] TodaHopfInvariantInjectiveStatement: `TodaHopfInvariantInjectiveStatement`
- `root/2/1/1/1/2/1/1/1/1` [GIVEN] TodaPrimaryGroupZeroStatement: `\pi_{2}^{1} = 0`
- `root/2/1/1/1/2/1/1/1/2` [GIVEN] TodaProp42ExactnessStatement: `\pi_{2}^{1} \xrightarrow{E} \pi_{3}^{2} \xrightarrow{H} \pi_{3}^{3} \text{ is exact}`
- `root/2/1/1/1/2/1/1/2` [INFERENCE] TodaHopfInvariantSurjectiveStatement: `H: \pi_{3}^{2} \to \pi_{3}^{3} \text{ is surjective}`
- `root/2/1/1/1/2/1/1/2/1` [INFERENCE] TodaDeltaZeroStatement: `TodaDeltaZeroStatement`
- `root/2/1/1/1/2/1/1/2/1/1` [INFERENCE] TodaSuspensionInjectiveStatement: `E: \pi_{1}^{1} \to \pi_{2}^{2} \text{ is injective}`
- `root/2/1/1/1/2/1/1/2/1/1/1` [GIVEN] TodaSuspensionIsomorphismStatement: `TodaSuspensionIsomorphismStatement`
- `root/2/1/1/1/2/1/1/2/1/2` [GIVEN] TodaProp42ExactnessStatement: `\pi_{3}^{3} \xrightarrow{\Delta} \pi_{1}^{1} \xrightarrow{E} \pi_{2}^{2} \text{ is exact}`
- `root/2/1/1/1/2/1/1/2/2` [GIVEN] TodaProp42ExactnessStatement: `\pi_{3}^{2} \xrightarrow{H} \pi_{3}^{3} \xrightarrow{\Delta} \pi_{1}^{1} \text{ is exact}`
- `root/2/1/1/1/2/1/2` [GIVEN] Relation: `\pi_{3}^{3} = \mathbb{Z}\{\iota_{3}\}`
- `root/2/1/1/1/2/1/3` [INFERENCE] TodaPi32Eta2DefinitionStatement: `TodaPi32Eta2DefinitionStatement`
- `root/2/1/1/1/2/2` [INFERENCE] Relation: `H\left(\eta_{2}\right) = \iota_{3}`
- `root/2/1/1/1/2/3` [INFERENCE] TodaDeltaImageUpToSignStatement: `\Delta\left(\iota_{5}\right) = \pm 2\eta_{2}`
- `root/2/1/1/1/2/3/1` [INFERENCE] TodaDeltaImageUpToSignStatement: `\Delta\left(\iota_{5}\right) = \pm [\iota_{2}, \iota_{2}]`
- `root/2/1/1/1/2/3/1/1` [GIVEN] TodaDeltaMap: `TodaDeltaMap`
- `root/2/1/1/1/2/3/2` [INFERENCE] TodaPi32WhiteheadSquareUpToSignStatement: `TodaPi32WhiteheadSquareUpToSignStatement`
- `root/2/1/1/1/2/3/2/1` [INFERENCE] TodaProp27HopfInvariantUpToSignStatement: `TodaProp27HopfInvariantUpToSignStatement`
- `root/2/1/1/1/2/3/2/1/1` [GIVEN] WhiteheadProduct: `[\iota_{2}, \iota_{2}]`
- `root/2/1/1/1/2/4` [INFERENCE] Relation: `\pi_{n + 1}^{n} = \mathbb{Z}/2\{\eta_{n}\}`
- `root/2/1/1/1/2/4/1` [INFERENCE] Relation: `\pi_{n + 1}^{n} = \mathbb{Z}/2\{E^{n - 3}\eta_{3}\}`
- `root/2/1/1/1/2/4/1/1` [INFERENCE] Relation: `\pi_{4}^{3} = \mathbb{Z}/2\{\eta_{3}\}`
- `root/2/1/1/1/2/4/1/1/1` [INFERENCE] Relation: `\pi_{4}^{3} = \mathbb{Z}/2\{E\eta_{2}\}`
- `root/2/1/1/1/2/4/1/1/1/2` [INFERENCE] TodaSuspensionKernelFreeCyclicStatement: `TodaSuspensionKernelFreeCyclicStatement`
- `root/2/1/1/1/2/4/1/1/1/2/1` [INFERENCE] TodaDeltaImageFreeCyclicStatement: `TodaDeltaImageFreeCyclicStatement`
- `root/2/1/1/1/2/4/1/1/1/2/1/1` [GIVEN] Relation: `\pi_{5}^{5} = \mathbb{Z}\{\iota_{5}\}`
- `root/2/1/1/1/2/4/1/1/1/2/2` [GIVEN] TodaProp42ExactnessStatement: `\pi_{5}^{5} \xrightarrow{\Delta} \pi_{3}^{2} \xrightarrow{E} \pi_{4}^{3} \text{ is exact}`
- `root/2/1/1/1/2/4/1/1/1/3` [INFERENCE] TodaSuspensionSurjectiveStatement: `E: \pi_{3}^{2} \to \pi_{4}^{3} \text{ is surjective}`
- `root/2/1/1/1/2/4/1/1/1/3/1` [GIVEN] TodaPrimaryGroupZeroStatement: `\pi_{4}^{5} = 0`
- `root/2/1/1/1/2/4/1/1/1/3/2` [GIVEN] TodaProp42ExactnessStatement: `\pi_{3}^{2} \xrightarrow{E} \pi_{4}^{3} \xrightarrow{H} \pi_{4}^{5} \text{ is exact}`
- `root/2/1/1/1/2/4/1/1/2` [INFERENCE] Relation: `\eta_{3} = E\eta_{2}`
- `root/2/1/1/1/2/4/1/1/2/1` [GIVEN] TodaEtaFamilyDefinitionStatement: `TodaEtaFamilyDefinitionStatement`
- `root/2/1/1/1/2/4/1/2` [INFERENCE] Toda45IsomorphismStatement: `Toda45IsomorphismStatement`
- `root/2/1/1/1/2/4/1/2/1` [GIVEN] ScalarGreaterEqualStatement: `ScalarGreaterEqualStatement`
- `root/2/1/1/1/2/4/1/2/2` [GIVEN] ScalarGreaterEqualStatement: `ScalarGreaterEqualStatement`
- `root/2/1/1/1/2/4/1/2/3` [GIVEN] TodaIteratedSuspensionMap: `TodaIteratedSuspensionMap`
- `root/2/1/1/1/2/4/2` [INFERENCE] Relation: `E^{n - 3}\eta_{3} = \eta_{n}`
- `root/2/1/1/1/2/4/2/1` [GIVEN] TodaEtaFamilyDefinitionStatement: `TodaEtaFamilyDefinitionStatement`
- `root/2/1/1/2` [GIVEN] TodaProp42ExactnessStatement: `\pi_{6}^{3} \xrightarrow{H} \pi_{6}^{5} \xrightarrow{\Delta} \pi_{4}^{2} \text{ is exact}`
- `root/2/1/2` [GIVEN] TodaProp42ExactnessStatement: `\pi_{6}^{5} \xrightarrow{\Delta} \pi_{4}^{2} \xrightarrow{E} \pi_{5}^{3} \text{ is exact}`
- `root/2/2` [INFERENCE] TodaSuspensionSurjectiveStatement: `E: \pi_{4}^{2} \to \pi_{5}^{3} \text{ is surjective}`
- `root/2/2/1` [INFERENCE] TodaHopfInvariantZeroStatement: `H: \pi_{5}^{3} \to \pi_{5}^{5} \text{ is the zero map}`
- `root/2/2/1/1` [INFERENCE] TodaDeltaInjectiveStatement: `\Delta: \pi_{5}^{5} \to \pi_{3}^{2} \text{ is injective}`
- `root/2/2/1/2` [GIVEN] TodaProp42ExactnessStatement: `\pi_{5}^{3} \xrightarrow{H} \pi_{5}^{5} \xrightarrow{\Delta} \pi_{3}^{2} \text{ is exact}`
- `root/2/2/2` [GIVEN] TodaProp42ExactnessStatement: `\pi_{4}^{2} \xrightarrow{E} \pi_{5}^{3} \xrightarrow{H} \pi_{5}^{5} \text{ is exact}`
- `root/3` [INFERENCE] Relation: `E\eta_{2}\eta_{3} = \eta_{3}\eta_{4}`
- `root/3/1` [GIVEN] TodaEtaFamilyDefinitionStatement: `TodaEtaFamilyDefinitionStatement`
- `root/3/2` [GIVEN] TodaEtaFamilyDefinitionStatement: `TodaEtaFamilyDefinitionStatement`

## 5. 本文段落

1. まず, $\nu'$ を定める.
2. $\pi_{4}^{3} = \mathbb{Z}/2\{\eta_{3}\}$.
3. $2\eta_{3} = 0$.
4. この前提条件を満たすので, Lemma 5.2 を適用できる. Lemma 5.2 の $\beta$ を $\nu'$ と定めると,
5. $\nu' \in \{\eta_{3}, 2\iota_{4}, \eta_{4}\}_{1}$.
6. 最後に, $\pi_{5}^{3}$ の群構造を決定するために, 次の完全列を考える.
7. \[ \pi_{6}^{3} \xrightarrow{H} \pi_{6}^{5} \xrightarrow{\Delta} \pi_{4}^{2} \xrightarrow{E} \pi_{5}^{3} \xrightarrow{H} \pi_{5}^{5} \xrightarrow{\Delta} \pi_{3}^{2} \xrightarrow{E} \pi_{4}^{3} \xrightarrow{H} \pi_{4}^{5}. \]
8. [R1]より, $H\left(\nu'\right) = \eta_{5}$.
9. 完全性より, $H: \pi_{3}^{2} \to \pi_{3}^{3}$ は単射.
10. 完全性より, $H: \pi_{3}^{2} \to \pi_{3}^{3}$ は全射.
11. $\pi_{4}^{2} = \mathbb{Z}/2\{\eta_{2}^{2}\}$.
12. $\pi_{3}^{2} = \mathbb{Z}\{\eta_{2}\}$.
13. $\pi_{5}^{5} = \mathbb{Z}\{\iota_{5}\}$.
14. $\pi_{4}^{5} = 0$.
15. 完全性より, $E: \pi_{3}^{2} \to \pi_{4}^{3}$ は全射.
16. これより, $\Delta\left(\iota_{5}\right) = \pm [\iota_{2}, \iota_{2}]$.
17. $[\iota_{2}, \iota_{2}]$.
18. これより, $H([\iota_{2}, \iota_{2}]) = \pm 2\iota_{3}$ が成り立つ.
19. [R2]より, $\pi_{n + 1}^{n} = \mathbb{Z}/2\{E^{n - 3}\eta_{3}\}$.
20. これより, $\Delta\left(\iota_{5}\right) = \pm [\iota_{2}, \iota_{2}]$.
21. $\Delta\left(\iota_{5}\right) = \pm [\iota_{2}, \iota_{2}]$.
22. $\operatorname{Im}\Delta = \mathbb{Z}\{2\eta_{2}\}$.
23. 完全性より, $\ker E=\operatorname{Im}Δ=\mathbb{Z}\{2\eta_{2}\}$.
24. $\pi_{3}^{2} = \mathbb{Z}\{\eta_{2}\}$.
25. これより, $H: \pi_{6}^{3} \to \pi_{6}^{5}$ は全射.
26. これより, $\Delta: \pi_{6}^{5} \to \pi_{4}^{2}$ は零写像.
27. 完全性より,
28. \[ E: \pi_{4}^{2} \to \pi_{5}^{3}\quad\text{は単射}. \qquad (1) \]
29. 完全性より, $\ker \Delta=\operatorname{Im}H=\pi_{6}^{5}$ である.
30. \[ \pi_{6}^{5} \xrightarrow{\Delta} \pi_{4}^{2} \xrightarrow{E} \pi_{5}^{3} \xrightarrow{H} \pi_{5}^{5}. \]
31. $\Delta: \pi_{5}^{5} \to \pi_{3}^{2}$ は単射.
32. 完全性より, これより, $H: \pi_{5}^{3} \to \pi_{5}^{5}$ は零写像.
33. 完全性より,
34. \[ E: \pi_{4}^{2} \to \pi_{5}^{3}\quad\text{は全射}. \qquad (2) \]
35. (1), (2) より, $E: \pi_{4}^{2} \to \pi_{5}^{3}$ は同型.
36. $\eta_{4}=E\eta_{3}$.
37. $\eta_{3}\eta_{3} = \eta_{3}^{2}$.
38. これより, $\eta_{3} = \eta_{3}$.
39. $\pi_{5}^{5} = \mathbb{Z}\{\iota_{5}\}$.
40. $[\iota_{2}, \iota_{2}]$.
41. これより, $H([\iota_{2}, \iota_{2}]) = \pm 2\iota_{3}$ が成り立つ.
42. これより, $\pi_{4}^{5} = 0$.
43. 以上より, $\pi_{5}^{3} = \mathbb{Z}/2\{\eta_{3}^{2}\}$.
44. 証明木に記録された群構造の移送について、$\pi_{4}^{3} = \mathbb{Z}/2\{\eta_{3}\}$ と $E^{n - 3}: \pi_{3 + 1}^{3} \xrightarrow{\cong} \pi_{n + 1}^{n}$ から $\pi_{n + 1}^{n} = \mathbb{Z}/2\{E^{n - 3}\eta_{3}\}$ を得る。生成元の対応は $E^{n - 3}\eta_{3} = \eta_{n}$ である。
45. □

## 6. 今後の判断

- 子孫にあるという理由だけで既知結果を Reference や本文に採用してよいわけではない。
- 次の修正では根の直接依存・必要な EHP 導出・内部補助導出を区別する。
- 意味の異なる完全列を文字列一致だけで統合しない。
