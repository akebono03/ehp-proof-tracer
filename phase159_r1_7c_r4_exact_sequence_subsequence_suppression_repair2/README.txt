Phase 159 R1-7c R4 exact-sequence subsequence suppression repair2

Finding from audit2
-------------------
pi_3^2:
- at the early merge stage only the shorter four-term sequence exists;
- the longer five-term sequence is introduced later in the public pipeline.

Therefore suppression inside the early merge helper is the wrong layer.

pi_6^3:
- the shorter exactness sequence occurs before a longer sequence;
- that existing earlier exactness statement must remain.

Repair
------
1. Restore merge_toda_group_proof_narrative_adjacent_ehp_exactness_windows()
   to the current GitHub behavior.
2. Add a late presentation helper:
   suppress_toda_group_proof_narrative_late_exact_sequence_prefix_restatements()
3. Invoke it near the end of the contribution pipeline.
4. Suppress only a shorter sequence that is a strict prefix of a LONGER
   sequence already seen earlier in the rendered proof.

No target-specific condition is introduced.
No eta_2 wording changes.
No reference changes.
No generator changes.
No full pytest.
