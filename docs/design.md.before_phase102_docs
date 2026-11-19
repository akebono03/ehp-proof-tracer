# EHP Proof Tracer 設計

この文書は EHP Proof Tracer の**現在有効なアーキテクチャ、意味論、invariant、設計境界**を記録する。

過去の実装経緯は `docs/development_log.md`、証明記録は `docs/proof_records.md`、今後の計画は `docs/roadmap.md`、コード探索は `docs/code_reference.md` を参照する。

---

# 1. 基本設計原則

```text
実際の数学的・proof-search 上の必要
↓
不足している最小表現
↓
必要な domain rule / orchestration
↓
既存 generic infrastructure
```

次を混同しない。

```text
representation != typing != theorem knowledge
structural equality != mathematical equality
catalog metadata != proof truth
search plan != proof result
calculation result != proof truth
presentation != proof truth
rendered prose != proof truth
production repository assembly != theorem truth
CLI != proof truth
exploration result != new theorem truth
generator input resolution != mathematical equality
```

---

# 2. 現在のレイヤー構造

計算経路:

```text
expression / statement representation
↓
generic proof / inference mechanics
↓
Toda-specific theorem knowledge
↓
Proof Repository / rule catalog
↓
bounded proof search
↓
Toda group query / lookup
↓
calculation-goal discovery / recovery / normalization
↓
group result
↓
EHP / exactness provenance
↓
flat / recursive proof provenance
↓
structured presentation
↓
human-readable proof report
↓
repository-explicit facade
↓
standard production repository
↓
minimal calculation CLI
```

generator exploration 経路:

```text
generator string
↓
resolve_generator_input()
↓
GeneratorSymbol
↓
standard production repository
↓
structural occurrence path extraction
↓
repository occurrence lookup
↓
semantic role classification
↓
element-centered exploration
↓
grouped presentation
↓
Markdown renderer
↓
production one-shot facade
↓
minimal explore CLI
```

---

# 3. 主要モジュール

```text
expression.py
proof.py
proof_repository.py
rule_catalog.py
repository_inference.py
homotopy_groups.py
toda_rules.py
```

計算 / provenance:

```text
toda_group_query.py
toda_group_lookup.py
toda_group_result.py
toda_calculation_goal*.py
toda_calculation.py
toda_calculation_result.py
toda_ehp_*.py
toda_proof_dependency.py
toda_explanation.py
```

presentation / report:

```text
toda_presentation.py
toda_ehp_presentation.py
toda_proof_presentation.py
toda_proof_flow_presentation.py
toda_end_to_end_presentation.py
toda_human_readable_renderer.py
toda_proof_narrative_renderer.py
toda_full_proof_report_renderer.py
toda_calculation_report*.py
```

production calculation:

```text
standard_production_repository.py
toda_calculation_facade.py
main.py
```

generator exploration:

```text
generator_input.py
structural_containment.py
repository_element_lookup.py
generator_occurrence_roles.py
repository_element_exploration.py
repository_element_presentation.py
repository_element_renderer.py
repository_element_facade.py
```

---

# 4. Toda group query

`TodaGroupQuery(n, k)` は

$$
\pi_{n+k}^n
$$

を query する。

valid domain:

```text
n > 0
k >= 0
```

---

# 5. Proof truth と metadata

proof truth の中心:

```text
ProofStep.conclusion
ProofStep.premises
ProofStep.inference_rule
```

`ProofRepositoryEntry.key / phase / theorem` は provenance metadata。

presentation、renderer、facade、production repository、CLI、exploration、resolver は proof truth を追加してはならない。

---

# 6. Repository read-only invariant

query / calculation / reporting / exploration は repository を read-only に扱う。

```text
before entries == after entries
```

必要な箇所では `ProofStep` identity も保持する。

---

# 7. Calculation result semantics

```text
0 candidates  → NOT_FOUND
1 candidate   → FOUND
2+ candidates → MULTIPLE_RESULTS
```

multiple candidate を自動 ranking / selection しない。

---

# 8. EHP / exactness provenance

truth source は final theorem-backed `ProofStep` から reachable な ancestry。

代表:

$$
\pi_{10}^9
\xrightarrow{\Delta}
\pi_8^4
\xrightarrow{E}
\pi_9^5
\xrightarrow{H}
\pi_9^9
\xrightarrow{\Delta}
\pi_7^4.
$$

---

# 9. Production calculation facade

repository-explicit:

```text
build_toda_report(repository, n, k)
```

production:

```text
build_standard_toda_report(n, k)
```

production path は既存 repository-explicit path を compose し、計算 logic を複製しない。

---

# 10. Generator input semantics

`resolve_generator_input()` は explicit user input を exact `GeneratorSymbol` へ変換する。

代表 alias:

```text
η / eta
ν / nu
σ / sigma
ι / iota

ν′ / ν' / nu' / nu_prime
σ' / sigma_prime
σ'' / sigma_double_prime
σ''' / sigma_triple_prime
```

indexed:

```text
eta_2
nu_5
sigma_8
iota_4
```

重要:

```text
unindexed generator != wildcard
```

free-form typo correctionや数学的同値判定は行わない。

---

# 11. Generator occurrence semantics

1 occurrence:

```text
entry
path
matched_generator
roles
```

重要 invariant:

```text
same entry + different structural path
= different occurrence
```

entry-level deduplication はしない。

順序:

```text
repository registration order
→ structural path order
```

---

# 12. Semantic roles

```text
RELATION_LHS
RELATION_RHS
GROUP_GENERATOR
COMPOSITION_LEFT
COMPOSITION_RIGHT
MAP_INPUT
TODA_BRACKET_FIRST
TODA_BRACKET_SECOND
TODA_BRACKET_THIRD
```

1 occurrence は複数 role を持ち得る。

grouped view は master occurrence order を保持する。

---

# 13. Exploration presentation

production repository の conclusion は aggregate theorem statement を含む。

Phase 101 では aggregate 全体を推測で LaTeX 化せず、occurrence path 上の既存 renderer が扱える concrete relation / expression を presentation context として使う。

```text
aggregate conclusion
↓
occurrence path
↓
renderable concrete ancestor
↓
existing renderer
```

---

# 14. Production exploration facade

repository-explicit:

```text
explore_repository_generator(repository, generator)
```

production:

```text
explore_standard_repository_generator_input(generator_input)
```

path:

```text
string
↓
resolver
↓
production repository
↓
structural exploration
↓
presentation
↓
Markdown
```

valid zero occurrence は error ではない。

---

# 15. CLI boundary

calculation:

```text
python main.py 5 7
```

exploration:

```text
python main.py explore "nu'"
```

calculation exit:

```text
FOUND / MULTIPLE_RESULTS → 0
NOT_FOUND                → 1
invalid input            → 2
```

exploration exit:

```text
valid occurrence(s)      → 0
valid zero occurrence    → 0
invalid generator        → 2
missing / extra argument → 2
explore --help           → 0
```

既存 positional `(n,k)` path は維持する。

---

# 16. Phase 101 validation

固定した項目:

```text
Unicode / ASCII alias equivalence
indexed exact lookup
zero occurrence
invalid input
distinct structural paths
deterministic order
grouped-view order
repository non-mutation
CLI help / missing / extra
stdout / stderr / exit code
legacy n,k compatibility
```

production `nu_prime` は Phase 101-5 時点で6 structural occurrence。

production `nu_5` は3 occurrence。

`eta_999` は0 occurrence。

総 occurrence 数自体は theorem coverage 増加で変化し得るため core invariant ではない。

---

# 17. 現在の境界

未実装:

```text
free-form natural-language search
wildcard family search
general composition evaluation
general Toda-bracket solving
coset / indeterminacy computation
automatic applicable-lemma discovery
automatic enumeration of unstated consequences
symbolic higher-range auto-instantiation
general proof ranking
Web UI
odd-primary full integration
all-primary ordinary sphere-homotopy calculation
```

---

# 18. 文書 TeX 方針

GitHub Markdown では数式に:

```text
inline:  $...$
display: $$...$$
```

を使用する。

`\(...\)` / `\[...\]` を標準表示方法として前提にしない。

コードや CLI は backtick / code block、数式は数式 delimiter を使う。

---

# 19. Completion baseline

Phase 101-5:

```text
57 passed in 8.49s

repository-wide:
8058 passed in 133.01s

git diff --check:
clean
```

Phase 101-6 は production code を増やさず、final audit / documentation correction のみを行う。
