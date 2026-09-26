# Phase 143-51 audit

This package does not modify repository source files.

It audits the four representative Narrative targets and reports every
visible fallback that reaches the final Narrative through either:

- `proof_step.inference_rule.name`
- the raw Python statement class name

For each fallback it prints:

- Narrative block role
- statement class
- inference rule name
- premise count
- a small structural shape summary

Use the output to decide whether the fallback should be rendered from
mathematical statement semantics or suppressed as provenance-only
material. No target-specific display rule is introduced by this audit.
