# EHP Proof Tracer ロードマップ

この文書は今後の capability dependency と Phase 順序を記録する。過去の詳細な実装履歴は `docs/development_log.md`、現在の設計は `docs/design.md`、代表記録は `docs/proof_records.md` を参照する。

---

# 1. 現在地

数学面では Toda Lemma 5.16 までの concrete proof spine と stable stem 0〜7 を formalize 済み。

proof infrastructure は Phase 87 で次の境界まで到達した。

```text
Proof Repository
-> automatic final-rule selection
-> missing-premise producer search
-> bounded dependency DAG selection
-> finite explicit producer retry
-> search diagnostics
-> retry-exhaustion diagnostics
-> unified report
-> exact selected-path execution
-> goal ProofStep
```

formal regression 済み bounded depth:

```text
max_depth = 2
max_depth = 3
max_depth = 4
```

default:

```text
max_depth = 2
retry_policy = None
```

retry policy:

```text
FiniteProducerRetryPolicy(max_attempts=N)
```

---

# 2. Phase 86 完了境界

Phase 86 では bounded producer search の depth parameterization を完成した。

代表:

```text
max_depth=2
max_depth=3
max_depth=4
```

維持 invariant:

```text
finite explicit depth bound
cycle-safe
shared dependency identity preservation
deterministic dependency-first order
diagnostic context preservation
exact selected-path execution
ProofStep provenance preservation
repository non-mutation
default max_depth=2 compatibility
```

---

# 3. Phase 87 完了境界

Phase 87 では producer ambiguity に対し general backtracking を導入せず、明示的な有限 retry policy のみを追加した。

代表:

```text
retry_policy=None
-> AMBIGUOUS_PRODUCER

max_attempts=1
-> first candidate selection failure
-> PRODUCER_RETRY_EXHAUSTED

max_attempts=2
-> first candidate selection failure
-> rollback
-> second candidate selection success
-> SUCCESS
-> selected-path execution
-> goal ProofStep
```

維持 invariant:

```text
finite explicit retry bound
catalog-order deterministic attempts
safe-producer filtering
failed-attempt state rollback
selected path only execution
ProofStep provenance
repository non-mutation
default ambiguity compatibility
```

Phase 87 で導入しなかったもの:

```text
general backtracking
producer ranking
proof-cost model
best-proof selection
DFS / BFS / A*
unbounded recursive search
```

---

# 4. 次候補：Phase 88

次の自然な候補は、finite retry infrastructure を実際の theorem-backed proof target で必要とする場面があるかを監査すること。

最初は実装を広げず:

```text
Phase 88-1
actual-theorem retry necessity / compatibility audit
```

を行う。

確認対象:

```text
actual Toda / EHP proof targets
producer ambiguity が現実に発生する箇所
synthetic retry と theorem-backed retry の意味論差
current retry diagnostics で十分か
selected-path provenance が theorem-backed case でも十分か
```

監査結果として concrete need が確認された場合だけ、最小の theorem integration を追加する。

先取りしない:

```text
general backtracking
ranking
cost model
best-proof selection
DFS / BFS / A*
```

---

# 5. 継続して保留する一般化

数学 / representation:

```text
general existential quantification
general witness / uniqueness framework
generic sign algebra
generic Toda-bracket coset algebra
generic symbolic dimension solver
generic map typing solver
generic stable theorem engine
stable ring machinery
```

proof search:

```text
formal max_depth > 4 regression
unbounded recursion
general backtracking
ranking
cost model
best-proof selection
DFS / BFS / A*
generic theorem prover
```

storage / presentation:

```text
persistent Proof Repository
persistent search cache
proof graph serialization
automatic proof narrative generation
```

---

# 6. 性能方針

wall-clock time は複数 PC 間で直接比較しない。

主要 signal:

```text
test count
semantic coverage
provenance coverage
focused regression
repository-wide regression
```

重い deterministic fixture builder が同一 object graph を繰り返し利用する場合は:

```python
@lru_cache(maxsize=1)
```

を優先する。
