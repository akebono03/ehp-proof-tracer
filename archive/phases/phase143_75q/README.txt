Phase 143-75Q
=============

Purpose
-------
Re-run the Phase 143-75A full production rule-name fallback audit after
Phase 143-75P.

Production changes
------------------
None.

Scan
----
n = 2..15
k = 0..7
max_depth = 7

Production path
---------------
build_standard_toda_report
-> build_toda_group_result_proof_replay
-> build_toda_group_proof_presentation
-> _render_group_proof_narrative_fact

Fallback definition
-------------------
A presentation node is counted as a rule-name fallback when:

_render_group_proof_narrative_fact(proof_step)
== proof_step.inference_rule.name

Expected checkpoint
-------------------
Phase 143-75N:
465 fallback occurrences across 33 statement types.

Phase 143-75P removed:
55 TodaProp44SuspensionInjectiveStatement occurrences.

Expected Phase 143-75Q:
410 fallback occurrences across 32 statement types.

The measured result is authoritative.

Expected unchanged scan size
----------------------------
112 groups
11033 presentation nodes

No tests
--------
This is an audit-only subphase.
No production file is changed.
No focused pytest or full pytest is run.

Next
----
Use the measured remaining inventory to select the next semantic family.
Do not infer the next implementation solely from the previous ranking.
