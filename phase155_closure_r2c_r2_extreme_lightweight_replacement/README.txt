Phase 155 Closure-R2C-R2 — extreme 3 lightweight replacements

Targets
-------
- 508.30s Phase97 goal-source provenance test
- 281.49s Phase95 aggregate registration-order test
- 276.88s Phase97 multiple aggregate goal-source order test

Replacement strategy
--------------------
Phase95:
- create two lightweight group candidates;
- register their source entries in a real ProofRepository;
- run the real goal discovery function with only extraction monkeypatched;
- verify repository registration order is preserved;
- run the real build_toda_calculation_result orchestration with only heavy
  normalization/discovery inputs replaced;
- verify candidate provenance/order remains intact.

Phase97:
- create lightweight TodaCalculationCandidate objects with real
  TodaCalculationGoalSource instances;
- monkeypatch only build_toda_calculation_result;
- run the real report/presentation API;
- verify goal-source identity/order reaches presentation.source.

No production code changes.
No repository-wide pytest.
