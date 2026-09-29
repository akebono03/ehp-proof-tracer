# Phase 146-9 Historical Difference Root-Cause Classification

## Scope

Production changes: none.

This audit groups the Phase 146-8 visible differences by internal cause. It does not treat every LOST/ADDED unit as an independent bug.

## Phase 146-8 baseline

- historical units: 17
- current units: 82
- PRESERVED: 0
- LOST: 17
- ADDED: 47
- MOVED: 0
- DUPLICATED: 35
- REWORDED: 0
- UNMATCHED: 0
- sequence-related units: historical 4 / current 44
- [R#] units: historical 8 / current 1

## Current pi_6^3 argument diagnostics

| index | role | method evidence | components | primary | primary windows | contributions |
| ---: | --- | ---: | ---: | --- | ---: | ---: |
| 0 | establish_group_structure | 3 | 1 | yes | 3 | 2 |
| 1 | establish_order | 2 | 1 | yes | 2 | 2 |
| 2 | establish_definition | 0 | 0 | no | 0 | 0 |

### Order argument

- purpose: $\nu'$ の位数を決定する.
- supporting roles: ('calculation', 'group_structure', 'map_property')
- primary exactness component: True
- contributions: 2

### Group-structure argument

- purpose: $\pi_{6}^{3}$ の群構造を決定する.
- supporting roles: ('membership', 'group_structure', 'map_property', 'exactness', 'map_property', 'group_structure')
- primary exactness component: True
- contributions: 2

## Renderer-layer evidence

- base multi-argument chars: 1377
- contribution-connected chars: 1579
- contribution renderer changes output: True
- argument builder uses direct dependency indices: True
- contribution renderer performs post-render insertion: True

## Root-cause classification

### RC1: Argument-method ownership is narrower than historical proof-purpose ownership

Phase 146-7 purpose fusion works only when a primary exactness component is selected. The order argument and group-structure argument differ at the method-evidence/component/primary-selection layer.

Mapped Phase 146-8 differences:
- 4. order argument と主要 EHP 完全列の ownership
- 5. EHP exact-sequence method introduction (partly)

### RC2: Recursive exactness evidence is exposed as body/contribution material

Exactness evidence not absorbed as the primary method remains eligible for body/contribution rendering. This explains the large increase in sequence-related material and is upstream of much of the visible noise.

Mapped Phase 146-8 differences:
- 6. 主要完全列の適切な範囲選択
- 7. 補助完全列の本文抑制
- 8. 重複 contribution の一部

### RC3: Contribution ownership/insertion is separate from argument dependency narration

The connected renderer first renders arguments and then inserts selected contributions around anchors. Therefore facts can be mathematically available yet appear outside the historical explanatory position.

Mapped Phase 146-8 differences:
- 8. 重複 contribution の一部
- 9. dependency order に沿った式配置
- 10. map-property chain の配置
- 11. short exact sequence → group structure の順序

### RC4: Historical provenance/reason prose is not reconstructed from generic provenance

Current reference presentation preserves compact references, but the historical '[R#] の n=... の場合より' derivation prose is not generally reconstructed.

Mapped Phase 146-8 differences:
- 1. Reference section の詳細
- 2. Reference → derived fact の理由付け
- 3. definition argument の理由文章の一部

### RC5: Exactness semantic type is rendered generically rather than as an EHP-named method

The generic transition says '次の完全列を考える' and does not encode the historical EHP family name.

Mapped Phase 146-8 differences:
- 5. EHP exact sequence の semantic naming

### RC6: Equation numbering is downstream of the selected/ordered narrative stream

Because selection and ordering differ from the historical proof, equation numbering also differs. This should be repaired after RC1-RC5 rather than with target-specific tag rules.

Mapped Phase 146-8 differences:
- 12. equation numbering / prose formatting

## Consolidated result

- visible difference families from Phase 146-8: 12
- root-cause families after consolidation: 6

Recommended dependency order:

RC1 → RC2 → RC3 → RC4 → RC5 → RC6

RC6 is intentionally last because numbering/formatting is downstream of selection and ordering. RC5 may be implemented independently after RC1 if desired, but should not be used to hide ownership defects.

## Boundary

This audit does not change route gates, exactness ownership, contribution selection, provenance rendering, EHP naming, or equation numbering.
