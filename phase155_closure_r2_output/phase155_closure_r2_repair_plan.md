# Phase 155 Closure-R2 repair plan

1. SAFE_STALE (38)
   - Repair historical presentation/rendering/reference expectations only.
   - Use focused tests; do not run repository-wide pytest.

2. HISTORICAL_HEAVY (36)
   - Review redundancy, fixed-count assumptions, internal renderer coupling,
     and measured runtime.
   - Do not automatically update counts or old snapshots.
   - Prefer delete/archive/split/lightweight replacement when justified.

3. CONTRACT_SENSITIVE (24)
   - Diagnose Reference ownership/provenance/source metadata/current
     aggregate-result contract.
   - No automatic stale repair.

4. Closure regression
   - Introduce sharded/checkpointed regression before final closure.
   - Do not return to one 40-minute monolithic retry loop.
