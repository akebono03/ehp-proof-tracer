Phase 143-75AE implementation R2

R1 failed before modifying production source because its fixed import anchor
matched GitHub main but not the locally accumulated Phase 143 import block.

R2 locates the current toda_rules import block structurally, preserves all
existing imports, adds TodaSuspensionZeroStatement, and adds the same generic
zero-map renderer.

Only focused tests are run. Full regression remains deferred.
