# Phase 174 R63 — 新規コード全文

既存コードの変更はありません。以下は新規ファイルの内容を省略せず掲載します。

## `audit.py`（新規：R63 ディレクトリ直下）

```python
"""R63: verify four targeted rendered attributions against actual ProofStep ancestry.

This does not establish sentence-level correctness of the entire narrative.
No renderer, proof step, mathematical rule, registered source, or database is changed.
"""
from __future__ import annotations

import argparse
from hashlib import sha1
import json
import os
from pathlib import Path
import subprocess
import tempfile

PACKAGE = "phase174_r3_r7_r63_sentence_witness_audit"
PINS = {
    "phase168_r3_3_proof_narrative_model.py": "6a298aae5f7cbc8ec1be5b02a931b6b7a72e9d52",
    "phase168_r3_12_body_binding.py": "ad8797c141216e410e81bafae284507f7797c3e4",
    "phase168_r3_5_model_renderer.py": "cb6989871ea4ad3964f714bfc5ada2a5099424a0",
    "phase168_r3_27_typed_statement_projection.py": "5b7bf647a7f7f427e2790cbe915709f014480d11",
    "phase174_r3_r7_r56_cyclic_generator_bridge/rule.py": "e6bbeb8efa47a46f7326b8711b6de9e79ff60319",
    "phase174_r3_r7_r57_narrative_source_cleanup/audit.py": "7cc7e7ac7f63c4bf28142c1d84c5d8ddd249cc8a",
    "phase174_r3_r7_r61_reference_attribution_route_audit/audit.py": "e399a0307408a779f35b9f08a8795977a23a7b4b",
}


def git_blob_sha(data: bytes) -> str:
    return sha1(b"blob " + str(len(data)).encode("ascii") + b"\x00" + data).hexdigest()


def source_guard(root: Path) -> tuple[str, ...]:
    """Pin reviewed production dependencies, not a moving Git HEAD."""
    checked: list[str] = []
    for relative, wanted in PINS.items():
        data = (root / relative).read_bytes()
        lf = data.replace(b"\r\n", b"\n")
        variants = (data, lf, lf.replace(b"\n", b"\r\n"))
        if wanted not in {git_blob_sha(item) for item in variants}:
            raise RuntimeError("R63_SOURCE_BLOB_MISMATCH: " + relative)
        checked.append(relative)
    return tuple(checked)


def local_head(root: Path) -> str:
    process = subprocess.run(
        ["git", "rev-parse", "HEAD"], cwd=root,
        capture_output=True, text=True, check=False,
    )
    if process.returncode:
        raise RuntimeError("R63_GIT_HEAD_UNAVAILABLE")
    return process.stdout.strip()


def unique_step_index(model, predicate, scope: frozenset[int]) -> int:
    """Fail closed if a targeted typed conclusion has zero or multiple witnesses."""
    matches = tuple(index for index in sorted(scope) if predicate(model.steps[index]))
    if len(matches) != 1:
        raise RuntimeError("R63_TARGET_STEP_NOT_UNIQUE: " + repr(matches))
    return matches[0]


def verified_ancestor_indices(model, start_index: int) -> frozenset[int]:
    """Traverse actual ProofStep premises, using unique-value fallback only."""
    if type(start_index) is not int or not 0 <= start_index < len(model.steps):
        raise ValueError("invalid proof step index")
    identities = {id(step): i for i, step in enumerate(model.steps)}
    if len(identities) != len(model.steps):
        raise RuntimeError("R63_DUPLICATE_STEP_IDENTITY")
    found: set[int] = set()
    pending = [start_index]
    while pending:
        index = pending.pop()
        if index in found:
            continue
        found.add(index)
        for premise in model.steps[index].premises:
            match = identities.get(id(premise))
            if match is None:
                alternatives = tuple(i for i, step in enumerate(model.steps) if step == premise)
                if len(alternatives) != 1:
                    raise RuntimeError("R63_MISSING_OR_AMBIGUOUS_PREMISE")
                match = alternatives[0]
            pending.append(match)
    return frozenset(found)


def given_witness_indices(model, step_index: int, number: int) -> tuple[int, ...]:
    """Find the exact GIVEN ancestors owning this already registered number."""
    from proof import ProofRule
    allowed = {citation.number for citation in model.citations}
    if type(number) is not int or number not in allowed:
        raise RuntimeError("R63_UNKNOWN_CITATION")
    ancestors = verified_ancestor_indices(model, step_index)
    matches = tuple(sorted(i for i in ancestors
        if model.steps[i].rule is ProofRule.GIVEN
        and number in model.step_citation_numbers[i]))
    return matches


def displayed_line(markdown: str, number: int, tokens: tuple[str, ...],
                   lead: str = "より") -> str:
    """Identify an actual body sentence, never a bibliography heading."""
    if not isinstance(markdown, str):
        raise TypeError("markdown must be text")
    if type(number) is not int or number < 1:
        raise ValueError("invalid reference number")
    if (not isinstance(tokens, tuple) or not tokens
            or any(not isinstance(token, str) or not token for token in tokens)):
        raise ValueError("nonempty tuple of text tokens required")
    tag = f"[R{number}]{lead}"
    matches = tuple(line.strip() for line in markdown.splitlines()
                    if tag in line and all(token in line for token in tokens))
    if len(matches) != 1:
        raise RuntimeError("R63_TARGET_LINE_NOT_UNIQUE: " + tag + " " + repr(tokens))
    return matches[0]


def certify_targeted_line(model, markdown: str, step_index: int, number: int,
                          tokens: tuple[str, ...], lead: str = "より") -> dict[str, object]:
    """Require a cited GIVEN ancestor AND an actual matching rendered sentence."""
    sources = given_witness_indices(model, step_index, number)
    if not sources:
        raise RuntimeError("R63_CITATION_NOT_IN_GIVEN_ANCESTRY")
    line = displayed_line(markdown, number, tokens, lead)
    return {
        "step_index": step_index,
        "citation": number,
        "given_witness_indices": list(sources),
        "proof_line": line,
        "attribution_has_verified_ancestor": True,
        "printed_tag_matches_targeted_line": True,
    }


def inspect_group(result, model, markdown: str, n: int) -> dict[str, object]:
    """Inspect only specifically typed, known proof-inference attribution sites."""
    from homotopy_groups import TodaPrimaryGroup
    from phase165_r14_r6_generic_iso import MapSurjective
    from phase168_r3_3_proof_narrative_model import root_ancestor_step_indices
    from phase165_r12_r11_prop42_unified import TodaProp42GeneralExactnessStatement
    from phase174_r3_r7_r25_prop27_isolated_inference.rule import (
        Prop27TypedHopfDeltaStatement, typed_specialization,
    )
    from phase174_r3_r7_r56_cyclic_generator_bridge.rule import SURJECTIVE_RULE_NAME
    from proof import ProofRule
    from toda_rules import TodaDeltaImageUpToSignStatement

    if model.root_index is None:
        raise RuntimeError("R63_COMPLETE_ROOT_MISSING")
    root_scope = root_ancestor_step_indices(model.steps, model.root_index)
    if n == 6:
        expected_count, exactness_ref = 7, 3
    elif n == 7:
        expected_count, exactness_ref = 3, 2
    else:
        raise ValueError("R63 supports only two reviewed query samples")
    if len(model.citations) != expected_count:
        raise RuntimeError("R63_REFERENCE_COUNT_CHANGED")

    def known_source(number: int, fragment: str) -> None:
        reference = model.citations[number - 1].reference
        locator = reference.locator or reference.label
        if fragment not in locator:
            raise RuntimeError("R63_UNEXPECTED_SOURCE_LOCATOR: " + str(locator))

    known_source(exactness_ref, "Proposition 4.2")
    citation_map = {id(step): model.step_citation_numbers[index]
                    for index, step in enumerate(model.steps)}
    general_step_index = unique_step_index(
        model,
        lambda step: (step.rule is ProofRule.GIVEN
                      and isinstance(step.conclusion, TodaProp42GeneralExactnessStatement)
                      and exactness_ref in citation_map[id(step)]),
        root_scope,
    )
    general_step = model.steps[general_step_index]
    # The source line's formula is an exactness statement, but the proof body
    # displays a certified exactness chain rather than that GIVEN itself.
    exactness_line = displayed_line(
        markdown, exactness_ref, ("完全列を考える",), "を用いて"
    )
    exactness_witnesses = tuple(index for index in sorted(root_scope)
        if index != general_step_index
        and model.steps[index].rule is ProofRule.INFERENCE
        and general_step_index in verified_ancestor_indices(model, index))
    if not exactness_witnesses:
        raise RuntimeError("R63_EXACTNESS_GIVEN_HAS_NO_VERIFIED_CONSUMER")

    evidence: dict[str, object] = {
        "exactness_chain": {
            "citation": exactness_ref,
            "given_step_index": general_step_index,
            "verified_consumer_indices": list(exactness_witnesses),
            "proof_line": exactness_line,
            "source_is_typed_general_given": True,
        }
    }

    if n == 6:
        known_source(6, "(5.10)")
        known_source(7, "Proposition 2.7")
        lower_index = unique_step_index(
            model,
            lambda step: (step.rule is ProofRule.GIVEN
                          and type(step.conclusion) is TodaDeltaImageUpToSignStatement
                          and step.conclusion.map.source_group == TodaPrimaryGroup(11, 11)
                          and 6 in citation_map[id(step)]),
            root_scope,
        )
        evidence["toda_510"] = certify_targeted_line(
            model, markdown, lower_index, 6, (r"\Delta(", "="), "より"
        )
        witness = typed_specialization(6)
        hopf_index = unique_step_index(
            model,
            lambda step: (step.rule is ProofRule.INFERENCE
                          and type(step.conclusion) is Prop27TypedHopfDeltaStatement
                          and step.conclusion == witness),
            root_scope,
        )
        evidence["prop27_hopf_image"] = certify_targeted_line(
            model, markdown, hopf_index, 7, ("H(", r"\pm2"), "より"
        )
    else:
        # The DB locator may be a display projection; the typed GIVEN note
        # and model-owned reference number are the authoritative witnesses.
        surj_index = unique_step_index(
            model,
            lambda step: (step.rule is ProofRule.INFERENCE
                          and type(step.conclusion) is MapSurjective
                          and getattr(step.inference_rule, "name", None) == SURJECTIVE_RULE_NAME),
            root_scope,
        )
        surj = model.steps[surj_index]
        if (len(surj.premises) != 1
                or surj.premises[0].rule is not ProofRule.GIVEN
                or "ADOPTED_DATABASE_PRIOR" not in (surj.premises[0].note or "")):
            raise RuntimeError("R63_SURJECTIVITY_NOT_FROM_SINGLE_VERIFIED_PRIOR")
        evidence["surjectivity_from_prior"] = certify_targeted_line(
            model, markdown, surj_index, 1, (r"\Delta:", "全射"), "より"
        )

    return {
        "references": expected_count,
        "targeted_lines": evidence,
        "targeted_line_count": len(evidence),
        "targeted_attribution_checked": True,
        "sentence_level_relevance_fully_proved": False,
    }


def inspect_public() -> dict[str, object]:
    """Re-run published verified searches and produce an evidence-limited result."""
    from phase165_r52_r9_shared_math import build_shared_typed_bridge
    from phase174_r3_r7_r56_cyclic_generator_bridge.audit import _search_with_model
    from phase174_r3_r7_r57_narrative_source_cleanup.audit import inspect_public as r57_public
    from phase174_r3_r7_r61_reference_attribution_route_audit.audit import (
        inspect_verified_group,
    )
    from phase168_r3_5_model_renderer import render_model_backed_narrative_markdown

    prior = r57_public()
    if prior["pi11_reference_count"] != 7 or prior["pi12_reference_count"] != 3:
        raise RuntimeError("R63_PRIOR_SOURCE_BOUNDARY_CHANGED")
    bridge = build_shared_typed_bridge()
    groups = {}
    for n, k, label in ((6, 5, "pi11_6"), (7, 5, "pi12_7")):
        result, model = _search_with_model(n, k, bridge)
        rendered = render_model_backed_narrative_markdown(result, model)
        ownership = inspect_verified_group(result, model, rendered)
        if ownership["model_owned_tags_only"] is not True:
            raise RuntimeError("R63_MODEL_OWNERSHIP_REGRESSION")
        groups[label] = inspect_group(result, model, rendered, n)
    return groups


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--dry-run", action="store_true")
    opts = parser.parse_args()
    root = Path(__file__).resolve().parents[1]
    verified = source_guard(root)
    head = local_head(root)
    print("PHASE174_R63_SOURCE_GUARD=PASS")
    print("PHASE174_R63_SOURCE_PINS=" + str(len(verified)))
    print("PHASE174_R63_LOCAL_HEAD=" + head)
    print("PHASE174_R63_PRODUCTION_CHANGES=0")
    if opts.dry_run:
        print("PHASE174_R63_GATE=PASS_R63_READ_ONLY_DRYRUN")
        print("(END)")
        return 0
    groups = inspect_public()
    report = {
        "source_pins": list(verified),
        "local_head": head,
        "groups": groups,
        "conclusion": "Only the four selected attribution categories were audited; all other sentences remain unproved as to individual source relevance.",
        "sentence_level_relevance_fully_proved": False,
        "production_changes": 0,
        "new_given": 0,
        "new_mathematical_rules": 0,
        "full_pytest_run": False,
    }
    dest = (Path(os.environ.get("LOCALAPPDATA", tempfile.gettempdir()))
            / "EHPProofTracerAudit" / PACKAGE / "report.json")
    dest.parent.mkdir(parents=True, exist_ok=True)
    dest.write_text(json.dumps(report, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    for name, record in groups.items():
        print("PHASE174_R63_" + name.upper() + "_TARGETED_LINES=" + str(record["targeted_line_count"]))
        print("PHASE174_R63_" + name.upper() + "_TARGETED_ATTRIBUTION_CHECKED=True")
        print("PHASE174_R63_" + name.upper() + "_FULL_SENTENCE_AUDIT=False")
    print("PHASE174_R63_NEW_GIVEN=0")
    print("PHASE174_R63_NEW_MATHEMATICAL_RULES=0")
    print("PHASE174_R63_REPORT=" + str(dest))
    print("PHASE174_R63_GATE=PASS_R63_TARGETED_SENTENCE_WITNESS_AUDIT_ONLY")
    print("(END)")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
```

## `tests/test_audit.py`（新規：R63/tests/）

```python
"""R63 targeted sentence proof-witness binding and negative tests."""
from __future__ import annotations

from pathlib import Path
from types import SimpleNamespace

import pytest

from phase174_r3_r7_r63_sentence_witness_audit.audit import (
    PINS, certify_targeted_line, displayed_line, git_blob_sha,
    given_witness_indices, source_guard, unique_step_index,
    verified_ancestor_indices,
)


def fixture_model():
    from proof import ProofRule
    given = SimpleNamespace(conclusion="source", rule=ProofRule.GIVEN, premises=())
    inferred = SimpleNamespace(conclusion="inferred", rule=ProofRule.INFERENCE,
                               premises=(given,))
    model = SimpleNamespace(
        steps=(given, inferred),
        step_citation_numbers=((1,), ()),
        citations=(SimpleNamespace(number=1),),
    )
    return model


def test_source_guard_pins_reviewed_code() -> None:
    root = Path(__file__).resolve().parents[2]
    assert len(PINS) == 7
    assert source_guard(root) == tuple(PINS)


def test_unique_step_index_accepts_only_one_target() -> None:
    model = fixture_model()
    assert unique_step_index(model, lambda s: s.conclusion == "source", frozenset({0, 1})) == 0
    with pytest.raises(RuntimeError):
        unique_step_index(model, lambda s: True, frozenset({0, 1}))
    with pytest.raises(RuntimeError):
        unique_step_index(model, lambda s: False, frozenset({0, 1}))


def test_verified_ancestry_and_exact_given_source() -> None:
    model = fixture_model()
    assert verified_ancestor_indices(model, 1) == frozenset({0, 1})
    assert given_witness_indices(model, 1, 1) == (0,)
    with pytest.raises(RuntimeError):
        given_witness_indices(model, 1, 2)


def test_missing_or_ambiguous_premise_rejected() -> None:
    from proof import ProofRule
    model = fixture_model()
    detached = SimpleNamespace(conclusion="unknown", rule=ProofRule.GIVEN, premises=())
    altered = SimpleNamespace(conclusion="consequence", rule=ProofRule.INFERENCE,
                              premises=(detached,))
    incomplete = SimpleNamespace(steps=(model.steps[0], altered))
    with pytest.raises(RuntimeError):
        verified_ancestor_indices(incomplete, 1)
    with pytest.raises(ValueError):
        verified_ancestor_indices(model, 5)


def test_rendered_sentence_requires_exact_ref_prefix_and_formula() -> None:
    markdown = "**[R1] Example.**\n\n[R1]より, $H(\\Delta(x))=y$.\n"
    line = displayed_line(markdown, 1, ("H(", r"\Delta("))
    assert "[R1]より" in line
    with pytest.raises(RuntimeError):
        displayed_line(markdown, 1, ("全射",))
    with pytest.raises(RuntimeError):
        displayed_line(markdown, 2, ("H(",))


def test_negative_attribution_not_in_given_ancestry() -> None:
    model = fixture_model()
    markdown = "[R1]より, $H(x)=y$.\n"
    result = certify_targeted_line(model, markdown, 1, 1, ("H(",))
    assert result["given_witness_indices"] == [0]
    with pytest.raises(RuntimeError):
        certify_targeted_line(model, markdown, 1, 1, ("not the same formula",))


def test_refuses_untrusted_line_inputs() -> None:
    with pytest.raises(TypeError):
        displayed_line(None, 1, ("x",))
    with pytest.raises(ValueError):
        displayed_line("[R1]より", 0, ("x",))
    with pytest.raises(ValueError):
        displayed_line("[R1]より", 1, ())
    with pytest.raises(ValueError):
        displayed_line("[R1]より", 1, ("",))


def test_source_guard_rejects_tampered_blob(tmp_path: Path) -> None:
    relative = next(iter(PINS))
    target = tmp_path / relative
    target.parent.mkdir(parents=True, exist_ok=True)
    target.write_text("tamper", encoding="utf-8")
    with pytest.raises(RuntimeError):
        source_guard(tmp_path)


def test_known_git_blob_fixture() -> None:
    assert git_blob_sha(b"hello\n") == "ce013625030ba8dba906f756967f9e9ca394464a"


def test_rejects_number_owned_only_by_unrelated_given() -> None:
    from proof import ProofRule
    relevant = SimpleNamespace(conclusion="relevant", rule=ProofRule.GIVEN, premises=())
    unrelated = SimpleNamespace(conclusion="unrelated", rule=ProofRule.GIVEN, premises=())
    derived = SimpleNamespace(conclusion="derived", rule=ProofRule.INFERENCE,
                              premises=(relevant,))
    model = SimpleNamespace(steps=(relevant, unrelated, derived),
                            step_citation_numbers=((), (1,), ()),
                            citations=(SimpleNamespace(number=1),))
    with pytest.raises(RuntimeError, match="R63_CITATION_NOT_IN_GIVEN_ANCESTRY"):
        certify_targeted_line(model, "[R1]より, $H(x)=y$.", 2, 1, ("H(",))
```

## `run.ps1`（新規）

```powershell
[CmdletBinding()]
param([switch]$DryRun)

$ErrorActionPreference = 'Stop'
$Root = (Resolve-Path (Join-Path $PSScriptRoot '..')).Path
Push-Location $Root
try {
    $module = 'phase174_r3_r7_r63_sentence_witness_audit.audit'
    if ($DryRun) {
        python -B -m $module --dry-run
        if ($LASTEXITCODE -ne 0) { throw 'R63 DryRun Source Guard failed' }
    } else {
        python -B -m $module
        if ($LASTEXITCODE -ne 0) { throw 'R63 targeted sentence witness audit failed' }
        python -B -m pytest -q -o addopts= -p no:cacheprovider --import-mode=importlib `
            'phase174_r3_r7_r63_sentence_witness_audit/tests/test_audit.py' `
            'phase174_r3_r7_r62_attribution_policy_boundary_audit/tests/test_audit.py' `
            'phase174_r3_r7_r61_reference_attribution_route_audit/tests/test_audit.py'
        if ($LASTEXITCODE -ne 0) { throw 'R63 focused pytest failed' }
        Write-Output 'PHASE174_R63_GATE=PASS_R63_FOCUSED_AND_TARGETED_PUBLIC_WITNESSES'
        Write-Output '(END)'
    }
}
finally {
    Pop-Location
}
```
