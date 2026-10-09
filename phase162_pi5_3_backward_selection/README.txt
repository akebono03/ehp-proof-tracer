Phase 162 pi_5^3 backward selection repair 2

Changes only _canonical_goals() in the Phase 162 module and adds a focused test.
The existing eta-family definition represents eta_4 with name "η_4", while
the existing transport inference rule produces a generator named "η₄".
These are distinct HomotopyElement objects under exact dataclass equality.
Repair only the local goal-construction spelling, preserving index, dimension,
source, target, inference rules, proof-step provenance, and strict equality.
No general normalization, Renderer changes, or whole-suite tests.
