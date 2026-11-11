# 変更後の関数全文 — phase171_r20r13_eta_sentence_layout/projection.py

```python
def format_complete_proof_sentences(lines: list[str], model) -> list[str]:
    """Keep the original tree/citations; alter only completed narrative prose."""
    from phase174_r3_r7_r70_verified_narrative_projection.projection import (
        project_verified_general_narrative,
    )
    return split_completed_proof_sentences(
        project_verified_general_narrative(
            combine_adjacent_verified_eta_sentences(lines, model), model,
        )
    )
```

# 新規追加 projection.py — 全文

```python
"""Source-bound, general explanation of existing completed ProofStep chains.

Never add a ProofStep, GIVEN, or inference. A displayed intermediate implication
of a verified four-premise EHP root is prose, not an independent new proof step.
Any missing, ambiguous or unrelated witness leaves original lines untouched.
"""
from __future__ import annotations


def _step_index(model, step, scope: frozenset[int]) -> int | None:
    """Resolve a real ancestor by unique identity, else unique value."""
    identities = tuple(i for i in scope if model.steps[i] is step)
    if len(identities) == 1:
        return identities[0]
    if identities:
        return None
    values = tuple(i for i in scope if model.steps[i] == step)
    return values[0] if len(values) == 1 else None


def _body_index(lines: list[str], sentence: str, *, prefix: str | None = None) -> int | None:
    """Match one whole existing proof line, never a Reference paragraph."""
    headings = [i for i, line in enumerate(lines) if line == "証明"]
    if len(headings) != 1 or not sentence:
        return None
    start = headings[0] + 1
    found = [i for i in range(start, len(lines))
             if (lines[i] == sentence or lines[i].endswith(sentence))
             and (prefix is None or lines[i].startswith(prefix))]
    return found[0] if len(found) == 1 else None


def _given_ancestor_tags(model, step, scope: frozenset[int]) -> tuple[int, ...]:
    """Collect only actually used registered GIVEN citations, not names."""
    from proof import ProofRule
    seen: set[int] = set()
    pending = [step]
    numbers: set[int] = set()
    while pending:
        current = pending.pop()
        index = _step_index(model, current, scope)
        if index is None:
            return ()
        if index in seen:
            continue
        seen.add(index)
        if current.rule is ProofRule.GIVEN:
            numbers.update(model.step_citation_numbers[index])
        pending.extend(current.premises)
    return tuple(sorted(numbers))


def _project_composite_images(lines: list[str], model, scope: frozenset[int]) -> list[str]:
    """Condense three displayed premises only for a verified composite-zero step."""
    from expression import Zero
    from phase165_r14_r6_generic_iso import GeneratorImage
    from phase168_r3_27_typed_statement_projection import typed_sentence
    from phase169_r10e5_composite_generator_image.rule import component_image_obligations
    from phase174_r3_r7_r7_composite_zero_audit.rule import (
        RULE_NAME, composite_zero_generator_inputs,
    )
    from proof import ProofRule
    from toda_proof_narrative_renderer import render_toda_expression_latex

    output = list(lines)
    for index in sorted(scope):
        zero_step = model.steps[index]
        zero_goal = zero_step.conclusion
        if (zero_step.rule is not ProofRule.INFERENCE
                or getattr(zero_step.inference_rule, "name", None) != RULE_NAME
                or not isinstance(zero_goal, GeneratorImage)
                or not isinstance(zero_goal.target_generator, Zero)
                or len(zero_step.premises) != 2):
            continue
        image_step, annihilator_step = zero_step.premises
        if (image_step.rule is not ProofRule.INFERENCE
                or annihilator_step.rule is not ProofRule.INFERENCE
                or _step_index(model, image_step, scope) is None
                or _step_index(model, annihilator_step, scope) is None
                or composite_zero_generator_inputs(
                    zero_goal, image_step.conclusion
                ) != (image_step.conclusion, annihilator_step.conclusion)):
            continue
        requirements = component_image_obligations(image_step.conclusion)
        if requirements is None or len(image_step.premises) != 2:
            continue
        component_steps = image_step.premises
        if (any(parent.rule is not ProofRule.INFERENCE
                or _step_index(model, parent, scope) is None
                for parent in component_steps)
                or tuple(parent.conclusion for parent in component_steps) != requirements):
            continue
        tags = _given_ancestor_tags(model, annihilator_step, scope)
        if len(tags) != 1:
            continue
        component_sentences = tuple(typed_sentence(parent.conclusion, parent)
                                    for parent in component_steps)
        annihilator_sentence = typed_sentence(annihilator_step.conclusion, annihilator_step)
        if (any(not isinstance(item, str) for item in component_sentences)
                or not isinstance(annihilator_sentence, str)):
            continue
        indices = tuple(_body_index(output, item) for item in component_sentences)
        related = _body_index(output, annihilator_sentence,
                              prefix=f"[R{tags[0]}]より, ")
        if (related is None or any(i is None for i in indices)
                or len(set(indices + (related,))) != 3):
            continue
        positions = sorted(indices + (related,))
        if (positions[0] != indices[0] or positions[1] != indices[1]
                or positions[2] != related
                or any(output[i] for i in range(positions[0], positions[2] + 1)
                       if i not in positions)):
            continue
        try:
            generator = render_toda_expression_latex(zero_goal.source_generator)
            composite = render_toda_expression_latex(image_step.conclusion.target_generator)
        except (TypeError, ValueError):
            continue
        if not generator or not composite or "\\" not in generator or "\\" not in composite:
            continue
        combined = (f"懸垂と合成の関係および [R{tags[0]}]より, "
                    f"$E({generator})={composite}=0$.")
        suffix = output[positions[2] + 1:]
        while suffix and suffix[0] == "":
            suffix.pop(0)
        output = output[:positions[0]] + [combined, ""] + suffix
    return output


def _project_delta_consequence(lines: list[str], model,
                               scope: frozenset[int]) -> list[str]:
    """Use よって only when an exact one-premise cyclic presentation precedes Delta."""
    from homotopy_groups import TodaDeltaMap
    from phase165_r14_r6_generic_iso import MapSurjective
    from phase168_r3_27_typed_statement_projection import group_tex, typed_sentence
    from phase174_r3_r7_r56_cyclic_generator_bridge.rule import (
        SURJECTIVE_RULE_NAME, delta_surjectivity_generator_inputs,
    )
    from proof import ProofRule, Relation

    output = list(lines)
    for index in sorted(scope):
        step = model.steps[index]
        goal = step.conclusion
        if (step.rule is not ProofRule.INFERENCE
                or getattr(step.inference_rule, "name", None) != SURJECTIVE_RULE_NAME
                or not isinstance(goal, MapSurjective)
                or not isinstance(goal.map, TodaDeltaMap)
                or len(step.premises) != 1):
            continue
        prior = step.premises[0]
        prior_idx = _step_index(model, prior, scope)
        expected = delta_surjectivity_generator_inputs(goal)
        if (prior_idx is None or expected != (prior.conclusion,)
                or prior.rule not in (ProofRule.INFERENCE, ProofRule.GIVEN)
                or not isinstance(prior.conclusion, Relation)):
            continue
        sentence = typed_sentence(goal, step)
        if not isinstance(sentence, str):
            continue
        tags = model.step_citation_numbers[prior_idx]
        if len(tags) != 1:
            continue
        delta_idx = _body_index(output, sentence, prefix=f"[R{tags[0]}]より, ")
        if delta_idx is None:
            continue
        group_name = group_tex(prior.conclusion.lhs)
        if group_name is None:
            continue
        prior_matches = [i for i in range(delta_idx)
                         if output[i].startswith(f"[R{tags[0]}]より, ")
                         and group_name in output[i]]
        if len(prior_matches) != 1:
            continue
        output[delta_idx] = "よって, " + sentence
    return output


def _project_zero_root_explanation(lines: list[str], model,
                                   scope: frozenset[int]) -> list[str]:
    """Explain the existing EHP root's four-premise implication, without new steps."""
    from homotopy_groups import TodaHopfInvariantMap, TodaSuspensionMap
    from map_property_rules import ImageZeroStatement
    from phase165_r14_r6_generic_iso import MapInjective
    from phase168_r3_27_typed_statement_projection import group_tex, typed_sentence
    from phase174_r3_r7_r3_ehp_zero_rule.rule import RULE_NAME, ehp_zero_inputs
    from proof import ProofRule

    if model.root_index not in scope:
        return list(lines)
    root = model.steps[model.root_index]
    required = ehp_zero_inputs(root.conclusion)
    if (root.rule is not ProofRule.INFERENCE
            or getattr(root.inference_rule, "name", None) != RULE_NAME
            or required is None
            or len(required) != 4
            or len(root.premises) != 4
            or any(parent.rule is not ProofRule.INFERENCE
                   or parent.conclusion != expected
                   or _step_index(model, parent, scope) is None
                   for parent, expected in zip(root.premises, required))):
        return list(lines)
    delta_window = required[1].window
    hopf_window = required[2].window
    e = TodaSuspensionMap(delta_window.middle_term, delta_window.target_term)
    h = TodaHopfInvariantMap(hopf_window.middle_term, hopf_window.target_term)
    if (e.target_group != h.source_group
            or delta_window.target_term != hopf_window.middle_term):
        return list(lines)
    if any(model.steps[i].rule is ProofRule.INFERENCE
           and model.steps[i].conclusion in (ImageZeroStatement(e), MapInjective(h))
           for i in scope):
        # Do not repeat separately certified intermediate ProofSteps.
        return list(lines)
    delta_sentence = typed_sentence(required[0], root.premises[0])
    if not isinstance(delta_sentence, str):
        return list(lines)
    index = _body_index(lines, delta_sentence)
    if index is None:
        return list(lines)
    source, middle = group_tex(e.source_group), group_tex(e.target_group)
    middle_h, terminal = group_tex(h.source_group), group_tex(h.target_group)
    if any(value is None for value in (source, middle, middle_h, terminal)):
        return list(lines)
    # These are explicitly the two elementary consequences of the verified
    # four-premise zero-root rule, NOT additional independent ProofSteps.
    first = (rf"完全性と $\Delta$ の全射性より, "
             rf"$E:{source}\to {middle}$ は零写像.")
    second = (rf"さらに完全性より, $\ker H=\operatorname{{Im}}E=0$ なので, "
              rf"$H:{middle_h}\to {terminal}$ は単射.")
    output = list(lines)
    output[index + 1:index + 1] = ["", first, "", second]
    return output


def project_verified_general_narrative(lines: list[str], model) -> list[str]:
    """General, fail-closed completion-only prose improvements from a verified root."""
    if not isinstance(lines, list) or model.root_index is None:
        return lines
    from phase168_r3_3_proof_narrative_model import root_ancestor_step_indices
    scope = root_ancestor_step_indices(model.steps, model.root_index)
    changed = _project_composite_images(lines, model, scope)
    changed = _project_delta_consequence(changed, model, scope)
    changed = _project_zero_root_explanation(changed, model, scope)
    return changed
```

# 新規追加 install.py — 全文

```python
"""R70 audited, idempotent patch of one shared completed-narrative formatter."""
from __future__ import annotations

import argparse
import ast
from hashlib import sha1
import os
from pathlib import Path
import subprocess


PACKAGE = "phase174_r3_r7_r70_verified_narrative_projection"
TARGET = "phase171_r20r13_eta_sentence_layout/projection.py"
REVIEWED_BLOB = "4c1ef57ed0a20d551ae24c80d4b7ddbbb7df9c31"
REVIEWED_DEPENDENCIES = {
    "phase168_r3_5_model_renderer.py": "cb6989871ea4ad3964f714bfc5ada2a5099424a0",
    "phase168_r3_3_proof_narrative_model.py": "6a298aae5f7cbc8ec1be5b02a931b6b7a72e9d52",
    "phase168_r3_27_typed_statement_projection.py": "9ce32b5db34a3981649b9b9f2c5ff897eb8de831",
    "phase174_r3_r7_r3_ehp_zero_rule/rule.py": "8834cbefbfca5bcca18dc01f072c9738a05f7bdc",
    "phase174_r3_r7_r56_cyclic_generator_bridge/rule.py": "e6bbeb8efa47a46f7326b8711b6de9e79ff60319",
    "phase174_r3_r7_r7_composite_zero_audit/rule.py": "d98a7b45e08cd3b07c16e3f38e0a558ccebfc9b6",
    "phase169_r10e5_composite_generator_image/rule.py": "01acace3eb273d47091421a61291ee54b51c369f",
    "phase171_r20r13_eta_sentence_layout/tests/test_projection.py": "6031f6a1b396d040181f04b792bc5c5caf2c5530",
}

BEFORE = '''def format_complete_proof_sentences(lines: list[str], model) -> list[str]:
    """Keep the original tree/citations; alter only completed narrative prose."""
    return split_completed_proof_sentences(
        combine_adjacent_verified_eta_sentences(lines, model)
    )
'''

AFTER = '''def format_complete_proof_sentences(lines: list[str], model) -> list[str]:
    """Keep the original tree/citations; alter only completed narrative prose."""
    from phase174_r3_r7_r70_verified_narrative_projection.projection import (
        project_verified_general_narrative,
    )
    return split_completed_proof_sentences(
        project_verified_general_narrative(
            combine_adjacent_verified_eta_sentences(lines, model), model,
        )
    )
'''


def git_blob_sha(data: bytes) -> str:
    return sha1(b"blob " + str(len(data)).encode("ascii") + b"\x00" + data).hexdigest()


def normalize(raw: bytes) -> tuple[str, bytes, str]:
    bom = b"\xef\xbb\xbf" if raw.startswith(b"\xef\xbb\xbf") else b""
    body = raw[len(bom):]
    if b"\r" in body.replace(b"\r\n", b""):
        raise RuntimeError("R70_UNEXPECTED_CR_OR_MIXED_EOL")
    if b"\r\n" in body and b"\n" in body.replace(b"\r\n", b""):
        raise RuntimeError("R70_MIXED_EOL")
    eol = "\r\n" if b"\r\n" in body else "\n"
    return body.decode("utf-8").replace("\r\n", "\n"), bom, eol


def accepts_sha(raw: bytes, sha: str) -> bool:
    content, bom, _ = normalize(raw)
    lf = bom + content.encode("utf-8")
    crlf = bom + content.replace("\n", "\r\n").encode("utf-8")
    return sha in {git_blob_sha(raw), git_blob_sha(lf), git_blob_sha(crlf)}


def replace_formatter(original: bytes) -> tuple[str, bytes]:
    content, bom, eol = normalize(original)
    sha_valid = accepts_sha(original, REVIEWED_BLOB)
    if content.count(BEFORE) == 1 and AFTER not in content:
        if not sha_valid:
            raise RuntimeError("R70_SOURCE_GUARD_FAILED")
        rewritten = content.replace(BEFORE, AFTER, 1)
        state = "PATCH_REQUIRED"
    elif content.count(AFTER) == 1 and BEFORE not in content:
        rewritten = content.replace(AFTER, BEFORE, 1)
        baseline = bom + rewritten.replace("\n", eol).encode("utf-8")
        if not accepts_sha(baseline, REVIEWED_BLOB):
            raise RuntimeError("R70_POST_PATCH_SOURCE_MISMATCH")
        rewritten = content
        state = "ALREADY_APPLIED"
    else:
        raise RuntimeError("R70_UNREVIEWED_FORMATTER_BODY")
    ast.parse(rewritten)
    result = bom + rewritten.replace("\n", eol).encode("utf-8")
    return state, result


def source_guard(root: Path) -> tuple[str, ...]:
    checked = []
    for relative, sha in REVIEWED_DEPENDENCIES.items():
        if not accepts_sha((root / relative).read_bytes(), sha):
            raise RuntimeError("R70_REVIEWED_DEPENDENCY_CHANGED: " + relative)
        checked.append(relative)
    return tuple(checked)


def write_full_formatter(root: Path) -> None:
    target = (root / TARGET).read_text(encoding="utf-8-sig")
    parsed = ast.parse(target)
    matches = [x for x in parsed.body
               if isinstance(x, ast.FunctionDef) and x.name == "format_complete_proof_sentences"]
    if len(matches) != 1:
        raise RuntimeError("R70_FORMATTER_NOT_UNIQUE")
    full = ast.get_source_segment(target, matches[0])
    if full is None or "project_verified_general_narrative" not in full:
        raise RuntimeError("R70_FULL_FUNCTION_MISSING")
    output = root / PACKAGE / "output"
    output.mkdir(parents=True, exist_ok=True)
    (output / "format_complete_proof_sentences_FULL_AFTER.py").write_text(
        full + "\n", encoding="utf-8")


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--dry-run", action="store_true")
    args = parser.parse_args()
    root = Path(__file__).resolve().parents[1]
    branch = subprocess.run(["git", "branch", "--show-current"], cwd=root,
                            text=True, capture_output=True, check=False)
    if branch.returncode != 0 or branch.stdout.strip() != "develop":
        raise RuntimeError("R70_DEVELOP_BRANCH_REQUIRED")
    head = subprocess.run(["git", "rev-parse", "HEAD"], cwd=root,
                          text=True, capture_output=True, check=True).stdout.strip()
    checked = source_guard(root)
    target = root / TARGET
    before = target.read_bytes()
    state, after = replace_formatter(before)
    print("PHASE174_R70_SOURCE_GUARD=PASS")
    print("PHASE174_R70_SOURCE_PINS=" + str(len(checked) + 1))
    print("PHASE174_R70_LOCAL_HEAD=" + head)
    print("PHASE174_R70_PATCH_STATUS=" + state)
    print("PHASE174_R70_NEW_GIVEN=0")
    print("PHASE174_R70_NEW_MATHEMATICAL_RULES=0")
    if args.dry_run:
        print("PHASE174_R70_PRODUCTION_CHANGES=0")
        print("PHASE174_R70_GATE=PASS_R70_READ_ONLY_DRYRUN")
        print("(END)")
        return 0
    if state == "PATCH_REQUIRED":
        target.write_bytes(after)
    write_full_formatter(root)
    print("PHASE174_R70_PRODUCTION_CHANGES=" + str(state == "PATCH_REQUIRED"))
    print("PHASE174_R70_GATE=PASS_R70_GENERAL_FORMATTER_PATCH_APPLIED_OR_PRESENT")
    print("(END)")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
```

# 新規追加 audit.py — 全文

```python
"""R70 public, source-first narrative-only regression after a one-function patch."""
from __future__ import annotations

import argparse
import json
import os
from pathlib import Path
import tempfile

from .install import source_guard, replace_formatter, TARGET


def inspect_public() -> dict[str, object]:
    """Verify two public completed searches, with no synthetic proof roots."""
    from phase165_r52_r9_shared_math import build_shared_typed_bridge
    from phase174_r3_r7_r56_cyclic_generator_bridge.audit import _search_with_model
    from phase168_r3_5_model_renderer import render_model_backed_narrative_markdown
    from phase174_r3_r7_r68_ehp_premise_semantics_audit.audit import (
        inspect_public as earlier_inference_audit,
    )

    previous = earlier_inference_audit()
    if (previous["pi11_6"]["reference_count"] != 7
            or previous["pi12_7"]["reference_count"] != 3):
        raise RuntimeError("R70_PRIOR_EHP_PREMISES_CHANGED")
    bridge = build_shared_typed_bridge()
    first, model1 = _search_with_model(6, 5, bridge)
    second, model2 = _search_with_model(7, 5, bridge)
    a = render_model_backed_narrative_markdown(first, model1)
    b = render_model_backed_narrative_markdown(second, model2)
    if len(model1.citations) != 7 or len(model2.citations) != 3:
        raise RuntimeError("R70_REFERENCE_COUNT_CHANGED")
    expected_composite = "懸垂と合成の関係および [R2]より, $E("
    if (expected_composite not in a or "=0$." not in a
            or r"E(\nu_{5})=\nu_{6}" in a):
        raise RuntimeError("R70_COMPOSITE_CHAIN_NOT_CONDENSED")
    delta_text = r"よって, $\Delta: \pi_{13}^{13}\to \pi_{11}^{6}$ は全射."
    if delta_text not in b or r"[R1]より, $\Delta:" in b:
        raise RuntimeError("R70_DELTA_CONNECTIVE_MISSING")
    e_reason = r"完全性と $\Delta$ の全射性より, $E:\pi_{11}^{6}\to \pi_{12}^{7}$ は零写像."
    h_reason = (r"さらに完全性より, $\ker H=\operatorname{Im}E=0$ なので, "
                r"$H:\pi_{12}^{7}\to \pi_{12}^{13}$ は単射.")
    if e_reason not in b or h_reason not in b:
        raise RuntimeError("R70_HOPF_REASONING_NOT_DISPLAYED")
    proof = b.split("\n証明\n", 1)[-1]
    terminal_index = proof.find("[R3]より, ", proof.find(h_reason))
    terminal_line = (proof[terminal_index:].splitlines()[0]
                     if terminal_index >= 0 else "")
    if (proof.find(delta_text) == -1 or proof.find(e_reason) == -1
            or proof.find(h_reason) == -1
            or terminal_index < 0 or r"\pi_{12}^{13}" not in terminal_line
            or not (proof.find(delta_text) < proof.find(e_reason)
                    < proof.find(h_reason) < terminal_index)):
        raise RuntimeError("R70_REASONING_ORDER_CHANGED")
    if r"\\to" in a or r"\\to" in b:
        raise RuntimeError("R70_INVALID_TEX_ARROW")
    if first.status.name != "COMPLETE" or second.status.name != "COMPLETE":
        raise RuntimeError("R70_COMPLETED_SEARCH_CHANGED")
    return {
        "pi11_6_complete": True,
        "pi11_6_reference_count": len(model1.citations),
        "pi11_6_composite_zero_line": next(
            line for line in a.splitlines() if expected_composite in line),
        "pi11_6_source_formula_kept_in_reference": "[R2] (5.9)." in a,
        "pi12_7_complete": True,
        "pi12_7_reference_count": len(model2.citations),
        "pi12_7_delta_connective": delta_text,
        "pi12_7_zero_e_explanation": e_reason,
        "pi12_7_hopf_injectivity_explanation": h_reason,
        "pi12_7_intermediates_are_presentation_not_new_steps": True,
        "pi12_7_delta_surjective_still_one_prior_given": True,
        "full_sentence_semantics_audited": False,
        "new_given": 0,
        "new_mathematical_rules": 0,
    }


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--dry-run", action="store_true")
    opts = parser.parse_args()
    root = Path(__file__).resolve().parents[1]
    checked = source_guard(root)
    status, _ = replace_formatter((root / TARGET).read_bytes())
    if status != "ALREADY_APPLIED" and not opts.dry_run:
        raise RuntimeError("R70_FORMATTER_NOT_APPLIED")
    print("PHASE174_R70_SOURCE_GUARD=PASS")
    print("PHASE174_R70_SOURCE_PINS=" + str(len(checked) + 1))
    if opts.dry_run:
        print("PHASE174_R70_GATE=PASS_R70_PUBLIC_DRYRUN")
        print("(END)")
        return 0
    evidence = inspect_public()
    report = {
        "phase": "174-R70", "evidence": evidence,
        "production_files_changed": [TARGET],
        "full_pytest_run": False,
    }
    output = (Path(os.environ.get("LOCALAPPDATA", tempfile.gettempdir()))
              / "EHPProofTracerAudit"
              / "phase174_r3_r7_r70_verified_narrative_projection"
              / "report.json")
    output.parent.mkdir(parents=True, exist_ok=True)
    output.write_text(json.dumps(report, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    print("PHASE174_R70_PI11_6_COMPOSITE_DISPLAY=PASS")
    print("PHASE174_R70_PI12_7_DELTA_CONNECTIVE=PASS")
    print("PHASE174_R70_PI12_7_E_ZERO_AND_H_INJECTIVE_EXPLANATION=PASS")
    print("PHASE174_R70_PI11_6_REFERENCES=7")
    print("PHASE174_R70_PI12_7_REFERENCES=3")
    print("PHASE174_R70_NEW_GIVEN=0")
    print("PHASE174_R70_NEW_MATHEMATICAL_RULES=0")
    print("PHASE174_R70_REPORT=" + str(output))
    print("PHASE174_R70_GATE=PASS_R70_PUBLIC_GENERAL_EXPLANATIONS")
    print("(END)")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
```

# 新規追加 tests/test_projection.py — import とテスト関数の全文

```python
"""Minimal fail-closed generic narrative contracts and source patch tests."""
from __future__ import annotations

from pathlib import Path
from types import SimpleNamespace

import pytest

from phase174_r3_r7_r70_verified_narrative_projection.install import (
    BEFORE, AFTER, REVIEWED_BLOB, TARGET, git_blob_sha, replace_formatter,
    source_guard,
)
from phase174_r3_r7_r70_verified_narrative_projection.projection import (
    _body_index, _step_index, project_verified_general_narrative,
)


def test_patch_updates_only_entire_formatter_and_is_idempotent() -> None:
    root = Path(__file__).resolve().parents[2]
    assert source_guard(root)
    raw = (root / TARGET).read_bytes()
    state, rewritten = replace_formatter(raw)
    assert state == "ALREADY_APPLIED"
    assert rewritten == raw
    assert BEFORE.encode() not in rewritten
    assert AFTER.encode() in rewritten.replace(b"\r\n", b"\n")


def test_line_endings_source_guard_and_patch_idempotence(
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    import phase174_r3_r7_r70_verified_narrative_projection.install as module
    sample = b"# test only\n" + BEFORE.encode("utf-8")
    monkeypatch.setattr(module, "REVIEWED_BLOB", git_blob_sha(sample))
    for content in (sample, sample.replace(b"\n", b"\r\n")):
        state, patched = module.replace_formatter(content)
        assert state == "PATCH_REQUIRED"
        assert b"\r\r\n" not in patched
        assert module.replace_formatter(patched) == ("ALREADY_APPLIED", patched)


def test_source_guard_rejects_unreviewed_change(monkeypatch: pytest.MonkeyPatch) -> None:
    import phase174_r3_r7_r70_verified_narrative_projection.install as module
    monkeypatch.setattr(module, "REVIEWED_BLOB", git_blob_sha(BEFORE.encode()))
    with pytest.raises(RuntimeError, match="R70_SOURCE_GUARD_FAILED"):
        module.replace_formatter(("# extra\n" + BEFORE).encode())


def test_rejects_mixed_eol_and_cr_only() -> None:
    import phase174_r3_r7_r70_verified_narrative_projection.install as module
    with pytest.raises(RuntimeError, match="R70_UNEXPECTED_CR"):
        module.replace_formatter(b"a\rb\n")
    with pytest.raises(RuntimeError, match="R70_MIXED_EOL"):
        module.replace_formatter(b"a\r\nb\n")


def test_body_line_search_does_not_match_reference_text() -> None:
    lines = ["使用する結果", "[R1]より, $x=0$.", "証明", "", "[R1]より, $x=0$."]
    assert _body_index(lines, "$x=0$.", prefix="[R1]より, ") == 4
    assert _body_index(lines, "$x=0$.", prefix="[R2]より, ") is None
    assert _body_index(["証明", "$x=0$.", "$x=0$."], "$x=0$.") is None


def test_step_index_rejects_ambiguous_value_fallback() -> None:
    source = SimpleNamespace(conclusion="x", premises=())
    identical = SimpleNamespace(conclusion="x", premises=())
    model = SimpleNamespace(steps=(source, identical))
    assert _step_index(model, source, frozenset({0, 1})) == 0
    assert _step_index(model, SimpleNamespace(conclusion="x", premises=()),
                       frozenset({0, 1})) is None


def test_incomplete_model_has_no_composed_rewrite() -> None:
    original = ["証明", "", "未完成", ""]
    model = SimpleNamespace(root_index=None)
    assert project_verified_general_narrative(original, model) == original


def test_git_sha_fixture() -> None:
    assert git_blob_sha(b"hello\n") == "ce013625030ba8dba906f756967f9e9ca394464a"
```

# 新規追加 run.ps1 — 全文

```powershell
param([switch]$DryRun)
$ErrorActionPreference = 'Stop'
$root = Split-Path -Parent $PSScriptRoot
Set-Location $root
$env:PYTHONPATH = $root
$package = 'phase174_r3_r7_r70_verified_narrative_projection'

if ($DryRun) {
    python -m "$package.install" --dry-run
    if ($LASTEXITCODE -ne 0) { throw 'R70 install DryRun failed' }
    python -m "$package.audit" --dry-run
    if ($LASTEXITCODE -ne 0) { throw 'R70 public audit DryRun failed' }
    Write-Output 'PHASE174_R70_GATE=PASS_R70_DRYRUN'
    Write-Output '(END)'
    exit 0
}

python -m "$package.install"
if ($LASTEXITCODE -ne 0) { throw 'R70 reviewed formatter patch failed' }
python -m pytest -q -o addopts= --import-mode=importlib `
    "$package/tests/test_projection.py" `
    'phase171_r20r13_eta_sentence_layout/tests/test_projection.py' `
    'phase171_r20r13r2_multiple_blank_eta_merge/tests/test_correction.py' `
    'phase174_r3_r7_r69_general_narrative_gap_audit/tests/test_audit.py' `
    'phase174_r3_r7_r68_ehp_premise_semantics_audit/tests/test_audit.py'
if ($LASTEXITCODE -ne 0) { throw 'R70 focused pytest failed' }
python -m "$package.audit"
if ($LASTEXITCODE -ne 0) { throw 'R70 public proof display audit failed' }
Write-Output 'PHASE174_R70_GATE=PASS_R70_FOCUSED_AND_PUBLIC_GENERAL_NARRATIVE'
Write-Output '(END)'
```
