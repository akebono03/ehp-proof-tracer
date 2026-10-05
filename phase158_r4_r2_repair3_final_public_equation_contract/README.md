# Phase 158-R4-R2 repair3 — Final public equation contract

This repair fixes the boundary discovered by the `pi_8^5` diagnostic.

`pi_8^5` uses proof-item numbering such as `(3), (4) より,`.
Those references are not equation-number references and must not be compared
with `\tag{N}`.

The repair:

- restores the contribution renderer to its pre-R4-R2 form;
- performs equation-number cleanup only at the final Phase 158 public
  Narrative normalization layer shared by all rendering routes;
- recognizes only standalone canonical equation connectors;
- removes unreferenced and duplicate equation tags;
- compacts retained equation tags;
- leaves proof-item numbering untouched;
- updates the Phase 158 R4 focused test to use the same distinction.

No future-Phase behavior is added.
The full pytest suite is deferred until Phase 158 closure.
