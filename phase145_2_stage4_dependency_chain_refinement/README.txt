Phase 145-2 Stage 4 - Dependency Chain Refinement

Purpose
-------
Refine only the 41 Stage 3 DEPENDENCY_CHAIN_REVIEW artifacts.

The Stage 3 token scan intentionally over-counted references, including an
artifact referring to its own package/output name. Stage 4 removes those self
references and keeps only references to a different known root Phase artifact.

No repository file is moved, deleted, or modified.

Baseline
--------
develop:
4737d71e339b704b787668f493201e4aebeeb991

Input
-----
phase145_2_stage3_historical_executability_classification/output/
phase145_2_stage3_historical_executability.csv

Classifications
---------------
TRUE_CROSS_ARTIFACT_DEPENDENCY
    At least one different, currently tracked root Phase artifact is referenced.

SELF_REFERENCE_ONLY_MOVE_CANDIDATE
    Stage 3 dependency evidence reduces to self-reference only. This artifact
    can return to the archive-move candidate population from the dependency
    perspective.

UNRESOLVED_PHASE_TOKEN_REVIEW
    A Phase-looking token remains but does not match a currently tracked root
    Phase artifact. Review before movement.

Boundary
--------
Stage 4 does not change historical runners or decide the path-update policy for
EXECUTABILITY_REQUIRED artifacts. It only corrects the dependency population.

No pytest is run. The repository-wide suite remains reserved for the end of
Phase 145-2.
