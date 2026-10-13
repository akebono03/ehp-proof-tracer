Phase 165 R52-R5 — fresh registered typed goal search from n,k.

Changes:
- New phase165_r52_r5_auto_search.py: typed target discovery + canonical recursive search.
- Replace entire phase165_r52_r4_flask_bridge.py: automatic search when no explicit Goal.
- Update web_app.create_app().index(): ordinary Group query invokes new proof progress.
- New test_phase165_r52_r5_auto_search.py.

Limitations:
- No old proof replay for new proof results.
- SOURCE_ARCHIVE strings are not accepted as typed proofs.
- A group without a typed structural candidate yields an actual failed search and an open Goal.
- Completeness is not claimed unless the canonical prover establishes one unique target.
- n>=2 and k>=0 is the present public R52 query domain.
- Flask restart is needed for updated code.
- Whole pytest suite is reserved until Phase 165 closes.
