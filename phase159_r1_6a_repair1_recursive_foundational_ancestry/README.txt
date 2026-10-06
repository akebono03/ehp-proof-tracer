Phase 159-R1-6a repair1

Cause 1:
The original foundational collector inspected only presentation.nodes.
At proof depth 2, pi_3^3 is visible, but pi_2^1=0 and the E isomorphism are
deeper premises. Their identities therefore existed but were not collected.

Fix:
Traverse ProofStep.premises recursively from presentation.root_step.
Use ProofStep identity for cycle/duplicate protection.

Cause 2:
The injection helper searched for a separator beginning with a newline even
though content_start points directly at `---`.

Fix:
Search for `---\n\n## 証明` and explicitly restore the blank line before it.

Production changes:
- toda_group_proof_narrative_renderer.py only

Test changes:
none

Full pytest:
not run
