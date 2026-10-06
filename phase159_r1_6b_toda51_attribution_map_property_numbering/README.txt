Phase 159-R1-6b

Purpose
-------
Replace the temporary foundational-reference display for pi_3^2 with
Toda (5.1) literature attribution, and make equation numbers apply to the
whole map-property statement.

Toda (5.1)
----------
The catalog records:
- pi_i^1 = 0 for i > 1
- pi_i^n = 0 for i < n
- G_k = (G_k;2) = 0 for k < 0
- pi_n^n = <iota_n> ~= Z
- G_0 = <iota> ~= Z

For the current pi_3^2 proof, the existing low-dimensional E-isomorphism fact
is also attributed to the (5.1) diagonal identity data, following the current
Phase 159 contract.

Public numbering
----------------
Before:
  $H: ... \tag{1}$ は単射.

After:
  $H: ... \text{ は単射}. \tag{1}$

The property is therefore part of the numbered statement.

Non-goals
---------
- No full pytest.
- No unrelated inference-rule refactor.
- No Proposition 5.1 attribution for the low-dimensional premises.
- No change to the pi_3^2 target reference exclusion.
