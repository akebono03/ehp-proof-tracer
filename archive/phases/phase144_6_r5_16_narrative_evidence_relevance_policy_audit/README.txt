Phase 144-6-R5-16
===================

Narrative evidence relevance policy audit.

Audit only. No production files are modified.

Purpose
-------
Phase 15U established that every edge-local Narrative-visible evidence edge can
receive a typed EvidenceContribution.

Phase 16 asks a different question:

  Which typed evidence should be retained as Narrative-relevant evidence?

Candidate layers
----------------
L0 = Argument conclusion
L1 = typed direct premises of L0
L2 = typed direct premises of L1

The audit compares:
- current R4-visible steps,
- L1,
- L1 + L2,
- recursive typed evidence closure.

It also inventories R4-visible evidence not explained by L1+L2 and evidence
gained only through recursive typed closure.

Important boundary
------------------
This Phase does NOT:
- change R4 visibility,
- change Narrative depth,
- change renderer,
- change CLI/Web,
- change EvidenceContribution vocabulary,
- change aggregate semantic metadata,
- modify project documents.

No full pytest is run.

Interpretation
--------------
If L1+L2 explains nearly all current R4-visible evidence, a two-level evidence
boundary may be sufficient.

If recursive typed closure adds substantial useful evidence, inspect its
semantic function before adopting recursion. Recursive closure must not be
accepted merely because it reaches more proof nodes.

The next subphase should be chosen from the actual audit distribution rather
than preselecting a production relevance rule.
