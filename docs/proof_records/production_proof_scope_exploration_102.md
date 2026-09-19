# Phase 102 — Production proof-scope exploration record

この記録は Phase 102 の recursive production proof-scope exploration capability をまとめる。

---

# 1. 目的

Phase 99 / 101 の探索は registered repository entry の `step.conclusion` を対象としていた。

しかし actual production proof では重要な relation / membership が root conclusion ではなく `ProofStep.premises` ancestry に存在する。

Phase 102 の目的は:

```text
registered production root
→ actual proof ancestry
→ already represented statement discovery
```

を read-only に可能にすること。

---

# 2. Truth boundary

数学的 truth source:

```text
ProofStep.conclusion
ProofStep.premises
```

Phase 102 は新規 theorem を生成しない。

```text
proof-scope traversal != theorem search
Toda membership discovery != bracket solving
known map relation discovery != map evaluation
```

---

# 3. Proof-scope node

```text
RepositoryProofScopeNode
```

保持:

```text
root_entry
proof_step
shortest_depth
```

semantics:

```text
depth 0
= root_entry.step

same proof under one root
= shortest-depth occurrence only

same proof under different roots
= separate provenance

cycle
= safe

repository
= unchanged
```

---

# 4. Generator occurrence

各 ancestry node の:

```text
proof_step.conclusion
```

を structural scan する。

保持:

```text
scope_node
path
matched_generator
roles
```

既存 `GeneratorOccurrenceRole` を再利用する。

---

# 5. Toda membership

対象:

```text
TodaBracketMembershipStatement
TodaBracketMembershipTheoremStatement
```

Phase 102 では:

```text
membership element
bracket first
bracket second
bracket third
```

を区別する。

production representative:

$$
\nu' \in \{\eta_3,2\iota_4,\eta_4\}_1.
$$

ここで $\nu'$ は membership element 側にある。

---

# 6. Known map relation

対象:

```text
RelationType.EQUALITY
lhs is MapApplication
generator occurrence has RELATION_LHS
generator occurrence has MAP_INPUT
```

production representative:

$$
H(\nu')=\eta_5.
$$

保持:

```text
relation
map_application
map
input_expression
output_expression
source_occurrence
```

---

# 7. Facade identity invariant

production result:

```text
RepositoryProofScopeExplorationResult
```

保持:

```text
generator
scope
occurrences
toda_memberships
map_relations
```

semantic result の `source_occurrence` は master `occurrences` 内の object identity を再利用する。

この invariant は Phase 102-6 の初回 failure により明示的に regression 固定された。

---

# 8. CLI

```text
python main.py explore-proof nu_prime
```

output:

```text
generator
proof-scope occurrence count
Toda membership count
map relation count
root key
shortest depth
renderable statement
```

valid zero result は exit 0。

invalid generator は argparse error / exit 2。

既存 `explore` と `(n,k)` path は維持。

---

# 9. Verification

```text
Phase 102-5A:
11 passed in 4.67s

Phase 102-5B:
22 passed in 10.29s

Phase 102-6 focused:
42 passed in 23.46s

Phase 102-6 related:
89 passed in 23.32s

final repository-wide:
8142 passed in 129.93s

git diff --check:
clean
```

Phase 102 は COMPLETE。
