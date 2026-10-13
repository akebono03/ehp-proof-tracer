# Phase 165 R50 final exactness duplicate cleanup

This patch updates only the existing reference-consumer function in the shared contribution Renderer. A reference-linked exactness subwindow repeated after the complete EHP sequence is removed, while its [R] marker is preserved at the original proof introduction.

It does not change the Reference Renderer, statement registry, proof rules, or R49 helper. Backups are created before applying, and only targeted pytest runs.
