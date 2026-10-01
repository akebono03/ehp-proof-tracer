# Phase153-R1 Fixed11

This package fixes the execution packaging error in fixed4-fixed10.

Those packages contained a revised test file but their runner did not copy it
into the repository `tests/` directory. As a result, pytest continued to run
the pre-existing Phase153 test.

Fixed11:

1. Copies the bundled corrected test to:
   `tests/test_phase153_scalar_order_narrative_classification.py`
2. Runs the existing Phase134-9 classifier baseline.
3. Runs the Phase153-R1 focused regression test.

Production code is not changed.
