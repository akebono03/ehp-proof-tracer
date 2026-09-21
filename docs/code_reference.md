# EHP Proof Tracer コード参照

この文書は**現行コードを探すための参照索引**である。

過去版には文字コード変換に起因する mojibake が広範囲に混在していたため、Phase 108 完了時点で UTF-8 の現行参照として全文を再構成した。

歴史的な実装経緯は `docs/development_log.md`、数学的・証明基盤の記録は `docs/proof_records.md` を参照する。

---

# 1. 基礎表現

## `expression.py`

Toda / EHP で使う式表現。

代表的な型:

```text
GeneratorSymbol
HomotopyElement
Composition
MapApplication
Suspension
IteratedSuspension
TodaBracket
WhiteheadProduct
Multiple
Sum
Zero
```

## `proof.py`

証明事実と provenance の中心。

重要な型:

```text
ProofStep
ProofRule
Relation
RelationType
```

`ProofStep` の重要な field:

```text
conclusion
premises
rule
note
inference_rule
```

## `proof_repository.py`

```text
ProofRepository
ProofRepositoryEntry
```

repository entry の `key / phase / theorem` は provenance metadata である。

## `rule_catalog.py`

inference rule catalog と applicability / producer 検索。

---

# 2. ホモトピー / Toda 基礎

## `homotopy_groups.py`

Toda primary group、可換群構造、EHP sequence / map 表現。

## `toda_rules.py`

Toda 固有の inference rule / theorem rule。

## `standard_production_repository.py`

標準運用 repository の構築。

入口:

```text
build_standard_production_proof_repository()
```

---

# 3. 有界証明探索

## `repository_inference.py`

repository 支援推論と有界 producer 探索の中心。

主要機能:

```text
goal に適合する final rule の選択
不足 premise の検出
producer 検索
有界 producer 依存探索
cycle 検出
max_depth
有限 retry
探索診断
実行診断
選択経路の実行
```

重要な result:

```text
RepositoryInferenceResult
BoundedProducerSearchResult
BoundedProducerSearchReport
BoundedProducerExecutionResult
```

実行成功時には:

```text
RepositoryInferenceResult.goal_step
```

が実際に導出された最終 `ProofStep` である。

---

# 4. Toda 群計算

## `toda_group_query.py`

```text
TodaGroupQuery(n, k)
```

対象:

```text
π_{n+k}^n
```

## `toda_group_lookup.py`

既知の定理に基づく群結果検索。

## `toda_group_result.py`

正規化済み Toda 群結果。

## `toda_calculation_facade.py`

運用用 convenience facade。

```text
build_standard_toda_report(n, k)
```

CLI:

```text
python main.py n k
```

---

# 5. 生成元入力

## `generator_input.py`

生成元文字列 → `GeneratorSymbol`。

代表的な入力:

```text
eta_2
nu_5
sigma_8
iota_4
nu_prime
ν′
nu'
sigma_prime
sigma_double_prime
sigma_triple_prime
```

index なし family は wildcard ではない。

---

# 6. 元中心の探索

## `repository_element_lookup.py`
## `repository_element_exploration.py`
## `repository_element_presentation.py`
## `repository_element_renderer.py`
## `repository_element_facade.py`

生成元の出現、意味論的 role、グループ化表示、Markdown、一括探索。

CLI:

```text
python main.py explore "nu'"
```

`repository_element_presentation.py` の

```text
render_repository_conclusion_latex()
```

は Phase 108 の利用者向け renderer でも数学 statement の LaTeX 表示に再利用する。

---

# 7. 再帰的 proof-scope 探索

## `repository_proof_scope.py`
## `repository_proof_scope_exploration.py`
## `repository_proof_scope_facade.py`

再帰的な `ProofStep` ancestry を走査する。

CLI:

```text
python main.py explore-proof nu_prime
```

代表的な探索結果:

```text
ν′ ∈ {η₃, 2ι₄, η₄}_1
H(ν′) = η₅
```

これは既存 proof 事実の発見であり、新しい定理 solving ではない。

---

# 8. 適用可能性探索

## `repository_proof_scope_applicability.py`

proof-scope の source step と inference-rule premise pattern の適合性を調べる。

## `repository_generator_applicability_facade.py`

標準 generator applicability の入口。

```text
explore_standard_repository_generator_applicability_input()
```

## `repository_generator_applicability_selection.py`

候補選択。

## `repository_generator_applicability_presentation.py`
## `repository_generator_applicability_renderer.py`

compact / detailed な適用可能性表示。

CLI:

```text
python main.py explore-applicable nu_prime
python main.py explore-applicable nu_prime --detailed
```

---

# 9. Phase 104 安全な候補引き渡し

主な module:

```text
repository_generator_applicability_handoff.py
repository_generator_applicability_execution_検証.py
repository_generator_applicability_execution_search.py
repository_generator_applicability_execution.py
```

概念的な経路:

```text
候補
→ 検証
→ READY
→ 明示的 final rule
→ 有界探索
→ 事前構築済み report の実行
→ 実際の ProofStep
```

重要な identity 不変条件:

```text
候補 rule
は execution entry rule と同一
は選択 final rule と同一
は 実行d goal_step.inference_rule と同一
```

---

# 10. Phase 105–107 qualified execution

## `repository_generator_applicability_execution_seed.py`

候補 source から exact seed を構成。

## `repository_generator_applicability_execution_entry.py`

qualified production execution family / entry を判定。

## `repository_generator_applicability_execution_orchestration.py`

第1 qualified family のオーケストレーション。

## `repository_generator_production_application_recovery.py`

複数前提 rule の既存 production application を正確に recovery。

照合条件:

```text
同一 root_entry identity
同一 inference_rule identity
同一の明示的 goal
候補 premise slot contains same source_step identity
```

状態:

```text
NONE
UNIQUE
AMBIGUOUS
```

## `repository_generator_production_application_execution_seed.py`

recovery された正確な premise tuple を execution seed に変換。

## `repository_generator_two_premise_execution_integration.py`

第2 qualified family の 2前提 execution 統合。

## `repository_generator_qualified_execution_selection.py`

qualified 候補選択。

## `repository_generator_qualified_execution_family.py`

qualified family の grouping。

grouping key は概念的に:

```text
scope_node identity
source_step identity
family 名
premise_index
bindings
```

## `repository_generator_qualified_execution_family_selection.py`

root / source / family 選択。

## `repository_generator_qualified_execution_dispatch.py`

family 名 dispatch。

premise 数では dispatch しない。

## `repository_generator_standard_qualified_execution_facade.py`

標準 execution facade。

Phase 105 互換経路:

```text
実行_standard_repository_generator_applicability_result_by_root_and_source()
```

Phase 107 multi-family:

```text
実行_standard_repository_generator_applicability_result_by_root_source_and_family()
```

admission 済み family:

```text
toda_58_delta_iota9_nu4_nu_prime_inference_rule
toda_lemma57_pi6_2_eta2_nu_prime_inference_rule
```

---

# 11. Phase 108 実行可能対象 resolver

## `repository_generator_user_execution_resolver.py`

主な型:

```text
RepositoryGeneratorExecutableTarget
StandardRepositoryGeneratorExecutableTargetResolution
```

入口:

```text
resolve_standard_repository_generator_executable_targets_input(
  generator_input,
)
```

役割:

```text
生成元入力
→ 適用可能性 result
→ qualified family 群
→ 元 target ProofStep の照合
→ 実行可能対象
```

target 照合には proof graph の identity を使う。

---

# 12. Phase 108 実行引き渡し

## `repository_generator_user_execution_handoff.py`

入口:

```text
実行_repository_generator_executable_target()
```

利用者向け target object を Phase 107 qualified execution facade へ渡す。

内部の root/source/family addressing は target object が保持し、CLI 利用者には直接入力させない。

---

# 13. Phase 108 最終 ProofStep 抽出

## `repository_generator_user_execution_proof_step.py`

主な型:

```text
RepositoryGeneratorExecutedProofStepResult
```

入口:

```text
extract_repository_generator_実行d_target_proof_step()
```

実際に使う最終 proof:

```text
execution_result
→ repository_inference_result
→ goal_step
```

元の repository target step を最終結果と誤認しない。

---

# 14. Phase 108 結果 + 証明表示

## `repository_generator_user_execution_presentation.py`

主な型:

```text
RepositoryGeneratorUserExecutionPresentation
```

builder:

```text
build_repository_generator_user_execution_presentation()
```

保持内容:

```text
実行済み ProofStep
conclusion
直接 premises
rule 名
```

## `repository_generator_user_execution_renderer.py`

入口:

```text
render_repository_generator_user_execution_markdown()
```

通常出力:

```text
# Result

...

## Proof

Premises:
...

Rule: ...

Conclusion:
...
```

---

# 15. Phase 108 workflow facade

## `repository_generator_user_execution_facade.py`

状態:

```text
RepositoryGeneratorUserExecutionWorkflowStatus.NONE
RepositoryGeneratorUserExecutionWorkflowStatus.AMBIGUOUS
RepositoryGeneratorUserExecutionWorkflowStatus.EXECUTED
```

result:

```text
RepositoryGeneratorUserExecutionWorkflowResult
```

入口:

```text
run_standard_repository_generator_user_execution_workflow(
  generator_input,
  候補_number=None,
  max_depth=2,
  retry_policy=None,
)
```

方針:

```text
対象 0 件
→ NONE

1 target + no 候補 number
→ 実行

multiple targets + no 候補 number
→ AMBIGUOUS

候補 number
→ 1-based の明示選択
```

---

# 16. Phase 108 候補-list presentation

## `repository_generator_user_execution_候補_presentation.py`

主な型:

```text
RepositoryGeneratorUserExecutionCandidatePresentation
RepositoryGeneratorUserExecutionCandidateListPresentation
```

builder:

```text
build_repository_generator_user_execution_候補_list_presentation()
```

## `repository_generator_user_execution_候補_renderer.py`

入口:

```text
render_repository_generator_user_execution_候補_list_markdown()
```

通常出力:

```text
# Executable 候補s

1. <target>
2. <target>

Select a 候補 number to 実行.
```

通常表示しない内部情報:

```text
family_name
root key
catalog
bindings
```

---

# 17. CLI

## `main.py`

現行コマンド:

```text
python main.py n k
python main.py explore <generator>
python main.py explore-proof <generator>
python main.py explore-applicable <generator>
python main.py explore-applicable <generator> --detailed
python main.py 実行 <generator>
python main.py 実行 <generator> --候補 N
```

実行 status mapping:

```text
NONE
→ stdout message / exit 1

AMBIGUOUS
→ 候補 list / exit 0

EXECUTED
→ Result + Proof / exit 0

不正入力
→ argparse error / exit 2
```

Windows script 実行では stdout / stderr を UTF-8 に設定する。

理由:

```text
CP932 では η₂、ν₄ などで使う一部の数学 Unicode 文字を encode できない。
```

---

# 18. Phase 108 テスト

主なテスト:

```text
tests/test_phase108_5_minimal_user_facing_executable_target_resolver.py
tests/test_phase108_6_executable_target_qualified_execution_handoff.py
tests/test_phase108_7_実行d_target_final_proof_step_extraction.py
tests/test_phase108_8_minimal_user_facing_result_proof_presentation.py
tests/test_phase108_9_minimal_user_facing_execution_workflow_facade.py
tests/test_phase108_10_user_facing_executable_候補_list.py
tests/test_phase108_11_cli_execution_command_integration.py
tests/test_phase108_12_end_to_end_cli_smoke_closure_audit.py
```

完了時:

```text
Phase 108-12 subprocess smoke:
3 passed in 21.55s

Phase 108 focused regression:
64 passed in 67.18s

repository 全体:
8850 passed in 380.25s
```

---

# 19. どこを見ればよいか

生成元 parser:

```text
generator_input.py
```

既存 generator 出現:

```text
repository_element_*.py
```

再帰的 proof ancestry:

```text
repository_proof_scope*.py
```

適用可能性:

```text
repository_generator_applicability_*.py
```

有界証明探索:

```text
repository_inference.py
```

qualified execution:

```text
repository_generator_qualified_execution_*.py
repository_generator_standard_qualified_execution_facade.py
```

利用者向け実行:

```text
repository_generator_user_execution_*.py
```

CLI:

```text
main.py
```

Toda 群計算:

```text
toda_group_*.py
toda_calculation_facade.py
```

---

# 20. 現在の重要な境界

```text
候補 != proof
候補 order != theorem ranking
qualified family != 実行成功保証
repository target step != 実行d goal_step identity
候補 number != theorem priority
表示 != 証明事実
CLI != 新しい定理事実
```

未実装:

```text
一般的な定理順位付け
最良証明の選択
一般的な無制限 backtracking
意味論的な自動 target 優先
一般 Toda bracket solver
一般合成 evaluator
一般 E / H / Δ evaluator
奇素数成分の完全統合
Web UI
```
