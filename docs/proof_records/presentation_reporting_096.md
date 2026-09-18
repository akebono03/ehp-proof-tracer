# Phase 96 — Presentation / Proof Report 記録

この文書は Phase 96 で追加した presentation / rendering capability と proof-truth boundary を記録する。

---

# 1. 目的

Phase 95 までで:

```text
TodaGroupQuery
→ TodaCalculationResult
→ group result
→ EHP / exactness provenance
→ flat / recursive proof provenance
```

が structured object として得られるようになった。

Phase 96 の目的:

```text
human-readable explanation / proof report
```

境界:

```text
presentation != proof truth
rendered prose != proof truth
```

---

# 2. Presentation architecture

```text
proof / calculation model
↓
structured presentation
↓
renderer
```

proof model に Markdown / LaTeX prose を埋め込まない。

---

# 3. Atomic mathematical presentation

group structure:

```text
ZERO
FREE_CYCLIC
FINITE_CYCLIC
DIRECT_SUM
```

generator order:

```text
INFINITE
FINITE
```

raw `None` order は semantic `INFINITE` として表示する。

---

# 4. EHP / exactness presentation

actual \(\pi_9^5\):

\[
\pi_{10}^9
\xrightarrow{\Delta}
\pi_8^4
\xrightarrow{E}
\pi_9^5
\xrightarrow{H}
\pi_9^9
\xrightarrow{\Delta}
\pi_7^4.
\]

source EHP result identity、term / map / window order、exactness-use provenance、consumer `ProofStep` identity を保持する。

---

# 5. Proof source presentation

表示可能:

```text
role
literature source
repository key
phase
theorem
calculation goal source
```

repository metadata は actual `ProofStep` identity に対応するときのみ付与する。

aggregate metadata を internal dependency へ誤伝播しない。

---

# 6. Dependency-first proof flow

recursive provenance から:

```text
premise before parent
```

の presentation order を導出。

shared dependency:

```text
one node
multiple incoming edges
incoming_use_count
is_shared_dependency
```

cycle-safe。

---

# 7. actual \(\pi_9^5\) end-to-end presentation

\[
\pi_9^5=\mathbb Z/2\{\nu_5\eta_8\}.
\]

goal source:

```text
Phase 68
Toda Proposition 5.8
pi9_5_group_relation
```

group / EHP / exactness / dependencies / proof flow / source metadata を統合。

root identity:

```text
group proof root
=
dependency root
=
proof-flow root
```

---

# 8. Representative expansion

同じ API で:

\[
\pi_7^4,\quad
\pi_9^5,\quad
\pi_{10}^4,\quad
\pi_{11}^5,\quad
\pi_9^2,\quad
\pi_{12}^5
\]

を処理。

代表:

\[
\pi_7^4
=
\mathbb Z\{\nu_4\}
\oplus
\mathbb Z/4\{E\nu'\},
\]

\[
\pi_{10}^4=\mathbb Z/8\{\nu_4^2\},
\qquad
\pi_{11}^5=\mathbb Z/2\{\nu_5^2\},
\]

\[
\pi_9^2=0,
\qquad
\pi_{12}^5=\mathbb Z/2\{\sigma'''\}.
\]

---

# 9. LaTeX / Markdown rendering

group result:

\[
\pi_9^5\cong\mathbb Z/2\{\nu_5\eta_8\}.
\]

EHP map symbol は LaTeX へ正規化し、\(\Delta\) は `\Delta` として出力する。

---

# 10. Mathematical statement rendering

actual \(\pi_9^5\) で:

\[
\Delta:\pi_9^9\to\pi_7^4
\]

injective、

\[
H:\pi_9^5\to\pi_9^9
\]

zero map、

\[
E:\pi_8^4\to\pi_9^5
\]

surjective、

\[
\pi_9^5=\mathbb Z/2\{\nu_5\eta_8\}
\]

を出力可能。

---

# 11. Safe fallback

未対応 statement:

```text
TodaProp56FiniteDimensionalStatement
```

などは class-name fallback。

```text
unknown semantic type
→ explicit fallback
```

を守る。

---

# 12. Readable narrative

dependency-first flow を narrative に利用。

proof ancestry にない因果説明を renderer が追加しない。

generic `MAP_PROPERTY` lead は:

```text
From the preceding statements
```

へ中立化。

---

# 13. Unified full proof report

main entry point:

```text
render_toda_full_proof_report_markdown()
```

sections:

```text
Result
Source
EHP sequence
Exactness
Proof flow
Readable proof narrative
```

`Proof flow` は machine-facing provenance view、`Readable proof narrative` は human-facing mathematical view。

---

# 14. Final audit

Phase 96-12:

```text
LaTeX Delta normalization
major section uniqueness
technical / readable section separation
safe unknown fallback
no Python object repr leakage
representative target rendering
deterministic output
repository non-mutation
```

最終 regression:

```text
focused / related:
75 passed in 6.50s

repository-wide:
7577 passed in 43.70s

git diff --check:
clean
```

---

# 15. Completion

```text
query
→ calculation result
→ structured presentation
→ EHP / exactness
→ proof source
→ dependency-first proof flow
→ LaTeX / Markdown
→ mathematical statement rendering
→ readable narrative
→ unified full proof report
```

```text
Phase 96
→ COMPLETE
```

次:

```text
Phase 97
→ user-facing proof-report query / calculation-to-report API
```
