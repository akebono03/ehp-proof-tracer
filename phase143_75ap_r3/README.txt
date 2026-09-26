Phase 143-75AP-R3

Repairs the literal-backslash-n corruption from R1/R2 without invoking
either old patcher. Missing imports are inserted using chr(10), so the
patcher cannot confuse source newlines with escaped backslash-n text.

Then the same six final semantic renderer branches are inserted.

Production file:
- toda_proof_narrative_renderer.py

No mathematical scope change.
Focused tests only.
No full pytest.
