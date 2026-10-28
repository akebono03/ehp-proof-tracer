# Phase 169 R10ET-R1 — Definition / Reference 依存関係監査

監査方式：AUDIT_ONLY。記録は実行時の検証済み Proof Tree から取得。

- Branch: `develop`
- HEAD: `36e4dc41427ec4437009c96b01cacb07dc165bf6`
- 期待 HEAD: `36e4dc41427ec4437009c96b01cacb07dc165bf6`
- HEAD 一致: `True`
- 既存 tracked 差分は不変: `True`
- 全体 pytest: 実行しない

## 実行結果

| 群 | 探索 | Trust | 共通 Definition 実使用 / 適用可能 / 引用付き適用可能 | Reference |
|---|---|---|---|---|
| `pi_69^43` | complete | PASS | 30/108/78 | 4 |
| `pi_56^30` | complete | PASS | 4/16/12 | 4 |
| `pi_41^30` | complete | PASS | 0/17/17 | 3 |
| `pi_44^30` | complete | PASS | 14/49/35 | 3 |
| `pi_46^30` | complete | PASS | 12/48/36 | 4 |
| `pi_39^30` | complete | PASS | 0/139/139 | 6 |
| `pi_3^2` | complete | PASS | 0/0/0 | 4 |
| `pi_4^3` | complete | PASS | 0/0/0 | 4 |
| `pi_5^4` | complete | PASS | 0/0/0 | 3 |
| `pi_4^2` | complete | PASS | 0/0/0 | 2 |
| `pi_5^3` | complete | PASS | 0/0/0 | 6 |
| `pi_6^4` | complete | PASS | 0/0/0 | 5 |

## Citation / image ancestor evidence

### `pi_69^43`

- status=complete, trust=PASS
- [R1] DB prior: sphere.csv (n=28, k=26) | root祖先=True | GIVEN=True | image祖先=[] | 本文マーカー=True
- [R2] (4.5) | root祖先=True | GIVEN=True | image祖先=[] | 本文マーカー=True
- [R3] Chapter V, ν-family definition (after Lemma 5.5) | root祖先=True | GIVEN=True | image祖先=[6, 9, 11, 12, 14, 16, 18, 19, 20, 22, 24, 25, 27, 29, 30, 32, 34, 35, 37, 39, 40, 42, 44, 45, 47, 49, 50, 52, 54, 55, 57, 59, 60, 62, 64, 65, 67, 69, 70, 72, 74, 75, 77, 79, 80, 82, 84, 85] | 本文マーカー=True
- [R4] Chapter V, i) | root祖先=True | GIVEN=True | image祖先=[90, 92, 95, 97, 100, 102, 105, 107, 110, 112, 115, 117, 120, 122, 125, 127, 130, 132, 135, 137, 140, 142, 145, 147, 150, 152, 155, 157, 160, 162] | 本文マーカー=True
- root 直前2前提の支持引用: [{'index': 0, 'type': 'Relation', 'conclusion_repr': "Relation(lhs=TodaPrimaryGroup(group_dimension=54, sphere_dimension=28), rhs=DirectSumGroup(summands=(FiniteCyclicGroup(order=2, generator=Composition(left=HomotopyElement(name='ν₂₈', dimension=28, source=31, target=28, generator=GeneratorSymbol(family='ν', index=28, decoration=None)), right=Composition(left=HomotopyElement(name='ν₃₁', dimension=31, source=34, target=31, generator=GeneratorSymbol(family='ν', index=31, decoration=None)), right=HomotopyElement(name='κ̅₃₄', dimension=34, source=54, target=34, generator=GeneratorSymbol(family='\\\\bar{\\\\kappa}', index=34, decoration=None))))), FiniteCyclicGroup(order=2, generator=Composition(left=HomotopyElement(name='η₂₈', dimension=28, source=29, target=28, generator=GeneratorSymbol(family='η',  [repr truncated]", 'citation_numbers': [1]}, {'index': 2, 'type': 'Toda45IsomorphismStatement', 'conclusion_repr': 'Toda45IsomorphismStatement(map=TodaIteratedSuspensionMap(exponent=15, source_group=TodaPrimaryGroup(group_dimension=54, sphere_dimension=28), target_group=TodaPrimaryGroup(group_dimension=69, sphere_dimension=43)))', 'citation_numbers': [2]}]
- 直和圧縮: {'statement': '[R3], [R4]より, $E^{15}(\\nu_{28}^{2}\\bar{\\kappa}_{34})=\\nu_{43}^{2}\\bar{\\kappa}_{49}$、$E^{15}(\\eta_{28}\\mu_{3,29})=\\eta_{43}\\mu_{3,44}$.', 'hidden_indices': [6, 9, 10, 11, 12, 14, 16, 17, 18, 19, 20, 22, 23, 24, 25, 27, 28, 29, 30, 32, 33, 34, 35, 37, 38, 39, 40, 42, 43, 44, 45, 47, 48, 49, 50, 52, 53, 54, 55, 57, 58, 59, 60, 62, 63, 64, 65, 67, 68, 69, 70, 72, 73, 74, 75, 77, 78, 79, 80, 82, 83, 84, 85, 89, 90, 91, 92, 94, 95, 96, 97, 99, 100, 101, 102, 104, 105, 106, 107, 109, 110, 111, 112, 114, 115, 116, 117, 119, 120, 121, 122, 124, 125, 126, 127, 129, 130, 131, 132, 134, 135, 136, 137, 139, 140, 141, 142, 144, 145, 146, 147, 149, 150, 151, 152, 154, 155, 156, 157, 159, 160, 161, 162], 'citation_numbers': [3, 4]}

### `pi_56^30`

- status=complete, trust=PASS
- [R1] DB prior: sphere.csv (n=28, k=26) | root祖先=True | GIVEN=True | image祖先=[] | 本文マーカー=True
- [R2] (4.5) | root祖先=True | GIVEN=True | image祖先=[] | 本文マーカー=True
- [R3] Chapter V, ν-family definition (after Lemma 5.5) | root祖先=True | GIVEN=True | image祖先=[6, 9, 11, 12, 14, 16, 18, 19] | 本文マーカー=True
- [R4] Chapter V, i) | root祖先=True | GIVEN=True | image祖先=[24, 26, 29, 31] | 本文マーカー=True
- root 直前2前提の支持引用: [{'index': 0, 'type': 'Relation', 'conclusion_repr': "Relation(lhs=TodaPrimaryGroup(group_dimension=54, sphere_dimension=28), rhs=DirectSumGroup(summands=(FiniteCyclicGroup(order=2, generator=Composition(left=HomotopyElement(name='ν₂₈', dimension=28, source=31, target=28, generator=GeneratorSymbol(family='ν', index=28, decoration=None)), right=Composition(left=HomotopyElement(name='ν₃₁', dimension=31, source=34, target=31, generator=GeneratorSymbol(family='ν', index=31, decoration=None)), right=HomotopyElement(name='κ̅₃₄', dimension=34, source=54, target=34, generator=GeneratorSymbol(family='\\\\bar{\\\\kappa}', index=34, decoration=None))))), FiniteCyclicGroup(order=2, generator=Composition(left=HomotopyElement(name='η₂₈', dimension=28, source=29, target=28, generator=GeneratorSymbol(family='η',  [repr truncated]", 'citation_numbers': [1]}, {'index': 2, 'type': 'Toda45IsomorphismStatement', 'conclusion_repr': 'Toda45IsomorphismStatement(map=TodaIteratedSuspensionMap(exponent=2, source_group=TodaPrimaryGroup(group_dimension=54, sphere_dimension=28), target_group=TodaPrimaryGroup(group_dimension=56, sphere_dimension=30)))', 'citation_numbers': [2]}]
- 直和圧縮: {'statement': '[R3], [R4]より, $E^{2}(\\nu_{28}^{2}\\bar{\\kappa}_{34})=\\nu_{30}^{2}\\bar{\\kappa}_{36}$、$E^{2}(\\eta_{28}\\mu_{3,29})=\\eta_{30}\\mu_{3,31}$.', 'hidden_indices': [6, 9, 10, 11, 12, 14, 16, 17, 18, 19, 23, 24, 25, 26, 28, 29, 30, 31], 'citation_numbers': [3, 4]}

### `pi_41^30`

- status=complete, trust=PASS
- [R1] DB prior: sphere.csv (n=13, k=11) | root祖先=True | GIVEN=True | image祖先=[] | 本文マーカー=True
- [R2] (4.5) | root祖先=True | GIVEN=True | image祖先=[] | 本文マーカー=True
- [R3] Chapter VI, v) Definition of indexed elements | root祖先=True | GIVEN=True | image祖先=[6, 8, 10, 12, 14, 16, 18, 20, 22, 24, 26, 28, 30, 32, 34, 36, 38] | 本文マーカー=False
- root 直前2前提の支持引用: [{'index': 0, 'type': 'Relation', 'conclusion_repr': "Relation(lhs=TodaPrimaryGroup(group_dimension=24, sphere_dimension=13), rhs=FiniteCyclicGroup(order=8, generator=HomotopyElement(name='ζ₁₃', dimension=13, source=24, target=13, generator=GeneratorSymbol(family='\\\\zeta', index=13, decoration=None))), relation_type=<RelationType.EQUALITY: 'equality'>, source=None, note=None)", 'citation_numbers': [1]}, {'index': 2, 'type': 'Toda45IsomorphismStatement', 'conclusion_repr': 'Toda45IsomorphismStatement(map=TodaIteratedSuspensionMap(exponent=17, source_group=TodaPrimaryGroup(group_dimension=24, sphere_dimension=13), target_group=TodaPrimaryGroup(group_dimension=41, sphere_dimension=30)))', 'citation_numbers': [2]}]
- 直和圧縮: None

### `pi_44^30`

- status=complete, trust=PASS
- [R1] DB prior: sphere.csv (n=16, k=14) | root祖先=True | GIVEN=True | image祖先=[] | 本文マーカー=True
- [R2] (4.5) | root祖先=True | GIVEN=True | image祖先=[] | 本文マーカー=True
- [R3] Chapter V, σ-family definition (after Lemma 5.14) | root祖先=True | GIVEN=True | image祖先=[6, 9, 10, 12, 14, 15, 17, 19, 20, 22, 24, 25, 27, 29, 30, 32, 34, 35, 36, 38, 39, 41, 42, 44, 45, 47, 48, 50, 51, 53, 54, 56, 57, 59, 60] | 本文マーカー=True
- root 直前2前提の支持引用: [{'index': 0, 'type': 'Relation', 'conclusion_repr': "Relation(lhs=TodaPrimaryGroup(group_dimension=30, sphere_dimension=16), rhs=DirectSumGroup(summands=(FiniteCyclicGroup(order=2, generator=Composition(left=HomotopyElement(name='σ₁₆', dimension=16, source=23, target=16, generator=GeneratorSymbol(family='σ', index=16, decoration=None)), right=HomotopyElement(name='σ₂₃', dimension=23, source=30, target=23, generator=GeneratorSymbol(family='σ', index=23, decoration=None)))), FiniteCyclicGroup(order=2, generator=HomotopyElement(name='κ₁₆', dimension=16, source=30, target=16, generator=GeneratorSymbol(family='\\\\kappa', index=16, decoration=None))))), relation_type=<RelationType.EQUALITY: 'equality'>, source=None, note=None)", 'citation_numbers': [1]}, {'index': 2, 'type': 'Toda45IsomorphismStatement', 'conclusion_repr': 'Toda45IsomorphismStatement(map=TodaIteratedSuspensionMap(exponent=14, source_group=TodaPrimaryGroup(group_dimension=30, sphere_dimension=16), target_group=TodaPrimaryGroup(group_dimension=44, sphere_dimension=30)))', 'citation_numbers': [2]}]
- 直和圧縮: {'statement': 'Definition と [R3] より, $E^{14}(\\sigma_{16}^{2})=\\sigma_{30}^{2}$、$E^{14}(\\kappa_{16})=\\kappa_{30}$.', 'hidden_indices': [6, 9, 10, 12, 14, 15, 17, 19, 20, 22, 24, 25, 27, 29, 30, 32, 34, 35, 36, 38, 39, 41, 42, 44, 45, 47, 48, 50, 51, 53, 54, 56, 57, 59, 60, 61, 62, 63, 64, 65, 66, 67, 68, 69, 70, 71, 72, 73, 74], 'citation_numbers': [3]}

### `pi_46^30`

- status=complete, trust=PASS
- [R1] DB prior: sphere.csv (n=18, k=16) | root祖先=True | GIVEN=True | image祖先=[] | 本文マーカー=True
- [R2] (4.5) | root祖先=True | GIVEN=True | image祖先=[] | 本文マーカー=True
- [R3] Chapter V, σ-family definition (after Lemma 5.14) | root祖先=True | GIVEN=True | image祖先=[18, 23, 25, 28, 30, 33, 35, 38, 40, 43, 45, 48, 50, 53, 55, 58, 60, 63, 65, 68, 70, 73, 75, 78] | 本文マーカー=True
- [R4] Chapter VI, iii) The elements mu_n (definition) | root祖先=True | GIVEN=True | image祖先=[22, 23, 27, 28, 32, 33, 37, 38, 42, 43, 47, 48, 52, 53, 57, 58, 62, 63, 67, 68, 72, 73, 77, 78] | 本文マーカー=True
- root 直前2前提の支持引用: [{'index': 0, 'type': 'Relation', 'conclusion_repr': "Relation(lhs=TodaPrimaryGroup(group_dimension=34, sphere_dimension=18), rhs=DirectSumGroup(summands=(FiniteCyclicGroup(order=2, generator=HomotopyElement(name='ω₁₈', dimension=18, source=34, target=18, generator=GeneratorSymbol(family='\\\\omega', index=18, decoration=None))), FiniteCyclicGroup(order=2, generator=Composition(left=HomotopyElement(name='σ₁₈', dimension=18, source=25, target=18, generator=GeneratorSymbol(family='σ', index=18, decoration=None)), right=HomotopyElement(name='μ₂₅', dimension=25, source=34, target=25, generator=GeneratorSymbol(family='\\\\mu', index=25, decoration=None)))))), relation_type=<RelationType.EQUALITY: 'equality'>, source=None, note=None)", 'citation_numbers': [1]}, {'index': 2, 'type': 'Toda45IsomorphismStatement', 'conclusion_repr': 'Toda45IsomorphismStatement(map=TodaIteratedSuspensionMap(exponent=12, source_group=TodaPrimaryGroup(group_dimension=34, sphere_dimension=18), target_group=TodaPrimaryGroup(group_dimension=46, sphere_dimension=30)))', 'citation_numbers': [2]}]
- 直和圧縮: {'statement': 'Definition と [R3], [R4] より, $E^{12}(\\omega_{18})=\\omega_{30}$、$E^{12}(\\sigma_{18}\\mu_{25})=\\sigma_{30}\\mu_{37}$.', 'hidden_indices': [3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 18, 22, 23, 25, 27, 28, 30, 32, 33, 35, 37, 38, 40, 42, 43, 45, 47, 48, 50, 52, 53, 55, 57, 58, 60, 62, 63, 65, 67, 68, 70, 72, 73, 75, 77, 78], 'citation_numbers': [3, 4]}

### `pi_39^30`

- status=complete, trust=PASS
- [R1] DB prior: sphere.csv (n=11, k=9) | root祖先=True | GIVEN=True | image祖先=[] | 本文マーカー=True
- [R2] (4.5) | root祖先=True | GIVEN=True | image祖先=[] | 本文マーカー=True
- [R3] Chapter V, ν-family definition (after Lemma 5.5) | root祖先=True | GIVEN=True | image祖先=[6, 9, 12, 13, 14, 16, 18, 20, 21, 22, 23, 24, 26, 27, 28, 30, 31, 32, 34, 35, 36, 38, 39, 40, 42, 43, 44, 46, 47, 48, 50, 51, 52, 54, 55, 56, 58, 59, 60, 62, 63, 64, 66, 67, 68, 70, 71, 72, 74, 75, 76, 78, 79, 80, 82, 83, 84, 86, 87, 88, 90, 91, 92] | 本文マーカー=True
- [R4] Chapter VI, iii) The elements mu_n (definition) | root祖先=True | GIVEN=True | image祖先=[96, 98, 100, 102, 104, 106, 108, 110, 112, 114, 116, 118, 120, 122, 124, 126, 128, 130, 132] | 本文マーカー=True
- [R5] Chapter V, i) | root祖先=True | GIVEN=True | image祖先=[137, 142, 145, 148, 151, 154, 157, 160, 163, 166, 169, 172, 175, 178, 181, 184, 187, 190, 193, 196, 199, 202, 205, 208, 211, 214, 217, 220, 223, 226, 229, 232, 235, 238, 241, 244, 247, 250] | 本文マーカー=True
- [R6] Chapter VI, i) The Elements epsilon_n (definition) | root祖先=True | GIVEN=True | image祖先=[141, 142, 147, 148, 153, 154, 159, 160, 165, 166, 171, 172, 177, 178, 183, 184, 189, 190, 195, 196, 201, 202, 207, 208, 213, 214, 219, 220, 225, 226, 231, 232, 237, 238, 243, 244, 249, 250] | 本文マーカー=True
- root 直前2前提の支持引用: [{'index': 0, 'type': 'Relation', 'conclusion_repr': "Relation(lhs=TodaPrimaryGroup(group_dimension=20, sphere_dimension=11), rhs=DirectSumGroup(summands=(FiniteCyclicGroup(order=2, generator=Composition(left=HomotopyElement(name='ν₁₁', dimension=11, source=14, target=11, generator=GeneratorSymbol(family='ν', index=11, decoration=None)), right=Composition(left=HomotopyElement(name='ν₁₄', dimension=14, source=17, target=14, generator=GeneratorSymbol(family='ν', index=14, decoration=None)), right=HomotopyElement(name='ν₁₇', dimension=17, source=20, target=17, generator=GeneratorSymbol(family='ν', index=17, decoration=None))))), FiniteCyclicGroup(order=2, generator=HomotopyElement(name='μ₁₁', dimension=11, source=20, target=11, generator=GeneratorSymbol(family='\\\\mu', index=11, decoration=None))) [repr truncated]", 'citation_numbers': [1]}, {'index': 2, 'type': 'Toda45IsomorphismStatement', 'conclusion_repr': 'Toda45IsomorphismStatement(map=TodaIteratedSuspensionMap(exponent=19, source_group=TodaPrimaryGroup(group_dimension=20, sphere_dimension=11), target_group=TodaPrimaryGroup(group_dimension=39, sphere_dimension=30)))', 'citation_numbers': [2]}]
- 直和圧縮: {'statement': '[R3], [R4], [R5], [R6]より, $E^{19}(\\nu_{11}^{3})=\\nu_{30}^{3}$、$E^{19}(\\mu_{11})=\\mu_{30}$、$E^{19}(\\eta_{11}\\varepsilon_{12})=\\eta_{30}\\varepsilon_{31}$.', 'hidden_indices': [6, 9, 12, 13, 14, 16, 18, 20, 21, 22, 23, 24, 26, 27, 28, 30, 31, 32, 34, 35, 36, 38, 39, 40, 42, 43, 44, 46, 47, 48, 50, 51, 52, 54, 55, 56, 58, 59, 60, 62, 63, 64, 66, 67, 68, 70, 71, 72, 74, 75, 76, 78, 79, 80, 82, 83, 84, 86, 87, 88, 90, 91, 92, 96, 98, 100, 102, 104, 106, 108, 110, 112, 114, 116, 118, 120, 122, 124, 126, 128, 130, 132, 136, 137, 141, 142, 144, 145, 147, 148, 150, 151, 153, 154, 156, 157, 159, 160, 162, 163, 165, 166, 168, 169, 171, 172, 174, 175, 177, 178, 180, 181, 183, 184, 186, 187, 189, 190, 192, 193, 195, 196, 198, 199, 201, 202, 204, 205, 207, 208, 210, 211, 213, 214, 216, 217, 219, 220, 222, 223, 225, 226, 228, 229, 231, 232, 234, 235, 237, 238, 240, 241, 243, 244, 246, 247, 249, 250], 'citation_numbers': [3, 4, 5, 6]}

### `pi_3^2`

- status=complete, trust=PASS
- [R1] (5.1) | root祖先=True | GIVEN=True | image祖先=[] | 本文マーカー=True
- [R2] Proposition 4.2 (4.4) | root祖先=True | GIVEN=True | image祖先=[] | 本文マーカー=True
- [R3] Foundational: suspension identity | root祖先=True | GIVEN=True | image祖先=[] | 本文マーカー=True
- [R4] Proposition 5.1 | root祖先=True | GIVEN=True | image祖先=[16] | 本文マーカー=True
- root 直前2前提の支持引用: [{'index': 14, 'type': 'MapIsomorphism', 'conclusion_repr': 'MapIsomorphism(map=TodaHopfInvariantMap(source_group=TodaPrimaryGroup(group_dimension=3, sphere_dimension=2), target_group=TodaPrimaryGroup(group_dimension=3, sphere_dimension=3)))', 'citation_numbers': [1, 2, 3]}, {'index': 15, 'type': 'Relation', 'conclusion_repr': "Relation(lhs=TodaPrimaryGroup(group_dimension=3, sphere_dimension=3), rhs=FreeCyclicGroup(generator=HomotopyElement(name='ι₃', dimension=3, source=3, target=3, generator=GeneratorSymbol(family='ι', index=3, decoration=None))), relation_type=<RelationType.EQUALITY: 'equality'>, source=None, note=None)", 'citation_numbers': [1]}]
- 直和圧縮: None

### `pi_4^3`

- status=complete, trust=PASS
- [R1] Chapter V, i) | root祖先=True | GIVEN=True | image祖先=[] | 本文マーカー=True
- [R2] (5.1) | root祖先=True | GIVEN=True | image祖先=[] | 本文マーカー=True
- [R3] Proposition 5.1 | root祖先=True | GIVEN=True | image祖先=[] | 本文マーカー=True
- [R4] Proposition 4.2 (4.4) | root祖先=True | GIVEN=True | image祖先=[] | 本文マーカー=True
- root 直前2前提の支持引用: [{'index': 23, 'type': 'CyclicStructureStatement', 'conclusion_repr': "CyclicStructureStatement(group=TodaPrimaryGroup(group_dimension=4, sphere_dimension=3), generator=HomotopyElement(name='η_3', dimension=3, source=4, target=3, generator=GeneratorSymbol(family='η', index=3, decoration=None)), order=2)", 'citation_numbers': [1, 2, 3, 4]}]
- 直和圧縮: None

### `pi_5^4`

- status=complete, trust=PASS
- [R1] Chapter V, i) | root祖先=True | GIVEN=True | image祖先=[] | 本文マーカー=True
- [R2] Proposition 5.1 | root祖先=True | GIVEN=True | image祖先=[] | 本文マーカー=True
- [R3] (4.5) | root祖先=True | GIVEN=True | image祖先=[] | 本文マーカー=True
- root 直前2前提の支持引用: [{'index': 8, 'type': 'Relation', 'conclusion_repr': "Relation(lhs=TodaPrimaryGroup(group_dimension=5, sphere_dimension=4), rhs=FiniteCyclicGroup(order=2, generator=IteratedSuspension(expression=HomotopyElement(name='η_3', dimension=3, source=4, target=3, generator=GeneratorSymbol(family='η', index=3, decoration=None)), exponent=1)), relation_type=<RelationType.EQUALITY: 'equality'>, source=None, note=None)", 'citation_numbers': [2, 3]}, {'index': 3, 'type': 'GeneratorSuspension', 'conclusion_repr': "GeneratorSuspension(map=TodaSuspensionMap(source_group=TodaPrimaryGroup(group_dimension=4, sphere_dimension=3), target_group=TodaPrimaryGroup(group_dimension=5, sphere_dimension=4)), source_generator=HomotopyElement(name='η₃', dimension=3, source=4, target=3, generator=GeneratorSymbol(family='η', index=3, decoration=None)), target_generator=HomotopyElement(name='η_4', dimension=4, source=5, target=4, generator=GeneratorSymbol(family='η', index=4, decoration=None)))", 'citation_numbers': [1]}]
- 直和圧縮: None

### `pi_4^2`

- status=complete, trust=PASS
- [R1] Proposition 5.1 | root祖先=True | GIVEN=True | image祖先=[] | 本文マーカー=True
- [R2] (5.2) | root祖先=True | GIVEN=True | image祖先=[] | 本文マーカー=True
- root 直前2前提の支持引用: [{'index': 0, 'type': 'Relation', 'conclusion_repr': "Relation(lhs=TodaPrimaryGroup(group_dimension=4, sphere_dimension=3), rhs=FiniteCyclicGroup(order=2, generator=HomotopyElement(name='η_3', dimension=3, source=4, target=3, generator=GeneratorSymbol(family='η', index=3, decoration=None))), relation_type=<RelationType.EQUALITY: 'equality'>, source=None, note=None)", 'citation_numbers': [1]}, {'index': 1, 'type': 'Toda52UniversalStatement', 'conclusion_repr': "Toda52UniversalStatement(map_formula='alpha -> eta_2 o alpha', source_group='pi_i^3', target_group='pi_i^2', variable='i', minimum_i=3)", 'citation_numbers': [2]}]
- 直和圧縮: None

### `pi_5^3`

- status=complete, trust=PASS
- [R1] DB prior: sphere.csv (n=2, k=2) [参考: Proposition 5.3] | root祖先=True | GIVEN=True | image祖先=[] | 本文マーカー=True
- [R2] (5.3) | root祖先=True | GIVEN=True | image祖先=[] | 本文マーカー=True
- [R3] Proposition 5.1 | root祖先=True | GIVEN=True | image祖先=[] | 本文マーカー=True
- [R4] Proposition 4.2 (4.4) | root祖先=True | GIVEN=True | image祖先=[] | 本文マーカー=True
- [R5] (5.1) | root祖先=True | GIVEN=True | image祖先=[] | 本文マーカー=True
- [R6] Chapter V, i) | root祖先=True | GIVEN=True | image祖先=[25] | 本文マーカー=True
- root 直前2前提の支持引用: [{'index': 0, 'type': 'Relation', 'conclusion_repr': "Relation(lhs=TodaPrimaryGroup(group_dimension=4, sphere_dimension=2), rhs=FiniteCyclicGroup(order=2, generator=Composition(left=HomotopyElement(name='η₂', dimension=2, source=3, target=2, generator=GeneratorSymbol(family='η', index=2, decoration=None)), right=HomotopyElement(name='η₃', dimension=3, source=4, target=3, generator=GeneratorSymbol(family='η', index=3, decoration=None)))), relation_type=<RelationType.EQUALITY: 'equality'>, source=None, note=None)", 'citation_numbers': [1]}, {'index': 18, 'type': 'TodaSuspensionIsomorphismStatement', 'conclusion_repr': 'TodaSuspensionIsomorphismStatement(map=TodaSuspensionMap(source_group=TodaPrimaryGroup(group_dimension=4, sphere_dimension=2), target_group=TodaPrimaryGroup(group_dimension=5, sphere_dimension=3)))', 'citation_numbers': [2, 3, 4, 5]}]
- 直和圧縮: None

### `pi_6^4`

- status=complete, trust=PASS
- [R1] DB prior: sphere.csv (n=3, k=2) [参考: Proposition 5.3] | root祖先=True | GIVEN=True | image祖先=[] | 本文マーカー=True
- [R2] Proposition 4.4 | root祖先=True | GIVEN=True | image祖先=[] | 本文マーカー=True
- [R3] Proposition 4.2 (4.4) | root祖先=True | GIVEN=True | image祖先=[] | 本文マーカー=True
- [R4] (5.1) | root祖先=True | GIVEN=True | image祖先=[] | 本文マーカー=True
- [R5] Chapter V, i) | root祖先=True | GIVEN=True | image祖先=[15] | 本文マーカー=True
- root 直前2前提の支持引用: [{'index': 0, 'type': 'Relation', 'conclusion_repr': "Relation(lhs=TodaPrimaryGroup(group_dimension=5, sphere_dimension=3), rhs=FiniteCyclicGroup(order=2, generator=Composition(left=HomotopyElement(name='η₃', dimension=3, source=4, target=3, generator=GeneratorSymbol(family='η', index=3, decoration=None)), right=HomotopyElement(name='η₄', dimension=4, source=5, target=4, generator=GeneratorSymbol(family='η', index=4, decoration=None)))), relation_type=<RelationType.EQUALITY: 'equality'>, source=None, note=None)", 'citation_numbers': [1]}, {'index': 8, 'type': 'TodaSuspensionIsomorphismStatement', 'conclusion_repr': 'TodaSuspensionIsomorphismStatement(map=TodaSuspensionMap(source_group=TodaPrimaryGroup(group_dimension=5, sphere_dimension=3), target_group=TodaPrimaryGroup(group_dimension=6, sphere_dimension=4)))', 'citation_numbers': [2, 3, 4]}]
- 直和圧縮: None

## 判定上の注意

- `image_cited_but_common_eligible` は **差し替え候補** であり、既存の証明から引用を削除してよいことの証明ではない。
- [R] が root の祖先なら、現行 Proof Tree で使用中。表示だけで消さない。
- (4.5) と DB prior は別の支持事実なので、Definition だけで代用しない。
- 依存置換の採否は、次段階の最小修正と限定テストで確認する。
