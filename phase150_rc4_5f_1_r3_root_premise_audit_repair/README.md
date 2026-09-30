# Phase 150 / RC4-5F-1-R3

Read-only repair of the final group-structure reason-chain audit.

The earlier audit made three incorrect assumptions:

1. It searched only `GROUP_STRUCTURE` blocks for the final conclusion, while
   the final known-group conclusion is `presentation.root_step` and therefore
   belongs to the target path.
2. It used the wrong membership statement family. The existing Phase 65
   contract uses `HomotopyGroupMembershipStatement`.
3. It inferred order availability indirectly instead of inspecting the root
   step's typed direct premises.

R3 audits `presentation.root_step` directly and verifies the existing Phase 65
provenance contract.

The intended distinction is important: the existing final inference rule
directly consumes the structural evidence, exact order-four fact, and
membership fact. It does not create a separate proof step saying that the
middle group has order four. Therefore a future prose reason may decompose the
existing typed premises, but it must not invent a mathematical proof step.

No production file and no existing test is changed. Repository-wide tests
remain deferred until the end of Phase 150.
