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

multi-family qualified execution:

```text
standard applicability result
→ all-qualified selection
→ execution-family grouping
→ explicit root + source + family selection
→ family-name dispatch
→ exact one- or multi-premise seed
→ bounded execution
→ actual ProofStep
```

最新:

```text
Phase 107 closure:
8783 passed in 290.63s
```

Phase 107 は完了。

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

admission 済み family:

```text
toda_58_delta_iota9_nu4_nu_prime_inference_rule
toda_lemma57_pi6_2_eta2_nu_prime_inference_rule
```

---

# 4. 確定した境界

selection:

```text
root_entry identity
+
source_step identity
+
family_name
```

goal:

```text
caller explicit
```

multi-premise context:

```text
arbitrary search しない
→ same-root exact production application recovery
→ UNIQUE exact premise tuple
```

ranking:

```text
candidate order / root order / shortest depth
!= theorem ranking
```

---

# 5. 保留：automatic execution targeting

```text
automatic root selection
automatic source selection
automatic family selection
automatic goal discovery
shortest-depth ranking
theorem ranking
```

Phase 107 では explicit contract で execution が成立したため保留する。

---

# 6. 保留：execution addressing / CLI

現行 contract は proof graph object identity を直接扱う。

CLI 化には

```text
stable root identifier
source ProofStep addressing
family identifier
goal serialization / parsing
identity recovery
```

が必要である。

単純な CLI command 追加ではないため保留する。

---

# 7. 保留：execution presentation

将来候補:

```text
selected family
recovery status
recovered premises
bounded-search result
executed ProofStep provenance
```

Phase 107 closure には不要だった。

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

Phase 106 の prefilter 以外に、現時点で新しい実性能圧力は確認されていない。

---

# 11. 次 Phase の開始境界

Phase 107 の保留事項を機械的に実装しない。

次 Phase は、次のどこに新しい実需要があるかを監査して開始する。

```text
additional qualified family
user-facing execution addressing
goal discovery
execution presentation
新しい数学的 theorem / stem coverage
```

最初の作業は実装ではなく pressure audit とする。
