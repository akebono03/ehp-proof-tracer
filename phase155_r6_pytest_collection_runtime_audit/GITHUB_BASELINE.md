# GitHub baseline — Phase 155-R6

Repository: `akebono03/ehp-proof-tracer`
Observed public baseline commit: `8301520a7434f3836b1dbc7e8fa08a60c024225a`

Inspected before R6:
- existing tests and R5-style audit naming,
- historical performance diagnostic tooling,
- prior `pytest --durations` practice.

Relevant prior design:
- Phase 150 performance diagnostics used bounded pytest windows rather than
  treating a diagnostic as another full-suite run.
- The diagnostic used per-test timeout and `--durations`.
- Phase-final full regressions used `--durations` in the same full run so a
  second full suite was unnecessary.

R6 follows the bounded-diagnostic pattern:
- checkpointed collection,
- bounded representative runtime probes,
- no full canonical regression,
- no repository-wide full pytest.

No production code or existing test is changed.
