"""Fail-closed R10ET-R5 change to the complete shared provider and affected tests."""
from __future__ import annotations

import ast
import hashlib
import subprocess
from pathlib import Path

HERE = Path(__file__).resolve().parent
PROVIDER = "phase165_r52_r9_shared_math.py"
R4_TARGETS = (
    "phase169_r10a_verified_stable_chain_projection/projection.py",
    "phase168_r3_5_model_renderer.py",
)
EXPECTED_BLOBS = {
    PROVIDER: "61cbadb06f770c51a9c1f5a3c8026acf9e3e14aa",
    "phase169_r10a_verified_stable_chain_projection/tests/test_r10a_verified_stable_chain.py": "430af1787191066b7f9326b4f56fe086393fcf19",
    "phase169_r10ec_direct_sum_narrative_projection/tests/test_r10ec_projection.py": "83e0100dfdd672fb2b635e5163d37981d3e97675",
    "phase169_r10el_shared_generator_suppression/tests/test_r10el_live.py": "341f1131899393e61e238fe8c21b97c7543b59c7",
    "phase169_r10er_r1_mixed_definition_projection/tests/test_r10er_projection.py": "e383f400eb1ad8a4f0241ea2b02c5bd00f90d7be",
}
OLD_EXPAND_START = '''    def expand(goal: object) -> tuple[GoalExpansion, ...]:
        options = []'''
NEW_EXPAND_START = '''    def expand(goal: object) -> tuple[GoalExpansion, ...]:
        # R10ET-R5: use the single, replayable Definition for every eligible
        # typed stable GeneratorImage, regardless of the generator's label.
        from phase169_r10eq_r1_universal_stable_definition.definition import (
            expand_defined_stable_element_image,
        )
        defined_options = expand_defined_stable_element_image(goal)
        if defined_options:
            return defined_options
        options = []'''
OLD_FALLBACK = '''        if not (eta_generator_options or cited_stable_options
                or composite_image_options):
            from phase169_r10eq_r1_universal_stable_definition.definition import (
                expand_defined_stable_element_image,
            )
            options.extend(expand_defined_stable_element_image(goal))
'''

REPLACEMENTS = {
    PROVIDER: ((OLD_EXPAND_START, NEW_EXPAND_START), (OLD_FALLBACK, "")),
    "phase169_r10a_verified_stable_chain_projection/tests/test_r10a_verified_stable_chain.py": ((
        "    assert display.citation_numbers\n",
        '    from phase169_r10et_r4_cyclic_definition_projection.policy import (\n        canonical_definition_image,\n    )\n    images = model.steps[model.root_index].premises[2:]\n    if all(canonical_definition_image(image) for image in images):\n        assert display.citation_numbers == ()\n        assert "Definition より, " in render_model_backed_narrative_markdown(result, model)\n    else:\n        assert display.citation_numbers\n',
    ),),
    "phase169_r10ec_direct_sum_narrative_projection/tests/test_r10ec_projection.py": ((
        "    assert len(display.citation_numbers) >= 3\n",
        "    assert display.citation_numbers == ()\n    assert display.statement.startswith(\"Definition より, \")\n",
    ),),
    "phase169_r10el_shared_generator_suppression/tests/test_r10el_live.py": ((
        '''    (22, 6, "cyclic", 14, 31),
    (22, 10, "cyclic", 10, 40),
    (15, 8, "direct_sum", 5, 10),
    (24, 9, "direct_sum", 13, 110),''',
        '''    (22, 6, "cyclic", 14, 14),
    (22, 10, "cyclic", 10, 10),
    (15, 8, "direct_sum", 5, 10),
    (24, 9, "direct_sum", 13, 39),''',
    ),),
    "phase169_r10er_r1_mixed_definition_projection/tests/test_r10er_projection.py": ((
        "    assert \"Definition\" in display.statement\n    assert display.citation_numbers\n",
        "    assert \"Definition\" in display.statement\n    assert display.citation_numbers == ()\n",
    ), (
        '''def test_r10er_earlier_fully_cited_direct_sum_keeps_its_old_prefix(cases):
    result, model, order = cases[(30, 9)]
    display = project_verified_direct_sum_transport(model, order)
    assert display is not None
    assert display.citation_numbers
    assert display.statement.startswith("[R")
    assert "Definition と" not in display.statement
    assert display.statement in render_model_backed_narrative_markdown(result, model)
''',
        '''def test_r10er_common_definition_replaces_cited_prefix(cases):
    result, model, order = cases[(30, 9)]
    display = project_verified_direct_sum_transport(model, order)
    assert display is not None
    assert display.citation_numbers == ()
    assert display.statement.startswith("Definition より, ")
    locators = tuple(item.reference.locator or item.reference.label
                     for item in model.citations)
    assert len(locators) == 2
    assert any("DB prior:" in locator for locator in locators)
    assert "(4.5)" in locators
    assert display.statement in render_model_backed_narrative_markdown(result, model)
''',
    )),
}


def git_blob(data: bytes) -> str:
    return hashlib.sha1(f"blob {len(data)}\0".encode() + data).hexdigest()


def git_bytes(root: Path, path: str) -> bytes:
    return subprocess.run(["git", "-C", str(root), "show", "HEAD:" + path],
                          capture_output=True, check=True).stdout


def complete_function(source: str, name: str) -> str:
    tree = ast.parse(source)
    funcs = [node for node in tree.body if isinstance(node, ast.FunctionDef) and node.name == name]
    if len(funcs) != 1:
        raise RuntimeError(f"expected exactly one top-level function {name}")
    node = funcs[0]
    lines = source.splitlines(keepends=True)
    return "".join(lines[node.lineno - 1:node.end_lineno])


def transform(path: str, original: bytes) -> tuple[bytes, dict[str, str]]:
    if path not in EXPECTED_BLOBS or git_blob(original) != EXPECTED_BLOBS[path]:
        raise RuntimeError(f"unreviewed or modified source: {path}")
    newline = "\r\n" if b"\r\n" in original else "\n"
    source = original.decode("utf-8").replace("\r\n", "\n")
    updated = source
    before_tree = ast.parse(source)
    for old, new in REPLACEMENTS[path]:
        count = updated.count(old)
        if count != 1:
            raise RuntimeError(f"expected one anchor but got {count}: {path}: {old[:40]}")
        updated = updated.replace(old, new, 1)
    after_tree = ast.parse(updated)
    if (len(before_tree.body) != len(after_tree.body)
            or [type(x).__name__ for x in before_tree.body]
            != [type(x).__name__ for x in after_tree.body]):
        raise RuntimeError(f"unintended AST structure changes: {path}")
    if path == PROVIDER:
        before = complete_function(source, "shared_expansion_provider")
        after = complete_function(updated, "shared_expansion_provider")
        if updated.replace(after, before, 1) != source:
            raise RuntimeError("changes outside shared_expansion_provider")
        outputs = {"shared_expansion_provider": after}
    else:
        old_functions = [node.name for node in before_tree.body
                         if isinstance(node, ast.FunctionDef)]
        new_functions = [node.name for node in after_tree.body
                         if isinstance(node, ast.FunctionDef)]
        if len(old_functions) != len(new_functions):
            raise RuntimeError(f"test function count changed: {path}")
        outputs = {}
        for old_name, new_name in zip(old_functions, new_functions):
            if (old_name != new_name and not (path.endswith("test_r10er_projection.py")
                    and old_name == "test_r10er_earlier_fully_cited_direct_sum_keeps_its_old_prefix"
                    and new_name == "test_r10er_common_definition_replaces_cited_prefix")):
                raise RuntimeError(f"unreviewed test rename: {old_name} => {new_name}")
            old_fn = complete_function(source, old_name)
            new_fn = complete_function(updated, new_name)
            if new_fn != old_fn:
                outputs[new_name] = new_fn
    return updated.replace("\n", newline).encode("utf-8"), outputs


def prepare(root: Path, output: Path) -> dict[str, tuple[bytes, bytes]]:
    output.mkdir(parents=True, exist_ok=False)
    before_after = {}
    for path in EXPECTED_BLOBS:
        original = (root / path).read_bytes()
        changed, functions = transform(path, original)
        before_after[path] = (original, changed)
        dest = output / "full_sources" / path
        dest.parent.mkdir(parents=True, exist_ok=True)
        dest.write_bytes(changed)
        (dest.parent / (dest.name + ".before")).write_bytes(original)
        for name, content in functions.items():
            (dest.parent / (dest.name + "." + name + ".FULL.py")).write_text(content, encoding="utf-8")
    return before_after


def apply(root: Path, versions: dict[str, tuple[bytes, bytes]]) -> None:
    modified = []
    try:
        for path, (before, after) in versions.items():
            target = root / path
            if target.read_bytes() != before:
                raise RuntimeError(f"concurrent modification of {path}")
            target.write_bytes(after)
            modified.append(path)
    except BaseException:
        for path in reversed(modified):
            (root / path).write_bytes(versions[path][0])
        raise


def restore(root: Path, versions: dict[str, tuple[bytes, bytes]]) -> None:
    for path, (before, _after) in versions.items():
        (root / path).write_bytes(before)
