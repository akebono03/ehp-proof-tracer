"""Patch only the R10EC focused test, never mathematical production code."""
from __future__ import annotations

import hashlib
import os
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
HERE = Path(__file__).resolve().parent
TEST_RELATIVE = (
    "phase169_r10ec_direct_sum_narrative_projection/tests/"
    "test_r10ec_projection.py"
)
EXPECTED_SHA256 = "2bec8d3cc27d6ebcd496468b4576dc9c9e48ffe7301f5c9a8da22b8cf588d713"
OLD_IMPORT = "import pytest\n\nfrom phase165_r52_partial_proof import ProofSearchStatus\n"
NEW_IMPORT = (
    "import pytest\n\n"
    "from homotopy_groups import FiniteCyclicGroup\n"
    "from phase165_r52_partial_proof import ProofSearchStatus\n"
)
OLD_TEST = '''def test_r10ec_cyclic_non_direct_sum_is_not_compressed():
    bridge = build_shared_typed_bridge()
    contexts = []
    result = search_group_from_registered_goal(
        n=4, k=1, bridge=bridge, context_sink=contexts.append,
    )
    assert result.status is ProofSearchStatus.COMPLETE
    assert contexts
    model = build_linked_proof_narrative_model(result, contexts[-1])
    order = tuple(entry.step_index for entry in project_narrative_order(model))
    assert project_verified_direct_sum_transport(model, order) is None
'''
NEW_TEST = '''def test_r10ec_cyclic_non_direct_sum_is_not_compressed():
    """Use the already verified complete cyclic pi_10^8 fixture from R10A."""
    bridge = build_shared_typed_bridge()
    contexts = []
    result = search_group_from_registered_goal(
        n=8, k=2, bridge=bridge, context_sink=contexts.append,
    )
    assert result.status is ProofSearchStatus.COMPLETE
    assert contexts
    assert isinstance(result.conclusion, Relation)
    assert isinstance(result.conclusion.rhs, FiniteCyclicGroup)
    model = build_linked_proof_narrative_model(result, contexts[-1])
    order = tuple(entry.step_index for entry in project_narrative_order(model))
    assert project_verified_direct_sum_transport(model, order) is None
'''


def transform_test(source: bytes) -> tuple[bytes, str]:
    """Replace exactly one complete test with a known completed cyclic case."""
    if hashlib.sha256(source).hexdigest() != EXPECTED_SHA256:
        raise RuntimeError("R10EC original focused test bytes do not match reviewed file")
    if b"\r\n" in source or b"\r" in source:
        raise RuntimeError("R10EC test unexpected newline format")
    text = source.decode("utf-8")
    if text.count(OLD_IMPORT) != 1 or text.count(OLD_TEST) != 1:
        raise RuntimeError("R10EC test import or function anchor changed")
    updated = text.replace(OLD_IMPORT, NEW_IMPORT, 1).replace(OLD_TEST, NEW_TEST, 1)
    compile(updated, TEST_RELATIVE, "exec")
    if updated.count("def test_r10ec_cyclic_non_direct_sum_is_not_compressed") != 1:
        raise RuntimeError("R10EC test function duplication")
    return updated.encode("utf-8"), updated


def main() -> None:
    source_path = ROOT / TEST_RELATIVE
    if not source_path.is_file():
        raise RuntimeError("R10EC extracted original test not found")
    data, full = transform_test(source_path.read_bytes())
    temp = source_path.with_suffix(".r10ecr1.tmp")
    try:
        temp.write_bytes(data)
        os.replace(temp, source_path)
    finally:
        if temp.exists():
            temp.unlink()
    output = HERE / "output"
    output.mkdir(exist_ok=True)
    (output / "test_r10ec_projection.py.FULL").write_text(full, encoding="utf-8")
    start = full.index("def test_r10ec_cyclic_non_direct_sum_is_not_compressed():")
    (output / "test_r10ec_cyclic_non_direct_sum_is_not_compressed_FULL.py").write_text(
        full[start:], encoding="utf-8"
    )
    import_end = full.index("@pytest.fixture")
    (output / "test_r10ec_projection_IMPORTS_FULL.py").write_text(
        full[:import_end], encoding="utf-8"
    )
    print("R10ECR1_PATCHED=" + str(source_path))
    print("R10ECR1_FULL_TEST=" + str(output / "test_r10ec_cyclic_non_direct_sum_is_not_compressed_FULL.py"))
    print("R10ECR1_FULL_IMPORTS=" + str(output / "test_r10ec_projection_IMPORTS_FULL.py"))
    print("R10ECR1_FULL_FILE=" + str(output / "test_r10ec_projection.py.FULL"))


if __name__ == "__main__":
    main()
