# EHP Proof Tracer コード参照

この文書は**現行コードを探すための参照索引**である。

過去版には文字コード変換に起因する mojibake が広範囲に混在していたため、Phase 108 完了時点で UTF-8 の現行参照として全文を再構成した。

歴史的な実装経緯は `docs/development_log.md`、数学的・証明基盤の記録は `docs/proof_records.md` を参照する。

---

# 1. 基礎表現

## `expression.py`

Toda / EHP で使う式表現。

代表型:

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

重要型:

```text
ProofStep
ProofRule
Relation
RelationType
```

`ProofStep` の重要 field:

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

repository entry の `key / phase / theorem` は provenance metadata。

## `rule_catalog.py`

inference rule catalog と applicability / producer lookup。

---

# 2. Homotopy / Toda 基礎

## `homotopy_groups.py`

Toda primary group、可換群構造、EHP sequence / map representation。

## `toda_rules.py`

Toda 固有の inference rule / theorem rule。

## `standard_production_repository.py`

standard production repository の構築。

入口:

```text
build_standard_production_proof_repository()
```

---

# 3. Bounded proof search

## `repository_inference.py`

repository-assisted inference と bounded producer search の中心。

主要 capability:

```text
goal-compatible final-rule selection
missing-premise detection
producer lookup
bounded producer dependency search
cycle detection
max_depth
finite retry
search diagnostics
execution diagnostics
selected-path execution
```

重要 result:

```text
RepositoryInferenceResult
BoundedProducerSearchResult
BoundedProducerSearchReport
BoundedProducerExecutionResult
```

successful execution では:

```text
RepositoryInferenceResult.goal_step
```

が実際に導出された final `ProofStep`。

---

# 4. Toda group calculation

## `toda_group_query.py`

```text
TodaGroupQuery(n, k)
```

target:

```text
π_{n+k}^n
```

## `toda_group_lookup.py`

known theorem-backed group result lookup。

## `toda_group_result.py`

normalized Toda group result。

## `toda_calculation_facade.py`

production convenience facade。

```text
build_standard_toda_report(n, k)
```

CLI:

```text
python main.py n k
```

---

# 5. Generator input

## `generator_input.py`

generator string → `GeneratorSymbol`。

代表入力:

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

unindexed family は wildcard ではない。

---

# 6. Element-centered exploration

## `repository_element_lookup.py`
## `repository_element_exploration.py`
## `repository_element_presentation.py`
## `repository_element_renderer.py`
## `repository_element_facade.py`

generator occurrence、semantic role、grouped presentation、Markdown、one-shot exploration。

CLI:

```text
python main.py explore "nu'"
```

`repository_element_presentation.py` の

```text
render_repository_conclusion_latex()
```

は Phase 108 user-facing renderer でも数学 statement の LaTeX 表示に再利用する。

---

# 7. Recursive proof-scope exploration

## `repository_proof_scope.py`
## `repository_proof_scope_exploration.py`
## `repository_proof_scope_facade.py`

recursive `ProofStep` ancestry を走査する。

CLI:

```text
python main.py explore-proof nu_prime
```

代表 discovery:

```text
ν′ ∈ {η₃, 2ι₄, η₄}_1
H(ν′) = η₅
```

これは既存 proof fact の発見であり、新しい theorem solving ではない。

---

# 8. Applicability discovery

## `repository_proof_scope_applicability.py`

proof-scope source step と inference-rule premise pattern の compatibility を調べる。

## `repository_generator_applicability_facade.py`

standard generator applicability entry point。

```text
explore_standard_repository_generator_applicability_input()
```

## `repository_generator_applicability_selection.py`

candidate selection。

## `repository_generator_applicability_presentation.py`
## `repository_generator_applicability_renderer.py`

compact / detailed applicability presentation。

CLI:

```text
python main.py explore-applicable nu_prime
python main.py explore-applicable nu_prime --detailed
```

---

# 9. Phase 104 safe candidate handoff

主な module:

```text
repository_generator_applicability_handoff.py
repository_generator_applicability_execution_validation.py
repository_generator_applicability_execution_search.py
repository_generator_applicability_execution.py
```

概念経路:

```text
candidate
→ validation
→ READY
→ explicit final rule
→ bounded search
→ prebuilt report execution
→ actual ProofStep
```

重要 identity invariant:

```text
candidate rule
is execution entry rule
is selected final rule
is executed goal_step.inference_rule
```

---

# 10. Phase 105–107 qualified execution

## `repository_generator_applicability_execution_seed.py`

candidate source から exact seed を構成。

## `repository_generator_applicability_execution_entry.py`

qualified production execution family / entry 判定。

## `repository_generator_applicability_execution_orchestration.py`

first qualified family の orchestration。

## `repository_generator_production_application_recovery.py`

multi-premise rule の exact existing production application recovery。

照合:

```text
same root_entry identity
same inference_rule identity
same explicit goal
candidate premise slot contains same source_step identity
```

status:

```text
NONE
UNIQUE
AMBIGUOUS
```

## `repository_generator_production_application_execution_seed.py`

recovered exact premise tuple を execution seed に変換。

## `repository_generator_two_premise_execution_integration.py`

second qualified family の 2-premise execution integration。

## `repository_generator_qualified_execution_selection.py`

qualified candidate selection。

## `repository_generator_qualified_execution_family.py`

qualified family grouping。

grouping key は概念的に:

```text
scope_node identity
source_step identity
family name
premise_index
bindings
```

## `repository_generator_qualified_execution_family_selection.py`

root / source / family selection。

## `repository_generator_qualified_execution_dispatch.py`

family-name dispatch。

premise 数では dispatch しない。

## `repository_generator_standard_qualified_execution_facade.py`

standard execution facade。

Phase 105 compatibility:

```text
execute_standard_repository_generator_applicability_result_by_root_and_source()
```

Phase 107 multi-family:

```text
execute_standard_repository_generator_applicability_result_by_root_source_and_family()
```

admission 済み family:

```text
toda_58_delta_iota9_nu4_nu_prime_inference_rule
toda_lemma57_pi6_2_eta2_nu_prime_inference_rule
```

---

# 11. Phase 108 executable-target resolver

## `repository_generator_user_execution_resolver.py`

主な型:

```text
RepositoryGeneratorExecutableTarget
StandardRepositoryGeneratorExecutableTargetResolution
```

entry point:

```text
resolve_standard_repository_generator_executable_targets_input(
  generator_input,
)
```

役割:

```text
generator input
→ applicability result
→ qualified family groups
→ original target ProofStep matching
→ executable targets
```

target matching は proof-graph identity を使う。

---

# 12. Phase 108 execution handoff

## `repository_generator_user_execution_handoff.py`

entry point:

```text
execute_repository_generator_executable_target()
```

user-facing target object を Phase 107 qualified execution facade へ渡す。

内部の root/source/family addressing は target object が保持し、CLI user に直接入力させない。

---

# 13. Phase 108 final ProofStep extraction

## `repository_generator_user_execution_proof_step.py`

主な型:

```text
RepositoryGeneratorExecutedProofStepResult
```

entry point:

```text
extract_repository_generator_executed_target_proof_step()
```

実際に使う final proof:

```text
execution_result
→ repository_inference_result
→ goal_step
```

original repository target step を final result と誤認しない。

---

# 14. Phase 108 Result + Proof presentation

## `repository_generator_user_execution_presentation.py`

主な型:

```text
RepositoryGeneratorUserExecutionPresentation
```

builder:

```text
build_repository_generator_user_execution_presentation()
```

保持:

```text
executed ProofStep
conclusion
direct premises
rule name
```

## `repository_generator_user_execution_renderer.py`

entry point:

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

status:

```text
RepositoryGeneratorUserExecutionWorkflowStatus.NONE
RepositoryGeneratorUserExecutionWorkflowStatus.AMBIGUOUS
RepositoryGeneratorUserExecutionWorkflowStatus.EXECUTED
```

result:

```text
RepositoryGeneratorUserExecutionWorkflowResult
```

entry point:

```text
run_standard_repository_generator_user_execution_workflow(
  generator_input,
  candidate_number=None,
  max_depth=2,
  retry_policy=None,
)
```

policy:

```text
0 target
→ NONE

1 target + no candidate number
→ execute

multiple targets + no candidate number
→ AMBIGUOUS

candidate number
→ one-based explicit selection
```

---

# 16. Phase 108 candidate-list presentation

## `repository_generator_user_execution_candidate_presentation.py`

主な型:

```text
RepositoryGeneratorUserExecutionCandidatePresentation
RepositoryGeneratorUserExecutionCandidateListPresentation
```

builder:

```text
build_repository_generator_user_execution_candidate_list_presentation()
```

## `repository_generator_user_execution_candidate_renderer.py`

entry point:

```text
render_repository_generator_user_execution_candidate_list_markdown()
```

通常出力:

```text
# Executable candidates

1. <target>
2. <target>

Select a candidate number to execute.
```

表示しない内部情報:

```text
family_name
root key
catalog
bindings
```

---

# 17. CLI

## `main.py`

現行 command:

```text
python main.py n k
python main.py explore <generator>
python main.py explore-proof <generator>
python main.py explore-applicable <generator>
python main.py explore-applicable <generator> --detailed
python main.py execute <generator>
python main.py execute <generator> --candidate N
```

execute status mapping:

```text
NONE
→ stdout message / exit 1

AMBIGUOUS
→ candidate list / exit 0

EXECUTED
→ Result + Proof / exit 0

invalid input
→ argparse error / exit 2
```

Windows script executionでは stdout / stderr を UTF-8 に設定する。

理由:

```text
CP932 cannot encode some mathematical Unicode,
including subscript characters used in η₂, ν₄, etc.
```

---

# 18. Phase 108 tests

主な test:

```text
tests/test_phase108_5_minimal_user_facing_executable_target_resolver.py
tests/test_phase108_6_executable_target_qualified_execution_handoff.py
tests/test_phase108_7_executed_target_final_proof_step_extraction.py
tests/test_phase108_8_minimal_user_facing_result_proof_presentation.py
tests/test_phase108_9_minimal_user_facing_execution_workflow_facade.py
tests/test_phase108_10_user_facing_executable_candidate_list.py
tests/test_phase108_11_cli_execution_command_integration.py
tests/test_phase108_12_end_to_end_cli_smoke_closure_audit.py
```

closure:

```text
Phase 108-12 subprocess smoke:
3 passed in 21.55s

Phase 108 focused regression:
64 passed in 67.18s

full repository:
8850 passed in 380.25s
```

---

# 19. どこを見ればよいか

generator parser:

```text
generator_input.py
```

既存 generator occurrence:

```text
repository_element_*.py
```

recursive proof ancestry:

```text
repository_proof_scope*.py
```

applicability:

```text
repository_generator_applicability_*.py
```

bounded proof search:

```text
repository_inference.py
```

qualified execution:

```text
repository_generator_qualified_execution_*.py
repository_generator_standard_qualified_execution_facade.py
```

user-facing execution:

```text
repository_generator_user_execution_*.py
```

CLI:

```text
main.py
```

Toda group calculation:

```text
toda_group_*.py
toda_calculation_facade.py
```

---

# 20. 現在の重要 boundary

```text
candidate != proof
candidate order != theorem ranking
qualified family != guaranteed execution success
repository target step != executed goal_step identity
candidate number != theorem priority
presentation != proof truth
CLI != new theorem truth
```

未実装:

```text
general theorem ranking
best-proof selection
general unbounded backtracking
automatic semantic target preference
general Toda-bracket solver
general composition evaluator
general E / H / Δ evaluator
odd-primary full integration
Web UI
```
