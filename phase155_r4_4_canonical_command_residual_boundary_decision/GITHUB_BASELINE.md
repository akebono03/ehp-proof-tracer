# GitHub baseline — Phase 155-R4-4

Repository: `akebono03/ehp-proof-tracer`
Branch: `main`
Observed public baseline commit: `8301520a7434f3836b1dbc7e8fa08a60c024225a`

Inspected before R4-4:
- `README.md`,
- `docs/roadmap.md`,
- `tests/conftest.py`,
- repository pytest configuration files.

No `pytest.ini`, `pyproject.toml`, or `setup.cfg` pytest configuration was found
on the public baseline. Repository-wide regression is documented as:

`python -m pytest tests -q`

The roadmap explicitly distinguishes:
- focused regression,
- canonical regression,
- complete historical regression.

R4-4 therefore defines canonical selection through an explicit node-ID
manifest rather than introducing a repository-wide marker scheme prematurely.

The runner calls `pytest.main()` inside Python, avoiding Windows shell command
length limits for thousands of node IDs.

No production code or existing test is changed.
Canonical test bodies and repository-wide pytest are not executed in R4-4.
