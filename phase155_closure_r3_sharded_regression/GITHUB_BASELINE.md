# GitHub baseline — Phase 155 Closure-R3

Repository: `akebono03/ehp-proof-tracer`
Observed public baseline commit: `8301520a7434f3836b1dbc7e8fa08a60c024225a`

Inspected before Closure-R3:
- `tests/conftest.py`
- root pytest configuration candidates (`pytest.ini`, `pyproject.toml`, `setup.cfg`), none present in the public baseline

Phase155 audit-boundary files are local Closure work and are therefore validated
at runtime rather than fetched from the public baseline.

Historical full-suite evidence used for planning:
- 10421 tests in the previous monolithic run
- 98 failed / 10323 passed
- 2380.08s test runtime
- three extreme tests at 508.30s, 281.49s, 276.88s
These three historical durations are ignored by the current shard planner because
their test bodies were replaced in R2C-R2.

No production code is changed.
No repository test file is changed.
No Phase156 functionality is implemented.
