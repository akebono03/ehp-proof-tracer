# Phase 144-6 R25-R5

R25-R4 confirmed that `main.py` and
`toda_group_proof_narrative_argument_multi_renderer.py` exactly match Git HEAD.

The focused test then reproduced the known depth=2 regression:

`test_phase144_6_cli_pi6_3_narrative_uses_generic_route`

R25-R5 treats that failure as diagnostic evidence instead of aborting.

The owner diagnosis also follows the actual production ordering:

1. render raw multi-argument Narrative
2. build ordered contributions using that raw Markdown
3. insert contributions
4. compare with the public Narrative

For both depth=2 and full/default presentations it reports:

- Argument roles and conclusion ProofStep identities
- definition Argument existence
- definition block ProofStep ownership
- contribution ownership
- raw / post-contribution / public visibility
- `pi_5^3` ProofStep ownership
- contribution role, placement, provider keys
- premise and parent edges
- final public Narrative

No production repair is applied.
The full test suite is not run.
Stop after diagnosis.
