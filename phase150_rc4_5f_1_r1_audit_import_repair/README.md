# Phase 150 / RC4-5F-1-R1

Audit-harness-only repair.

The original RC4-5F-1 audit incorrectly imported `Relation` and
`RelationType` from a nonexistent top-level `relation` module.

Current `develop` defines both in `proof.py`, and current production modules
import them with:

```python
from proof import (
  Relation,
  RelationType,
)
```

This package changes only the RC4-5F-1 audit script to use that canonical
import. No production file and no existing test is changed.

Repository-wide tests remain deferred until the end of Phase 150.
