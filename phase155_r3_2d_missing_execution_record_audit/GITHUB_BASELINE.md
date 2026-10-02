# GitHub baseline — Phase 155-R3-2D

Repository: `akebono03/ehp-proof-tracer`
Branch: `main`
Observed baseline commit: `8301520a7434f3836b1dbc7e8fa08a60c024225a`

Checked before R3-2D:

- `tests/conftest.py`
- repository test usage of `pytest.mark.parametrize`

`tests/conftest.py` only adds the tests directory to `sys.path`; it does not
normalize or rewrite pytest node IDs.

The current repository contains many parameterized tests, including Phase
143, Phase 148, Phase 149, Phase 150, and Web tests.

Therefore a candidate recorded statically as:

`file.py::test_name`

can legitimately execute as multiple pytest call-phase records:

`file.py::test_name[param-id]`

R3-2 used exact dictionary lookup by the base candidate ID. R3-2D verifies
whether this node-ID shape difference explains the six missing records.
