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
user-facing target resolver != theorem ranking
candidate number != mathematical priority
presentation != proof object
repository target goal equality != executed conclusion object identity
CLI addressing != proof-graph internal addressing
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

qualified execution:

```text
RepositoryGeneratorApplicabilityExplorationResult
→ all-qualified selection
→ execution-family grouping
→ root_entry + source_step + family_name selection
→ family-name dispatch
├─ 1-premise family
│  → exact source seed
│  → bounded execution
└─ 2-premise family
   → exact production-application recovery
   → exact premise tuple seed
   → bounded execution
→ actual executed ProofStep
```

user-facing execution:

```text
generator input
→ executable-target resolver
→ 0 / 1 / multiple target classification
→ 1-based candidate selection
→ qualified execution handoff
→ final executed ProofStep extraction
→ Result + Proof presentation
→ Markdown
→ execute CLI
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
repository_generator_applicability_presentation.py
repository_generator_applicability_renderer.py
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

Phase 108 user-facing execution:

```text
repository_generator_user_execution_resolver.py
repository_generator_user_execution_handoff.py
repository_generator_user_execution_proof_step.py
repository_generator_user_execution_presentation.py
repository_generator_user_execution_renderer.py
repository_generator_user_execution_facade.py
repository_generator_user_execution_candidate_presentation.py
repository_generator_user_execution_candidate_renderer.py
main.py
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

必要な経路では既存 `ProofStep` identity を保持する。

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

# 8. Phase 105–107 qualified-execution boundary

admission 済み family:

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

multi-premise candidate から companion premise を任意探索しない。

一致条件:

```text
same root_entry identity
same inference_rule identity
target conclusion == explicit goal
target premises[candidate premise_index] is candidate.source_step
```

`UNIQUE` のときだけ exact `premises` tuple を利用する。

recovered premise tuple は同じ順序・同じ `ProofStep` identity のまま execution seed に使う。

---

# 9. Phase 106 performance boundary

初期 `nu_prime` applicability:

```text
27.89 s / 274.10 MiB
```

generator-relevant scope prefilter 後:

```text
8.16 s / 62.42 MiB
```

candidate sequence / identity / provenance は保持された。

---

# 10. User-facing executable-target resolver

Phase 108 の resolver は generator input から **実行可能な target** を列挙する。

概念的な照合:

```text
root_entry identity
+
inference_rule identity
+
candidate premise_index
+
candidate source_step identity
→ original target ProofStep
```

一致 target が一意に定まる場合だけ user-facing executable target として採用する。

resolver は theorem ranking を行わない。

---

# 11. Ambiguity semantics

workflow status:

```text
NONE
AMBIGUOUS
EXECUTED
```

規則:

```text
0 executable targets
→ NONE

1 executable target + candidate_number omitted
→ automatic execution

multiple executable targets + candidate_number omitted
→ AMBIGUOUS

candidate_number supplied
→ select that one-based target
```

複数候補で「先頭を自動採用」はしない。

`candidate_number` は表示順に対応する 1-based addressing であり、数学的優先度を意味しない。

---

# 12. Executed final ProofStep boundary

Phase 108 は repository 側の original target step を presentation しない。

実際に bounded execution が生成した

```text
repository_inference_result.goal_step
```

を final executed `ProofStep` として取り出す。

重要:

```text
executed goal_step
is not necessarily original repository target_step
```

ただし

```text
executed goal_step.conclusion == selected target goal
```

である。

presentation は

```text
presentation.conclusion
is executed proof_step.conclusion
```

を保持する。

repository target goal とは object identity ではなく equality で対応する。

---

# 13. Minimal Result + Proof presentation

通常表示の対象:

```text
final conclusion
direct premises
rule
conclusion
```

表示しない内部情報:

```text
root key
catalog key
bindings
internal family addressing
```

default proof depth は direct premises の 1 段。

再帰的 proof tree の完全表示は Phase 108 では行わない。

---

# 14. Executable candidate-list presentation

`AMBIGUOUS` のとき:

```text
# Executable candidates

1. <mathematical target>
2. <mathematical target>
...

Select a candidate number to execute.
```

resolver の target 順をそのまま保持する。

同じ数学的 conclusion が複数 target に現れる可能性があっても、Phase 108 は勝手に deduplicate / rank しない。

---

# 15. User execution workflow facade

entry point:

```text
run_standard_repository_generator_user_execution_workflow(
  generator_input,
  candidate_number=None,
  max_depth=2,
  retry_policy=None,
)
```

identity chain:

```text
resolution
→ selected target
→ execution_result
→ proof_result
→ presentation
→ markdown
```

各 layer は同一 workflow 内で前段 object identity を保持する。

---

# 16. CLI boundary

現行:

```text
python main.py n k
python main.py explore "nu'"
python main.py explore-proof nu_prime
python main.py explore-applicable nu_prime
python main.py explore-applicable nu_prime --detailed
python main.py execute nu_prime
python main.py execute nu_prime --candidate 1
```

`execute`:

```text
NONE
→ message + exit 1

AMBIGUOUS
→ candidate list + exit 0

EXECUTED
→ Result + Proof + exit 0

invalid generator / candidate
→ argparse error + exit 2
```

---

# 17. Windows UTF-8 CLI boundary

Windows の既定 CP932 では `η₂`、`ν₄` などの Unicode 数学文字を stdout に出力できない場合がある。

実プロセス CLI のみ

```text
sys.stdout.reconfigure(encoding="utf-8")
sys.stderr.reconfigure(encoding="utf-8")
```

相当の設定を行う。

`main(...)` を直接呼ぶ既存 in-process pytest の capture stream は変更しない。

---

# 18. Phase 108 closure tests

end-to-end subprocess smoke:

```text
python main.py execute nu_prime
python main.py execute nu_prime --candidate 1
python main.py execute nu_prime --candidate 2
```

確認:

```text
3 passed in 21.55s
```

Phase 108 focused regression:

```text
64 passed in 67.18s
```

repository-wide:

```text
8850 passed in 380.25s
```

---

# 19. Deferred capabilities

```text
semantic auto-selection among multiple executable targets
theorem ranking
proof-cost optimization
producer ranking
general unbounded backtracking
persistent cache / parallelization
repository snapshot / versioning
stale-search-report detection
third qualified family without new production pressure
general Toda-bracket solver
general composition / E / H / Δ evaluator
coset / indeterminacy computation
broader unstable stems
odd-primary full integration
all-primary ordinary sphere-homotopy calculation
Web UI
```

---

# 20. 次 Phase との境界

Phase 108 の user-facing execution path は完了。

次 Phase は automatic selection や additional family を自動的に実装しない。

まず operational audit により

```text
どの generator が executable target を持つか
どの family が実運用可能か
NONE / AMBIGUOUS / EXECUTED の分布
追加 family の実需要
表示や性能の新しい圧力
```

を確認する。
