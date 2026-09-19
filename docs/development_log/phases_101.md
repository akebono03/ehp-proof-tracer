# Phase 101 — Production Generator Exploration

Phase 101 は、Phase 99 で完成していた generator-centered repository exploration を production user-facing path へ接続した。

## Phase 101-1

production-input / CLI pressure audit。

監査により、resolver・repository-explicit exploration・standard production repository は既に存在し、欠けていたのは production one-shot facade と `main.py` dispatch であることを確認した。

## Phase 101-2

追加:

```text
explore_standard_repository_generator_input(generator_input)
```

production aggregate statement の presentation では aggregate 全体を推測描画せず、occurrence path 上の既存描画可能な concrete relation / expression を再利用した。

```text
108 passed in 9.43s
repository-wide: 8022 passed in 206.43s
```

## Phase 101-3

既存:

```text
python main.py 5 7
```

を維持しつつ:

```text
python main.py explore "nu'"
```

を追加。

```text
repository-wide: 8028 passed in 190.79s
```

## Phase 101-4

validation:

```text
alias equivalence
indexed exact lookup
zero occurrence
invalid input
distinct structural path
deterministic order
grouped order
repository non-mutation
```

probe:

```text
nu_prime → 6 occurrences
nu_5     → 3 occurrences
eta_999  → 0 occurrences
```

```text
104 passed in 11.12s
repository-wide: 8042 passed in 118.12s
```

## Phase 101-5

CLI boundary:

```text
help
missing argument
extra argument
malformed input
stdout / stderr
exit 0 / 2
legacy n,k path
legacy NOT_FOUND exit 1
```

```text
57 passed in 8.49s
repository-wide: 8058 passed in 133.01s
git diff --check: clean
```

## Phase 101-6

production code は追加せず final audit / documentation correction。

README の TeX は GitHub Markdown で安定する `$...$` / `$$...$$` へ統一する。

Phase 101 は新しい theorem truth を追加していない。既存 structural occurrence truth への production input / presentation / CLI path を追加した。
