Phase 159 pi_4^3 repair2g fix1

Purpose
=======
Repair the repair2g apply-script failure against the accumulated local Phase159 state.
The mathematical/production policy is unchanged:
- (5.1) and Proposition 5.1 are fixed literature References.
- EHP exactness remains proof-internal and is not a Reference.
- Im Delta / ker E semantic closure is recovered by generic map-property classification.

Fix1 changes only the packaging/application robustness relative to repair2g:
- patch bootstrap ProofSteps by function + conclusion marker, not an exact whole-block string;
- tolerate already-present inference_rule metadata in the accumulated local state;
- tolerate the current repair1 generic ImDelta statement class in focused tests;
- remain safe after the partial repair2g application (dependency/boundary may already be changed).

Repository-wide pytest is NOT run.
