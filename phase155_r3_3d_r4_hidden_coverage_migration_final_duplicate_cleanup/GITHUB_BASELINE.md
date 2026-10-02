# GitHub baseline — Phase 155-R3-3D-r4

Repository: `akebono03/ehp-proof-tracer`
Branch: `main`
Observed public baseline commit: `8301520a7434f3836b1dbc7e8fa08a60c024225a`

Before implementation, current GitHub test material and test-collection
guidance were re-inspected, including:
- `tests/test_phase109_14_decorated_sigma_finite_cyclic_fallback.py`,
- `tests/test_phase143_61b_direct_premise_narrative.py`,
- `tests/conftest.py`,
- project README collection/backup guidance.

The public baseline still contains historical same-name test definitions and
older presentation expectations. The user's current local Phase 155 audit
outputs are therefore authoritative for the exact R3-3D-r4 targets.

R3-3D-r2/r3 established:
- runtime binding uses the final same-name definition in all 8 groups;
- 6 groups have hidden unique assertions;
- 2 groups are cleanup-ready;
- both unresolved pairs are safe `delete older / keep newer` candidates;
- manual semantic review required: 0.

This repair changes tests only, preserves hidden coverage by renaming rather
than rewriting the 6 shadowed test bodies, and does not run repository-wide
pytest.
