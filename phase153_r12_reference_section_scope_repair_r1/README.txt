Phase 153-R12 Reference-section Scope Repair R1
================================================

Cause
-----
The first R12 test defined the Reference section as everything before
"## 証明". That range also included the theorem/provenance line, for example:

Toda Proposition 5.15を用いる。

Therefore the test falsely reported that Proposition 5.15 remained as an
external Reference.

Repair
------
Production changes: none.

The R12 test and audit now inspect only the actual Reference section:
from "## 使用する結果" to "## 証明".

This preserves the valid provenance/theorem line while verifying that the same
root LiteratureReference is not listed as an external [Rk] Reference.

Full pytest remains deferred until the end of Phase 153.
Punctuation normalization remains deferred.
