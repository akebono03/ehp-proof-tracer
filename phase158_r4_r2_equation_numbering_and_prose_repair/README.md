# Phase 158-R4-R2 — Equation numbering and prose repair

This repair is limited to defects confirmed by the Phase 158-R4 audit.

Production changes:

- skip equation numbering for render-equivalent transitions;
- skip reflexive equality transition sources;
- remove public equation tags that are not referenced;
- compact remaining public equation numbers;
- remove ambiguous `この群構造と` prose.

Focused tests and a 112-group R4 re-audit are run.
The full pytest suite is intentionally deferred until Phase 158 closure.
