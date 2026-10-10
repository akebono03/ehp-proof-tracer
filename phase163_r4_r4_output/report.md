# Phase 163 R4-R4 — 数学的役割候補の分類監査

## 候補数（命題数ではない）

- InferenceRule 生成箇所: 403
- toda_rules.py の未掲載候補: 277
- 明示規則名への対応がない文献 component: 10

## 分類

- general_inference_candidate: 63
- literature_mapping_candidate: 63
- toda_rule_unclassified: 277

## 制約

- Role labels are candidates only, not verified theorem identities.
- A constructor site is not an instantiated rule or a unique statement.
- A non-Toda rule is not necessarily generic mathematics.
- Unlisted Toda rules can be fixed statements, specializations, or helper rules.
- No automatic conversion into Unified Statement Registry is performed.
- Definitions and runtime registrations are not exhaustively audited.
- Publication and proof-completion order remain unknown.
- No proof search, renderer, or existing API is modified.

**全命題の統合・数学的同一性検証は未完了。**
全体 pytest は未実施。
