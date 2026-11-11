"""R71: source-pinned, read-only regression audit of shared completed proof text.

This module checks the existing Verified Proof Tree -> ProofNarrativeModel ->
common Renderer pipeline. It adds no mathematical assertions or inference rules.
"""
from __future__ import annotations

import argparse
from hashlib import sha1, sha256
import json
import os
from pathlib import Path
import subprocess
import tempfile


PACKAGE = "phase174_r3_r7_r71_common_narrative_regression"
REVIEWED_REMOTE_HEAD = "01c5246a011b43e10ed85699a6048f117562a748"
PINS = {
    "phase171_r20r13_eta_sentence_layout/projection.py": "77c7345f8d4c0c0c40c1059fad13de0e85e9910e",
    "phase174_r3_r7_r70_verified_narrative_projection/projection.py": "ba11bd850aba3f0eaacbe0d733c018a87e677070",
    "phase174_r3_r7_r70_verified_narrative_projection/tests/test_projection.py": "afd572c810d4e302710701530257057066ea548c",
    "phase174_r3_r7_r70r1_assoc_chain_display_fix/tests/test_install.py": "352d1a869a3aa188b770699d7cb7d5bb4f98d51b",
    "phase168_r3_5_model_renderer.py": "cb6989871ea4ad3964f714bfc5ada2a5099424a0",
    "phase174_r3_r7_r56_cyclic_generator_bridge/audit.py": "868e4dfad4d97bb3e5d5da462260bab3759d4af8",
    "phase174_r3_r7_r68_ehp_premise_semantics_audit/audit.py": "ab3506e1d7163546d1966b0187b0b583aa72d22f",
    "phase171_r20r13_eta_sentence_layout/tests/test_projection.py": "6031f6a1b396d040181f04b792bc5c5caf2c5530",
    "phase174_r3_r7_r70_verified_narrative_projection/audit.py": "1f44bb35d08d5d203a8171118e648f40320e6945",
}

# Existing, previously completed public goals; these are regression samples,
# never a list of inference-rule exceptions or special-case proof constructors.
COMPLETE_CASES = (
    (3, 3),  # pi_6^3: nontrivial eta display and eight references
    (4, 3),  # pi_7^4: mixed free / finite group
    (4, 4),  # pi_8^4: two-summand finite group
    (4, 5),  # pi_9^4: eta-squared composition
    (4, 7),  # pi_11^4: trivial group
    (5, 3),  # pi_8^5: cyclic finite extension
    (6, 5),  # pi_11^6: new R70 combined composition display
    (7, 5),  # pi_12^7: new R70 EHP prose explanation
)
EXPECTED_REFERENCE_COUNTS = {(3, 3): 8, (6, 5): 7, (7, 5): 3}


def git_blob_sha(raw: bytes) -> str:
    """Return the Git object ID of exact file bytes."""
    return sha1(b"blob " + str(len(raw)).encode("ascii") + b"\x00" + raw).hexdigest()


def source_guard(root: Path) -> tuple[str, ...]:
    """Fail closed on unreviewed code while permitting uniform CRLF checkouts."""
    matched: list[str] = []
    for path, expected in PINS.items():
        raw = (root / path).read_bytes()
        lf = raw.replace(b"\r\n", b"\n")
        if b"\r" in lf:
            raise RuntimeError("R71_UNEXPECTED_MIXED_EOL: " + path)
        variants = (raw, lf, lf.replace(b"\n", b"\r\n"))
        if expected not in {git_blob_sha(v) for v in variants}:
            raise RuntimeError("R71_UNREVIEWED_SOURCE: " + path)
        matched.append(path)
    return tuple(matched)


def local_head(root: Path) -> str:
    """Report the local HEAD; never mutate git state or force a pull."""
    command = subprocess.run(
        ["git", "rev-parse", "HEAD"], cwd=root,
        capture_output=True, text=True, check=False,
    )
    if command.returncode != 0:
        raise RuntimeError("R71_GIT_HEAD_UNAVAILABLE")
    return command.stdout.strip()


def reference_body_contract(markdown: str, reference_count: int) -> tuple[str, str]:
    """Check the existing complete-proof framing without interpreting prose."""
    if not isinstance(markdown, str) or not markdown.startswith("使用する結果\n"):
        raise RuntimeError("R71_COMPLETE_REFERENCE_HEADER_CHANGED")
    if markdown.count("\n証明\n") != 1:
        raise RuntimeError("R71_COMPLETE_PROOF_HEADING_CHANGED")
    reference_text, proof_text = markdown.split("\n証明\n", 1)
    if not proof_text.rstrip().endswith("□"):
        raise RuntimeError("R71_COMPLETE_END_MARKER_CHANGED")
    if reference_count < 1:
        raise RuntimeError("R71_MISSING_CITATIONS")
    for number in range(1, reference_count + 1):
        if f"[R{number}]" not in reference_text:
            raise RuntimeError(f"R71_MISSING_REFERENCE_R{number}")
    if r"\\to" in markdown:
        raise RuntimeError("R71_DOUBLE_ESCAPED_TEX_ARROW")
    return reference_text, proof_text


def inspect_public() -> list[dict[str, object]]:
    """Execute real searches and render their verified narratives without patching."""
    from phase165_r52_partial_proof import ProofSearchStatus
    from phase165_r52_r9_shared_math import build_shared_typed_bridge
    from phase165_r55_nk_only_goal import search_group_from_registered_goal
    from phase166_r3t_goal_source_binding.goal_source import resolve_specialized_goal_citing_id
    from phase168_r3_4_link_bridge import build_linked_proof_narrative_model
    from phase168_r3_41p13_trust_boundary import verify_proof_tree_for_narrative
    from phase168_r3_5_model_renderer import render_model_backed_narrative_markdown
    from phase174_r3_r7_r56_cyclic_generator_bridge.audit import _search_with_model

    bridge = build_shared_typed_bridge()
    report: list[dict[str, object]] = []
    for n, k in COMPLETE_CASES:
        if (n, k) in ((6, 5), (7, 5)):
            result, model = _search_with_model(n, k, bridge)
        else:
            contexts = []
            result = search_group_from_registered_goal(
                n=n, k=k, bridge=bridge, context_sink=contexts.append,
            )
            if result.status is not ProofSearchStatus.COMPLETE or result.open_goals:
                raise RuntimeError(f"R71_EARLIER_COMPLETE_BECAME_PARTIAL: n={n} k={k}")
            if len(contexts) != 1:
                raise RuntimeError(f"R71_SOURCE_CONTEXT_COUNT_CHANGED: n={n} k={k}")
            cited_id = resolve_specialized_goal_citing_id(bridge, result.conclusion)
            if cited_id is None:
                verify_proof_tree_for_narrative(
                    result, contexts[0], citing_assertion_id=None,
                    derived_target_without_citing_id=True,
                )
            else:
                verify_proof_tree_for_narrative(
                    result, contexts[0], citing_assertion_id=cited_id,
                )
            model = build_linked_proof_narrative_model(result, contexts[0])

        if result.status is not ProofSearchStatus.COMPLETE or result.open_goals:
            raise RuntimeError(f"R71_COMPLETED_STATE_CHANGED: n={n} k={k}")
        if model.root_index is None or not (0 <= model.root_index < len(model.steps)):
            raise RuntimeError(f"R71_MISSING_VERIFIED_ROOT: n={n} k={k}")
        if model.steps[model.root_index].conclusion != result.conclusion:
            raise RuntimeError(f"R71_ROOT_CONCLUSION_CHANGED: n={n} k={k}")
        original_steps = tuple(model.steps)
        original_citations = tuple(model.citations)
        markdown = render_model_backed_narrative_markdown(result, model)
        if (tuple(model.steps) != original_steps
                or tuple(model.citations) != original_citations):
            raise RuntimeError(f"R71_RENDERER_MUTATED_PROOF_MODEL: n={n} k={k}")
        reference_count = len(model.citations)
        reference_body_contract(markdown, reference_count)
        expected = EXPECTED_REFERENCE_COUNTS.get((n, k))
        if expected is not None and reference_count != expected:
            raise RuntimeError(f"R71_REFERENCE_COUNT_CHANGED: n={n} k={k}")
        if (n, k) == (6, 5):
            if (r"E(\nu_{5}\eta_{8}^{2})=\nu_{6}\eta_{9}^{2}=0"
                    not in markdown):
                raise RuntimeError("R71_R70_COMPOSITE_DISPLAY_REGRESSION")
        if (n, k) == (7, 5):
            if (r"\ker H=\operatorname{Im}E=0" not in markdown
                    or r"\Delta: \pi_{13}^{13}\to \pi_{11}^{6}" not in markdown):
                raise RuntimeError("R71_R70_EHP_DISPLAY_REGRESSION")
        report.append({
            "n": n, "k": k, "group": f"pi_{n+k}^{n}",
            "status": result.status.name, "verified_root": True,
            "step_count": len(model.steps), "reference_count": reference_count,
            "markdown_sha256": sha256(markdown.encode("utf-8")).hexdigest(),
            "narrative_characters": len(markdown),
        })
    return report


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--dry-run", action="store_true")
    args = parser.parse_args()
    root = Path(__file__).resolve().parents[1]
    pins = source_guard(root)
    head = local_head(root)
    print("PHASE174_R71_SOURCE_GUARD=PASS")
    print("PHASE174_R71_SOURCE_PINS=" + str(len(pins)))
    print("PHASE174_R71_REVIEWED_REMOTE_HEAD=" + REVIEWED_REMOTE_HEAD)
    print("PHASE174_R71_LOCAL_HEAD=" + head)
    print("PHASE174_R71_PRODUCTION_CHANGES=0")
    if args.dry_run:
        print("PHASE174_R71_GATE=PASS_R71_READ_ONLY_DRYRUN")
        print("(END)")
        return 0
    results = inspect_public()
    target = (Path(os.environ.get("LOCALAPPDATA", tempfile.gettempdir()))
              / "EHPProofTracerAudit" / PACKAGE / "report.json")
    target.parent.mkdir(parents=True, exist_ok=True)
    payload = {
        "phase": "174-R71", "reviewed_remote_head": REVIEWED_REMOTE_HEAD,
        "local_head": head, "source_files_checked": list(pins),
        "public_samples": results, "production_changes": [],
        "new_given": 0, "new_mathematical_rules": 0,
        "whole_test_suite_executed": False,
        "full_sentence_semantics_certified": False,
    }
    target.write_text(json.dumps(payload, ensure_ascii=False, indent=2) + "\n",
                      encoding="utf-8")
    print("PHASE174_R71_PUBLIC_COMPLETE_CASES=" + str(len(results)))
    for item in results:
        print("PHASE174_R71_CASE=" + str(item["group"]) + ":PASS:" +
              str(item["reference_count"]) + "_REFERENCES")
    print("PHASE174_R71_NEW_GIVEN=0")
    print("PHASE174_R71_NEW_MATHEMATICAL_RULES=0")
    print("PHASE174_R71_REPORT=" + str(target))
    print("PHASE174_R71_GATE=PASS_R71_READ_ONLY_FOCUSED_PUBLIC_REGRESSION")
    print("(END)")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
