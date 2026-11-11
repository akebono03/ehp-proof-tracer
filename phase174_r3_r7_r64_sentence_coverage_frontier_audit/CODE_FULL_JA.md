# Phase 174 R64 — 新規コード全文

既存本体ファイルに変更はありません。

## audit.py（新規）

```python
"""Phase 174 R64: inventory NOT-YET-AUDITED narrative attribution sentences.

A line can be a recorded R63 targeted witness without being a proof of the
mathematical correctness of arbitrary prose. Untargeted lines remain explicitly
UNREVIEWED; lack of an explicit [R#] is not considered a defect by itself.
No ProofStep, registered source, rule, renderer, or database item is changed.
"""
from __future__ import annotations

import argparse
from hashlib import sha1
import json
import os
from pathlib import Path
import re
import subprocess
import tempfile


PACKAGE = "phase174_r3_r7_r64_sentence_coverage_frontier_audit"
PINS = {'phase168_r3_3_proof_narrative_model.py': '6a298aae5f7cbc8ec1be5b02a931b6b7a72e9d52', 'phase168_r3_12_body_binding.py': 'ad8797c141216e410e81bafae284507f7797c3e4', 'phase168_r3_5_model_renderer.py': 'cb6989871ea4ad3964f714bfc5ada2a5099424a0', 'phase168_r3_27_typed_statement_projection.py': '5b7bf647a7f7f427e2790cbe915709f014480d11', 'phase174_r3_r7_r57_narrative_source_cleanup/audit.py': '7cc7e7ac7f63c4bf28142c1d84c5d8ddd249cc8a', 'phase174_r3_r7_r60_reference_ownership_audit/audit.py': 'c549e27bebc53ef9fe24c12f2cafc08b47807514', 'phase174_r3_r7_r61_reference_attribution_route_audit/audit.py': 'e399a0307408a779f35b9f08a8795977a23a7b4b', 'phase174_r3_r7_r63_sentence_witness_audit/audit.py': '115b1bccb657035ef5ed002157c9487509190013'}
REFERENCE_TAG = re.compile(r"\[R(\d+)\]")


def git_blob_sha(content: bytes) -> str:
    """Compute the source blob hash without depending on Git's working tree."""
    return sha1(b"blob " + str(len(content)).encode("ascii") + b"\x00" + content).hexdigest()


def source_guard(root: Path) -> tuple[str, ...]:
    """Verify reviewed source and prior-audit files; support CRLF/LF only."""
    verified = []
    for relative, expected in PINS.items():
        raw = (root / relative).read_bytes()
        lf = raw.replace(b"\r\n", b"\n")
        variants = (raw, lf, lf.replace(b"\n", b"\r\n"))
        if expected not in {git_blob_sha(blob) for blob in variants}:
            raise RuntimeError("R64_SOURCE_BLOB_MISMATCH: " + relative)
        verified.append(relative)
    return tuple(verified)


def local_head(root: Path) -> str:
    """HEAD is logged, not used as an invalidation of independently pinned files."""
    proc = subprocess.run(
        ["git", "rev-parse", "HEAD"], cwd=root,
        text=True, capture_output=True, check=False,
    )
    if proc.returncode != 0:
        raise RuntimeError("R64_GIT_HEAD_UNAVAILABLE")
    return proc.stdout.strip()


def proof_body_lines(markdown: str) -> tuple[str, ...]:
    """Read the completed proof body, never count Reference paragraphs as proof.

    The shared renderer emits the standalone heading '証明' after citations.
    Each non-empty line thereafter is a rendered proof paragraph or equation.
    """
    if not isinstance(markdown, str):
        raise TypeError("markdown must be a string")
    lines = markdown.splitlines()
    headings = tuple(i for i, line in enumerate(lines) if line.strip() == "証明")
    if len(headings) != 1 or "使用する結果" not in markdown:
        raise RuntimeError("R64_PROOF_BOUNDARY_NOT_UNIQUE")
    start = headings[0]
    if start == len(lines) - 1:
        raise RuntimeError("R64_EMPTY_PROOF_BODY")
    actual = tuple(line.strip() for line in lines[start + 1:]
                   if line.strip() and line.strip() != "□")
    if not actual or any(line.startswith("**[R") for line in actual):
        raise RuntimeError("R64_REFERENCE_HEADING_INSIDE_PROOF")
    if not markdown.rstrip().endswith("□"):
        raise RuntimeError("R64_PROOF_HAS_NO_CLOSING_BOX")
    return actual


def priority_of_untested_line(text: str, tags: tuple[int, ...]) -> str:
    """Flag where to inspect next; this is triage, NOT source certification."""
    if tags:
        return "P1_CITED_SENTENCE"
    if any(token in text for token in ("零写像", "単射", "全射", "ker", "\\ker", "以上より")):
        return "P1_UNCITED_INFERENCE"
    if "$" in text or "\\pi" in text:
        return "P2_MATH_WITHOUT_INLINE_TAG"
    return "P3_PROSE_OR_TRANSITION"


def audited_line_inventory(markdown: str, citations: tuple[int, ...],
                            targeted: dict[str, object]) -> dict[str, object]:
    """Inventory every paragraph; R63 targeted lines are the ONLY audited ones.

    No logic turns a legitimate model citation or a graph ancestor into proof
    of sentence-level relevance. This is a coverage accounting operation.
    """
    if (not isinstance(citations, tuple)
            or any(type(number) is not int for number in citations)
            or citations != tuple(range(1, len(citations) + 1))):
        raise ValueError("citation numbers must be an ordered contiguous tuple")
    if not isinstance(targeted, dict) or not targeted:
        raise ValueError("R63 targeted witness dictionary is required")
    paragraphs = proof_body_lines(markdown)
    target_by_sentence = {}
    for key, claim in targeted.items():
        if not isinstance(key, str) or not isinstance(claim, dict):
            raise ValueError("invalid R63 witness record")
        sentence = claim.get("proof_line")
        if not isinstance(sentence, str) or not sentence:
            raise ValueError("R63 witness proof line is missing")
        if sentence in target_by_sentence:
            raise RuntimeError("R64_DUPLICATE_R63_WITNESS_LINE")
        target_by_sentence[sentence] = key
    records = []
    matched = set()
    for index, text in enumerate(paragraphs, 1):
        tags = tuple(int(match) for match in REFERENCE_TAG.findall(text))
        if any(number not in citations for number in tags):
            raise RuntimeError("R64_UNKNOWN_RENDERED_CITATION")
        if text in target_by_sentence:
            identifier = target_by_sentence[text]
            if identifier in matched:
                raise RuntimeError("R64_AMBIGUOUS_TARGETED_LINE")
            matched.add(identifier)
            status = "R63_TARGETED_ANCESTOR_ATTESTED"
            priority = "ALREADY_TARGETED"
        else:
            identifier = None
            status = "UNREVIEWED_SENTENCE_RELEVANCE"
            priority = priority_of_untested_line(text, tags)
        records.append({
            "paragraph_number": index,
            "text": text,
            "citation_numbers": list(tags),
            "attribution_review": status,
            "targeted_witness": identifier,
            "priority": priority,
        })
    if matched != set(target_by_sentence.values()):
        raise RuntimeError("R64_R63_TARGET_LINES_NOT_ALL_RENDERED: " + repr(sorted(set(target_by_sentence.values())-matched)))
    unreviewed = [item for item in records
                  if item["attribution_review"] == "UNREVIEWED_SENTENCE_RELEVANCE"]
    prioritized = sorted(unreviewed, key=lambda item:(0 if item["priority"].startswith("P1")
                                                      else 1 if item["priority"].startswith("P2") else 2,
                                                      item["paragraph_number"]))
    return {
        "total_proof_paragraphs": len(records),
        "r63_targeted_paragraphs": len(matched),
        "sentence_relevance_not_yet_audited": len(unreviewed),
        "full_sentence_attribution_audited": len(unreviewed) == 0,
        "lines": records,
        "next_review_candidates": prioritized[:8],
    }


def inspect_public() -> dict[str, object]:
    """Reuse real certified searches and R63 proof witnesses, without new proofs."""
    from phase165_r52_r9_shared_math import build_shared_typed_bridge
    from phase174_r3_r7_r56_cyclic_generator_bridge.audit import _search_with_model
    from phase174_r3_r7_r60_reference_ownership_audit.audit import audit_narrative_ownership
    from phase174_r3_r7_r63_sentence_witness_audit.audit import inspect_group
    from phase168_r3_5_model_renderer import render_model_backed_narrative_markdown

    bridge = build_shared_typed_bridge()
    groups = {}
    for n, k, label, expected in ((6, 5, "pi11_6", 3), (7, 5, "pi12_7", 2)):
        result, model = _search_with_model(n, k, bridge)
        markdown = render_model_backed_narrative_markdown(result, model)
        ownership = audit_narrative_ownership(result, model, markdown)
        evidence = inspect_group(result, model, markdown, n)
        if evidence["targeted_line_count"] != expected:
            raise RuntimeError("R64_R63_TARGET_WITNESS_COUNT_CHANGED: " + label)
        citation_numbers = tuple(citation.number for citation in model.citations)
        detail = audited_line_inventory(markdown, citation_numbers,
                                        evidence["targeted_lines"])
        if detail["r63_targeted_paragraphs"] != expected:
            raise RuntimeError("R64_TARGETED_LINE_BINDING_CHANGED: " + label)
        if detail["full_sentence_attribution_audited"]:
            raise RuntimeError("R64_UNEXPECTED_FULL_SENTENCE_ATTESTATION: " + label)
        if ownership["reference_count"] != (7 if n == 6 else 3):
            raise RuntimeError("R64_REFERENCE_REGRESSION: " + label)
        groups[label] = detail
    return groups


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--dry-run", action="store_true")
    args = parser.parse_args()
    root = Path(__file__).resolve().parents[1]
    checked = source_guard(root)
    head = local_head(root)
    print("PHASE174_R64_SOURCE_GUARD=PASS")
    print("PHASE174_R64_SOURCE_PINS=" + str(len(checked)))
    print("PHASE174_R64_LOCAL_HEAD=" + head)
    print("PHASE174_R64_PRODUCTION_CHANGES=0")
    if args.dry_run:
        print("PHASE174_R64_GATE=PASS_R64_READ_ONLY_DRYRUN")
        print("(END)")
        return 0
    groups = inspect_public()
    report = {
        "phase": "174-R3-R7-R64",
        "local_head": head,
        "source_pins": list(checked),
        "groups": groups,
        "interpretation": "R63 targets are anchored to verified ancestry. Other rendered paragraphs are NOT YET audited sentence by sentence; absence of a tag is not a defect.",
        "production_changes": 0,
        "new_given": 0,
        "new_mathematical_rules": 0,
        "full_pytest": False,
    }
    destination = Path(os.environ.get("LOCALAPPDATA", tempfile.gettempdir()))
    destination = destination / "EHPProofTracerAudit" / PACKAGE / "report.json"
    destination.parent.mkdir(parents=True, exist_ok=True)
    destination.write_text(json.dumps(report, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    for label, data in groups.items():
        prefix = "PHASE174_R64_" + label.upper() + "_"
        print(prefix + "PROOF_PARAGRAPHS=" + str(data["total_proof_paragraphs"]))
        print(prefix + "R63_TARGETED_PARAGRAPHS=" + str(data["r63_targeted_paragraphs"]))
        print(prefix + "SENTENCE_RELEVANCE_NOT_YET_AUDITED=" + str(data["sentence_relevance_not_yet_audited"]))
        print(prefix + "FULL_SENTENCE_ATTRIBUTION_AUDITED=" + str(data["full_sentence_attribution_audited"]))
    print("PHASE174_R64_NEW_GIVEN=0")
    print("PHASE174_R64_NEW_MATHEMATICAL_RULES=0")
    print("PHASE174_R64_REPORT=" + str(destination))
    print("PHASE174_R64_GATE=PASS_R64_SENTENCE_COVERAGE_FRONTIER_ONLY")
    print("(END)")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
```

## tests/test_audit.py（新規）

```python
"""Focused isolated R64 coverage inventory and failure-closed controls."""
from __future__ import annotations

from pathlib import Path
from types import SimpleNamespace

import pytest

from phase174_r3_r7_r64_sentence_coverage_frontier_audit.audit import (
    PINS, audited_line_inventory, git_blob_sha, priority_of_untested_line,
    proof_body_lines, source_guard,
)


def sample_markdown() -> str:
    return (
        "使用する結果\n\n**[R1] Example.**\n\n$x=y$.\n\n証明\n\n"
        "[R1]より, $x=y$.\n\n"
        "$z=w$.\n\n"
        "以上より, $A=B$.\n\n□\n"
    )


def test_full_line_inventory_is_conservative() -> None:
    result = audited_line_inventory(
        sample_markdown(), (1,), {"given": {"proof_line": "[R1]より, $x=y$."}}
    )
    assert result["total_proof_paragraphs"] == 3
    assert result["r63_targeted_paragraphs"] == 1
    assert result["sentence_relevance_not_yet_audited"] == 2
    assert result["full_sentence_attribution_audited"] is False
    assert result["lines"][1]["attribution_review"] == "UNREVIEWED_SENTENCE_RELEVANCE"
    assert result["lines"][2]["priority"] == "P1_UNCITED_INFERENCE"


def test_reference_paragraphs_not_counted_as_proof() -> None:
    assert proof_body_lines(sample_markdown()) == (
        "[R1]より, $x=y$.", "$z=w$.", "以上より, $A=B$."
    )


@pytest.mark.parametrize("value", [None, "", "証明\n\n[R1]よりx\n□", "使用する結果\n\n証明\n", "使用する結果\n証明\n証明\n□"])
def test_missing_or_ambiguous_proof_boundary_rejected(value) -> None:
    with pytest.raises((TypeError, RuntimeError)):
        proof_body_lines(value)


def test_unknown_rendered_tag_is_rejected() -> None:
    changed = sample_markdown().replace("[R1]より", "[R2]より")
    with pytest.raises(RuntimeError, match="UNKNOWN_RENDERED_CITATION"):
        audited_line_inventory(changed, (1,), {"given": {"proof_line": "[R2]より, $x=y$."}})


def test_duplicate_r63_witness_sentence_rejected() -> None:
    sentence = "[R1]より, $x=y$."
    with pytest.raises(RuntimeError, match="DUPLICATE_R63_WITNESS_LINE"):
        audited_line_inventory(sample_markdown(), (1,), {
            "first": {"proof_line": sentence}, "second": {"proof_line": sentence},
        })


def test_r63_target_line_must_exist_exactly() -> None:
    with pytest.raises(RuntimeError, match="R63_TARGET_LINES_NOT_ALL_RENDERED"):
        audited_line_inventory(sample_markdown(), (1,), {
            "given": {"proof_line": "[R1]より, $x=wrong$."},
        })


def test_r63_target_line_must_not_repeat() -> None:
    duplicated = sample_markdown().replace("$z=w$.", "[R1]より, $x=y$.")
    with pytest.raises(RuntimeError, match="AMBIGUOUS_TARGETED_LINE"):
        audited_line_inventory(duplicated, (1,), {
            "given": {"proof_line": "[R1]より, $x=y$."},
        })


def test_unverified_citation_does_not_become_certified() -> None:
    changed = sample_markdown().replace("$z=w$.", "[R1]より, $z=w$.")
    report = audited_line_inventory(changed, (1,), {
        "given": {"proof_line": "[R1]より, $x=y$."},
    })
    assert report["lines"][1]["priority"] == "P1_CITED_SENTENCE"
    assert report["lines"][1]["attribution_review"] == "UNREVIEWED_SENTENCE_RELEVANCE"


def test_no_citation_is_not_an_automatic_defect() -> None:
    assert priority_of_untested_line("$x=y$.", ()) == "P2_MATH_WITHOUT_INLINE_TAG"
    assert priority_of_untested_line("説明の続き.", ()) == "P3_PROSE_OR_TRANSITION"


def test_invalid_citation_number_tuple_rejected() -> None:
    for values in ((2,), (1, 3), (1, 1), [1], ("1",)):
        with pytest.raises(ValueError):
            audited_line_inventory(sample_markdown(), values, {"given": {"proof_line": "[R1]より, $x=y$."}})


def test_empty_or_untyped_witness_rejected() -> None:
    for targets in ({}, {"x": {"proof_line": ""}}, {"x": object()}):
        with pytest.raises(ValueError):
            audited_line_inventory(sample_markdown(), (1,), targets)


def test_readonly_source_pin_contract() -> None:
    root = Path(__file__).resolve().parents[2]
    assert len(PINS) == 8
    assert source_guard(root) == tuple(PINS)


def test_source_guard_rejects_tamper(tmp_path: Path) -> None:
    relative = next(iter(PINS))
    target = tmp_path / relative
    target.parent.mkdir(parents=True)
    target.write_bytes(b"unreviewed")
    with pytest.raises(RuntimeError, match="R64_SOURCE_BLOB_MISMATCH"):
        source_guard(tmp_path)


def test_git_blob_fixture() -> None:
    assert git_blob_sha(b"hello\n") == "ce013625030ba8dba906f756967f9e9ca394464a"
```

## run.ps1（新規）

```powershell
[CmdletBinding()]
param([switch]$DryRun)

$ErrorActionPreference = 'Stop'
$Root = (Resolve-Path (Join-Path $PSScriptRoot '..')).Path
Push-Location $Root
try {
    $module = 'phase174_r3_r7_r64_sentence_coverage_frontier_audit.audit'
    if ($DryRun) {
        python -B -m $module --dry-run
        if ($LASTEXITCODE -ne 0) { throw 'R64 DryRun Source Guard failed' }
    } else {
        python -B -m $module
        if ($LASTEXITCODE -ne 0) { throw 'R64 public sentence inventory failed' }
        python -B -m pytest -q -o addopts= -p no:cacheprovider --import-mode=importlib `
            'phase174_r3_r7_r64_sentence_coverage_frontier_audit/tests/test_audit.py' `
            'phase174_r3_r7_r63_sentence_witness_audit/tests/test_audit.py'
        if ($LASTEXITCODE -ne 0) { throw 'R64 focused pytest failed' }
        Write-Output 'PHASE174_R64_GATE=PASS_R64_FOCUSED_AND_COVERAGE_FRONTIER'
        Write-Output '(END)'
    }
}
finally {
    Pop-Location
}
```
