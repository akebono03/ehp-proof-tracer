# Phase 175 R3R12R5 — コード全文

## 変更対象

- `projection.py` の `project_verified_hopf_lift_conclusion()` 全体（import は既存のまま）
- `tests/test_projection.py` の関連テスト5件（既存 import に新規外部 import は不要）
- `audit.py` の `GATE`、`_public_gate()`、`run()`、`main()`
- `run.ps1` の出力識別子

新規クラス・関数なし。全コードをそのまま置き換えられるファイル単位で収録する。変更対象以外のクラス・関数は維持。

## `projection.py`（変更後の全文）

```python
"""Shared certified finite-cyclic Hopf-lift conclusion presentation.

This module reads a completed, verified Proof Tree and already rendered lines.
It never performs a search, registers a mathematical rule or adds a ProofStep.
It refuses presentation changes if any source, image or displayed anchor is
ambiguous. It is intentionally independent of concrete sphere dimensions.
"""
from __future__ import annotations

from homotopy_groups import FiniteCyclicGroup, TodaPrimaryGroup
from phase165_r12_r2_quotient_rules import CyclicStructureStatement
from phase165_r14_r6_generic_iso import MapInjective
from phase165_r52_partial_proof import ProofSearchStatus
from phase168_r3_3_proof_narrative_model import root_ancestor_step_indices
from phase168_r3_27_typed_statement_projection import group_tex, map_symbol_tex, typed_sentence
from phase175_r3_pi73_hopf_lift.rule import RULE_NAME, hopf_lift_inputs
from proof import ProofRule, Relation, RelationType
from toda_human_readable_renderer import render_toda_public_group_generator_latex
from web_group_proof_common import _group_proof_statement_latex

VERIFIED_PRIOR_LIFT_NAME = "verified prior DB Hopf cyclic generator preimage lift"


def _unique_index_by_identity(steps: tuple, wanted: object, scope: frozenset[int]) -> int | None:
    """Require an actual ProofStep object, not a merely equal fake step."""
    found = [i for i in scope if steps[i] is wanted]
    return found[0] if len(found) == 1 else None


def _source_numbers(model, step_index: int, scope: frozenset[int]) -> tuple[int, ...]:
    """Return citation numbers of real GIVEN ancestors of one proved step."""
    try:
        ancestry = root_ancestor_step_indices(model.steps, step_index)
    except ValueError:
        return ()
    if not ancestry.issubset(scope):
        return ()
    source_numbers = set()
    for index in ancestry:
        step = model.steps[index]
        if step.rule is ProofRule.GIVEN:
            source_numbers.update(model.step_citation_numbers[index])
    known = {citation.number for citation in model.citations}
    if not source_numbers.issubset(known):
        return ()
    return tuple(sorted(source_numbers))


def _certified_hopf_lift(model):
    """Identify one consumed instance of the existing general Hopf lift rule."""
    if (getattr(model, "status", None) is not ProofSearchStatus.COMPLETE
            or getattr(model, "open_goals", ())):
        return None
    steps = getattr(model, "steps", None)
    citations = getattr(model, "step_citation_numbers", None)
    registered_citations = getattr(model, "citations", None)
    root_index = getattr(model, "root_index", None)
    if (not isinstance(steps, tuple) or not isinstance(citations, tuple)
            or len(steps) != len(citations)
            or not isinstance(registered_citations, tuple) or not registered_citations
            or type(root_index) is not int
            or not 0 <= root_index < len(steps)):
        return None
    try:
        scope = root_ancestor_step_indices(steps, root_index)
    except ValueError:
        return None
    root = steps[root_index]
    claim = root.conclusion
    if (root.rule is not ProofRule.INFERENCE
            or not isinstance(claim, Relation)
            or claim.relation_type is not RelationType.EQUALITY
            or not isinstance(claim.lhs, TodaPrimaryGroup)
            or not isinstance(claim.rhs, FiniteCyclicGroup)):
        return None
    candidates = []
    for index in scope:
        step = steps[index]
        cyclic = step.conclusion
        name = getattr(getattr(step, "inference_rule", None), "name", None)
        if (index == root_index or step.rule is not ProofRule.INFERENCE
                or not isinstance(cyclic, CyclicStructureStatement)
                or cyclic.group != claim.lhs or cyclic.order != claim.rhs.order
                or name not in (RULE_NAME, VERIFIED_PRIOR_LIFT_NAME)
                or len(step.premises) != 3 or citations[index]):
            continue
        injectivity, codomain, image = step.premises
        if (injectivity.rule is not ProofRule.INFERENCE
                or image.rule is not ProofRule.INFERENCE
                or not isinstance(injectivity.conclusion, MapInjective)):
            continue
        # The original general lift proves the codomain by INFERENCE.
        # The verified-prior variant explicitly admits a citation-bearing
        # earlier database GIVEN, validated by its own existing rule/trust gate.
        if (name == RULE_NAME and codomain.rule is not ProofRule.INFERENCE):
            continue
        if (name == VERIFIED_PRIOR_LIFT_NAME
                and (codomain.rule is not ProofRule.GIVEN
                     or bool(codomain.premises))):
            continue
        required = hopf_lift_inputs(cyclic, codomain.conclusion, image.conclusion)
        if required is None or tuple(parent.conclusion for parent in step.premises) != required:
            continue
        positions = tuple(
            _unique_index_by_identity(steps, parent, scope)
            for parent in step.premises
        )
        if any(pos is None for pos in positions) or len(set(positions)) != 3:
            continue
        # The lift must be on the actual root path; all three certified
        # premises must be the exact premises consumed by that inference.
        candidates.append((scope, root, step, positions))
    return candidates[0] if len(candidates) == 1 else None


def project_verified_hopf_lift_conclusion(lines: list[str], model) -> list[str]:
    """Explain generator-surjectivity/isomorphism and hide one duplicate.

    The isomorphism is the direct verbal consequence of the *existing* typed
    general lift's proved injectivity + proved finite cyclic target + proved
    generator image. This function creates neither MapSurjective nor a theorem.
    """
    original = list(lines)
    if original.count("証明") != 1 or original.count("□") != 1:
        return original
    certificate = _certified_hopf_lift(model)
    if certificate is None:
        return original
    scope, root, cyclic_step, positions = certificate
    injective_step, codomain_step, image_step = cyclic_step.premises
    group_relation = root.conclusion
    codomain_relation = codomain_step.conclusion
    image_relation = image_step.conclusion
    # The existing lift's typed generator identity is already checked by
    # hopf_lift_inputs().  Its internal CyclicStructureStatement may use a
    # different generator spelling from the published root Relation.  Match
    # the two *displayed* copies of the root's certified conclusion instead.
    root_latex, root_fallback = _group_proof_statement_latex(group_relation)
    codomain_latex, codomain_fallback = _group_proof_statement_latex(codomain_relation)
    if (root_fallback is not None or codomain_fallback is not None
            or not root_latex or not codomain_latex):
        return original
    source_group = group_tex(group_relation.lhs)
    target_group = group_tex(codomain_relation.lhs)
    if not source_group or not target_group:
        return original
    # The general Hopf-lift premise already certifies the *typed* generator
    # identity. A source generator can have a different internal spelling from
    # the canonical public group generator; do not compare their TeX strings.
    # Use the same public generator renderer as the cited codomain equation.
    try:
        generator_tex = render_toda_public_group_generator_latex(
            codomain_relation.rhs.generator,
        )
    except (TypeError, ValueError, AttributeError):
        return original
    if not generator_tex:
        return original
    boundary = original.index("証明")
    final = f"以上より, ${root_latex}$."
    intermediate = f"${root_latex}$."
    intermediate_indices = [
        i for i in range(boundary + 1, len(original))
        if original[i] == intermediate
    ]
    final_indices = [
        i for i in range(boundary + 1, len(original))
        if original[i] == final
    ]
    # R3R11 has already certified every equality in its compact Hopf chain.
    # Match the source numbers of the actual proved image step, not a guessed
    # generator-name spelling or a narrative line from an unrelated proof.
    image_sources = _source_numbers(model, positions[2], scope)
    image_prefix = (
        ", ".join(f"[R{number}]" for number in image_sources)
        + "より, $H("
    )
    image_indices = [
        i for i in range(boundary + 1, len(original))
        if len(image_sources) >= 2
        and original[i].startswith(image_prefix)
        and original[i].endswith(f"={generator_tex}$.")
        and original[i].count("$") == 2
    ]
    # The common renderer inserts spacing after "H:" and decorates the
    # sentence using the proved exactness premises. Reuse that same typed
    # sentence instead of guessing its textual punctuation or whitespace.
    # The certificate has already identified this exact MapInjective step.
    injectivity_sentence = typed_sentence(
        injective_step.conclusion, injective_step,
    )
    if (not isinstance(injectivity_sentence, str)
            or not injectivity_sentence.endswith("は単射.")):
        return original
    injection_indices = [
        i for i in range(boundary + 1, len(original))
        if original[i] == injectivity_sentence
    ]
    if (len(intermediate_indices) != 1 or len(final_indices) != 1
            or len(image_indices) != 1 or len(injection_indices) != 1):
        return original
    duplicate_at = intermediate_indices[0]
    final_at = final_indices[0]
    if not (injection_indices[0] < image_indices[0] < duplicate_at < final_at):
        return original
    source_numbers = _source_numbers(model, positions[1], scope)
    # The target group structure must already be displayed with its real
    # unique source. Without that source binding, leave all text untouched.
    if len(source_numbers) != 1:
        return original
    expected = f"[R{source_numbers[0]}]より, ${codomain_latex}$."
    if original.count(expected) != 1:
        return original
    # Existing typed premises certify surjectivity and, together with
    # injectivity, an isomorphism.  Render only their short common
    # consequences; do not manufacture MapSurjective/MapIsomorphism steps.
    symbol = map_symbol_tex(injective_step.conclusion.map)
    if not symbol:
        return original
    map_tex = rf"{symbol}: {source_group}\to {target_group}"
    surjective = f"よって, ${map_tex}$ は全射."
    isomorphism = f"よって, ${map_tex}$ は同型."
    changed = []
    for index, line in enumerate(original):
        if index == duplicate_at:
            changed.extend((surjective, "", isomorphism))
        else:
            changed.append(line)
    return changed

```

## `tests/test_projection.py`（変更後の全文）

```python
"""Live public model and fail-closed cyclic Hopf-lift narrative contracts."""
from __future__ import annotations

from dataclasses import replace

import pytest

from phase165_r52_partial_proof import ProofSearchStatus
from phase165_r52_r9_shared_math import build_shared_typed_bridge
from phase165_r55_nk_only_goal import search_group_from_registered_goal
from phase166_r3t_goal_source_binding.goal_source import resolve_specialized_goal_citing_id
from phase168_r3_4_link_bridge import build_linked_proof_narrative_model
from phase168_r3_5_model_renderer import render_model_backed_narrative_markdown
from phase168_r3_41p13_trust_boundary import verify_proof_tree_for_narrative
from phase175_r3r12_hopf_conclusion.projection import (
    _certified_hopf_lift,
    project_verified_hopf_lift_conclusion,
)


@pytest.fixture(scope="module")
def pi73_verified():
    bridge = build_shared_typed_bridge()
    contexts = []
    result = search_group_from_registered_goal(
        n=3, k=4, bridge=bridge, context_sink=contexts.append,
    )
    assert result.status is ProofSearchStatus.COMPLETE
    assert not result.open_goals
    assert len(contexts) == 1
    citing_id = resolve_specialized_goal_citing_id(bridge, result.conclusion)
    assert citing_id is not None
    verify_proof_tree_for_narrative(
        result, contexts[0], citing_assertion_id=citing_id,
    )
    model = build_linked_proof_narrative_model(result, contexts[0])
    return result, model


def test_pi73_single_final_conclusion_and_hopf_isomorphism(pi73_verified) -> None:
    result, model = pi73_verified
    before = tuple(id(step) for step in model.steps)
    assert _certified_hopf_lift(model) is not None
    markdown = render_model_backed_narrative_markdown(result, model)
    references, body = markdown.split("\n証明\n", 1)
    summary = (
        r"[R5], [R6], [R7]より, $H(\nu'\eta_{6})=H(\nu'E\eta_{5})"
        r"=H(\nu')E\eta_{5}=\eta_{5}E\eta_{5}=\eta_{5}^{2}$."
    )
    conclusion = r"$\pi_{7}^{3} = \mathbb{Z}/2\{\nu'\eta_{6}\}$."
    assert body.count(summary) == 1
    assert body.count(conclusion) == 1, (
        "Duplicated root conclusion; root and cyclic generator renderers may differ",
        body,
    )
    assert "以上より, " + conclusion in body
    assert "\n" + conclusion + "\n" not in body
    assert body.count(r"よって, $H: \pi_{7}^{3}\to \pi_{7}^{5}$ は全射.") == 1
    assert body.count(r"よって, $H: \pi_{7}^{3}\to \pi_{7}^{5}$ は同型.") == 1
    assert "の生成元であり" not in body
    assert "すでに $H$ は単射なので" not in body
    assert (body.index(summary) < body.index(r"よって, $H: \pi_{7}^{3}\to \pi_{7}^{5}$ は全射.")
            < body.index(r"よって, $H: \pi_{7}^{3}\to \pi_{7}^{5}$ は同型.")
            < body.index("以上より, " + conclusion))
    assert "**[R2] Lemma 5.7.**" in references
    assert "**[R6] Proposition 2.2.**" in references
    assert len(model.citations) == 7
    assert before == tuple(id(step) for step in model.steps)


def test_public_generator_and_source_anchors_match_verified_image(pi73_verified) -> None:
    """The public generator is allowed a different internal source spelling."""
    from phase175_r3r12_hopf_conclusion.projection import _source_numbers
    from toda_human_readable_renderer import render_toda_public_group_generator_latex

    result, model = pi73_verified
    certificate = _certified_hopf_lift(model)
    assert certificate is not None
    scope, _, cyclic_step, positions = certificate
    codomain = cyclic_step.premises[1].conclusion
    generator = render_toda_public_group_generator_latex(codomain.rhs.generator)
    numbers = _source_numbers(model, positions[2], scope)
    markdown = render_model_backed_narrative_markdown(result, model)
    _, body = markdown.split("\n証明\n", 1)
    prefix = ", ".join(f"[R{number}]" for number in numbers) + "より, $H("
    assert len(numbers) >= 2, (numbers, generator)
    assert any(
        line.startswith(prefix) and line.endswith(f"={generator}$.")
        for line in body.splitlines()
    ), (prefix, generator, body)


def test_internal_cyclic_latex_is_not_a_second_proof_requirement(
    pi73_verified, monkeypatch: pytest.MonkeyPatch,
) -> None:
    """Typed Hopf-lift certificate, not an internal string, owns generator identity."""
    from phase165_r12_r2_quotient_rules import CyclicStructureStatement
    from phase175_r3r12_hopf_conclusion import projection

    result, model = pi73_verified
    original_renderer = projection._group_proof_statement_latex

    def internal_cyclic_unrenderable(statement):
        if isinstance(statement, CyclicStructureStatement):
            return None, "internal cyclic spelling intentionally unavailable"
        return original_renderer(statement)

    monkeypatch.setattr(
        projection, "_group_proof_statement_latex", internal_cyclic_unrenderable,
    )
    content = render_model_backed_narrative_markdown(result, model)
    _, body = content.split("\n証明\n", 1)
    conclusion = r"$\pi_{7}^{3} = \mathbb{Z}/2\{\nu'\eta_{6}\}$."
    assert body.count(conclusion) == 1, body
    assert r"よって, $H: \pi_{7}^{3}\to \pi_{7}^{5}$ は同型." in body


def test_concise_consequences_follow_typed_hopf_map(pi73_verified) -> None:
    """The same certified map symbol owns both short consequences."""
    from phase168_r3_27_typed_statement_projection import group_tex, map_symbol_tex

    result, model = pi73_verified
    certificate = _certified_hopf_lift(model)
    assert certificate is not None
    _, _, cyclic_step, _ = certificate
    typed_map = cyclic_step.premises[0].conclusion.map
    map_symbol = map_symbol_tex(typed_map)
    assert map_symbol == "H"
    source = group_tex(typed_map.source_group)
    target = group_tex(typed_map.target_group)
    map_text = rf"{map_symbol}: {source}\to {target}"
    assert map_text == r"H: \pi_{7}^{3}\to \pi_{7}^{5}"
    markdown = render_model_backed_narrative_markdown(result, model)
    _, body = markdown.split("\n証明\n", 1)
    sentences = body.splitlines()
    assert sentences.count(f"よって, ${map_text}$ は全射.") == 1
    assert sentences.count(f"よって, ${map_text}$ は同型.") == 1
    assert all("生成元であり" not in sentence for sentence in sentences)


def test_partial_or_missing_source_citations_are_unchanged(pi73_verified) -> None:
    _, model = pi73_verified
    text = ["使用する結果", "", "証明", "", "確認済み", "", "□"]
    assert project_verified_hopf_lift_conclusion(
        text, replace(model, status=ProofSearchStatus.PARTIAL),
    ) == text
    assert project_verified_hopf_lift_conclusion(
        text, replace(model, citations=()),
    ) == text
    assert project_verified_hopf_lift_conclusion(
        text, replace(model, root_index=None),
    ) == text
    assert _certified_hopf_lift(replace(model, citations=())) is None


def test_injectivity_line_matches_the_real_typed_renderer(pi73_verified) -> None:
    """The actual renderer emits a space after H:, unlike an old hand-coded guard."""
    from phase168_r3_27_typed_statement_projection import typed_sentence

    result, model = pi73_verified
    certificate = _certified_hopf_lift(model)
    assert certificate is not None
    _, _, cyclic_step, _ = certificate
    injective_step = cyclic_step.premises[0]
    sentence = typed_sentence(injective_step.conclusion, injective_step)
    assert sentence is not None
    assert r"$H: \pi_{7}^{3}\to \pi_{7}^{5}$ は単射." in sentence
    markdown = render_model_backed_narrative_markdown(result, model)
    _, body = markdown.split("\n証明\n", 1)
    assert sentence in body.splitlines()
    assert r"よって, $H: \pi_{7}^{3}\to \pi_{7}^{5}$ は同型." in body


def test_missing_injectivity_line_preserves_original(pi73_verified) -> None:
    """A genuinely missing injectivity display must not invent an isomorphism."""
    from phase168_r3_27_typed_statement_projection import typed_sentence

    result, model = pi73_verified
    certificate = _certified_hopf_lift(model)
    assert certificate is not None
    injective_step = certificate[2].premises[0]
    sentence = typed_sentence(injective_step.conclusion, injective_step)
    assert sentence is not None
    markdown = render_model_backed_narrative_markdown(result, model)
    # Drop only the sentence to check the fail-closed presentation contract.
    before = markdown.splitlines()
    assert before.count(sentence) == 1
    damaged = [line for line in before if line != sentence]
    assert project_verified_hopf_lift_conclusion(damaged, model) == damaged


def test_missing_rendered_summary_does_not_infer_surjectivity(pi73_verified) -> None:
    _, model = pi73_verified
    text = [
        "使用する結果", "", "証明", "",
        r"完全性より, $H:\pi_{7}^{3}\to\pi_{7}^{5}$ は単射.", "",
        r"[R4]より, $\pi_{7}^{5} = \mathbb{Z}/2\{\eta_{5}^{2}\}$.", "",
        r"$\pi_{7}^{3} = \mathbb{Z}/2\{\nu'\eta_{6}\}$.", "",
        r"以上より, $\pi_{7}^{3} = \mathbb{Z}/2\{\nu'\eta_{6}\}$.",
        "", "□",
    ]
    assert project_verified_hopf_lift_conclusion(text, model) == text


def test_pi63_old_narrative_remains_unchanged() -> None:
    bridge = build_shared_typed_bridge()
    contexts = []
    result = search_group_from_registered_goal(
        n=3, k=3, bridge=bridge, context_sink=contexts.append,
    )
    assert result.status is ProofSearchStatus.COMPLETE
    citing_id = resolve_specialized_goal_citing_id(bridge, result.conclusion)
    assert citing_id is not None
    verify_proof_tree_for_narrative(
        result, contexts[0], citing_assertion_id=citing_id,
    )
    model = build_linked_proof_narrative_model(result, contexts[0])
    markdown = render_model_backed_narrative_markdown(result, model)
    _, body = markdown.split("\n証明\n", 1)
    assert r"[R3]より, $E(\eta_{5})=\eta_{6}$." in body
    assert "[R4]より, " in body
    assert "[R3], [R4], [R5]より, " in body
    assert r"よって, $H: \pi_{7}^{3}\to \pi_{7}^{5}$ は同型." not in body

```

## `audit.py`（変更後の全文）

```python
"""R3R12 read-only preflight, focused tests and public source-bound gate."""
from __future__ import annotations

import argparse
from datetime import datetime, timezone
from hashlib import sha256
import json
import os
from pathlib import Path
import subprocess
import sys
import tempfile
import traceback

from phase175_r3r12_hopf_conclusion import install

GATE = "PASS_R3R12R5_VERIFIED_HOPF_MAP_DOMAIN_CODOMAIN"
TEST_PATHS = (
    "phase175_r3r12_hopf_conclusion/tests",
    "phase175_r3r11_cited_hopf_narrative/tests",
    "phase175_r3r10_generator_zero_narrative/tests/test_public.py",
    "phase175_r3r10_generator_zero_narrative/tests/test_projection.py",
    "phase175_r3r9_lemma57_explicit_public/tests/test_public_search.py",
    "phase171_r20r13_eta_sentence_layout/tests/test_projection.py",
    "phase172_r3_hopf_chain_display/tests/test_projection.py",
    "phase174_r3_r7_r70_verified_narrative_projection/tests/test_projection.py::test_line_endings_source_guard_and_patch_idempotence",
    "phase174_r3_r7_r70_verified_narrative_projection/tests/test_projection.py::test_source_guard_rejects_unreviewed_change",
    "phase174_r3_r7_r70_verified_narrative_projection/tests/test_projection.py::test_rejects_mixed_eol_and_cr_only",
    "phase174_r3_r7_r70_verified_narrative_projection/tests/test_projection.py::test_body_line_search_does_not_match_reference_text",
    "phase174_r3_r7_r70_verified_narrative_projection/tests/test_projection.py::test_step_index_rejects_ambiguous_value_fallback",
    "phase174_r3_r7_r70_verified_narrative_projection/tests/test_projection.py::test_incomplete_model_has_no_composed_rewrite",
    "phase174_r3_r7_r70_verified_narrative_projection/tests/test_projection.py::test_git_sha_fixture",
)


def _read_git(root: Path, *args: str) -> str:
    result = subprocess.run(
        ["git", *args], cwd=root, capture_output=True, text=True,
        encoding="utf-8", errors="replace", check=False,
    )
    if result.returncode:
        raise RuntimeError("R3R12_GIT_READ_FAILED: " + " ".join(args))
    return result.stdout.strip()


def preflight(root: Path) -> dict[str, object]:
    if not (root / ".git").exists():
        raise RuntimeError("R3R12_GIT_REPOSITORY_REQUIRED")
    if _read_git(root, "branch", "--show-current") != "develop":
        raise RuntimeError("R3R12_DEVELOP_REQUIRED")
    if not (root / "phase175_r3r9_lemma57_explicit_public" / "route.py").is_file():
        raise RuntimeError("R3R12_R3R9_REQUIRED")
    if not (root / "phase175_r3r11_cited_hopf_narrative" / "run.ps1").is_file():
        raise RuntimeError("R3R12_R3R11_REQUIRED")
    prior_projection = (root / "phase175_r3r11_cited_hopf_narrative" / "projection.py")
    normalized, _ = install._canonical(prior_projection.read_bytes())
    current_blob = install.git_blob_sha(normalized)
    plan = install.plan_patch(root)
    return {
        "head": _read_git(root, "rev-parse", "HEAD"),
        "reviewed_blob": current_blob,
        "plan": plan,
    }


def _public_gate() -> dict[str, object]:
    from phase175_r1_k4_audit.audit import inspect_one_group
    from phase175_r3r9_lemma57_explicit_public.audit import verify_public_result

    recorded = inspect_one_group(3, 4)
    previous = verify_public_result(recorded)
    markdown = recorded.get("markdown")
    if not isinstance(markdown, str) or markdown.count("\n証明\n") != 1:
        raise RuntimeError("R3R12_PUBLIC_MARKDOWN_MISSING")
    references, body = markdown.split("\n証明\n", 1)
    if (recorded.get("web_key") != "generic-complete-proof"
            or recorded.get("trust_verified") is not True
            or recorded.get("reference_count") != 7
            or previous["search_status"] != "complete"
            or previous["lemma54_used"] is not False):
        raise RuntimeError("R3R12_PROOF_OR_TRUST_CHANGED")
    summary = (
        r"[R5], [R6], [R7]より, $H(\nu'\eta_{6})=H(\nu'E\eta_{5})"
        r"=H(\nu')E\eta_{5}=\eta_{5}E\eta_{5}=\eta_{5}^{2}$."
    )
    conclusion = r"$\pi_{7}^{3} = \mathbb{Z}/2\{\nu'\eta_{6}\}$."
    surjective = r"よって, $H: \pi_{7}^{3}\to \pi_{7}^{5}$ は全射."
    isomorphism = r"よって, $H: \pi_{7}^{3}\to \pi_{7}^{5}$ は同型."
    if (body.count(summary) != 1 or body.count(conclusion) != 1
            or body.count("以上より, " + conclusion) != 1
            or body.count(surjective) != 1 or body.count(isomorphism) != 1
            or "の生成元であり" in body or "すでに $H$ は単射なので" in body
            or not (body.index(summary) < body.index(surjective)
                    < body.index(isomorphism)
                    < body.index("以上より, " + conclusion))):
        raise RuntimeError("R3R12_SINGLE_CONCLUSION_OR_HOPF_EXPLANATION_FAILED")
    if (r"$E(\eta_2\nu')=0$." not in references
            or r"$H(\alpha E\beta)=H(\alpha) E\beta$." not in references
            or "特に, " in references or "右合成公式: " in references):
        raise RuntimeError("R3R12_OLDER_REFERENCE_BODIES_CHANGED")
    return {
        "search": previous["search_status"],
        "web": recorded["web_key"],
        "trust": recorded["trust_verified"],
        "reference_count": recorded["reference_count"],
        "lemma54_used": previous["lemma54_used"],
        "hopf_summary": summary,
        "hopf_surjective": surjective,
        "hopf_isomorphism": isomorphism,
        "final_conclusion": "以上より, " + conclusion,
        "final_conclusion_count": body.count(conclusion),
        "markdown_sha256": sha256(markdown.encode("utf-8")).hexdigest(),
    }


def run(root: Path, dry_run: bool, timeout_seconds: int) -> int:
    root = root.resolve()
    checked = preflight(root)
    plan = checked["plan"]
    label = "PHASE175_R3R12R5_"
    print(label + "BRANCH=develop")
    print(label + "HEAD=" + checked["head"])
    print(label + "REVIEWED_BLOB=" + checked["reviewed_blob"])
    print(label + "PATCH_STATUS=" + plan.status)
    print(label + "NEW_GIVEN=0")
    print(label + "NEW_MATHEMATICAL_RULES=0")
    if dry_run:
        print(label + "GATE=PASS_R3R12R5_READ_ONLY_DRYRUN")
        return 0

    folder = (Path(os.environ.get("LOCALAPPDATA") or tempfile.gettempdir())
              / "EHPProofTracerAudit" / "phase175_r3r12r5_hopf_conclusion")
    folder.mkdir(parents=True, exist_ok=True)
    target = root / install.TARGET
    if plan.status == "PATCH_REQUIRED":
        (folder / "r3r11_projection_backup.py").write_bytes(plan.old_bytes)
    try:
        install.apply_patch(root, plan)
        environment = dict(os.environ)
        environment.update(
            PYTHONUTF8="1", PYTHONIOENCODING="utf-8", PYTHONDONTWRITEBYTECODE="1",
        )
        command = [
            sys.executable, "-B", "-m", "pytest", "-q", "--disable-warnings",
            "-p", "no:cacheprovider", "-o", "addopts=", "--import-mode=importlib",
            *TEST_PATHS,
        ]
        result = subprocess.run(
            command, cwd=root, env=environment, capture_output=True,
            text=True, encoding="utf-8", errors="replace",
            timeout=timeout_seconds, check=False,
        )
        (folder / "focused_pytest.txt").write_text(
            result.stdout + "\n" + result.stderr, encoding="utf-8",
        )
        print(result.stdout[-6000:])
        if result.returncode:
            raise RuntimeError("R3R12_FOCUSED_PYTEST_FAILED")
        print(label + "FOCUSED_PYTEST=PASS")
        public = _public_gate()
        (folder / "report.json").write_text(json.dumps({
            "timestamp": datetime.now(timezone.utc).isoformat(),
            "gate": GATE,
            "head": checked["head"],
            "before_sha256": sha256(plan.old_bytes).hexdigest(),
            "after_sha256": sha256(target.read_bytes()).hexdigest(),
            "public": public,
        }, ensure_ascii=False, indent=2), encoding="utf-8")
        for key, value in public.items():
            print(label + key.upper() + "=" + str(value))
        print(label + "GATE=" + GATE)
        return 0
    except Exception:
        if plan.status == "PATCH_REQUIRED":
            if target.read_bytes() == plan.new_bytes:
                target.write_bytes(plan.old_bytes)
                print(label + "ROLLBACK=RESTORED")
            else:
                print(label + "ROLLBACK=MANUAL_INSPECTION_REQUIRED")
        raise


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--root", type=Path, required=True)
    parser.add_argument("--dry-run", action="store_true")
    parser.add_argument("--timeout-seconds", type=int, default=300)
    args = parser.parse_args()
    try:
        return run(args.root, args.dry_run, args.timeout_seconds)
    except Exception:
        traceback.print_exc()
        print("PHASE175_R3R12R5_GATE=FAIL")
        return 1


if __name__ == "__main__":
    raise SystemExit(main())

```

## `run.ps1`（変更後の全文）

```powershell
param(
    [switch]$DryRun,
    [int]$TimeoutSeconds = 300
)

$ErrorActionPreference = 'Stop'
$env:PYTHONUTF8 = '1'
$env:PYTHONIOENCODING = 'utf-8'
$env:PYTHONDONTWRITEBYTECODE = '1'
$root = (Resolve-Path (Join-Path $PSScriptRoot '..')).Path
Set-Location $root

if ($DryRun) {
    & python -B -m phase175_r3r12_hopf_conclusion.audit `
        --root $root --dry-run --timeout-seconds $TimeoutSeconds
    $code = $LASTEXITCODE
    Write-Output "PHASE175_R3R12R5_EXIT_CODE=$code"
    exit $code
}

& python -B -m phase175_r3r12_hopf_conclusion.audit `
    --root $root --timeout-seconds $TimeoutSeconds
$code = $LASTEXITCODE
Write-Output "PHASE175_R3R12R5_EXIT_CODE=$code"
exit $code

```

## 実行する限定 pytest と完了条件

- ZIP 展開後、`phase175_r3r12_hopf_conclusion/run.ps1 -DryRun` を実行する。
- 正常なら同じ `run.ps1` を本実行する。限定 pytest は監査 `TEST_PATHS` のみ。Phase 175 途中で全体 pytest を実施しない。
- 期待 Gate：`PASS_R3R12R5_VERIFIED_HOPF_MAP_DOMAIN_CODOMAIN`。
- 次の Phase の新規 EHP 規則、専用 Narrative、群構造探索は実装しない。
