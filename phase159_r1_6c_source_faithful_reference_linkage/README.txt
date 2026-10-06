Phase 159-R1-6c

Purpose
-------
Refine the public Narrative contract around Toda (5.1) and the low-dimensional
EHP proof chain.

Changes
-------
1. Render Toda (5.1) as source-faithful general statements instead of three
   specialized facts.
2. Move the low-dimensional suspension isomorphism use into the proof body.
3. Add "完全性より," to conclusions that directly use an exactness premise.
4. When the prose already introduces "次の完全列", omit the redundant
   "は完全である." after the displayed sequence.
5. Render statement numbers as prose:
     ... は単射. (1)
   rather than MathJax \tag or \text.

Scope
-----
The implementation is semantic:
- locator "(5.1)"
- TodaSuspensionIsomorphismStatement
- TodaSuspensionInjectiveStatement
- TodaProp42ExactnessStatement

It does not key off the pi_3^2 target string.

Full pytest
-----------
Not run. Full-suite execution remains reserved for the end of Phase 159.
