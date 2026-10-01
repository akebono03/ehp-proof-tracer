$ErrorActionPreference = "Stop"

Copy-Item `
  ".\phase153_r1_scalar_order_semantic_fixed2\tests\test_phase153_scalar_order_narrative_classification.py" `
  ".\tests\test_phase153_scalar_order_narrative_classification.py" `
  -Force

python ".\phase153_r1_scalar_order_semantic_fixed2\apply_phase153_r1_scalar_order_semantic.py"

pytest `
  ".\tests\test_phase153_scalar_order_narrative_classification.py" `
  ".\tests\test_phase134_9_group_proof_narrative_classifier.py"
