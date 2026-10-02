# Phase 155-R1 GitHub baseline

確認対象:

```text
repository: akebono03/ehp-proof-tracer
branch: main
commit: 8301520a7434f3836b1dbc7e8fa08a60c024225a
```

GitHub の current tree から確認した `tests/test_*.py` inventory:

```text
test files: 843
core test files: 23
Phase-numbered test files: 820
total bytes: 6,796,313
```

Phase 153 / 154 の current tests も `tests/` に残っている一方、Phase 144 などには `audit`, `completion`, `cross_group` 等を名前に含む historical audit tests が多数存在する。

README の current closure record では、Phase 153 の canonical `tests/` run が stale presentation expectations を露出し、test-suite consolidation を別 maintenance task として延期したことが記録されている。Phase 154 closure も repository-wide all-pass を主張していない。

この R1 パッケージは、その状況を削除なしで inventory 化するための静的監査ツールである。
