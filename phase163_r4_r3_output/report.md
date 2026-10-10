# Phase 163 R4-R3 — Statement 実体と文献境界の対応監査

## 監査範囲
- ehp_rules.py
- hopf_rules.py
- relation_rules.py
- scalar_rules.py
- set_rules.py
- stable_rules.py
- toda_rules.py

## 集計（命題数ではない）
- boundary_components: 67
- boundary_rule_mapping_names: 72
- rule_constructor_sites: 403
- unlinked_boundary_components: 10

## 対応状態
- aggregate_or_no_component: 5
- candidate_mapped_metadata_only: 67

## InferenceRule 生成箇所の状態
- listed_in_boundary_mapping: 63
- not_listed_in_boundary_mapping: 340

## 注意・未解決事項
- Only literal InferenceRule names and literal mapping dictionaries are inspected.
- Constructor sites are not instantiated runtime rules or unique theorems.
- A boundary mapping is not verified mathematical Statement equality.
- Definitions, indirect registrations, dynamic names and proof positions remain unverified.
- No citation availability or semantic equivalence is inferred.
- Existing registries, proof search and renderer are untouched.

**これは対応候補の監査であり、全命題統合の完了ではない。**
全体 pytest は Phase 163 の最後まで実施しない。
