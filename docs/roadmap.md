# EHP Proof Tracer ロードマップ

この文書は**今後の capability dependency と Phase 順序**を記録する。

過去の実装履歴は `docs/development_log.md`、現在の設計は `docs/design.md`、代表的な証明記録は `docs/proof_records.md` を参照する。

---

# 1. 現在地

数学面では、Toda の finite-dimensional calculation spine と stable \(G_0\) through \(G_7\) の主要 2-primary data を実装済み。

proof infrastructure では:

```text
Proof Repository
→ automatic rule selection
→ concrete producer compatibility
→ bounded dependency search
→ max_depth parameterization
→ finite retry
→ diagnostics
→ selected-path execution
→ ProofStep provenance
```

まで完成している。

calculation / explanation infrastructure では:

```text
TodaGroupQuery
→ direct theorem-backed lookup
→ aggregate concrete-branch fallback
→ branch ProofStep recovery
→ TodaGroupResult normalization
→ EHP / exactness provenance
→ flat dependencies
→ recursive proof provenance
→ TodaCalculationResult
```

まで完成している。

Phase 95-20 の representative end-to-end regression では:

\[
\pi_7^4,\quad
\pi_9^5,\quad
\pi_{10}^4,\quad
\pi_{11}^5,\quad
\pi_9^2,\quad
\pi_{12}^5
\]

を aggregate theorem entries だけから top-level API で取得できることを確認済み。

最新 repository-wide regression:

```text
7419 passed in 38.11s
```

---

# 2. 完了済み capability 群

Phase 90–95 で次を完成させた。

```text
query target construction
theorem-backed known-result lookup
normalized group structure / generators / orders
actual EHP extraction
exactness-use provenance
flat proof dependency extraction
dependency role classification
recursive proof provenance
aggregate theorem concrete-branch discovery
original branch ProofStep recovery
aggregate provenance preservation
direct-result precedence
multiple-result preservation
top-level calculation orchestration
representative end-to-end regression
```

Phase 95 の implementation capability は完了している。

正式な completion record は Phase 95-22D で development / proof record archive に追記する。

---

# 3. Phase 95 COMPLETE

Phase 95 の calculation orchestration と documentation synchronization は完了した。

completion sequence:

```text
Phase 95-22A
documentation structure audit
→ COMPLETE

Phase 95-22B
development_log / proof_records archival split
→ COMPLETE

Phase 95-22C
README / design / roadmap current-state rewrite
→ COMPLETE

Phase 95-22D
Phase 95 completion record
→ COMPLETE

Phase 95-22E
document links / consistency / final verification
→ COMPLETE
```

Phase 95 の正式な最終状態:

```text
implementation capability
→ COMPLETE

representative end-to-end regression
→ COMPLETE

documentation synchronization
→ COMPLETE

formal Phase status
→ COMPLETE
```

---

# 4. 次 Phase：Phase 96

Phase 96 の主題:

```text
human-readable explanation / proof report
```

Phase 95 までで structured calculation result は揃った。

Phase 96 ではこれを presentation に変換する。

原則:

```text
structured proof truth
!=
presentation
```

presentation layer は proof truth を生成・変更しない。

---

# 5. Phase 96 の初期監査候補

最初は実装せず、current structured result から何を安全に説明できるかを監査する。

推奨:

```text
Phase 96-1
current presentation inputs / explanation boundary audit
```

監査対象:

```text
TodaCalculationResult
TodaCalculationCandidate
TodaGroupResult
TodaRepresentativeExplanationResult
TodaEHPSequenceResult
TodaEHPExactnessUseProvenanceResult
TodaProofDependencyResult
TodaRecursiveProofProvenanceResult
TodaCalculationGoalSource
```

確認する中心:

```text
1. user-facing report に必要な field は何か

2. direct result と aggregate-derived result を
   どう表示上区別するか

3. group structure / generators / orders を
   どこまで canonical に表示できるか

4. EHP sequence を
   machine truth を壊さず表示できるか

5. recursive provenance を
   proof narrative にどう変換するか

6. shared dependency / repeated use / cycle を
   presentation でどう扱うか

7. theorem / phase metadata と
   mathematical proof truth をどう区別するか

8. Markdown / console / LaTeX / structured export の
   最小共通 representation は何か
```

---

# 6. Phase 96 の候補 capability

監査後に必要性を確認してから段階的に追加する。

候補:

```text
structured presentation model
group-result formatter
EHP formatter
proof-dependency formatter
recursive proof-tree / DAG formatter
literature-reference formatter
Markdown report
LaTeX report
console report
```

自然言語 narrator は machine-readable structure を入力として構築し、証明 facts の追加推測を避ける。

---

# 7. Deferred：symbolic higher-range instantiation

現在 concrete aggregate branches は top-level calculation 可能。

一方、例えば:

\[
\pi_{n+3}^n=\mathbb Z/8\{\nu_n\},
\]

\[
\pi_{n+6}^n=\mathbb Z/2\{\nu_n^2\},
\]

\[
\pi_{n+7}^n=\mathbb Z/16\{\sigma_n\}
\]

のような symbolic theorem branch を concrete `TodaGroupQuery` に instantiate する capability は未実装。

必要なのは:

```text
symbolic theorem statement
+
range condition
+
concrete query
↓
safe theorem specialization
```

であり、Phase 95 orchestration の単純 extension ではない。

actual need が生じた時点で独立 Phase として扱う。

---

# 8. Deferred：target-only proof-search fallback

現在の bounded proof search は concrete goal を必要とする。

query が持つのは:

```text
target group
```

だけであり、

```text
π_{n+k}^n = ?
```

の RHS は未知である。

したがって:

```text
target-only query
→ concrete unknown-RHS theorem goal
```

を生成する一般機構はまだない。

Phase 95 では aggregate theorem 内の既存 concrete statement を発見することで安全に fallback を実現した。

target-only bounded-search fallback は、target-to-goal generation の actual requirement が生じたときに別 Phase で扱う。

---

# 9. Deferred：calculation failure diagnostics

現在の top-level status:

```text
NOT_FOUND
FOUND
MULTIPLE_RESULTS
```

`NOT_FOUND` の細分類:

```text
no direct result
no aggregate candidate
candidate found but branch recovery failed
normalization failed
symbolic-only theorem coverage
```

などは未導入。

user-facing report で actual need が確認されるまで追加しない。

---

# 10. Deferred：proof optimization

現時点で不要:

```text
general backtracking
producer ranking
proof-cost optimization
best-proof selection
persistent proof cache
global proof optimization
```

multiple valid candidates は保持し、orchestration が勝手に優劣をつけない。

---

# 11. Deferred：mathematical scope expansion

将来候補:

```text
odd-primary integration
broader unstable stems
additional Toda propositions / lemmas
symbolic stable-range theorem specialization
ordinary all-primary π_{n+k}(S^n)
```

ただし既存 2-primary Toda semantics を壊さない形で actual need に応じて追加する。

---

# 12. 文書整備

Phase 95 completion に合わせて文書体系を整理した。

```text
README.md
→ concise current status

docs/design.md
→ current architecture only

docs/roadmap.md
→ future-oriented plan

docs/development_log.md
→ history index

docs/development_log/
→ chronological archives

docs/proof_records.md
→ proof-record index

docs/proof_records/
→ mathematical / infrastructure archives
```

長期履歴を current-state document に重複掲載しない。

---

# 13. Completion policy

各 Phase は最低限:

```text
focused pytest
related regression
repository-wide pytest
git diff --check
```

を確認する。

実装前には:

```text
current GitHub code
related tests
actual theorem-backed need
```

を確認する。

文書変更では current implementation と記述が一致していることを確認する。

---

# 14. 直近の次作業

Phase 95 は正式 COMPLETE。

次:

```text
Phase 96-1
current presentation inputs / explanation boundary audit
```

まず実装せず、Phase 95 の structured calculation result から human-readable presentation に安全に渡せる情報と presentation boundary を監査する。
