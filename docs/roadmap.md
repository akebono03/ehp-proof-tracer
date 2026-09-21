# EHP Proof Tracer ロードマップ

この文書は**今後の capability dependency と Phase 順序**を記録する。

過去の実装履歴は `docs/development_log.md`、現在の設計は `docs/design.md`、代表的な証明記録は `docs/proof_records.md` を参照する。

---

# 1. 現在地

運用計算:

```text
raw n,k
→ python main.py n k
→ standard production repository
→ proof report
```

generator exploration:

```text
generator
→ recursive proof scope
→ Toda membership / known map relation
→ applicability candidates
→ relevance-classified presentation
```

user-facing qualified execution:

```text
generator input
→ executable-target resolution
→ NONE / AMBIGUOUS / executable target
→ candidate list / one-based candidate selection
→ qualified execution
→ final executed ProofStep
→ Result + Proof
→ python main.py execute ...
```

最新:

```text
Phase 108 closure:
8850 passed in 380.25s
```

Phase 108 は完了。

---

# 2. 完了済み capability

Phase 90–104:

```text
query / normalization
EHP / proof provenance
calculation orchestration / report
generator exploration
recursive proof scope
applicability discovery
relevance classification
safe candidate handoff
bounded execution provenance
```

Phase 105:

```text
first qualified family
exact source seed
family grouping
explicit root + source selection
standard first-family facade
```

Phase 106:

```text
applicability performance audit
generator-relevant scope prefilter
```

Phase 107:

```text
multi-premise recovery
exact premise-tuple seed
second qualified family
explicit root + source + family selection
family dispatch
multi-family standard facade
```

Phase 108:

```text
user-facing executable-target resolver
ambiguity-safe workflow
one-based candidate addressing
final executed ProofStep extraction
minimal Result + Proof presentation
candidate-list presentation
execute CLI
Windows UTF-8 CLI boundary
end-to-end subprocess smoke
```

---

# 3. 現在の execution API

Phase 105 compatibility:

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

Phase 107 multi-family:

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

Phase 108 user workflow:

```text
run_standard_repository_generator_user_execution_workflow(
  generator_input,
  candidate_number=None,
  max_depth=2,
  retry_policy=None,
)
```

admission 済み family:

```text
toda_58_delta_iota9_nu4_nu_prime_inference_rule
toda_lemma57_pi6_2_eta2_nu_prime_inference_rule
```

---

# 4. 現在の CLI

```text
python main.py n k
python main.py explore "nu'"
python main.py explore-proof nu_prime
python main.py explore-applicable nu_prime
python main.py explore-applicable nu_prime --detailed
python main.py execute nu_prime
python main.py execute nu_prime --candidate 1
```

`execute` は proof-graph の root/source/family internal identifier を user input に要求しない。

---

# 5. 確定した user-facing execution 境界

ambiguity:

```text
multiple executable targets
→ 自動選択しない
→ numbered candidate list
```

candidate number:

```text
1-based addressing
!= theorem ranking
```

executed result:

```text
actual repository_inference_result.goal_step
→ final ProofStep
```

presentation:

```text
final conclusion
direct premises
rule
conclusion
```

internal addressing は通常表示に出さない。

---

# 6. Phase 109 候補：post-Phase-108 operational audit

次 Phase の第一候補は implementation ではなく operational audit。

確認対象:

```text
どの generator input が executable target を持つか
NONE / UNIQUE / AMBIGUOUS の分布
現在の2 family がどの production target をカバーするか
実際に candidate list が有用な対象
追加 family の具体的需要
execution 時間 / applicability 時間の新しい性能圧力
presentation 上の不足
```

この audit で追加実装の圧力を確認してから Phase 109 の scope を固定する。

---

# 7. 保留：semantic automatic target selection

Phase 108 は user-facing addressing を実現したが、複数候補から数学的に「最善」を選ぶ機能は実装していない。

保留:

```text
theorem ranking
shortest-proof ranking
proof-cost optimization
semantic goal priority
automatic target preference
```

候補順を ranking と解釈しない。

---

# 8. 保留：additional qualified families

third family 以降は coverage 拡張だけを目的に admission しない。

次を確認する。

```text
actual production source
execution safety
goal compatibility
required seed context
rule identity preservation
producer-search behavior
user-facing need
new architectural pressure
```

---

# 9. 保留：数学的 evaluator / broader coverage

```text
general Toda-bracket solver
general composition evaluation
general E / H / Δ evaluation
indeterminacy / coset normalization
broader unstable stems
odd-primary integration
all-primary ordinary sphere-homotopy calculation
```

---

# 10. 保留：optimization / versioning

```text
general backtracking
producer ranking
proof-cost optimization
best-proof selection
persistent cache
parallelization
repository snapshot / versioning
stale-search-report detection
```

Phase 106 の prefilter 以降、次の optimization は実測圧力を確認してから行う。

---

# 11. 保留：UI 拡張

CLI は Phase 108 で実装済み。

未実装:

```text
Web UI
interactive candidate selection
persistent execution history
rich recursive proof visualization
```

必要性を operational audit で確認する。

---

# 12. 次 Phase の開始境界

Phase 108 の完了事項を機械的に拡張しない。

次はまず:

```text
Phase 109
post-Phase-108 operational audit
/ next execution scope diagnosis
```

その結果から、additional family、presentation、性能、数学 coverage のどこに実需要があるかを決める。
