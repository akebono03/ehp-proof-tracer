# Phase 165 R6-2 R4-4 Stage 3

This patch adds two generic exactness-to-kernel/image inference rules to `map_property_rules.py`. It requires Stage 2 to be installed. The new rules use explicitly typed zero-image and whole-kernel premises; they never infer zero or whole structures from unverified computations. Rule factory discovery remains automatic. The run script performs only targeted tests, not the full suite. The installer is idempotent and writes a backup.
