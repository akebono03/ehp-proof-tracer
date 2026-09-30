# Phase 150 RC4-7D-3 Test Import Repair R1

## Failure diagnosis

The RC4-7D-3 production repair was successfully applied and passed syntax
preflight. Test collection then failed because the new focused test imported
`build_toda_group_result_proof_replay` from a nonexistent module:

```python
from toda_group_proof_replay import (
  build_toda_group_result_proof_replay,
)
```

The current repository and existing tests use:

```python
from toda_group_result_proof_replay import (
  build_toda_group_result_proof_replay,
)
```

## Changed target

Test only:

- `tests/test_phase150_rc4_7d_3_public_narrative_generic_route.py`
  - import section only

Production files are not reapplied or changed by this package.

## Full changed import section

```python
from toda_group_proof_narrative_renderer import (
  render_toda_group_proof_narrative_markdown,
)
from toda_group_proof_presentation import (
  build_toda_group_proof_presentation,
)
from toda_group_result_proof_replay import (
  build_toda_group_result_proof_replay,
)
from toda_report import (
  build_standard_toda_report,
)
from web_group_proof import (
  build_standard_web_group_proof_view,
)
```

## Runner

The runner does not reapply the production patch. It repairs the test import,
runs focused and related regressions, then prints actual Web Narrative
snapshots for `pi_10^4`, `pi_12^5`, and `pi_16^9`.

Repository-wide pytest remains reserved for the end of Phase 150.
