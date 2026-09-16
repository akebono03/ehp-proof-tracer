# EHP Proof Tracer ロードマップ

この文書は今後の capability dependency と Phase 順序を記録する。過去の詳細な実装履歴は `docs/development_log.md`、現在の設計は `docs/design.md`、代表記録は `docs/proof_records.md` を参照する。

---

# 1. 現在地

数学面では Toda Lemma 5.16 までの concrete proof spine と stable stem 0〜7 を formalize 済み。

proof infrastructure は Phase 86-3 で次の境界まで到達した。

```text
Proof Repository
-> automatic final-rule selection
-> missing-premise producer search
-> bounded dependency DAG selection
-> search diagnostics
-> execution diagnostics
-> unified report
-> exact selected-path execution
-> goal ProofStep
```

現在サポートする bounded depth:

```text
max_depth = 2
max_depth = 3
```

default:

```text
max_depth = 2
```

Phase 86-3-6 は depth=3 representative probe / regression / completion documentation の段階であり、機能追加ではなく completion 固定を目的とする。

最新確認済み repository-wide baseline:

```text
Phase 86-3-5
6989 passed in 35.32s
```

Phase 86-3-6 の最終 regression 値は実行後に確定する。

---

# 2. Phase 86 完了境界

Phase 86-1:

```text
hard-coded depth=2 compatibility audit
```

Phase 86-2:

```text
explicit max_depth parameterization
max_depth=2 backward compatibility
```

Phase 86-3:

```text
depth=3 synthetic boundary fixture
max_depth=3 selection
DEPTH_LIMIT / cycle diagnostics
search report integration
selected-path execution
representative probe
completion regression / documentation
```

Phase 86-3 の代表 pair:

```text
同じ unique dependency chain

max_depth=2
-> DEPTH_LIMIT

max_depth=3
-> SUCCESS
-> dependency-first C, B, A
-> C -> B -> A -> final
-> goal ProofStep
```

維持する invariant:

```text
finite explicit depth bound
cycle-safe
unique safe producer policy
shared dependency identity preservation
deterministic dependency-first order
diagnostic context preservation
exact selected-path execution
ProofStep provenance preservation
repository non-mutation
default max_depth=2 compatibility
```

---

# 3. 次の proof-search 候補

Phase 86 完了後の次候補は、depth をさらに増やすことよりも producer ambiguity の扱いを明示化すること。

現在:

```text
複数の safe producer candidate
-> AMBIGUOUS_PRODUCER
-> stop
```

次候補:

```text
Phase 87
alternative producer planning / explicit retry policy
```

ただし Phase 87 の開始時には、まず現行 ambiguity semantics と関連テストを監査し、以下を先取りしない。

```text
general backtracking
producer ranking
proof-cost model
best-proof selection
DFS / BFS / A*
```

最初の target は「複数候補のうち一方が失敗した場合に、明示された有限 policy の範囲で次候補を試す必要があるか」を設計監査することとする。

---

# 4. 継続して保留する一般化

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
max_depth > 3
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

これらは concrete need が発生した時点で個別 Phase として設計する。

---

# 5. 性能方針

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
