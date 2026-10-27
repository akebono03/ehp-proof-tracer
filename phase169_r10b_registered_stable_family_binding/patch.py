"""Replace one complete R7 generator-candidate function with DB-bound version."""
from __future__ import annotations

import ast
import hashlib
import subprocess
from pathlib import Path


ROOT = Path(__file__).resolve().parent.parent
HERE = Path(__file__).resolve().parent
TARGET = ROOT / "phase169_r7_general_stable_transport" / "rule.py"
OUTPUT = HERE / "output"
BACKUP = OUTPUT / "phase169_r7_general_stable_transport.rule.py.before"

# The exact reviewed R7 function body is the only allowed patch anchor.
OLD_FUNCTION_START = "def _intermediate_typed_generator(source: object, target: object, step: int,"


NEW_FUNCTION = '''def _intermediate_typed_generator(source: object, target: object, step: int,
                                  exponent: int) -> object | None:
    """Build DB-identified typed candidates, never a proven image equality.

    The HyoujiGen kinds=0 row is identity metadata. The downstream R7 rule
    continues to demand independently proved GeneratorImage obligations.
    """
    if type(step) is not int or type(exponent) is not int or not 0 <= step <= exponent:
        return None
    if isinstance(source, HomotopyElement) and isinstance(target, HomotopyElement):
        from phase169_r10b_registered_stable_family_binding.family_registry import (
            registered_stable_family_pair,
        )
        family = registered_stable_family_pair(source, target)
        s, t = source.generator, target.generator
        if (family is None
                or not isinstance(s, GeneratorSymbol)
                or not isinstance(t, GeneratorSymbol)
                or type(s.index) is not int
                or type(t.index) is not int
                or t.index - s.index != exponent
                or target.dimension - source.dimension != exponent
                or target.source - source.source != exponent
                or target.target - source.target != exponent):
            return None
        if step == 0:
            return source
        if step == exponent:
            return target
        middle_index = s.index + step
        return replace(
            source,
            name=family.name_at(middle_index),
            dimension=source.dimension + step,
            source=source.source + step,
            target=source.target + step,
            generator=replace(s, index=middle_index),
        )
    if isinstance(source, Composition) and isinstance(target, Composition):
        left = _intermediate_typed_generator(source.left, target.left, step, exponent)
        right = _intermediate_typed_generator(source.right, target.right, step, exponent)
        return Composition(left, right) if left is not None and right is not None else None
    if isinstance(source, Sum) and isinstance(target, Sum):
        left = _intermediate_typed_generator(source.left, target.left, step, exponent)
        right = _intermediate_typed_generator(source.right, target.right, step, exponent)
        return Sum(left, right) if left is not None and right is not None else None
    if (isinstance(source, Multiple) and isinstance(target, Multiple)
            and source.coefficient == target.coefficient):
        inner = _intermediate_typed_generator(source.expression, target.expression,
                                              step, exponent)
        return Multiple(source.coefficient, inner) if inner is not None else None
    if step == 0:
        return source
    if step == exponent:
        return target
    if (isinstance(target, IteratedSuspension)
            and target.expression == source
            and type(target.exponent) is int
            and target.exponent == exponent):
        return IteratedSuspension(source, step)
    if (isinstance(source, IteratedSuspension)
            and isinstance(target, IteratedSuspension)
            and source.expression == target.expression
            and type(source.exponent) is int
            and type(target.exponent) is int
            and target.exponent - source.exponent == exponent):
        return IteratedSuspension(source.expression, source.exponent + step)
    return None
'''


def _function_range(code: str) -> tuple[int, int]:
    lines = code.splitlines(keepends=True)
    tree = ast.parse(code)
    matches = [node for node in tree.body
               if isinstance(node, ast.FunctionDef)
               and node.name == "_intermediate_typed_generator"]
    if len(matches) != 1:
        raise RuntimeError("expected exactly one R7 generator candidate function")
    node = matches[0]
    if not lines[node.lineno - 1].startswith(OLD_FUNCTION_START):
        raise RuntimeError("R7 generator function signature drifted")
    return sum(len(line) for line in lines[:node.lineno - 1]), sum(
        len(line) for line in lines[:node.end_lineno]
    )


def replacement_content(original: bytes) -> tuple[bytes, str]:
    """Only change the function; preserve all other R7 source bytes and EOLs."""
    windows = b"\r\n" in original
    code = original.decode("utf-8").replace("\r\n", "\n")
    start, end = _function_range(code)
    original_function = code[start:end]
    if ("Every index/dimension change is checked structurally" not in original_function
            or "_indexed_display(source)" not in original_function
            or "_indexed_display(target)" not in original_function):
        raise RuntimeError("R7 baseline function has changed; no patch applied")
    replacement = NEW_FUNCTION + ("\n" if code[end:end + 1] == "\n" else "")
    updated = code[:start] + replacement + code[end:]
    ast.parse(updated)
    if updated.count("def _intermediate_typed_generator(") != 1:
        raise RuntimeError("duplicate generator-candidate function")
    new_content = updated.replace("\n", "\r\n") if windows else updated
    return new_content.encode("utf-8"), NEW_FUNCTION


def main() -> None:
    branch = subprocess.run(["git", "branch", "--show-current"], cwd=ROOT,
                            capture_output=True, text=True, check=True).stdout.strip()
    if branch != "develop":
        raise RuntimeError("R10B requires the develop branch")
    original = TARGET.read_bytes()
    changed, function = replacement_content(original)
    OUTPUT.mkdir(exist_ok=True)
    if BACKUP.exists():
        if BACKUP.read_bytes() != original:
            raise RuntimeError("existing R10B restore point does not match production")
    else:
        BACKUP.write_bytes(original)
    (OUTPUT / "_intermediate_typed_generator_FULL.py").write_text(
        function, encoding="utf-8"
    )
    (OUTPUT / "phase169_r7_general_stable_transport.rule.py.FULL").write_bytes(changed)
    tmp = TARGET.with_name(TARGET.name + ".r10b-tmp")
    try:
        tmp.write_bytes(changed)
        tmp.replace(TARGET)
    finally:
        if tmp.exists():
            tmp.unlink()
    print("R10B_PATCHED=" + str(TARGET))
    print("R10B_BACKUP=" + str(BACKUP))
    print("R10B_FULL_FUNCTION=" + str(OUTPUT / "_intermediate_typed_generator_FULL.py"))
    print("R10B_FULL_FILE=" + str(OUTPUT / "phase169_r7_general_stable_transport.rule.py.FULL"))


if __name__ == "__main__":
    main()
