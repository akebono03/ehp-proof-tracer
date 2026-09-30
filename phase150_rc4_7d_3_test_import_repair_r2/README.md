# Phase 150 RC4-7D-3 Test Import Repair R2

Production is not reapplied.

The focused test now uses the same canonical modules as current repository
tests:

```python
from toda_calculation_facade import (
  build_standard_toda_report,
)
from toda_group_proof_narrative_renderer import (
  render_toda_group_proof_narrative_markdown,
)
from toda_group_proof_presentation import (
  build_toda_group_proof_presentation,
)
from toda_group_result_proof_replay import (
  build_toda_group_result_proof_replay,
)
from web_group_proof import (
  build_standard_web_group_proof_view,
)
```

The `_presentation()` helper already matches the existing repository pattern:
`build_standard_toda_report` -> selected `group_result` ->
`build_toda_group_result_proof_replay` ->
`build_toda_group_proof_presentation`.

Only the focused test import section is changed. The production route repair
from RC4-7D-3 R1 remains untouched.

The runner performs module-import preflight before pytest, then focused and
related regressions, followed by actual Web Narrative snapshots.

Repository-wide pytest remains reserved for the end of Phase 150.
