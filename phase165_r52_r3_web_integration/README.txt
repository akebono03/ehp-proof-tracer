Phase 165 R52-R3: partial proof result to existing common WebGroupProofView.
Run from repository root using run.ps1.
This is an explicit Web adapter entry, not a replacement for legacy report selection.
Existing WebGroupProofView and Markdown line parser are reused. No dedicated per-group rendering.
The existing Flask POST UI is not rewired in R52-R3; it can call build_web_partial_group_proof_view(result) in the next routing step.
No full pytest. No mathematical theorem additions.
