# Phase 168 R3-41P5 — Name-independent Renderer suppression

The package makes one **minimal modification** inside the existing
`render_model_backed_narrative_markdown()` function in
`phase168_r3_5_model_renderer.py`. It replaces a literal normalization-rule
name check with checks of existing, typed ProofStep conclusions and premises.

No inference rule is called from the Renderer. No new Adapter, Model,
mathematical theorem, or bibliography mechanism is introduced.

## Windows PowerShell

From the repository root:

```powershell
Expand-Archive `
  -Path "$HOME\Downloads\phase168_r3_41p5_rule_name_independent.zip" `
  -DestinationPath "." `
  -Force

powershell `
  -ExecutionPolicy Bypass `
  -File ".\phase168_r3_41p5_rule_name_independent\run.ps1"
```

## Safety / review

The patcher requires the exact R3-41P4 SHA-256 of the Renderer file.
Unexpected source differences abort the update. On successful patch it saves
an original backup and complete post-change function and file into `output/`.
Test failure triggers restoration of the original Renderer.

To restore manually:

```powershell
python -B -m phase168_r3_41p5_rule_name_independent.restore
```

The runner runs only the focused tests (including three group fulltext captures
from R3-41P4), and **does not run the full pytest suite**.
