# Phase 101 — Production Generator Exploration Record

## 1. Truth source

generator exploration の truth source:

```text
ProofRepositoryEntry.step.conclusion
```

exploration は新しい theorem を証明しない。

## 2. Input

`resolve_generator_input()` は explicit user string を exact `GeneratorSymbol` へ変換する。

```text
ν′ / ν' / nu' / nu_prime
```

は同じ prime-decorated $\nu$ symbol。

```text
eta_2
nu_5
sigma_8
iota_4
```

は exact indexed symbol。

unindexed family は wildcard ではない。

## 3. Production path

```text
generator string
↓
resolve_generator_input()
↓
standard production repository
↓
find_repository_generator_occurrences()
↓
classify_generator_occurrence_roles()
↓
RepositoryGeneratorExplorationResult
↓
presentation
↓
Markdown
```

## 4. Occurrence identity

```text
entry
path
matched_generator
roles
```

```text
same entry + different path
= different occurrence
```

entry-level deduplication はしない。

## 5. Representative results

`nu_prime` は Phase 101-5 時点で6 occurrence。

$$
\pi_6^3=\mathbb Z/4\{\nu'\}
$$

$$
\pi_7^4=\mathbb Z\{\nu_4\}\oplus\mathbb Z/4\{E\nu'\}
$$

$$
\pi_6^2=\mathbb Z/4\{\eta_2\nu'\}
$$

$$
\pi_7^3=\mathbb Z/2\{\nu'\eta_6\}
$$

`nu_5` は3 occurrence。

$$
\pi_8^5=\mathbb Z/8\{\nu_5\},
\qquad
\pi_9^5=\mathbb Z/2\{\nu_5\eta_8\},
\qquad
\pi_{11}^5=\mathbb Z/2\{\nu_5\nu_8\}.
$$

## 6. Zero occurrence

```text
eta_999
→ Occurrences: 0
→ normal result
→ CLI exit 0
```

## 7. Invalid input

```text
malformed generator
missing argument
extra argument
→ argparse error
→ stderr
→ exit 2
→ no traceback
```

`explore --help` は stdout / exit 0。

## 8. Repository invariant

exploration は repository を mutation しない。

## 9. Verification

```text
Phase 101-2 related:
108 passed in 9.43s

Phase 101-4 related:
104 passed in 11.12s

Phase 101-5 related:
57 passed in 8.49s

repository-wide:
8058 passed in 133.01s

git diff --check:
clean
```

Phase 101 は COMPLETE。
