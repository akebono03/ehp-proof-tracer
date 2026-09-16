# EHP Proof Tracer ロードマップ

この文書は今後の capability dependency と Phase 順序を記録する。過去の詳細な実装履歴は `docs/development_log.md`、現在の設計は `docs/design.md`、代表記録は `docs/proof_records.md` を参照する。

---

# 1. 現在地

数学面:

```text
Toda Lemma 5.16 までの concrete proof spine
stable G_0 through G_7
```

proof infrastructure:

```text
Proof Repository
→ automatic final-rule selection
→ missing-premise producer analysis
→ multiple producer generation
→ bounded dependency DAG selection
→ max_depth parameterization
→ search / execution diagnostics
→ finite explicit producer retry
→ concrete theorem-instance compatibility filtering
→ selected concrete requested-premise provenance
→ concrete execution-output validation
→ goal ProofStep
```

formal bounded-depth regression:

```text
max_depth = 2
max_depth = 3
max_depth = 4
```

defaults:

```text
max_depth = 2
retry_policy = None
```

latest confirmed repository-wide regression:

```text
7096 passed in 35.90s
```

---

# 2. Phase 86 完了境界

Phase 86 で bounded producer search の explicit depth parameterization を完成した。

```text
max_depth=2
max_depth=3
max_depth=4
```

維持:

```text
finite explicit depth bound
cycle-safe search
shared dependency identity reuse
dependency-first execution
diagnostic context
ProofStep provenance
repository non-mutation
default max_depth=2 compatibility
```

---

# 3. Phase 87 完了境界

Phase 87 で producer ambiguity に対する finite retry を追加した。

```text
FiniteProducerRetryPolicy(max_attempts=N)
```

default:

```text
retry_policy=None
→ multiple safe producers
→ AMBIGUOUS_PRODUCER
```

explicit retry:

```text
candidate failure
→ temporary selection rollback
→ next candidate
```

budget exhaustion:

```text
PRODUCER_RETRY_EXHAUSTED
```

Phase 87 は general backtracking を導入しない。

---

# 4. Phase 88 完了境界

Phase 88 の目的は、same conclusion type collision を concrete theorem-instance ambiguity と区別することだった。

代表 collision:

```text
TodaDeltaImageUpToSignStatement

Δ(ι₅)
Δ(ι₉)
Δ(ι₁₇)
```

完成 flow:

```text
known sibling premises
→ bindings
→ concrete requested_statement
→ producer conclusion type
→ goal_compatibility
→ concrete-compatible producer candidates
→ bounded search
→ selected node preserves requested_statement
→ execution validates exact concrete output
```

結果:

```text
false ambiguity
→ Phase 88 filtering で除去

same concrete target に複数 producer
→ true ambiguity
→ Phase 87 finite retry の対象
```

safe lookup と unsafe diagnostic は同じ concrete compatibility semantics を使う。

Phase 88 end-to-end regression:

```text
real Δι5 / Δι9 / Δι17 collision
→ concrete Δι17 request
→ Δι17 only
→ unique selection
→ report SUCCESS
→ execution SUCCESS
→ correct ProofStep provenance
→ repository non-mutation
```

Phase 88 は COMPLETE。

---

# 5. 次候補：Phase 89

Phase 89 は新しい search algorithm を直ちに実装しない。

最初の自然な段階:

```text
Phase 89-1
post-Phase88 proof-search pressure / true-ambiguity necessity audit
```

確認する中心:

```text
actual theorem-backed search で
same concrete requested statement に
複数 viable producer が残る実例があるか

Phase 87 finite retry で十分か

candidate 1 が deeper branch で失敗し、
candidate 2 へ戻る general backtracking が
実際に必要な theorem-backed case があるか

producer ranking / proof cost に
具体的な need があるか

現在の deterministic registration order が
どこまで十分か

search cache / persistence が
現在の performance bottleneck か
```

この監査で具体的 need が確認された場合のみ次の最小実装を決める。

---

# 6. Phase 89 で先取りしないもの

監査前に次を実装しない:

```text
general backtracking
producer ranking
proof-cost model
best-proof selection
DFS
BFS
A*
unbounded recursion
generic theorem prover
```

アルゴリズム名から設計を始めず、実際の proof-search failure から必要 capability を決める。

---

# 7. 継続保留：数学 / representation

```text
general existential quantification
general witness / uniqueness framework
generic sign algebra
generic Toda-bracket coset algebra
generic symbolic dimension solver
generic map typing solver
generic stable theorem engine
stable ring machinery
generic mathematical-equivalence normalizer
```

---

# 8. 継続保留：storage / presentation

```text
persistent Proof Repository
proof graph serialization
schema migration
persistent search cache
proof replay persistence
automatic proof narrative generation
```

現在の `ProofRepository` は in-memory。

現在の proof-style probe は hand-authored presentation layer。

---

# 9. 性能方針

wall-clock time は複数 PC 間で直接比較しない。

主要 signal:

```text
test count
semantic coverage
provenance coverage
focused regression
repository-wide regression
```

重い deterministic fixture builder が同一 object graph を繰り返し利用する場合:

```python
@lru_cache(maxsize=1)
```

を優先する。

最適化は:

```text
pytest --durations
→ profiler
→ concrete bottleneck
→ minimum change
→ same-machine comparison
→ full regression
```

の順で行う。
