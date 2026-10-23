# Phase 168 R3-35 — Reference 命題本文の接続監査

監査専用・変更なし

## pi_3^2

registry_available: True

### [R1] (5.1)
assertion_ids: ['shared:1:adopted:assertion:6', 'shared:1:adopted:assertion:1', 'shared:1:adopted:assertion:2', 'shared:1:adopted:assertion:4']
reference_ids: ['shared:1:adopted:ref:6', 'shared:1:adopted:ref:1', 'shared:1:adopted:ref:2', 'shared:1:adopted:ref:4']
step_indices: [0, 4, 5, 13]
- assertion shared:1:adopted:assertion:6: type=TodaPrimaryGroupZeroStatement, renderable=True, latex=\pi_{2}^{1} = 0, problem=None
- assertion shared:1:adopted:assertion:1: type=Relation, renderable=True, latex=\pi_{1}^{1} = \mathbb{Z}\{\iota_{1}\}, problem=None
- assertion shared:1:adopted:assertion:2: type=Relation, renderable=True, latex=\pi_{2}^{2} = \mathbb{Z}\{\iota_{2}\}, problem=None
- assertion shared:1:adopted:assertion:4: type=Relation, renderable=True, latex=\pi_{3}^{3} = \mathbb{Z}\{\iota_{3}\}, problem=None
- step 0: type=TodaPrimaryGroupZeroStatement, latex=\pi_{2}^{1} = 0, fallback=None
- step 4: type=Relation, latex=\pi_{1}^{1} = \mathbb{Z}\{\iota_{1}\}, fallback=None
- step 5: type=Relation, latex=\pi_{2}^{2} = \mathbb{Z}\{\iota_{2}\}, fallback=None
- step 13: type=Relation, latex=\pi_{3}^{3} = \mathbb{Z}\{\iota_{3}\}, fallback=None

### [R2] Proposition 4.2 (4.4)
assertion_ids: ['shared:5:adopted:assertion:prop42:general']
reference_ids: ['shared:5:adopted:reference:prop42:general']
step_indices: [1]
- assertion shared:5:adopted:assertion:prop42:general: type=TodaProp42GeneralExactnessStatement, renderable=False, latex=None, problem=None
- step 1: type=TodaProp42GeneralExactnessStatement, latex=None, fallback=TodaProp42GeneralExactnessStatement

### [R3] Foundational: suspension identity
assertion_ids: []
reference_ids: []
step_indices: [6]
- step 6: type=GeneratorSuspension, latex=None, fallback=GeneratorSuspension

### [R4] Proposition 5.1
assertion_ids: ['shared:1:adopted:assertion:5']
reference_ids: ['shared:1:adopted:ref:5']
step_indices: [14]
- assertion shared:1:adopted:assertion:5: type=GeneratorImage, renderable=False, latex=None, problem=None
- step 14: type=GeneratorImage, latex=None, fallback=GeneratorImage
## pi_4^3

registry_available: True

### [R1] Chapter V, i) The Groups pi^(n)_(n+1), eta-family notation
assertion_ids: ['shared:7:adopted:assertion:toda5:eta_family_definition']
reference_ids: ['shared:7:adopted:reference:toda5:eta_family_definition']
step_indices: [0]
- assertion shared:7:adopted:assertion:toda5:eta_family_definition: type=TodaEtaFamilyGeneralDefinition, renderable=False, latex=None, problem=None
- step 0: type=TodaEtaFamilyGeneralDefinition, latex=None, fallback=TodaEtaFamilyGeneralDefinition

### [R2] (5.1)
assertion_ids: ['shared:3:adopted:assertion:toda51:diagonal', 'shared:6:adopted:assertion:toda51:below_diagonal_zero']
reference_ids: ['shared:3:adopted:toda51:diagonal', 'shared:6:adopted:reference:toda51:below_diagonal_zero']
step_indices: [5, 15]
- assertion shared:3:adopted:assertion:toda51:diagonal: type=Relation, renderable=True, latex=\pi_{n}^{n} = \mathbb{Z}\{\iota_{n}\}, problem=None
- assertion shared:6:adopted:assertion:toda51:below_diagonal_zero: type=Toda51BelowDiagonalZeroStatement, renderable=False, latex=None, problem=None
- step 5: type=Relation, latex=\pi_{n}^{n} = \mathbb{Z}\{\iota_{n}\}, fallback=None
- step 15: type=Toda51BelowDiagonalZeroStatement, latex=None, fallback=Toda51BelowDiagonalZeroStatement

### [R3] Proposition 5.1
assertion_ids: ['shared:2:toda:adopted:prop5.1:finite_dimensional:component:delta_iota5_relation', 'shared:2:toda:adopted:prop5.1:finite_dimensional:component:pi3_2_group_relation']
reference_ids: ['shared:2:adopted:toda:adopted:prop5.1:finite_dimensional']
step_indices: [7, 21]
- assertion shared:2:toda:adopted:prop5.1:finite_dimensional:component:delta_iota5_relation: type=TodaDeltaImageUpToSignStatement, renderable=True, latex=\Delta\left(\iota_{5}\right) = \pm 2\eta_{2}, problem=None
- assertion shared:2:toda:adopted:prop5.1:finite_dimensional:component:pi3_2_group_relation: type=Relation, renderable=True, latex=\pi_{3}^{2} = \mathbb{Z}\{\eta_{2}\}, problem=None
- step 7: type=TodaDeltaImageUpToSignStatement, latex=\Delta\left(\iota_{5}\right) = \pm 2\eta_{2}, fallback=None
- step 21: type=Relation, latex=\pi_{3}^{2} = \mathbb{Z}\{\eta_{2}\}, fallback=None

### [R4] Proposition 4.2 (4.4)
assertion_ids: ['shared:5:adopted:assertion:prop42:general']
reference_ids: ['shared:5:adopted:reference:prop42:general']
step_indices: [9]
- assertion shared:5:adopted:assertion:prop42:general: type=TodaProp42GeneralExactnessStatement, renderable=False, latex=None, problem=None
- step 9: type=TodaProp42GeneralExactnessStatement, latex=None, fallback=TodaProp42GeneralExactnessStatement
## pi_5^4

registry_available: True

### [R1] Chapter V, i) The Groups pi^(n)_(n+1), eta-family notation
assertion_ids: ['shared:7:adopted:assertion:toda5:eta_family_definition']
reference_ids: ['shared:7:adopted:reference:toda5:eta_family_definition']
step_indices: [0]
- assertion shared:7:adopted:assertion:toda5:eta_family_definition: type=TodaEtaFamilyGeneralDefinition, renderable=False, latex=None, problem=None
- step 0: type=TodaEtaFamilyGeneralDefinition, latex=None, fallback=TodaEtaFamilyGeneralDefinition

### [R2] Proposition 5.1
assertion_ids: []
reference_ids: []
step_indices: [5]
- step 5: type=Relation, latex=\pi_{4}^{3} = \mathbb{Z}/2\{\eta_{3}\}, fallback=None

### [R3] (4.5)
assertion_ids: []
reference_ids: []
step_indices: [6]
- step 6: type=Toda45IsomorphismStatement, latex=None, fallback=Toda45IsomorphismStatement

## 判断の限界

- 引用された命題内容と固定基準の一般公式が一致するかは、出力を個別に照合する必要がある。
- 引用された具体的ステップを一般命題として言い換えることはしない。
- 監査は source/assertion の型と引用接続を記録するだけで、本文を変更しない。
