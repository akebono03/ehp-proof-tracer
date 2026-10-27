"""Guarded replacement of one outdated inference matcher regression test."""
from __future__ import annotations

import ast
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
HERE = Path(__file__).resolve().parent
OUTPUT = HERE / "output"
TARGET_RELATIVE = "phase169_r10e5_composite_generator_image/tests/test_r10e5_composite_generator_image.py"
TARGET = ROOT / TARGET_RELATIVE
TEST_NAME = "test_r10e5_two_inferred_images_are_required_to_prove_composition"

OLD_TEST = 'def test_r10e5_two_inferred_images_are_required_to_prove_composition():\n    goal = _image(8, 6, _square(8), _square(9))\n    obligations = component_image_obligations(goal)\n    assert obligations is not None\n    rule = composite_generator_image_rule(goal)\n    steps = tuple(ProofStep(item, (), ProofRule.INFERENCE)\n                  for item in obligations)\n    matches = find_inference_matches_for_rule(rule, steps)\n    assert len(matches) == 1\n    assert apply_inference_match(matches[0]).conclusion == goal\n    assert find_inference_matches_for_rule(rule, steps[:1]) == ()\n    assert find_inference_matches_for_rule(\n        rule, (replace(steps[0], rule=ProofRule.GIVEN), steps[1]),\n    ) == ()\n    assert find_inference_matches_for_rule(rule, tuple(reversed(steps))) == ()\n'
NEW_TEST = 'def test_r10e5_two_inferred_images_are_required_to_prove_composition():\n    goal = _image(8, 6, _square(8), _square(9))\n    obligations = component_image_obligations(goal)\n    assert obligations is not None\n    rule = composite_generator_image_rule(goal)\n    steps = tuple(ProofStep(item, (), ProofRule.INFERENCE)\n                  for item in obligations)\n    matches = find_inference_matches_for_rule(rule, steps)\n    assert len(matches) == 1\n    assert matches[0].premises == steps\n    assert apply_inference_match(matches[0]).conclusion == goal\n    assert find_inference_matches_for_rule(rule, steps[:1]) == ()\n    assert find_inference_matches_for_rule(\n        rule, (replace(steps[0], rule=ProofRule.GIVEN), steps[1]),\n    ) == ()\n    # The inference matcher accepts premises in arbitrary input order and\n    # returns them in their typed premise-pattern order.\n    reversed_matches = find_inference_matches_for_rule(rule, tuple(reversed(steps)))\n    assert len(reversed_matches) == 1\n    assert reversed_matches[0].premises == steps\n    assert apply_inference_match(reversed_matches[0]).conclusion == goal\n'


def _extract_test(source: str) -> tuple[str, int, int]:
    tree = ast.parse(source)
    matches = tuple(
        item for item in tree.body
        if isinstance(item, ast.FunctionDef) and item.name == TEST_NAME
    )
    if len(matches) != 1:
        raise RuntimeError("R10E5R3 requires exactly one named test")
    node = matches[0]
    lines = source.splitlines(keepends=True)
    return "".join(lines[node.lineno - 1:node.end_lineno]), node.lineno - 1, node.end_lineno


def transform(raw: bytes) -> tuple[bytes, str]:
    crlf = b"\r\n" in raw
    source = raw.decode("utf-8-sig").replace("\r\n", "\n")
    found, first, end = _extract_test(source)
    if found != OLD_TEST:
        raise RuntimeError("R10E5R3 test anchor missing, changed or already applied")
    lines = source.splitlines(keepends=True)
    updated = "".join(lines[:first]) + NEW_TEST + "".join(lines[end:])
    ast.parse(updated)
    updated_found, _, _ = _extract_test(updated)
    if updated_found != NEW_TEST:
        raise RuntimeError("R10E5R3 replacement did not preserve full test")
    encoded = updated.encode("utf-8")
    if crlf:
        encoded = encoded.replace(b"\n", b"\r\n")
    return encoded, NEW_TEST


def main() -> None:
    raw = TARGET.read_bytes()
    updated, function = transform(raw)
    OUTPUT.mkdir(parents=True, exist_ok=True)
    before = OUTPUT / "test_r10e5_composite_generator_image.py.before"
    before.write_bytes(raw)
    (OUTPUT / "test_r10e5_composite_generator_image.py.FULL").write_bytes(updated)
    full_fn = OUTPUT / (TEST_NAME + "_FULL.py")
    full_fn.write_text(function, encoding="utf-8")
    TARGET.write_bytes(updated)
    print("R10E5R3_TEST_PATCHED=" + str(TARGET))
    print("R10E5R3_FULL_TEST_FUNCTION=" + str(full_fn))
    print("R10E5R3_FULL_TEST_FILE=" + str(OUTPUT / "test_r10e5_composite_generator_image.py.FULL"))


if __name__ == "__main__":
    main()
