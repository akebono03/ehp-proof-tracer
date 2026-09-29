Phase 144-6-R5-43-R2 recursive repr repair

Observed failure:
pytest entered repeated dataclass __repr__ calls and was interrupted.

Root cause repaired:
R5-42 production contribution grouping used repr(proof_step.conclusion).
Some conclusion dataclasses contain recursive proof structures, so repr is not
a safe production semantic key.

Minimal repair:
_group_key now uses:
- conclusion statement type
- normalized generic rendered statement
- provider membership keys

No renderer route is switched.
No pi_6^3-specific branch is added.
No public CLI/Web behavior is changed.
No full suite is run.

Targeted verification:
1. R5-43-R2 safety tests
2. R5-42 production foundation tests
3. R5-43 renderer connection tests
