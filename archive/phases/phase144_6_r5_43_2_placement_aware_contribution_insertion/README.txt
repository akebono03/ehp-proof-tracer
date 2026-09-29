Phase 144-6-R5-43-2 placement-aware contribution insertion

Production change:
- toda_group_proof_narrative_contribution_renderer.py only.

Behavior:
- AT_PROVIDER_ANCHOR: insert after the last visible rendered step in the
  supporting provider block; fall back to the Argument conclusion only if
  no visible provider anchor exists.
- BEFORE_DEPENDENT_CONTRIBUTION: insert at the next resolved contribution
  position in topological order.
- BEFORE_ARGUMENT_CONCLUSION: insert immediately before the owning Argument
  conclusion.
- Contributions sharing one insertion index preserve R5-42 ordering.

Not changed:
- R5-42 contribution selection/order/ownership.
- mathematical prose rules.
- public renderer route.
- full test suite.
