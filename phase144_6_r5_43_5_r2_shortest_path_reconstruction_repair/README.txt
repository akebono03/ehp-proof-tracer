Phase 144-6-R5-43-5-R2 shortest-path reconstruction repair

Production changes: none.

Repair:
The audit shortest-path reconstruction already accumulated the suffix in
source-to-target order while walking predecessor links backward. The original
code reversed that completed sequence again, producing target-to-source paths.

R2 removes only that extra reversal.

The audit scope, segment selection, shortest-distance calculation, visibility
classification, and production code are unchanged.
