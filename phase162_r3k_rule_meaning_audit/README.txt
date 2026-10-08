Phase 162 R3-K — InferenceRule meaning/description inventory

Purpose:
- Inspect only R3-J's 45 replay-verified, still-unexplained inference steps.
- Group by exact rule name, premise types, conclusion type.
- Produce structured drafts containing original ProofStep facts and recorded rule descriptions.
- Do NOT treat descriptions as verified mathematical reasons.
- No existing implementation, public Renderer, proof rule or existing test is changed.

Install:
  cd C:\Users\user\Dropbox\Python\fitz\ehp_proof
  Expand-Archive -Path "$HOME\Downloads\phase162_r3k_rule_meaning_audit.zip" -DestinationPath "." -Force
  powershell -ExecutionPolicy Bypass -File ".\phase162_r3k_rule_meaning_audit\run_phase162_r3k.ps1"

Outputs (relative to repository root):
- phase162_r3k_output/rule_meaning_entries.json
- phase162_r3k_output/rule_meaning_groups.json
- phase162_r3k_output/rule_meaning_audit.json
- phase162_r3k_output/rule_explanation_drafts.md

Focused pytest only. Full suite reserved for Phase 162 closure.
Completion: 45 steps accounted for without falsely certifying a rule description.
Next boundary: review actual rule families, add mathematical reason renderers only where a typed general implication can be justified.
