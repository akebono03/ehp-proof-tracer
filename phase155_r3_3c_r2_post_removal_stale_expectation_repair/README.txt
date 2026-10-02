Phase 155-R3-3C-r2 — post-removal stale expectation repair

This subphase repairs exactly the three stale expectations exposed after the
R3-3C-r1 duplicate removal.

Changes:
- Phase 132 pi16_9 web Narrative test now checks the root source theorem via
  `view.theorem == "Toda Proposition 5.15"` instead of requiring the root
  theorem to appear in a rendered-line prefix.
- Two Phase 143 ordering tests now use the current Phase 154 ASCII connector
  `以上より, ` instead of `以上より、`.

No imports change.
No production code changes.
The 161 duplicate-test removals and 5 whole-file removals remain in place.

The prior post-removal run already recorded 858 passing affected/importer
tests and only these three failures. Therefore R3-3C-r2 re-runs only the three
repaired tests after first auditing the current runtime contract.

Repository-wide pytest is not run here.
