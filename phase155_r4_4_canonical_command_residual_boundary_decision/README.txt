Phase 155-R4-4 — canonical command / residual boundary decision

Purpose
-------
R4-3 established 9,068 canonical source test IDs and left 750
`review_required` plus one `lineage_support_candidate`.

R4-4 makes the concrete routine-regression boundary without deleting the
residual population.

Potentially heavy step
----------------------
The R4-4 validation performs `pytest --collect-only` across the large canonical
set. This can be moderately heavy, similar to or somewhat heavier than R4-3.

It prints progress as:

`collect batch N/M (...)`

Test bodies are NOT executed.

Residual decision
-----------------
R4-4 first adds one final ownership pass for module-level dependencies. Example:

```python
from toda_rules import make_rule

RULE = make_rule()

def test_x():
    assert RULE is not None
```

The test does not directly mention `make_rule`, but its module-level global
does. Such tests become `canonical_module_global_contract_candidate`.

Anything still lacking direct/helper/module-global current production ownership
is retained as `residual_validation_lane`.

Residual does NOT mean removable. R5/R6 decide historical/heavy/runtime
treatment.

Production-module boundary
--------------------------
The current root production import graph is also analyzed.

Modules without direct test ownership may still be indirectly covered when
they are imported by directly owned current production modules.

Canonical command
-----------------
R4-4 generates:

- `phase155_r4_4_canonical_nodeids.txt`
- `run_phase155_canonical_regression.py`
- `run_phase155_canonical_regression.ps1`

The Python runner reads the manifest and calls `pytest.main()` directly.
This avoids Windows command-line length limits from expanding thousands of
node IDs in PowerShell.

The canonical execution command is:

```powershell
powershell -ExecutionPolicy Bypass `
  -File ".\phase155_r4_4_audit_output\run_phase155_canonical_regression.ps1"
```

IMPORTANT: that command executes the large canonical regression and can be
heavy. R4-4 does NOT execute it.

For collection-only validation:

```powershell
python `
  ".\phase155_r4_4_audit_output\run_phase155_canonical_regression.py" `
  --collect-only
```

Changes
-------
- production code: unchanged
- existing tests: unchanged
- imports: unchanged
- test deletion/move/markers: none
- canonical regression: NOT run
- repository-wide pytest: NOT run

Next
----
Phase 155-R5 separates historical compatibility and performance-heavy
integration from the routine canonical path.
