"""Update only historical tests contradicted by the unified public Narrative contract.

Verified helper/legacy contracts remain intact. Never replace test functions with
skips or remove their mathematical invariants. All anchors are exact and fail closed.
"""
from __future__ import annotations

import ast
from dataclasses import dataclass


@dataclass(frozen=True)
class Change:
    function: str
    before: str
    after: str


P = "phase173_r4_"
FILES = {
    P + "r15r9_shared_abstract_renderer/tests/test_projection.py": "4082d38c92a111cbada89a31791ba38efc384e3c",
    P + "r15r11_model_abstract_integration/tests/test_integration.py": "26ad2bca42c9cc445d5df715f470c2974202ef4b",
    P + "r15r12_reference_correction/tests/test_integration.py": "ead4223ec8166323618d496a31f82298b91a73f9",
    P + "r15r13_unified_presentation/tests/test_integration.py": "b973d61d46cb6668cf584b9675206d110a76700c",
    P + "r15r14_common_partial_presentation/tests/test_integration.py": "3ed31e139a057634c93990ce62482bcfd20c9f8e",
    P + "r15r15_abstract_result_banner/tests/test_integration.py": "a9848df04b861394e6b1fea36fece43796433731",
    P + "r15r15r2_head_guard_fix/tests/test_integration.py": "a9848df04b861394e6b1fea36fece43796433731",
    P + "r15r16_verified_progress_punctuation/tests/test_integration.py": "c5ac2f5129ad20f4de287cacb59afbf84279834f",
    P + "r15r16r2_shared_tree_narrative/tests/test_integration.py": "d6b97ab92dd75e3d01acf3c0357cc072d461a73e",
    P + "r15r16r3_staged_guard_fix/tests/test_integration.py": "3a3e2b6f9170af3918bceab41712406e43fda70b",
}


def change(function: str, before: str, after: str) -> Change:
    if not before or before == after:
        raise ValueError("a contract change must be nonempty")
    return Change(function, before, after)


MODEL_FIRST = change(
    "test_source_first_certificate_is_owned_by_model_and_rendered_once",
    '''    abstract = render_certified_abstract_model_section(model)
    assert abstract == render_certified_abstract_section(result)
    after = render_model_backed_narrative_markdown(result, model)
    assert after.count("## 証明済みの抽象群構造") == 1
    assert abstract in after
    assert "## 未解決 Goal" in after
''',
    '''    abstract = render_certified_abstract_model_section(model)
    assert abstract == ""
    assert "## 証明済みの抽象群構造" in render_certified_abstract_section(result)
    assert any(step is result.abstract_structure.proof_step for step in model.steps)
    after = render_model_backed_narrative_markdown(result, model)
    assert after.count("## 使用する結果") == 1
    assert "## 証明済みの抽象群構造" not in after
    assert "### 検証済み証明木の Reference" not in after
    assert "Proposition 4.4" in after
    assert "Lemma 5.4" in after
    assert r"\\cong" in after
    assert "## 未解決 Goal" in after
''',
)

MODEL_LEGACY = change(
    "test_public_default_path_and_legacy_path_keep_one_abstract_section",
    '''        assert headings.count("証明済みの抽象群構造") == 1
        if citation_source == "model":
            assert headings.count("未解決 Goal") == 1
''',
    '''        if citation_source == "model":
            assert headings.count("使用する結果") == 1
            assert headings.count("証明済みの抽象群構造") == 0
            assert headings.count("検証済みの途中経過") == 0
            assert headings.count("未解決 Goal") == 1
            shown = "\\n".join(
                segment.value for line in view.rendered_lines
                for segment in line.segments
            )
            assert r"\\cong" in shown
        else:
            # The separately requested legacy API retains its old projection.
            assert headings.count("証明済みの抽象群構造") == 1
''',
)

ONE_REFERENCE_NO_SIDECAR = '''    assert headings.count("使用する結果") == 1
    assert headings.count("証明済みの抽象群構造") == 0
    assert headings.count("検証済みの途中経過") == 0
    assert headings.count("未解決 Goal") == 1
'''

REF_CORRECTION = change(
    "test_abstract_only_groups_remain_partial",
    '''    assert sum(line.kind == 'heading' and line.prefix == '証明済みの抽象群構造'
               for line in view.rendered_lines) == 1
''',
    '''    headings = [line.prefix for line in view.rendered_lines if line.kind == 'heading']
''' + ONE_REFERENCE_NO_SIDECAR + '''    assert view.abstract_structure_certified
    assert any(r"\\cong" in segment.value
               for line in view.rendered_lines for segment in line.segments)
''',
)

PRESENTATION = change(
    "test_one_presentation_contract_for_both_proof_states",
    '''        assert headings.count("証明済みの抽象群構造") == 1
        assert any("探索状態" in segment.value for line in view.rendered_lines
                   for segment in line.segments)
''',
    '''        assert headings.count("証明済みの抽象群構造") == 0
        assert headings.count("検証済みの途中経過") == 0
        assert headings.count("確認済み ProofStep（与件を含む）") == 1
        assert any("探索状態" in segment.value for line in view.rendered_lines
                   for segment in line.segments)
        assert any(r"\\cong" in segment.value for line in view.rendered_lines
                   for segment in line.segments)
''',
)

PARTIAL = change(
    "test_real_partial_web_does_not_leak_internal_diagnostics",
    '''    assert sum(line.kind == "heading" and line.prefix == "証明済みの抽象群構造"
               for line in view.rendered_lines) == 1
''',
    '''    headings = [line.prefix for line in view.rendered_lines if line.kind == "heading"]
    assert headings.count("使用する結果") == 1
    assert headings.count("証明済みの抽象群構造") == 0
    assert headings.count("確認済み ProofStep（与件を含む）") == 1
    assert view.abstract_structure_certified
''',
)

BANNER_CERT = change(
    "test_certificate_flag_comes_from_actual_verified_partial_result",
    '''        assert any(
            line.kind == "heading" and line.prefix == "証明済みの抽象群構造"
            for line in view.rendered_lines
        )
''',
    '''        headings = [line.prefix for line in view.rendered_lines if line.kind == "heading"]
        assert headings.count("使用する結果") == 1
        assert headings.count("証明済みの抽象群構造") == 0
        assert headings.count("未解決 Goal") == 1
        assert any(r"\\cong" in segment.value for line in view.rendered_lines
                   for segment in line.segments)
''',
)

BANNER_FLASK = change(
    "test_real_flask_result_explains_abstract_only_status",
    '''    assert "証明済みの抽象群構造" in text
''',
    '''    assert "使用する結果" in text
    assert r"\\cong" in text
''',
)

PUNCTUATION = change(
    "test_abstract_certificate_displays_actual_verified_milestones",
    '''    progress = render_certified_abstract_model_section(model)
    assert progress == render_certified_abstract_section(result)
    assert "## 検証済みの途中経過" in progress
    assert "### 検証済み証明木の Reference" in progress
    assert "### 検証済み ProofStep" in progress
    assert "Proposition 4.4" in progress
    assert "Lemma 5.4" in progress
    assert progress.count("DB prior: sphere.csv") >= 2
    assert "## 証明済みの抽象群構造" in progress
    assert "記名生成元の対応は未証明" in progress
    assert "先行データベースの " not in progress
    assert "Proposition 4.4 の適用前提となる定理を検証した" not in progress
    assert progress in render_model_backed_narrative_markdown(result, model)
''',
    '''    progress = render_certified_abstract_model_section(model)
    assert progress == ""
    # The explicit legacy helper remains available without a public sidecar.
    legacy_section = render_certified_abstract_section(result)
    assert "## 検証済みの途中経過" in legacy_section
    assert "### 検証済み証明木の Reference" in legacy_section
    assert "## 証明済みの抽象群構造" in legacy_section
    assert any(step is result.abstract_structure.proof_step for step in model.steps)
    assert len(model.citations) >= 4
    markdown = render_model_backed_narrative_markdown(result, model)
    assert markdown.count("## 使用する結果") == 1
    assert "### 検証済み証明木の Reference" not in markdown
    assert "## 検証済みの途中経過" not in markdown
    assert "## 証明済みの抽象群構造" not in markdown
    assert "Proposition 4.4" in markdown
    assert "Lemma 5.4" in markdown
    assert markdown.count("DB prior: sphere.csv") >= 2
    assert r"\\cong" in markdown
    assert "先行データベースの " not in markdown
''',
)

PUNCTUATION_VIEW = change(
    "test_abstract_certificate_displays_actual_verified_milestones",
    '''    assert headings.count("検証済みの途中経過") == 1
    assert headings.count("証明済みの抽象群構造") == 1
    assert headings.count("未解決 Goal") == 1
''',
    '''    assert headings.count("使用する結果") == 1
    assert headings.count("検証済みの途中経過") == 0
    assert headings.count("証明済みの抽象群構造") == 0
    assert headings.count("確認済み ProofStep（与件を含む）") == 1
    assert headings.count("未解決 Goal") == 1
''',
)

PUNCTUATION_LEGACY = change(
    "test_legacy_and_model_paths_share_abstract_progress",
    '''    for view in views:
        assert view.key == "generic-partial-proof"
        assert any(
            line.kind == "heading" and line.prefix == "検証済みの途中経過"
            for line in view.rendered_lines
        )
''',
    '''    for source, view in zip(("model", "legacy"), views):
        assert view.key == "generic-partial-proof"
        headings = [line.prefix for line in view.rendered_lines if line.kind == "heading"]
        if source == "model":
            assert headings.count("使用する結果") == 1
            assert headings.count("検証済みの途中経過") == 0
            assert headings.count("証明済みの抽象群構造") == 0
        else:
            assert headings.count("検証済みの途中経過") == 1
            assert headings.count("証明済みの抽象群構造") == 1
''',
)

TREE_MODEL_VIEW = change(
    "test_real_abstract_tree_reuses_common_renderer",
    '''    assert headings.count("検証済みの途中経過") == 1
    assert headings.count("証明済みの抽象群構造") == 1
    assert headings.count("未解決 Goal") == 1
''',
    '''    assert headings.count("使用する結果") == 1
    assert headings.count("検証済みの途中経過") == 0
    assert headings.count("証明済みの抽象群構造") == 0
    assert headings.count("確認済み ProofStep（与件を含む）") == 1
    assert headings.count("未解決 Goal") == 1
''',
)

PROJECTION = change(
    "test_shared_model_backed_web_displays_abstract_and_keeps_named_pending",
    '''    assert any(line.kind == "heading" and line.prefix == "証明済みの抽象群構造"
               for line in view.rendered_lines)
''',
    '''    headings = [line.prefix for line in view.rendered_lines if line.kind == "heading"]
    assert headings.count("使用する結果") == 1
    assert headings.count("証明済みの抽象群構造") == 0
    assert headings.count("検証済みの途中経過") == 0
    assert view.abstract_structure_certified
    assert any(step is proved_abstract_result.abstract_structure.proof_step
               for step in model.steps)
''',
)

CHANGES = {
    P + "r15r9_shared_abstract_renderer/tests/test_projection.py": (PROJECTION,),
    P + "r15r11_model_abstract_integration/tests/test_integration.py": (MODEL_FIRST, MODEL_LEGACY),
    P + "r15r12_reference_correction/tests/test_integration.py": (REF_CORRECTION,),
    P + "r15r13_unified_presentation/tests/test_integration.py": (PRESENTATION,),
    P + "r15r14_common_partial_presentation/tests/test_integration.py": (PARTIAL,),
    P + "r15r15_abstract_result_banner/tests/test_integration.py": (BANNER_CERT, BANNER_FLASK),
    P + "r15r15r2_head_guard_fix/tests/test_integration.py": (BANNER_CERT, BANNER_FLASK),
    P + "r15r16_verified_progress_punctuation/tests/test_integration.py": (PUNCTUATION, PUNCTUATION_VIEW, PUNCTUATION_LEGACY),
    P + "r15r16r2_shared_tree_narrative/tests/test_integration.py": (TREE_MODEL_VIEW,),
    P + "r15r16r3_staged_guard_fix/tests/test_integration.py": (TREE_MODEL_VIEW,),
}

assert set(FILES) == set(CHANGES)


def transform(path: str, original: str) -> str:
    """Replace exact anchors inside complete selected test functions only."""
    if path not in FILES:
        raise ValueError("unreviewed test path: " + path)
    normalized = original.replace("\r\n", "\n")
    if "\r" in normalized:
        raise RuntimeError("mixed/unexpected line endings")
    syntax = ast.parse(normalized, filename=path)
    lines = normalized.splitlines(keepends=True)
    functions = {node.name: node for node in syntax.body if isinstance(node, (ast.FunctionDef, ast.AsyncFunctionDef))}
    mutations: dict[str, str] = {}
    for entry in CHANGES[path]:
        node = functions.get(entry.function)
        if node is None:
            raise RuntimeError("missing test function: " + entry.function)
        source = mutations.get(entry.function)
        if source is None:
            source = "".join(lines[node.lineno-1:node.end_lineno])
        if source.count(entry.before) != 1:
            raise RuntimeError("unreviewed or already patched test: " + path + ":" + entry.function)
        mutations[entry.function] = source.replace(entry.before, entry.after, 1)
    updated = normalized
    for name in sorted(mutations, key=lambda name:functions[name].lineno, reverse=True):
        node = functions[name]
        old_function = "".join(lines[node.lineno-1:node.end_lineno])
        if updated.count(old_function) != 1:
            raise RuntimeError("ambiguous complete test function replacement: " + path + ":" + name)
        updated = updated.replace(old_function, mutations[name], 1)
    ast.parse(updated, filename=path)
    if updated == normalized:
        raise RuntimeError("empty contract patch: " + path)
    return updated
