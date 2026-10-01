# Phase 154-R5 Representative Re-audit Fix1

Production changes: none.

Fix:
- Reference-section headings are never classified as proof-body marker defects.
- Section splitting is line-based on exact `## 使用する結果` / `## 証明` headings.

## Summary

residual_linkage_candidates: 0
incomplete_reference_marker_lines: 0

## pi6_3

reference_count: 0
linked_reference_markers: 0
neutral_reference_markers: 0
accepted_root_or_ambiguous_neutral_markers: 0
residual_linkage_candidates: 0
incomplete_reference_marker_lines: 0

## pi10_4

reference_count: 0
linked_reference_markers: 0
neutral_reference_markers: 0
accepted_root_or_ambiguous_neutral_markers: 0
residual_linkage_candidates: 0
incomplete_reference_marker_lines: 0

## pi11_4

reference_count: 2
linked_reference_markers: 1
neutral_reference_markers: 1
accepted_root_or_ambiguous_neutral_markers: 1
residual_linkage_candidates: 0
incomplete_reference_marker_lines: 0

Linked markers: [R2]

Accepted neutral markers: [R1]

## pi12_5

reference_count: 0
linked_reference_markers: 0
neutral_reference_markers: 0
accepted_root_or_ambiguous_neutral_markers: 0
residual_linkage_candidates: 0
incomplete_reference_marker_lines: 0

## pi16_9

reference_count: 0
linked_reference_markers: 0
neutral_reference_markers: 0
accepted_root_or_ambiguous_neutral_markers: 0
residual_linkage_candidates: 0
incomplete_reference_marker_lines: 0

## Completion rule

- R5 is complete if `residual_linkage_candidates = 0` and `incomplete_reference_marker_lines = 0`.
- Neutral `[R#]を用いる。` remains acceptable when no unique visible non-root consumer exists.
