# EHP Proof Tracer 設計

この文書は EHP Proof Tracer の**現在有効なアーキテクチャ、意味論、不変条件、設計境界**を記録する。

過去の実装経緯は `docs/development_log.md`、証明記録は `docs/proof_records.md`、今後の計画は `docs/roadmap.md`、コード探索は `docs/code_reference.md` を参照する。

---

# 1. 基本設計原則

```text
実際の数学的・証明探索上の必要
↓
不足している最小表現
↓
必要な領域固有規則 / オーケストレーション
↓
既存の汎用基盤
```

次を混同しない。

```text
表現 != 型付け != 定理知識
構造的等値 != 数学的等値
探索計画 != 証明結果
表示層 != 証明事実
運用リポジトリの組み立て != 定理事実
証明範囲の走査 != 定理探索
既知関係の発見 != 写像評価
Toda bracket membership の発見 != bracket の解法
適用可能候補 != 証明成功
関連度カテゴリ != 定理順位
handoff 検証 != 定理事実
実行資格を満たす候補 != 一意な実行対象
実行ファミリーのグループ化 != 生カタログの重複除去
代表候補の選択 != 定理順位付け
generic qualification != family-specific execution strategy
family dispatch != theorem ranking
production application recovery != arbitrary companion-premise search
性能最適化 != 数学的意味論の変更
```

---

# 2. 現在の主要経路

計算:

```text
式 / statement
→ proof / inference
→ Toda 固有知識
→ ProofRepository / rule catalog
→ bounded search
→ TodaGroupQuery / lookup
→ group result
→ EHP / proof provenance
→ presentation
→ report
```

generator / applicability:

```text
generator 文字列
→ GeneratorSymbol
→ standard production repository
→ recursive ProofStep ancestry
→ occurrence
→ Toda membership / known map relation
→ premise-pattern compatibility
→ applicability candidates
→ relevance-classified presentation
```

multi-family qualified execution:

```text
RepositoryGeneratorApplicabilityExplorationResult
→ all-qualified selection
→ execution-family grouping
→ explicit root_entry + source_step + family_name selection
→ representative
→ family-name dispatch
├─ 1-premise family
│  → exact source seed
│  → bounded execution
└─ 2-premise family
   → exact production-application recovery
   → exact premise tuple seed
   → bounded execution
→ actual ProofStep provenance
```

---

# 3. 主要モジュール

基礎:

```text
expression.py
proof.py
proof_repository.py
rule_catalog.py
repository_inference.py
homotopy_groups.py
toda_rules.py
```

探索 / applicability:

```text
generator_input.py
repository_proof_scope.py
repository_proof_scope_exploration.py
repository_proof_scope_facade.py
repository_proof_scope_applicability.py
repository_generator_applicability_facade.py
repository_generator_applicability_selection.py
```

qualified execution:

```text
repository_generator_applicability_execution_seed.py
repository_generator_applicability_execution_entry.py
repository_generator_applicability_execution_orchestration.py
repository_generator_production_application_recovery.py
repository_generator_production_application_execution_seed.py
repository_generator_two_premise_execution_integration.py
repository_generator_qualified_execution_selection.py
repository_generator_qualified_execution_family.py
repository_generator_qualified_execution_family_selection.py
repository_generator_qualified_execution_dispatch.py
repository_generator_standard_qualified_execution_facade.py
```

---

# 4. 証明事実と metadata

証明事実の中心:

```text
ProofStep.conclusion
ProofStep.premises
ProofStep.inference_rule
```

`ProofRepositoryEntry.key / phase / theorem` は provenance metadata である。

renderer、facade、CLI、resolver、探索、applicability 分類、execution selection は証明事実を追加しない。

---

# 5. Repository 非破壊

query / exploration / applicability / execution planning は元の repository を読み取り専用として扱う。

execution は新しい inference result を構成できるが、元 repository を変更しない。

```text
entries before == entries after
```

必要な経路では `ProofStep` identity を保持する。

---

# 6. Applicability semantics

candidate は概念的に

```text
catalog_entry
premise_index
premise_pattern
source_step
bindings
```

を保持する。

```text
premise compatibility != 全 premise 成立
candidate != rule execution
candidate != proof success
candidate != theorem truth
```

relevance category は theorem ranking ではない。

---

# 7. Phase 104 handoff invariants

```text
candidate rule
is validation.execution_entry.rule
is search_result.final_rule
is goal_step.inference_rule
```

```text
execution_result.report
is search_report.report
```

READY 後に final rule を再選択しない。

---

# 8. Phase 105 first-family boundary

最初の qualified family:

```text
toda_58_delta_iota9_nu4_nu_prime_inference_rule
```

clone candidate は raw catalog から除去せず execution layer で family grouping する。

Phase 105 compatibility selection:

```text
root_entry identity
+
source_step identity
```

既存 first-family facade はそのまま維持する。

---

# 9. Phase 106 performance boundary

初期 `nu_prime` applicability:

```text
27.89 s / 274.10 MiB
```

full-scope candidates:

```text
797573
```

generator-relevant candidates:

```text
176616
```

generator-relevant scope prefilter 後:

```text
8.16 s / 62.42 MiB
```

candidate sequence / identity / provenance は保持された。

---

# 10. Phase 107 generic qualification

現在 admission 済み family:

```text
toda_58_delta_iota9_nu4_nu_prime_inference_rule
toda_lemma57_pi6_2_eta2_nu_prime_inference_rule
```

generic qualification は「execution 対象 family として admission 済み」を表す。

```text
generic qualification
!= concrete execution success
```

既存 `first_qualified_*` API は Phase 105 compatibility path として残す。

---

# 11. Exact production-application recovery

multi-premise candidate から companion premise を任意探索しない。

一致条件:

```text
same root_entry identity
same inference_rule identity
target conclusion == caller-explicit goal
target premises[candidate premise_index] is candidate.source_step
```

status:

```text
NONE
UNIQUE
AMBIGUOUS
```

`UNIQUE` のときだけ target の exact `premises` tuple を利用する。

first-match heuristic、cross-root companion search、goal 自動推定は禁止する。

---

# 12. Exact multi-premise seed

recovered premise tuple を

```text
同じ順序
同じ ProofStep identity
```

のまま temporary execution repository に登録する。

target step 自体は seed しない。

これにより、execution で導いた goal step は recovered premises を provenance として持つ。

---

# 13. Family grouping / selection

grouping key は概念的に

```text
scope_node identity
source_step identity
qualified family name
premise_index
bindings
```

multi-family selection contract:

```text
root_entry identity
+
source_step identity
+
family_name
```

proof object は identity (`is`) で照合し、family name は文字列値で照合する。

unknown family は拒否する。

automatic root/source/family ranking は行わない。

---

# 14. Family-name dispatch

dispatch key は premise 数ではなく semantic family identity とする。

```text
family 1
→ execute_first_qualified_production_applicability_candidate()

family 2
→ execute_second_qualified_production_applicability_candidate()
→ exact two-premise integration
```

premise count で推測しない。

generic qualification に family が増えても dispatch strategy がなければ明示的に失敗させる。

---

# 15. Standard multi-family facade

Phase 105 compatibility facade:

```text
execute_standard_repository_generator_applicability_result_by_root_and_source(
  applicability_result,
  root_entry,
  source_step,
  goal,
  max_depth=2,
  retry_policy=None,
)
```

Phase 107 multi-family facade:

```text
execute_standard_repository_generator_applicability_result_by_root_source_and_family(
  applicability_result,
  root_entry,
  source_step,
  family_name,
  goal,
  max_depth=2,
  retry_policy=None,
)
```

新 facade は

```text
select_all_qualified...
→ group...
→ root/source/family selection
→ dispatch
```

を接続する。

generator 文字列から proof graph を作り直さず、同じ applicability result graph の identity を使う。

---

# 16. Goal boundary

Phase 107 closure 時点でも `goal` は caller-explicit。

未実装:

```text
candidate から goal 自動推定
unknown RHS target search
複数 goal ranking
```

multi-family execution に不要だったため実装しない。

---

# 17. `nu_prime` exploration visibility

standard generator applicability は指定 generator occurrence を含む source node だけを candidate source とする。

family 2 の companion premise が `nu_prime` を含まない場合、その premise 側 candidate は `nu_prime` exploration に現れない。

companion premise は exact production-application recovery から得る。

---

# 18. CLI boundary

現行:

```text
python main.py n k
python main.py explore "nu'"
python main.py explore-proof nu_prime
python main.py explore-applicable nu_prime
python main.py explore-applicable nu_prime --detailed
```

Phase 107 は execution CLI を追加しない。

CLI 化には proof object identity の addressing / serialization 設計が必要であり、別問題である。

---

# 19. Deferred capabilities

```text
automatic root/source/family selection
automatic goal discovery
shortest-depth / theorem ranking
producer ranking
proof-cost optimization
general backtracking
persistent cache / parallelization
repository snapshot / versioning
execution addressing / serialization
execution CLI
execution-result presentation
third family without new pressure
general Toda-bracket solver
general composition / E / H / Δ evaluator
odd-primary full integration
all-primary ordinary sphere-homotopy calculation
```

---

# 20. Closure baselines

```text
Phase 103:
409 passed in 186.07s

Phase 104:
8644 passed in 374.63s

Phase 105:
8709 passed in 659.02s

Phase 106:
8712 passed in 337.86s

Phase 107:
8783 passed in 290.63s
```

Phase 107 focused confirmations:

```text
Phase 107-18:
10 passed in 13.69s

Phase 107-16 dispatch:
10 passed in 1.71s
```

Phase 107 は完了。

---

# 21. 次 Phase との境界

Phase 107 で保留した機能を機械的に実装しない。

次 Phase は、新しい数学的対象、additional qualified family、user-facing addressing、goal discovery、presentation のいずれに実需要があるかを pressure audit してから開始する。
