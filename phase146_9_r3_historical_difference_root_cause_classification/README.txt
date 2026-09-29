Phase 146-9 Historical Difference Root-Cause Classification

Purpose
-------
Consolidate the 12 visible difference families identified after Phase 146-8
into internal root-cause families.

Inputs
------
- Current local code, including the locally applied Phase 146-7 change.
- phase146_8_historical_narrative_structural_diff.md

Production changes
------------------
None.

Existing test changes
---------------------
None.

Dynamic diagnostics
-------------------
For pi_6^3, the audit measures each NarrativeArgument:
- method-evidence exactness blocks
- exactness method components
- primary exactness component selection
- ordered contribution count
- supporting block roles

It also checks the renderer layering:
- base multi-argument renderer
- contribution-connected renderer
- direct-dependency argument construction
- post-render contribution insertion

Output
------
phase146_9_historical_difference_root_causes.md

The report proposes root-cause families and a dependency order. These are audit
results, not production changes.

Full suite
----------
Not run. Phase 146-9 is an audit only.

R1 repair
---------
The initial audit harness guessed the selector module name incorrectly.
Current develop imports
select_toda_group_proof_narrative_primary_exactness_component
from toda_group_proof_narrative_exactness_selection.
R1 uses that exact current module. Audit logic is otherwise unchanged.

R2 repair
---------
R1 called build_toda_group_proof_narrative_ordered_contributions without the
current required proof_chains argument. R2 now mirrors the production
contribution renderer exactly:
1. render base multi-argument Markdown
2. build proof chains
3. build ordered contributions with proof_chains and current_markdown
Audit classification logic is otherwise unchanged.

R3 repair
---------
R2 still used outdated call shapes for exactness components and primary
selection. R3 was rebuilt against the current develop production call path:
- build_toda_group_proof_narrative_exactness_method_components(evidence)
- extract_toda_group_proof_narrative_argument_relevant_groups(...)
- select_toda_group_proof_narrative_primary_exactness_component(
    relevant_groups, components
  )
R3 also preflights all directly called production API signatures before running
the audit, so another API mismatch fails with an explicit signature diagnostic.
