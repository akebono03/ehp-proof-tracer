Phase 162: pi_5^3 reconstructed ProofStep -> existing public Narrative Renderer

Unzip at repository root; run:
powershell -ExecutionPolicy Bypass -File .\phase162_pi5_3_renderer_audit\run_phase162_pi5_3_renderer_audit.ps1

Added files (no production edits):
- phase162_pi5_3_renderer_audit/phase162_pi5_3_renderer_audit.py
  - Pi53RendererAuditResult (new dataclass)
  - render_phase162_pi5_3_reconstructed_proof (new function)
- phase162_pi5_3_renderer_audit/test_phase162_pi5_3_renderer_audit.py
  - _inputs (new test helper)
  - test_renderer_receives_reconstructed_pi5_3_root
  - test_existing_renderer_returns_nonempty_markdown
- phase162_pi5_3_renderer_audit/run_phase162_pi5_3_renderer_audit.ps1

Scope: audit only. No custom proof prose, mathematical rules, or production
renderer changes. Existing Phase 161/162 reconstruction and existing presentation
pipeline are reused. The resulting Markdown is emitted and saved to:
phase162_pi5_3_renderer_audit/pi5_3_reconstructed_narrative.md
Review the actual narrative before any renderer edits. Full pytest at phase end only.
