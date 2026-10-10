# Phase 163 R4 — 部分統合監査

この件数は bridge に読み込んだ登録レコード数であり、数学的に異なる全命題数ではない。

## データソース別
- boundary: 67
- theorem_fact: 1

## 状態別
- metadata_only: 67
- unresolved_source: 1

## 未解決

- theorem_fact / 0: LiteratureReference.locator is missing; no attribution invented

## R4 の境界

- toda_rules.py の全推論規則についての網羅的移行は未実施。
- standard_repository.py の ProofStep は明示的に渡した場合だけ橋渡しする。
- boundary component は構造化した数学的 Statement ではなく metadata_only。
- Definition の出典調査・全件登録は未実施。
- 数学的同値性や文献内の証明完了時点は推定していない。
- 既存 API、proof search、renderer の動作は変更しない。
- 全体 pytest は未実施。
