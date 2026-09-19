# EHP Proof Tracer ロードマップ

この文書は**今後の capability dependency と Phase 順序**を記録する。

過去の実装履歴は `docs/development_log.md`、現在の設計は `docs/design.md`、代表的な証明記録は `docs/proof_records.md` を参照する。

---

# 1. 現在地

production calculation:

```text
raw n,k
→ python main.py n k
  or build_standard_toda_report()
→ standard production repository
→ proof report
```

production generator exploration:

```text
generator string
→ python main.py explore <generator>
  or explore_standard_repository_generator_input()
→ canonical GeneratorSymbol
→ standard production repository
→ structural occurrence lookup
→ semantic roles
→ grouped Markdown
```

最新確認:

```text
Phase 101-5 related:
57 passed in 8.49s

repository-wide:
8058 passed in 133.01s

git diff --check:
clean
```

---

# 2. 完了済み capability

Phase 90–98:

```text
query
group normalization
EHP / exactness provenance
flat / recursive proof provenance
calculation orchestration
structured presentation
readable full proof report
raw n,k facade
```

Phase 99:

```text
structural generator containment
repository occurrence lookup
semantic roles
element exploration
grouped Markdown
repository-explicit one-shot facade
```

Phase 100:

```text
standard production repository
repository-free calculation facade
minimal calculation CLI
production calculation closure
```

Phase 101:

```text
production generator-input audit
production exploration facade
aggregate occurrence presentation bridge
main.py explore dispatch
alias / indexed / zero / invalid validation
deterministic structural occurrence semantics
repository non-mutation
CLI boundary regression
legacy n,k compatibility
```

---

# 3. 現在の user-facing APIs

```text
build_toda_report(repository, n, k)
build_standard_toda_report(n, k)
python main.py n k
```

```text
explore_repository_generator(repository, generator)
explore_standard_repository_generator_input(generator_input)
python main.py explore "nu'"
```

---

# 4. Phase 101 で確定した境界

resolver:

```text
explicit alias
exact indexed generator
prime decoration
```

を扱う。

扱わない:

```text
natural-language interpretation
wildcard family
automatic typo correction
mathematical equivalence inference
```

occurrence:

```text
same entry + different structural path
= different occurrence
```

valid zero occurrence は normal result / exit 0。

---

# 5. 次の候補

Phase 101 で「既知 generator の production exploration」は closure。

次の自然な候補:

```text
Phase 102-1
relation / theorem-pattern exploration pressure audit
```

監査候補:

```text
指定 generator を含む Toda bracket relation
nu' in {a,b,c} 型 membership query
map input / known map image relation
applicable lemma discovery
```

最初に audit し、general solver を先取りしない。

---

# 6. Deferred：Toda bracket exploration

既存 role:

```text
TODA_BRACKET_FIRST
TODA_BRACKET_SECOND
TODA_BRACKET_THIRD
```

を利用し、TodaBracketMembershipStatement / theorem source を絞り込めるか監査する。

bracket value の一般計算とは別 capability。

---

# 7. Deferred：map exploration

候補:

```text
E / H / Δ の input occurrence
既知 map image relation
map property と element occurrence の接続
```

`MAP_INPUT` role は structural occurrence であり、一般 map evaluator ではない。

---

# 8. Deferred：applicable lemma discovery

候補:

```text
element / relation
→ premise-pattern compatibility
→ theorem / lemma candidates
```

proof-search executionと read-only discovery を分離する。

---

# 9. Deferred：coset / indeterminacy

既存 theorem-specific indeterminacy statement を一般 coset engine とみなさない。

---

# 10. Deferred：composition evaluation

known relation lookup から開始し、general composition calculator を先取りしない。

---

# 11. Deferred：derived-but-not-explicit result discovery

まず actual proof ancestry に既に存在する `ProofStep` の discovery を監査する。

「既存導出済み結果」と「新規 theorem search」を区別する。

---

# 12. Deferred：symbolic higher-range instantiation

$$
\pi_{n+3}^n=\mathbb Z/8\{\nu_n\},
\qquad
\pi_{n+6}^n=\mathbb Z/2\{\nu_n^2\},
\qquad
\pi_{n+7}^n=\mathbb Z/16\{\sigma_n\}
$$

の concrete specialization は別 capability。

---

# 13. Deferred：proof optimization

```text
general backtracking
producer ranking
proof-cost optimization
best-proof selection
persistent proof cache
```

actual pressure が出るまで deferred。

---

# 14. Deferred：user interfaces

実装済み:

```text
minimal calculation CLI
minimal generator-exploration CLI
```

将来:

```text
Web UI
structured export
interactive proof graph
filterable exploration UI
```

---

# 15. Deferred：mathematical scope

```text
odd-primary integration
broader unstable stems
additional Toda propositions / lemmas
all-primary ordinary sphere-homotopy calculation
```

---

# 16. 直近の次作業

Phase 101 は COMPLETE。

次候補:

```text
Phase 102-1
relation / theorem-pattern exploration pressure audit
```

まず existing structural occurrence、Toda bracket role、map-input role、theorem statement 型を監査する。
