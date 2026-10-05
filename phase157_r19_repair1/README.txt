Phase157-R19 repair1

Repairs two defects in the first R19 package.

1. The helper insertion guard tested the first line of a triple-quoted
   string. Because that line was empty, it incorrectly concluded that
   the helpers were already present. The renderer call sites were added,
   but the helper functions were not, causing NameError.

2. The new R19 test used report.group_result and depth=2. Existing
   repository tests use:
     report.candidates[0].source_candidate.group_result
     max_depth=2

This repair applies on top of the first R19 patch.
It does not run repository-wide pytest.
Focused tests use -x to stop immediately on the first failure.
