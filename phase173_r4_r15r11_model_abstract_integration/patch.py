"""Guarded, minimal R15R11 display-only transformations of reviewed sources."""
from __future__ import annotations

import ast
from pathlib import Path

EXPECTED_BLOBS = {
    "phase165_r52_r3_web_adapter.py": "a5c402c86e624010e5521ceda0cb1734ab32bcae",
    "phase168_r3_3_proof_narrative_model.py": "f09be949a7a07fc3f082bcd267f41c9f606590ea",
    "phase168_r3_5_model_renderer.py": "6bfd5e992f6c9ee9441920e10e63e0db4bece289",
    "phase173_r4_r15r9_shared_abstract_renderer/projection.py": "777db698e8da026571c8046b84fc3b875ee6dfe0",
}
EXPECTED_HEAD = "7e9e00f42e8b125480cd2928b0ee7ec2c5269d3a"


def _replace_once(source: str, before: str, after: str, *, label: str) -> str:
    """Reject already-applied replacements, even when the old anchor remains."""
    if after in source:
        raise RuntimeError(f"Unreviewed source or already patched anchor: {label}")
    if source.count(before) != 1:
        raise RuntimeError(f"Unreviewed source or duplicate anchor: {label}")
    return source.replace(before, after, 1)


def _patch_model(source: str) -> str:
    source = _replace_once(
        source,
        "from phase165_r52_partial_proof import PartialProofResult, ProofSearchStatus",
        "from phase165_r52_partial_proof import CertifiedAbstractStructure, PartialProofResult, ProofSearchStatus",
        label="model import",
    )
    source = _replace_once(
        source,
        "    diagnostics: tuple[str, ...] = ()\n\n\ndef root_ancestor_step_indices(",
        "    diagnostics: tuple[str, ...] = ()\n"
        "    abstract_structure: CertifiedAbstractStructure | None = None\n\n\n"
        "def root_ancestor_step_indices(",
        label="model dataclass field",
    )
    source = _replace_once(
        source,
        "        open_goals=result.open_goals,\n"
        "        diagnostics=result.diagnostics,\n"
        "    )",
        "        open_goals=result.open_goals,\n"
        "        diagnostics=result.diagnostics,\n"
        "        abstract_structure=result.abstract_structure,\n"
        "    )",
        label="model builder result",
    )
    return source


def _patch_model_renderer(source: str) -> str:
    source = _replace_once(
        source,
        "    incomplete = result.status is not ProofSearchStatus.COMPLETE\n",
        "    if model.abstract_structure is not result.abstract_structure:\n"
        "        raise ValueError(\"Narrative Model abstract certificate must match searched result\")\n"
        "    incomplete = result.status is not ProofSearchStatus.COMPLETE\n",
        label="model evidence identity check",
    )
    source = _replace_once(
        source,
        '        lines.extend(("", "未解決 Goal は証明済みの結論ではありません。"))\n'
        '    else:\n'
        '        lines.append("□")',
        '        if model.abstract_structure is not None:\n'
        '            from phase173_r4_r15r9_shared_abstract_renderer.projection import (\n'
        '                render_certified_abstract_model_section,\n'
        '            )\n'
        '            lines.extend(("", render_certified_abstract_model_section(model)))\n'
        '        lines.extend(("", "未解決 Goal は証明済みの結論ではありません。"))\n'
        '    else:\n'
        '        lines.append("□")',
        label="existing common Model Renderer terminal section",
    )
    return source


_WEB_BEFORE = '''        if narrative_model is None:\n            markdown = render_partial_proof_markdown(result)\n        else:\n            from phase168_r3_5_model_renderer import render_model_backed_narrative_markdown\n            markdown = render_model_backed_narrative_markdown(result, narrative_model)\n        from phase173_r4_r15r9_shared_abstract_renderer.projection import (\n            render_certified_abstract_section,\n        )\n        abstract_markdown = render_certified_abstract_section(result)\n        if abstract_markdown:\n            markdown = markdown.rstrip() + "\\n\\n" + abstract_markdown + "\\n"\n        rendered_lines = _build_group_proof_rendered_lines(markdown)'''

_WEB_AFTER = '        if narrative_model is None:\n            # Preserve the existing legacy/compatibility narrative route.\n            markdown = render_partial_proof_markdown(result)\n            from phase173_r4_r15r9_shared_abstract_renderer.projection import (\n                render_certified_abstract_section,\n            )\n            abstract_markdown = render_certified_abstract_section(result)\n            if abstract_markdown:\n                markdown = markdown.rstrip() + "\\n\\n" + abstract_markdown + "\\n"\n        else:\n            from phase168_r3_5_model_renderer import render_model_backed_narrative_markdown\n            markdown = render_model_backed_narrative_markdown(result, narrative_model)\n        rendered_lines = _build_group_proof_rendered_lines(markdown)'

def _patch_web(source: str) -> str:
    return _replace_once(source, _WEB_BEFORE, _WEB_AFTER, label="common web adapter block")


_PROJECTION_BEFORE = '''    target = result.target\n    if type(target.group_dimension) is not int or type(target.sphere_dimension) is not int:\n        raise ValueError("abstract result has nonconcrete group dimensions")\n    invariant_latex = abstract_invariants_latex(structure.invariant_summands)\n    target_latex = rf"\\pi_{{{target.group_dimension}}}^{{{target.sphere_dimension}}}"\n    return (\n        "## 証明済みの抽象群構造\\n\\n"\n        + rf"${target_latex} \\cong {invariant_latex}$."\n        + "\\n\\n"\n        + "これは出典検査済みの抽象群 ProofStep による結論であり、"\n        + "登録済みの先行 DB 群を前提とする。"\n        + "記名生成元の対応は未証明であり、上記の未解決 Goal と探索状態は変わらない。"\n    )\n'''

_PROJECTION_AFTER = '''    return _render_abstract_claim(result.target, structure)\n\n\ndef _render_abstract_claim(target: object, structure: CertifiedAbstractStructure) -> str:\n    """Format only an already certified abstract structure, never identify generators."""\n    if type(target.group_dimension) is not int or type(target.sphere_dimension) is not int:\n        raise ValueError("abstract result has nonconcrete group dimensions")\n    invariant_latex = abstract_invariants_latex(structure.invariant_summands)\n    target_latex = rf"\\pi_{{{target.group_dimension}}}^{{{target.sphere_dimension}}}"\n    return (\n        "## 証明済みの抽象群構造\\n\\n"\n        + rf"${target_latex} \\cong {invariant_latex}$."\n        + "\\n\\n"\n        + "これは出典検査済みの抽象群 ProofStep による結論であり、"\n        + "登録済みの先行 DB 群を前提とする。"\n        + "記名生成元の対応は未証明であり、上記の未解決 Goal と探索状態は変わらない。"\n    )\n\n\ndef render_certified_abstract_model_section(model: object) -> str:\n    """Render only certificate evidence explicitly carried by ProofNarrativeModel."""\n    from phase168_r3_3_proof_narrative_model import ProofNarrativeModel\n\n    if not isinstance(model, ProofNarrativeModel):\n        raise TypeError("expected canonical ProofNarrativeModel")\n    structure = model.abstract_structure\n    if structure is None:\n        return ""\n    if (\n        not isinstance(structure, CertifiedAbstractStructure)\n        or structure.group != model.target\n        or model.status not in (ProofSearchStatus.PARTIAL, ProofSearchStatus.SEARCH_FAILED)\n        or model.root_index is not None\n    ):\n        raise ValueError("unverified Model abstract result cannot be presented")\n    return _render_abstract_claim(model.target, structure)\n'''


def _patch_projection(source: str) -> str:
    source = _replace_once(
        source,
        "The common Web adapter invokes this function after its usual narrative has\n"
        "been rendered. No n/k special case and no alternate Narrative pipeline exists.",
        "The default Model-backed renderer and legacy Web adapter share this\n"
        "formatter. No n/k special case or alternate Narrative pipeline exists.",
        label="projection module purpose",
    )
    return _replace_once(source, _PROJECTION_BEFORE, _PROJECTION_AFTER, label="abstract projection formatter")


PATCHES = {
    "phase165_r52_r3_web_adapter.py": _patch_web,
    "phase168_r3_3_proof_narrative_model.py": _patch_model,
    "phase168_r3_5_model_renderer.py": _patch_model_renderer,
    "phase173_r4_r15r9_shared_abstract_renderer/projection.py": _patch_projection,
}


def apply_to_source(relative: str, source: bytes) -> bytes:
    """Return proposed full-source replacement, preserving its original line ending."""
    if relative not in PATCHES:
        raise ValueError("unexpected target file")
    if b"\r\n" in source and b"\n" in source.replace(b"\r\n", b""):
        raise RuntimeError("Mixed EOLs in reviewed file")
    eol = b"\r\n" if b"\r\n" in source else b"\n"
    original = source.decode("utf-8")
    normalized = original.replace("\r\n", "\n")
    proposed = PATCHES[relative](normalized)
    if proposed == normalized:
        raise RuntimeError("Expected nonempty change")
    ast.parse(proposed, filename=relative)
    if eol == b"\r\n":
        proposed = proposed.replace("\n", "\r\n")
    return proposed.encode("utf-8")


def changed_units(relative: str, patched: bytes) -> str:
    """Export actual complete changed class/function and import block (not snippets)."""
    content = patched.decode("utf-8").replace("\r\n", "\n")
    tree = ast.parse(content)
    lines = content.splitlines()
    output = [f"## {relative}"]
    imports = [node for node in tree.body if isinstance(node, (ast.Import, ast.ImportFrom))]
    if relative == "phase168_r3_3_proof_narrative_model.py":
        # All top-level imports appear before the first class definition.
        last_import = max(node.end_lineno for node in imports)
        output.extend(("### Changed complete import block", "```python", "\n".join(lines[:last_import]), "```"))
        names = {"ProofNarrativeModel", "build_proof_narrative_model"}
    elif relative == "phase165_r52_r3_web_adapter.py":
        last_import = max(node.end_lineno for node in imports)
        output.extend(("### Complete unchanged import block", "```python", "\n".join(lines[:last_import]), "```"))
        names = {"build_partial_web_group_proof_view"}
    elif relative == "phase168_r3_5_model_renderer.py":
        names = {"render_model_backed_narrative_markdown"}
    else:
        names = {"render_certified_abstract_section", "_render_abstract_claim", "render_certified_abstract_model_section"}
    for node in tree.body:
        if isinstance(node, (ast.ClassDef, ast.FunctionDef)) and node.name in names:
            start = min((dec.lineno for dec in node.decorator_list), default=node.lineno)
            output.extend((f"### Complete {node.name}", "```python", "\n".join(lines[start-1:node.end_lineno]), "```"))
    assert all(any(f"### Complete {name}" == item for item in output) for name in names)
    return "\n\n".join(output) + "\n"
