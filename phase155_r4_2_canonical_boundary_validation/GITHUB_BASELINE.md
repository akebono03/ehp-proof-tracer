# GitHub baseline — Phase 155-R4-2

Repository: `akebono03/ehp-proof-tracer`
Branch: `main`
Observed public baseline commit: `8301520a7434f3836b1dbc7e8fa08a60c024225a`

Before R4-2, current GitHub public entry points and related tests were
re-inspected.

Current public entry points include the CLI in `main.py` and the Flask/Web
adapters:
- `web_app.py`
- `web_group_query.py`
- `web_group_proof.py`
- `web_operation_query.py`
- `web_operation_query_proof.py`
- `web_generator_proof.py`
- `web_generator_exploration.py`
- `web_generator_proof_scope.py`
- `web_generator_applicability.py`
- `web_generator_execution.py`

GitHub search confirms that older numbered Phase tests still directly exercise
these current public modules, including Web operation query/proof (Phase 118),
generator proof (Phase 120), exploration (Phase 121), proof scope (Phase 122),
applicability (Phase 123), and execution (Phase 125).

Therefore R4-2 uses actual public-module reachability rather than Phase age as
canonical evidence.

No production/test changes are made and repository-wide pytest remains
reserved for the end of Phase 155.
