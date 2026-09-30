# Phase 150 / RC4-5F-1-R2

Audit-harness-only repair for the current narrative block API.

Current `develop` defines:

```python
@dataclass(frozen=True)
class TodaGroupProofNarrativeBlock:
  role: TodaGroupProofNarrativeMathematicalBlockRole
  steps: tuple[ProofStep, ...]
```

The RC4-5F-1 audit incorrectly accessed `block.proof_steps`. This package
changes that access to the canonical `block.steps`.

No production file and no existing test is changed.

Repository-wide tests remain deferred until the end of Phase 150.
