# Phase 163 R1D — 登録実体と重複候補の横断監査

既存コードへの変更・import 実行を行わない静的監査。集計は数学的に異なる命題の数ではない。

## 集計

- inspected_registration_files: 25
- registration_sites: 115
- statement_type_definition_sites: 162
- literal_entry_keys: 8
- duplicate_literal_key_candidates: 0
- repeated_entry_expression_candidates: 1
- container_constructor: 5
- entry_constructor: 21
- reference_constructor: 50
- registration_call: 39

## 解釈上の注意

- A constructor site is not a mathematical statement count
- Same signature hash is not a proof of mathematical identity
- Dynamic registration and runtime instances not counted
- Literature publication order and availability not checked
- Fixed statements and proof-internal steps not yet validated
- AST call detection can miss indirect or aliased constructors

R1 完了には、登録候補の実体・数学的同一性・追加の登録方式を確認する必要がある。R2 の新規 Registry は実装しない。
