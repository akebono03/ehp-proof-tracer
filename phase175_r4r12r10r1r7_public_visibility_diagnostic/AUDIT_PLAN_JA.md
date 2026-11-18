# Phase 175 R4R12R10R1R7 — 公開候補の階層監査

## 背景

R10R1R6 の DryRun は PASS したが、本実行で `R10R1_CITED_511_NOT_PUBLIC` が発生した。このエラーは共有候補が 0 件、または複数件である場合のいずれも意味する。ログだけでは判断できない。

## 対象ファイル・関数

- 新規 `phase175_r4r12r10r1r7_public_visibility_diagnostic/audit.py`: `git`, `count_named`, `source_link_state`, `investigate`, `main`
- 新規 `tests/test_audit.py`: `test_count_named_exact_name`, `test_diagnostic_never_declares_group_complete`, `test_report_gate_is_diagnostic_only`, `test_no_git_mutations_in_diagnostic`
- 新規 `run.ps1`, `README.md`, `AUDIT_PLAN_JA.md`, `CODE_FULL_JA.md`, `__init__.py`
- 既存ファイルの変更なし

## 調査項目

1. Toda (5.11) の直接 Source Bridge での GIVEN リンク
2. 統合した共有 Bridge に残る GIVEN リンク
3. `screened_cited_facts()` が認識した GIVEN
4. 単独の `build_cited_511_provider` の候補
5. 共有 `shared_expansion_provider` での Relation / GeneratorImage 候補
6. 既存 Installer の挿入箇所が現時点のソースに存在するか

## 制約・完了条件

文献とデータベースの証明境界は変更しない。新規 GIVEN=0、新規数学規則=0。本番ファイル編集=0。全体 pytest は実施しない。Gate `PASS_R7_PUBLIC_VISIBILITY_DIAGNOSED_NOT_COMPLETE` は候補数の記録にのみ対応する。
