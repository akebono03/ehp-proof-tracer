# EHP Proof Tracer ロードマップ

この文書は **今後の capability dependency と Phase 順序**を記録する。

現在の仕様は `README.md` / `docs/design.md` を優先し、過去の詳細な実装履歴は `docs/development_log.md`、代表証明・infrastructure record は `docs/proof_records.md` を参照する。

---

# 1. 文書運用方針

roadmap は future-oriented に保つ。

完了済み Phase の詳細な subphase、focused test、implementation history は roadmap に蓄積せず、milestone summary のみに圧縮する。

```text
README.md
= current status / current capability

docs/design.md
= current architecture / semantics / boundaries

docs/development_log.md
= chronological implementation history

docs/code_reference.md
= current code navigation / public infrastructure

docs/proof_records.md
= representative mathematical proof records
  + infrastructure records

docs/roadmap.md
= future plan / dependency / deferred boundary
```

---

# 2. 開発原則

```text
実際の数学的必要 / capability need
↓
current code / related tests audit
↓
既存 semantics / API compatibility
↓
不足している最小 representation / orchestration
↓
focused implementation
↓
actual integration
↓
applicability / provenance / safety
↓
representative probe
↓
full regression
↓
completion documentation
```

原則:

```text
future Phase の framework を先取りしない
既存 API を不必要に壊さない
generic theorem prover 化しない
representation と theorem knowledge を混同しない
診断結果と実行経路を一致させる
repository は明示しない限り非破壊
```

---

# 3. 完了済み milestone summary

```text
Phase 1–27
generic proof / algebra / Toda-bracket foundation

Phase 28–48
actual H branch
PrimaryComponent / TodaPrimaryGroup
WhiteheadProduct
Toda Lemma 4.1
Proposition 4.2
Toda (4.5)
Proposition 4.4

Phase 49–63
η-family / ν-family concrete branch
Proposition 5.1
Lemma 5.2
Proposition 5.3
Lemma 5.4
Lemma 5.5
Toda (5.5)
Toda (5.6)

Phase 64
performance stabilization

Phase 65–77
Toda Chapter V finite-dimensional continuation
Proposition 5.6
Equation (5.8)
Lemma 5.7
Proposition 5.8
Equation (5.10)
Proposition 5.9
Equation (5.12)
Lemma 5.10 canonical correction
Proposition 5.11
Lemma 5.12
Proposition 5.15
Equation (5.16)
Lemma 5.16

Phase 78
stable G_0 through G_7 consolidation

Phase 79
minimal in-memory Proof Repository

Phase 80
repository-assisted automatic inference
with explicitly supplied rules

Phase 81
automatic goal-compatible rule selection

Phase 82
one-level goal-directed missing-premise production

Phase 83
multiple one-level producers

Phase 84
bounded depth=2 producer search / execution
shared dependency reuse

Phase 85
search-failure diagnostics
execution-failure diagnostics
unified bounded-search report
integrated selected-path execution
actual Toda Lemma 5.16 verification
```

Phase 85 completion repository-wide regression:

```text
6945 passed in 108.60s
```

Wall-clock time is machine-dependent because development is performed on multiple PCs. Test count, semantics, provenance coverage, and focused regression remain the primary cross-machine signals.

---

# 4. 現在の数学 capability

Low stable stems:

```text
G_0=Z{ι}

(G_1;2)=Z/2{η}
(G_2;2)=Z/2{η²}
(G_3;2)=Z/8{ν}
(G_4;2)=0
(G_5;2)=0
(G_6;2)=Z/2{ν²}
(G_7;2)=Z/16{σ}
```

Toda Lemma 5.16 までの concrete proof spine は provenance 付きで formalized されている。

代表 actual theorem:

```text
Toda Lemma 5.16 final bracket-sum consequence
```

は現在:

```text
initial repository facts
↓
automatic bounded search
↓
selected producer dependency DAG
↓
integrated execution
↓
final ProofStep
```

として再導出可能。

---

# 5. 現在の proof-search capability

現在の high-level flow:

```text
goal
↓
goal-compatible final-rule selection
↓
missing-premise analysis
↓
bounded producer search
↓
search-failure diagnostics
↓
execution-failure diagnostics
↓
unified report
↓
exact selected-path execution
↓
goal ProofStep
```

現在の bounded search:

```text
maximum producer depth = 2
unique producer policy
shared producer identity deduplication
dependency-first execution
producer max_rounds = 1
repository non-mutation
```

Phase 85 status model:

```text
SUCCESS
GOAL_ALREADY_AVAILABLE

NO_FINAL_RULE
AMBIGUOUS_FINAL_RULE
NO_PRODUCER
UNSAFE_PRODUCER
AMBIGUOUS_PRODUCER
CYCLE_DETECTED
DEPTH_LIMIT

PRODUCER_NOT_APPLICABLE
PRODUCER_OUTPUT_NOT_USABLE
FINAL_RULE_NOT_APPLICABLE
GOAL_NOT_DERIVED
```

Actual Toda Lemma 5.16 representative path:

```text
final
├─ bracket-sum              depth 1 and 2
└─ composition              depth 1
   └─ bracket-sum           depth 2
```

shared bracket-sum:

```text
depths = (1, 2)
is_shared = True
```

---

# 6. 現在の安全境界

Phase 85 完了時点で意図的に未実装:

```text
depth > 2
arbitrary recursive producer search
retry / backtracking
multiple alternative-path planning
producer ranking
proof-cost model
best-proof selection
DFS / BFS / A*
mathematical-equivalence goal normalization
persistent search cache
persistent Proof Repository
automatic proof narrative generation
generic theorem prover
```

これらは互いに独立した capability として扱う。

特に:

```text
depth parameterization
!=
backtracking
!=
ranking
!=
general theorem proving
```

を維持する。

---

# 7. 次 Phase：Phase 86 bounded-search generalization / depth parameterization

Phase 86 の第一目的は **現在の depth=2 semantics を壊さず、depth limit を明示的に扱える設計へ一般化可能か監査すること**。

最初から arbitrary recursive theorem search を実装しない。

## Phase 86-1：hard-coded depth=2 compatibility audit

確認対象:

```text
BoundedProducerSearchNode
BoundedProducerSearchResult

diagnose_depth_two_producer_search_failure()
select_unique_depth_two_producer_chain()
diagnose_depth_two_producer_execution_failure()
build_depth_two_producer_search_report()
execute_depth_two_producer_search()

depth-related tests / probe
```

確認事項:

```text
どのAPI名・分岐・diagnosticがdepth=2を仮定しているか
shared-node depths semantics
cycle detection semantics
DEPTH_LIMIT diagnostic semantics
dependency-first order
repository non-mutation
actual Toda Lemma 5.16 compatibility
```

Phase 86-1 は audit を先行し、必要性が確定するまで production generalization を行わない。

## Phase 86-2：explicit depth-limit representation / API

監査で安全と確認できた場合のみ:

```text
max_depth
```

を明示的な入力として扱う最小 API を検討する。

最初の完了条件:

```text
max_depth=2
→ Phase 85 と同じ selected path
→ 同じ diagnostics
→ 同じ proof result
→ 同じ provenance
```

既存 depth=2 API は不必要に壊さない。

## Phase 86-3：bounded depth > 2

Phase 86-2 が成立し、具体的 proof need がある場合のみ検討する。

必要条件:

```text
finite explicit max_depth
cycle-safe
unique producer policy preserved
deterministic dependency ordering
diagnostic context preserved
exact selected-path execution
repository non-mutation
```

depth > 2 を許しても:

```text
retry / backtracking
ranking
A*
best-proof selection
```

は同時導入しない。

---

# 8. Phase 86 以降の別候補

Phase 86 と独立して、将来以下を検討できる。

## Alternative producer planning

現在:

```text
distinct producer ambiguity
→ stop
```

将来候補:

```text
multiple safe producer alternatives
↓
explicit planning policy
```

ただし ranking / cost model が必要になるまで先取りしない。

## Retry / backtracking

現在:

```text
selected unique path fails execution
→ diagnostic failure
```

将来候補:

```text
execution failure
↓
alternative path retry
```

これは depth parameterization とは別 Phase とする。

## Proof ranking / cost model

将来候補:

```text
multiple valid proofs
↓
cost / provenance / depth policy
↓
preferred proof
```

現在は不要。

---

# 9. Persistent Proof Repository / search cache

現在の `ProofRepository` は process-local in-memory catalog。

Phase 85 の generated proof steps は repository に自動登録されない。

将来 persistence を導入する場合、少なくとも:

```text
typed conclusion
ProofRule
premise edges
inference-rule identity
literature provenance
repository metadata
schema / semantic compatibility version
```

を保存する必要がある。

現在は:

```text
DEFERRED
```

persistent search cache と persistent Proof Repository は同一 capability とみなさない。

---

# 10. Automatic proof narrative generation

現在:

```text
proof inference       = automatic
proof provenance      = automatic
bounded proof search  = automatic through depth 2
diagnostics           = automatic
proof records         = human curated
probe narrative       = hand-authored
```

将来 target:

```text
ProofStep graph
+ Expression tree
+ InferenceRule provenance
+ LiteratureStatement
+ search diagnostic / execution metadata
↓
relevant-path extraction
↓
step grouping / compression
↓
equation-chain generation
↓
citation insertion
↓
console / Markdown / LaTeX narrative
```

formal mathematical proof records は現在13件。

Phase 79–85 infrastructure records は数学的 proof record とは別に管理する。

状態:

```text
DEFERRED
```

---

# 11. 証明記録

数学的 formal proof records:

```text
13
```

infrastructure records:

```text
Phase 79
Phase 80
Phase 81
Phase 82
Phase 83
Phase 84
Phase 85

total = 7
```

Phase 85 infrastructure record は:

```text
bounded-search diagnostics
unified report
integrated selected-path execution
actual Toda Lemma 5.16 verification
```

を記録する。

---

# 12. 性能方針

Phase 64 same-machine baseline:

```text
3657 passed in 259.11s
↓
3657 passed in 29.97s
```

Phase 85 final regression:

```text
6945 passed in 108.60s
```

異なるPC間の wall-clock time をコード性能の直接比較に使用しない。

performance regression が顕著になった場合のみ:

```text
pytest duration
cProfile
repeated builder reconstruction
premise matching
algebra crosscheck
```

を再調査する。

heavy deterministic builder が同じ object graph を繰り返し利用する場合は:

```python
@lru_cache(maxsize=1)
```

を優先する。

---

# 13. 保留中の一般化

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
arbitrary recursion
backtracking
alternative-path planning
ranking
cost model
best-proof selection
DFS / BFS / A*
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

# 14. 現在地点

```text
mathematical frontier:
Toda Lemma 5.16
stable G_0 through G_7

proof infrastructure frontier:
bounded depth=2 producer search
search / execution diagnostics
unified report
integrated selected-path execution

repository-wide regression:
6945 passed
```

次の開発開始点:

```text
Phase 86-1
bounded-search depth parameterization compatibility audit
```

Phase 86 でも最小変更原則を維持し、現在の Phase 85 depth=2 semantics を regression baseline とする。
