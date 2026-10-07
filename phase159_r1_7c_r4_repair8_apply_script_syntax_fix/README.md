# Phase 159 R1-7c R4 repair8

## Apply-script syntax fix

Repair7 failed before applying repository changes because its generated apply
script contained a quoting conflict around `nu'`.

Repair8 removes that fragile quoting pattern and replaces the affected Phase150
test function as a whole.

Production change:

- `toda_group_proof_narrative_reason_renderer.py`
- `render_toda_group_proof_narrative_reason_sentence()`
- removes redundant `ord(generator)=4=4`
- emits `ord(generator)=4`

Test changes:

- updates stale R4 prose expectations under `tests/`
- replaces the Phase150 final-group visibility test with a visible-prose contract
- adds the repair8 focused regression

No import changes.

The package generation process syntax-checks both the apply script and focused
test before creating the ZIP.

Repository-wide pytest is intentionally not run.
