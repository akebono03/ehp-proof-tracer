# Phase 150 RC4-7D-2 Web Narrative Route Integration Audit

Audit-only package. No production files, tests, or documentation are changed.

## Current-code finding

The current Web flow is:

```text
web_app
  -> build_standard_web_group_proof_view
  -> render_toda_group_proof_narrative_markdown
```

The public Narrative renderer currently dispatches as follows:

```text
pi_15^8
  -> dedicated Phase 134-24 renderer

pi_6^3
  -> generic multi-Argument contribution renderer

pi_8^5
  -> dedicated Phase 134-9 renderer

all remaining groups
  -> legacy _append_narrative_for_step recursive renderer
```

Therefore `pi_10^4`, `pi_12^5`, and `pi_16^9` do not currently consume the
generic reason-prose route used by the RC4-7D focused tests.

## Audit targets

- `pi_6^3`: generic-route control
- `pi_8^5`: dedicated-route control
- `pi_10^4`: RC4 target
- `pi_12^5`: RC4 target
- `pi_15^8`: dedicated-route control
- `pi_16^9`: RC4 target

## Audit output

For each group:

- public renderer route classification
- generic contribution reason visibility
- public Narrative reason visibility
- Web Narrative reason visibility
- public-vs-Web agreement
- generic-vs-public agreement
- first 32 lines of both public and generic output

Expected decisive result:

```text
RC4_TARGETS_ON_LEGACY_RECURSIVE_FALLBACK=3/3
AUDIT_DECISION=PUBLIC_RENDERER_DISPATCH_BYPASSES_GENERIC_REASON_ROUTE
```

## Completion criterion

The audit is complete when it establishes whether the actual Web Narrative
fails to show RC4-7D prose because the public renderer dispatch bypasses the
generic contribution/reason route.

No production repair is included. The next repair, if confirmed, should be a
minimal public-renderer integration change rather than a Web-template change.

Repository-wide pytest is intentionally not run.
