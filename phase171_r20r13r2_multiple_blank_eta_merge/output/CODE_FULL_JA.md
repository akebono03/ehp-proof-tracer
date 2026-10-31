# Phase 171 R20R13R2 — 変更後コード全文

変更対象ファイル：`phase171_r20r13_eta_sentence_layout/projection.py`。
変更関数：`combine_adjacent_verified_eta_sentences` 全体。
既存 import・Proof Tree・Reference・Renderer 本体は変更しない。
新規ファイル：`phase171_r20r13r2_multiple_blank_eta_merge/` の installer, audit, tests。

## 変更対象 import 全文

```python
from __future__ import annotations

from phase165_r12_r20_eta_definition import TodaEtaFamilyGeneralDefinition
from phase165_r14_r14_diagonal_and_prop42 import GeneratorSuspension
from phase165_r14_r6_generic_iso import GeneratorImage
from phase168_r3_27_typed_statement_projection import element_tex, typed_sentence
from phase168_r3_3_proof_narrative_model import root_ancestor_step_indices
from homotopy_groups import TodaSuspensionMap
from proof import ProofRule

```

## 変更関数全文

```python
def combine_adjacent_verified_eta_sentences(lines: list[str], model) -> list[str]:
    """Combine neighboring printed certified equations sharing one citation.

    Empty Markdown separators between these equations may be crossed. Other
    mathematics, differently sourced results and nonadjacent lines are kept.
    """
    allowed = verified_eta_display_sentences(model)
    result: list[str] = []
    index = 0
    while index < len(lines):
        first = allowed.get(lines[index])
        if first is None:
            result.append(lines[index])
            index += 1
            continue
        tag, first_math = first
        terms = [first_math]
        cursor = index + 1
        while cursor < len(lines):
            # Earlier presentation-only duplicate suppression can leave
            # several empty Markdown separators between surviving lines.
            # Ignore only empty lines, never a distinct mathematical step.
            next_index = cursor
            while next_index < len(lines) and lines[next_index] == "":
                next_index += 1
            if next_index >= len(lines):
                break
            candidate = allowed.get(lines[next_index])
            if candidate is None or candidate[0] != tag:
                break
            terms.append(candidate[1])
            cursor = next_index + 1
        if len(terms) < 2:
            result.append(lines[index])
            index += 1
            continue
        result.append(tag + "$" + r",\quad ".join(terms) + "$.")
        index = cursor
    return result

```

## 修正後 projection.py 全文

```python
"""Source-bound presentation of adjacent eta equations and sentence boundaries.

This module never infers new mathematics. It combines only existing rendered
sentences whose exact content is backed by INFERENCE ProofSteps in the final
root ancestry and a cited general eta definition. Partial proofs are unchanged.
"""
from __future__ import annotations

from phase165_r12_r20_eta_definition import TodaEtaFamilyGeneralDefinition
from phase165_r14_r14_diagonal_and_prop42 import GeneratorSuspension
from phase165_r14_r6_generic_iso import GeneratorImage
from phase168_r3_27_typed_statement_projection import element_tex, typed_sentence
from phase168_r3_3_proof_narrative_model import root_ancestor_step_indices
from homotopy_groups import TodaSuspensionMap
from proof import ProofRule


def verified_eta_display_sentences(model) -> dict[str, tuple[str, str]]:
    """Map existing source-tagged sentences to (same tag, existing math body).

    A line is eligible only if it is an exact rendering of a certified typed
    suspension step with an actually cited eta-definition GIVEN ancestor.
    """
    if model.root_index is None:
        return {}
    scope = root_ancestor_step_indices(model.steps, model.root_index)
    allowed: dict[str, tuple[str, str]] = {}
    for index in scope:
        step = model.steps[index]
        statement = step.conclusion
        if step.rule is not ProofRule.INFERENCE:
            continue
        if not isinstance(statement, (GeneratorSuspension, GeneratorImage)):
            continue
        if not isinstance(statement.map, TodaSuspensionMap):
            continue
        source = element_tex(statement.source_generator)
        target = element_tex(statement.target_generator)
        if source is None or target is None:
            continue
        if not (source.startswith(r"\eta_{") and target.startswith(r"\eta_{")):
            continue
        sentence = typed_sentence(statement, step)
        if sentence is None or not sentence.startswith("$E(") or not sentence.endswith("$."):
            continue
        cited: list[int] = []
        visited: set[int] = set()
        pending = [step]
        while pending:
            ancestor = pending.pop()
            if id(ancestor) in visited:
                continue
            visited.add(id(ancestor))
            if (ancestor.rule is ProofRule.GIVEN
                    and isinstance(ancestor.conclusion, TodaEtaFamilyGeneralDefinition)):
                for source_index, source_step in enumerate(model.steps):
                    if source_step is ancestor or source_step == ancestor:
                        for number in model.step_citation_numbers[source_index]:
                            if number not in cited:
                                cited.append(number)
                        break
            pending.extend(ancestor.premises)
        if not cited:
            continue
        tag = ", ".join(f"[R{number}]" for number in cited) + "より, "
        full_line = tag + sentence
        math_body = sentence[1:-2]  # take only existing TeX, excluding $ and period
        allowed[full_line] = (tag, math_body)
    return allowed


def combine_adjacent_verified_eta_sentences(lines: list[str], model) -> list[str]:
    """Combine neighboring printed certified equations sharing one citation.

    Empty Markdown separators between these equations may be crossed. Other
    mathematics, differently sourced results and nonadjacent lines are kept.
    """
    allowed = verified_eta_display_sentences(model)
    result: list[str] = []
    index = 0
    while index < len(lines):
        first = allowed.get(lines[index])
        if first is None:
            result.append(lines[index])
            index += 1
            continue
        tag, first_math = first
        terms = [first_math]
        cursor = index + 1
        while cursor < len(lines):
            # Earlier presentation-only duplicate suppression can leave
            # several empty Markdown separators between surviving lines.
            # Ignore only empty lines, never a distinct mathematical step.
            next_index = cursor
            while next_index < len(lines) and lines[next_index] == "":
                next_index += 1
            if next_index >= len(lines):
                break
            candidate = allowed.get(lines[next_index])
            if candidate is None or candidate[0] != tag:
                break
            terms.append(candidate[1])
            cursor = next_index + 1
        if len(terms) < 2:
            result.append(lines[index])
            index += 1
            continue
        result.append(tag + "$" + r",\quad ".join(terms) + "$.")
        index = cursor
    return result


def _split_outside_math_at_period(line: str) -> list[str]:
    """Split ASCII '. ' prose boundaries, not decimals or math expressions."""
    pieces: list[str] = []
    begin = 0
    math_mode = False
    index = 0
    while index < len(line):
        char = line[index]
        if char == "$" and (index == 0 or line[index - 1] != "\\"):
            math_mode = not math_mode
        if (not math_mode and char == "."
                and index + 1 < len(line) and line[index + 1] == " "
                and index > 0):
            # Dot is part of the sentence. Subsequent prose starts a new line.
            pieces.append(line[begin:index + 1].strip())
            begin = index + 2
        index += 1
    pieces.append(line[begin:].strip())
    return [piece for piece in pieces if piece]


def split_completed_proof_sentences(lines: list[str]) -> list[str]:
    """Use real Markdown paragraph breaks at periods only in the proof body.

    Do not touch citation locators (e.g. Proposition 5.6.), reference bodies,
    math notation, or an incomplete proof's diagnostic section.
    """
    result: list[str] = []
    in_body = False
    for line in lines:
        if line == "証明":
            in_body = True
            result.append(line)
            continue
        if not in_body or not line or line == "□":
            result.append(line)
            continue
        sentences = _split_outside_math_at_period(line)
        if len(sentences) < 2:
            result.append(line)
            continue
        for i, sentence in enumerate(sentences):
            if i:
                result.append("")
            result.append(sentence)
    return result


def format_complete_proof_sentences(lines: list[str], model) -> list[str]:
    """Keep the original tree/citations; alter only completed narrative prose."""
    return split_completed_proof_sentences(
        combine_adjacent_verified_eta_sentences(lines, model)
    )

```

## 新規テスト全文

```python
"""R20R13R2 installer guard tests; no live target mutation."""
from __future__ import annotations

import ast
import hashlib

import pytest

from phase171_r20r13r2_multiple_blank_eta_merge.install import (
    CORRECTED_SHA256, ORIGINAL_SHA256, transform,
)
from pathlib import Path

HERE = Path(__file__).resolve().parent.parent


def test_exact_reviewed_source_hashes_and_compilation():
    original = (HERE / "reviewed_projection.py").read_text(encoding="utf-8")
    corrected = (HERE / "corrected_projection.py").read_text(encoding="utf-8")
    assert hashlib.sha256(original.encode("utf-8")).hexdigest() == ORIGINAL_SHA256
    assert hashlib.sha256(corrected.encode("utf-8")).hexdigest() == CORRECTED_SHA256
    assert transform(original) == corrected
    ast.parse(corrected)


def test_unreviewed_anchors_fail_closed():
    with pytest.raises(RuntimeError):
        transform("def unrelated():\n    return None\n")


def test_only_whitespace_separator_walk_changed():
    original = (HERE / "reviewed_projection.py").read_text(encoding="utf-8")
    corrected = transform(original)
    assert original.count("def combine_adjacent_verified_eta_sentences") == 1
    assert corrected.count("def combine_adjacent_verified_eta_sentences") == 1
    assert original.split("def combine_adjacent_verified_eta_sentences")[0] == corrected.split("def combine_adjacent_verified_eta_sentences")[0]
    assert "ProofStep(" not in corrected


def test_does_not_change_verified_citation_eligibility():
    original = (HERE / "reviewed_projection.py").read_text(encoding="utf-8")
    corrected = transform(original)
    first = original.split("def combine_adjacent_verified_eta_sentences")[0]
    assert first == corrected.split("def combine_adjacent_verified_eta_sentences")[0]
    assert "verified_eta_display_sentences(model)" in corrected

```

```python
"""Focused separator-only fix; real proof still verifies via R20R13 audit."""
from __future__ import annotations

from types import SimpleNamespace

import pytest

from phase171_r20r13_eta_sentence_layout.projection import (
    combine_adjacent_verified_eta_sentences,
    verified_eta_display_sentences,
)


@pytest.fixture
def eligible(monkeypatch):
    values = {
        r"[R3]より, $E(\eta_{2})=\eta_{3}$.":
            ("[R3]より, ", r"E(\eta_{2})=\eta_{3}"),
        r"[R3]より, $E(\eta_{3}^{2})=\eta_{4}^{2}$.":
            ("[R3]より, ", r"E(\eta_{3}^{2})=\eta_{4}^{2}"),
        r"[R3]より, $E(\eta_{2}^{3})=\eta_{3}^{3}$.":
            ("[R3]より, ", r"E(\eta_{2}^{3})=\eta_{3}^{3}"),
    }
    monkeypatch.setattr(
        "phase171_r20r13_eta_sentence_layout.projection.verified_eta_display_sentences",
        lambda model: values,
    )
    return values


def test_orphan_blank_lines_do_not_break_three_verified_eta_equations(eligible):
    a, b, c = tuple(eligible)
    lines = ["証明", "", a, "", "", "", b, "", c, "", "□"]
    actual = combine_adjacent_verified_eta_sentences(lines, SimpleNamespace())
    merged = r"[R3]より, $E(\eta_{2})=\eta_{3},\quad E(\eta_{3}^{2})=\eta_{4}^{2},\quad E(\eta_{2}^{3})=\eta_{3}^{3}$."
    assert merged in actual
    assert sum(line.startswith("[R3]より, ") for line in actual) == 1
    assert a not in actual and b not in actual and c not in actual
    assert actual[-1] == "□"


def test_no_merge_across_other_proof_sentence(eligible):
    a, b, c = tuple(eligible)
    barrier = r"[R5]より, $2\nu'=\eta_{3}^{3}$."
    original = [a, "", "", barrier, "", b, "", c]
    actual = combine_adjacent_verified_eta_sentences(original, SimpleNamespace())
    assert a in actual
    assert barrier in actual
    assert not any(r"E(\eta_{2})=\eta_{3},\quad" in s for s in actual)
    assert any(r"E(\eta_{3}^{2})=\eta_{4}^{2},\quad E(\eta_{2}^{3})=\eta_{3}^{3}" in s for s in actual)


def test_no_merge_across_different_citation(eligible, monkeypatch):
    a, b, c = tuple(eligible)
    other_line = "[R4]より, $" + eligible[b][1] + "$."
    differing = dict(eligible)
    differing[other_line] = ("[R4]より, ", eligible[b][1])
    monkeypatch.setattr(
        "phase171_r20r13_eta_sentence_layout.projection.verified_eta_display_sentences",
        lambda model: differing,
    )
    original = [a, "", "", other_line, "", "", c]
    actual = combine_adjacent_verified_eta_sentences(original, SimpleNamespace())
    assert actual == original


def test_uncertified_lines_stay_unchanged(eligible):
    a, b, c = tuple(eligible)
    unknown = r"[R3]より, $E(\kappa)=\lambda$."
    original = [a, "", "", unknown, "", b, "", c]
    actual = combine_adjacent_verified_eta_sentences(original, SimpleNamespace())
    assert a in actual
    assert unknown in actual


def test_complete_real_pi63_three_eta_equations_in_one_line():
    from phase165_r52_partial_proof import ProofSearchStatus
    from phase165_r52_r9_shared_math import build_shared_typed_bridge
    from phase165_r55_nk_only_goal import search_group_from_registered_goal
    from phase166_r3t_goal_source_binding.goal_source import resolve_specialized_goal_citing_id
    from phase168_r3_4_link_bridge import build_linked_proof_narrative_model
    from phase168_r3_41p13_trust_boundary import verify_proof_tree_for_narrative
    from phase168_r3_5_model_renderer import render_model_backed_narrative_markdown
    bridge = build_shared_typed_bridge()
    contexts = []
    result = search_group_from_registered_goal(
        n=3, k=3, bridge=bridge, context_sink=contexts.append,
    )
    assert result.status is ProofSearchStatus.COMPLETE
    assert not result.open_goals
    assert len(contexts) == 1
    citing = resolve_specialized_goal_citing_id(bridge, result.conclusion)
    assert citing is not None
    verify_proof_tree_for_narrative(result, contexts[0], citing_assertion_id=citing)
    model = build_linked_proof_narrative_model(result, contexts[0])
    markdown = render_model_backed_narrative_markdown(result, model)
    reference, body = markdown.split("\n証明\n", 1)
    lines = body.splitlines()
    grouped = [line for line in lines
               if line.startswith("[R3]より, $E(") and r",\quad E(" in line]
    assert any(
        all(eta in line for eta in (
            r"E(\eta_{2})=\eta_{3}",
            r"E(\eta_{3}^{2})=\eta_{4}^{2}",
            r"E(\eta_{2}^{3})=\eta_{3}^{3}",
        )) for line in grouped
    )
    assert r"\operatorname{ord}" in body
    assert r"\neq0" in body
    assert "短完全列となる. 両端" not in body
    assert len(model.citations) == 8
    assert "[R3] Chapter V, i)." in reference

```
