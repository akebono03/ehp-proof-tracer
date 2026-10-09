# Phase 162 R4-A 監査結果

対象: $\pi_5^4$

## 判定（候補分類であり、数学的な証明認定ではない）

- toda45: TREE_PRESENT_CANDIDATE / tree=[16] / presentation=[5] / public=True / baseline=True
- base_group: TREE_PRESENT_CANDIDATE / tree=[0, 1, 2, 3, 4, 5, 8, 14, 20, 22] / presentation=[0, 1, 2, 3, 4, 7] / public=True / baseline=False
- generator_transport: RENDERER_ONLY_CANDIDATE / tree=[] / presentation=[] / public=True / baseline=False
- target_structure: TREE_PRESENT_CANDIDATE / tree=[0, 1, 2, 3, 4, 5, 8, 14, 20, 22] / presentation=[0, 1, 2, 3, 4, 7] / public=True / baseline=True

## 証明木

root: `Relation(lhs=TodaPrimaryGroup(group_dimension=5, sphere_dimension=4), rhs=FiniteCyclicGroup(order=2, generator=HomotopyElement(name='η_4', dimension=4, source=5, target=4, generator=GeneratorSymbol(family='η', index=4, decoration=None))), relation_type=<RelationType.EQUALITY: 'equality'>, source=None, note=None)`

| index | depth | statement type | inference rule | reference | premises |
|---:|---:|---|---|---|---:|
| 0 | 0 | Relation | None | None | 1 |
| 1 | 1 | Relation | Toda higher eta-family finite-cyclic generator bridge | None | 2 |
| 2 | 2 | Relation | Toda 4.5 generic finite-cyclic transport | None | 2 |
| 3 | 3 | Relation | Toda pi_4^3 eta_3 generator notation | None | 2 |
| 4 | 4 | Relation | Toda pi_4^3 finite cyclic quotient calculation | None | 3 |
| 5 | 5 | Relation | Toda Proposition 5.1 pi_3^2 group relation | LiteratureReference(label='Toda Proposition 5.1', author='H. Toda', title='Composition Methods in Homotopy Groups of Spheres', year=1962, locator='Proposition 5.1') | 0 |
| 6 | 5 | TodaSuspensionKernelFreeCyclicStatement | Toda pi_4^3 exactness Delta image equals E kernel | None | 2 |
| 7 | 6 | TodaDeltaImageFreeCyclicStatement | free cyclic generator Delta image | None | 2 |
| 8 | 7 | Relation | Toda (5.1) diagonal identity group | LiteratureReference(label='Toda (5.1)', author='H. Toda', title='Composition Methods in Homotopy Groups of Spheres', year=1962, locator='(5.1)') | 0 |
| 9 | 7 | TodaDeltaImageUpToSignStatement | Toda Proposition 5.1 Delta iota_5 | LiteratureReference(label='Toda Proposition 5.1', author='H. Toda', title='Composition Methods in Homotopy Groups of Spheres', year=1962, locator='Proposition 5.1') | 0 |
| 10 | 6 | TodaProp42ExactnessStatement | None | None | 0 |
| 11 | 5 | TodaSuspensionSurjectiveStatement | Toda pi_4^3 E-H exactness zero-right suspension surjectivity | None | 2 |
| 12 | 6 | TodaPrimaryGroupZeroStatement | Toda (5.1) sphere connectivity zero | LiteratureReference(label='Toda (5.1)', author='H. Toda', title='Composition Methods in Homotopy Groups of Spheres', year=1962, locator='(5.1)') | 0 |
| 13 | 6 | TodaProp42ExactnessStatement | None | None | 0 |
| 14 | 4 | Relation | Toda eta_3 notation suspension bridge | None | 1 |
| 15 | 5 | TodaEtaFamilyDefinitionStatement | None | None | 0 |
| 16 | 3 | Toda45IsomorphismStatement | Toda 4.5 stable-range iterated suspension isomorphism | None | 3 |
| 17 | 4 | ScalarGreaterEqualStatement | None | None | 0 |
| 18 | 4 | ScalarGreaterEqualStatement | None | None | 0 |
| 19 | 4 | TodaIteratedSuspensionMap | None | None | 0 |
| 20 | 2 | Relation | Toda higher eta-family iterated suspension bridge | None | 2 |
| 21 | 3 | TodaEtaFamilyDefinitionStatement | None | None | 0 |
| 22 | 3 | Relation | Toda eta_3 notation suspension bridge | None | 1 |
| 23 | 4 | TodaEtaFamilyDefinitionStatement | None | None | 0 |

## baseline経路の例外

なし

## 解釈上の注意

- type 名の出現だけでは、結論に必要な数学的依存関係の存在を証明しない。
- `public.md` は現在のstable専用経路を含む。
- `baseline.md` は既存baselineを呼び出すが、semantic closureを含む。
- `audit.json` の各 conclusion_repr と presentation_edges を照合してR4-Bの方針を判断する。
- R4-Aでは削除・公開関数の切替・推論規則の追加を行わない。
