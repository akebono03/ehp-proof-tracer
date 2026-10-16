# Proposition 5.1 range R2: candidate skip

This focused patch corrects the candidate producers for Toda Proposition 5.1 when the dimension is outside the adopted range (`n >= 4`). The predicate in `specialize_eta_group_relation` continues to raise `ValueError` on invalid direct calls, while the discovery paths return no candidate for `n=3`.

Run `run.ps1` from the repository root. A backup is written before the first mutation. Only the targeted tests run. The installer checks AST structure before making any changes and is idempotent.

No general applicability engine or EHP proof machinery is added by this change.
