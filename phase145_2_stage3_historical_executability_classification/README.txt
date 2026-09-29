Phase 145-2 Stage 3 - Historical Executability Classification

Purpose
-------
Classify only the 91 artifacts that Stage 2 identified as having concrete
archive-sensitive path assumptions.

This stage performs NO move, deletion, production change, test change, or
documentation change.

Baseline
--------
develop:
4737d71e339b704b787668f493201e4aebeeb991

Input
-----
phase145_2_stage2_relative_path_risk_refinement/output/
phase145_2_stage2_relative_path_refinement.csv

Classifications
---------------
EXECUTABILITY_REQUIRED
    Historical package contains an apply/installer/payload path, or is a
    finalization/full-suite gate. Preserve its ability to execute until an
    explicit retirement decision is made.

DEPENDENCY_CHAIN_REVIEW
    Package explicitly refers to another Phase artifact. Its relocation must
    be considered together with that dependency chain.

HISTORICAL_ONLY
    Package is retained as historical audit/verification material. No evidence
    in this mechanical classification requires preserving the old root-level
    execution contract.

Boundary
--------
Stage 3 does not rewrite historical runners. It only narrows the set requiring
special handling before archive movement.

No pytest is run here. Repository-wide pytest remains reserved for the end of
Phase 145-2.
