Phase 145 — group-proof default only

Change only the group-proof defaults:
- mode -> narrative
- depth -> 2

Explicit mode/depth behavior remains unchanged.

Production targets:
- main.py: build_group_proof_argument_parser, _run_group_proof_command
- web_app.py: create_app group-proof form defaults
- web_group_proof.py: build_standard_web_group_proof_view

Focused tests only are run by this package.
Repository-wide pytest is intentionally NOT run here.
