# GitHub baseline — Phase 155-R3-2E

Repository: `akebono03/ehp-proof-tracer`
Branch: `main`
Observed baseline commit: `8301520a7434f3836b1dbc7e8fa08a60c024225a`

Rechecked before R3-2E:

- `tests/conftest.py`
- `tests/test_phase148_rc2_4_repair_r5.py`
- `tests/test_phase149_rc3_4_cross_group_ordering.py`
- repository usage of `pytest.mark.parametrize`

The current repository uses parameterized tests where a single source-level
function expands into multiple pytest node IDs.

Examples include Phase 148 and Phase 149 tests using:

`@pytest.mark.parametrize(..., CASES)`

This confirms that a source-level candidate ID and a pytest runtime node ID
can differ only by a parameter suffix.

R3-2E therefore captures runtime reports directly instead of inferring a
runtime outcome from the synthetic base-level `missing` rows written by the
earlier R3-2 audit.
