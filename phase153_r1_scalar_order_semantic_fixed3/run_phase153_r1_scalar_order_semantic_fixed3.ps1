$ErrorActionPreference = "Stop"

Copy-Item `
  ".\phase153_r1_scalar_order_semantic_fixed3\tests\test_phase153_scalar_order_narrative_classification.py" `
  ".\tests\test_phase153_scalar_order_narrative_classification.py" `
  -Force

pytest `
  ".\tests\test_phase153_scalar_order_narrative_classification.py" `
  ".\tests\test_phase134_9_group_proof_narrative_classifier.py"
