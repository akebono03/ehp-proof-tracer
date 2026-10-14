# Phase 165 R27-R23

This targeted patch moves the CLI group query (`n k`) and `group-proof` away from the legacy `build_standard_toda_report` implementation, toward the registered common Backward Search. It preserves command-line option parsing and reports partial/failed progress rather than silently returning a proof. The three `--mode` values are accepted; currently they share the common partial-proof narrative renderer. A non-complete proof exits with status 1.

Run `run.ps1` from the extracted directory. Only R27-R23 targeted pytest tests are run; full pytest is deferred until the end of Phase 165.
