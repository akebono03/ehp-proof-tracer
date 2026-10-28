"""Phase 169 R10ET-R6: read-only proof-DAG residual Definition audit.

This does not change a provider, proof step, registry, test or Git index.
It certifies the exact already-reviewed R5 production provider by byte equality
with a transform of Git's R4 baseline, then reads real completed proof trees.
"""
from __future__ import annotations

import argparse
import json
import os
import re
import subprocess
import sys
import traceback
from pathlib import Path
from typing import Any

sys.dont_write_bytecode = True

R4_COMMITTED = "3a8014efb91ddf76060c4d07d73153e55ea52c75"
R2_BASELINE = (
    "phase169_r10et_r2_shadow_common_definition_comparison/"
    "output/20261028_151843_654/audit.json"
)
R5_PROVIDER = "phase165_r52_r9_shared_math.py"
R4_OUTPUTS = (
    "phase168_r3_5_model_renderer.py",
    "phase169_r10a_verified_stable_chain_projection/projection.py",
)
REQUIRED = (
    (43, 26), (30, 26), (30, 11), (30, 14), (30, 16), (30, 9),
    (2, 1), (3, 1), (4, 1), (2, 2), (3, 2), (4, 2),
    (22, 6), (22, 10), (15, 8), (24, 9),
)
# Previously published completed proofs, outside the R5 acceptance corpus.
# These are probes, not grounds to rewrite mathematics or assert universality.
PROBES = ((8, 2), (13, 9), (15, 9))
STABLE_TRANSPORT = (
    (43, 26), (30, 26), (30, 11), (30, 14), (30, 16), (30, 9),
    (22, 6), (22, 10), (15, 8), (24, 9),
)


def git_bytes(root: Path, *args: str) -> bytes:
    return subprocess.run(
        ("git", "-C", str(root), *args), check=True,
        stdout=subprocess.PIPE, stderr=subprocess.PIPE,
    ).stdout


def git_text(root: Path, *args: str) -> str:
    return git_bytes(root, *args).decode("utf-8", errors="replace").strip()


def tracked_snapshot(root: Path) -> dict[str, str]:
    """Include staged blob ids, preserving existing user changes verbatim."""
    return {
        "unstaged_raw": git_bytes(root, "diff", "--raw", "-z").hex(),
        "staged_raw": git_bytes(root, "diff", "--cached", "--raw", "-z").hex(),
        "unstaged_names": git_text(root, "diff", "--name-status"),
        "staged_names": git_text(root, "diff", "--cached", "--name-status"),
    }


def certify_reviewed_production(root: Path) -> dict[str, str]:
    """Certify exact R5D and R6C production against reviewed Git R4 bytes.

    R6C is a source-verified root-reachability change. Verify its *exact*
    transformation of the reviewed R4 Model and Renderer; do not loosen
    acceptance to arbitrary modified renderers or arbitrary citations.
    """
    from hashlib import sha256
    from phase169_r10et_r5d_staged_audit_guard.patch import (
        EXPECTED_BLOBS, git_blob, transform,
    )
    from phase169_r10et_r6c_root_reachable_citations.patch import (
        EXPECTED_GIT_BLOBS, MODEL, RENDERER, transform as transform_r6c,
    )

    branch = git_text(root, "branch", "--show-current")
    head = git_text(root, "rev-parse", "HEAD")
    if branch != "develop":
        raise RuntimeError(f"R6 refuses branch {branch!r}; develop required")
    ancestor = subprocess.run(
        ("git", "-C", str(root), "merge-base", "--is-ancestor", R4_COMMITTED, head),
        capture_output=True,
    )
    if ancestor.returncode != 0:
        raise RuntimeError("R6 refuses HEAD outside the reviewed R4 ancestry")

    r6c_path = root / "phase169_r10et_r6c_root_reachable_citations/patch.py"
    r6c_expected_sha256 = "dc2c79ad779119f553ebbfeb39a424d8ea816d971e638d09f2df143d4daefdd0"
    if sha256(r6c_path.read_bytes()).hexdigest() != r6c_expected_sha256:
        raise RuntimeError("R6 refuses changed or unknown R6C transform source")

    checked: dict[str, str] = {}
    for path, original_blob in EXPECTED_BLOBS.items():
        before = git_bytes(root, "show", f"{R4_COMMITTED}:{path}")
        if git_blob(before) != original_blob:
            raise RuntimeError(f"reviewed R4 source changed: {path}")
        after, _functions = transform(path, before)
        if (root / path).read_bytes() != after:
            raise RuntimeError(f"R6 requires exact completed R5 production: {path}")
        checked[path] = git_blob(after)

    r4_blobs = {
        "phase168_r3_3_proof_narrative_model.py":
            "1080843a2a90bf60f0b8096d3c5542a24a9abb7c",
        "phase168_r3_5_model_renderer.py":
            "6694fa68205628d5bd870a08f38b1d4df2d45681",
        "phase169_r10a_verified_stable_chain_projection/projection.py":
            "a166ffbbb64d3cc60bc964cb4c42f854d1207953",
    }
    if set(EXPECTED_GIT_BLOBS) != {MODEL, RENDERER}:
        raise RuntimeError("R6C certified Model/Renderer scope is unexpected")
    if (EXPECTED_GIT_BLOBS.get(MODEL) != r4_blobs[MODEL]
            or EXPECTED_GIT_BLOBS.get(RENDERER) != r4_blobs[RENDERER]):
        raise RuntimeError("R6C source baselines differ from reviewed R4")
    for path, expected_blob in r4_blobs.items():
        before = git_bytes(root, "show", f"{R4_COMMITTED}:{path}")
        if git_blob(before) != expected_blob:
            raise RuntimeError(f"reviewed R4 Projection/Model/Renderer differs: {path}")
        after = transform_r6c(path, before) if path in (MODEL, RENDERER) else before
        if (root / path).read_bytes() != after:
            raise RuntimeError(f"reviewed R6C Projection/Model/Renderer differs: {path}")
        checked[path] = git_blob(after)
    return checked

def summarize_dependency(case: dict[str, Any], baseline: dict | None,
                         *, stable_transport: bool, required: bool) -> dict[str, Any]:
    """Check verified proof ancestry, not reference-title filtering."""
    problems: list[str] = []
    if case.get("status") != "complete" or case.get("trust") != "PASS":
        problems.append("proof is not complete and trusted")
    citations = case.get("references", ())
    locators = [item.get("locator") for item in citations]
    if citations and any(not item.get("reachable_from_root")
                         or not item.get("reference_heading_displayed")
                         or not item.get("directly_attributed_to_given")
                         for item in citations):
        problems.append("citation is detached from root/GIVEN/Reference heading")
    eligible = case.get("image_common_eligible", 0)
    canonical = case.get("image_actual_common", 0)
    if canonical != eligible or case.get("image_cited_but_common_eligible", 0) != 0:
        problems.append("some eligible image has noncanonical or cited dependency")
    if baseline is not None:
        old = [item.get("locator") for item in baseline.get("references", ())]
        if locators != old:
            problems.append("Reference differs from independently verified R2 shadow proof")
        if canonical != baseline.get("image_actual_common"):
            problems.append("canonical Definition count differs from R2 shadow proof")
        if (case.get("root_first_two_premise_support")
                != baseline.get("root_first_two_premise_support")):
            problems.append("root source / (4.5) support changed from baseline")
    elif required:
        problems.append("required case missing from reviewed R2 baseline")
    if stable_transport:
        if (len(locators) != 2 or not isinstance(locators[0], str)
                or not locators[0].startswith("DB prior:")
                or locators[1] != "(4.5)"):
            problems.append("DB prior / (4.5) references missing or polluted")
        support = case.get("root_first_two_premise_support", ())
        if (len(support) != 2
                or 1 not in support[0].get("citation_numbers", ())
                or 2 not in support[1].get("citation_numbers", ())):
            problems.append("DB prior and Toda (4.5) are not independently rooted")
    return {
        "case": case.get("group"), "required": required,
        "status": case.get("status"), "trust": case.get("trust"),
        "canonical_image_steps": canonical,
        "eligible_image_steps": eligible,
        "remaining_eligible_cited_steps": case.get("image_cited_but_common_eligible", 0),
        "noneligible_image_steps": case.get("images", 0) - eligible,
        "root_ancestry_steps": case.get("root_ancestry_steps"),
        "reference_locators": locators,
        "root_support": case.get("root_first_two_premise_support", ()),
        "problems": problems, "passed": not problems,
    }


def markdown_report(report: dict[str, Any]) -> str:
    lines = [
        "# Phase 169 R10ET-R6 — 個別 Definition の残存依存監査", "",
        "AUDIT_ONLY。既存 Proof Tree、命題台帳、Renderer、既存テスト、Git index は変更しない。", "",
        f"- Git HEAD: `{report['head']}`",
        f"- 本番 R4/R5 ファイル一致: `{report['source_verified']}`",
        f"- Git tracked/index 完全保持: `{report['tracked_unchanged']}`",
        "- 全体 pytest: 実行しない", "",
        "| 群 | 区分 | 完成/Trust | 共通Definition採用 | 置換可能な引用付き像 | Reference |",
        "|---|---|---|---:|---:|---|",
    ]
    for item in report["cases"]:
        state = f"{item['status']} / {item['trust']}"
        locators = ", ".join(item["reference_locators"])
        lines.append(
            f"| `{item['case']}` | {'必須' if item['required'] else '追加調査'} | "
            f"{state} | {item['canonical_image_steps']} | "
            f"{item['remaining_eligible_cited_steps']} | {locators} |"
        )
    lines.extend(("", "## 残存依存と検証上の注意", ""))
    for item in report["cases"]:
        if item["problems"]:
            lines.append(f"- `{item['case']}`: " + "; ".join(item["problems"]))
    if not any(row["problems"] for row in report["cases"]):
        lines.append("- 今回調査した全ケースで検出した問題はありません。")
    lines.extend((
        "", "Proof Tree で引用されない個別 Definition が命題台帳に残ることは、",
        "その Definition が証明に依存していることを意味しない。",
        "共通 Definition の適用範囲外に残る証明は無条件に削除しない。",
        "この監査は対象ケースでの依存解消を確認するもので、全 stem への数学的な完全性を主張しない。",
        "DB prior と Toda (4.5) は独立した証明根拠として維持する。", "",
    ))
    return "\n".join(lines)


def run(root: Path, output: Path, include_probes: bool) -> int:
    if output.exists():
        raise RuntimeError(f"refuse overwrite existing report: {output}")
    baseline_path = root / R2_BASELINE
    baseline_data = json.loads(baseline_path.read_text(encoding="utf-8"))
    if (baseline_data.get("mode") != "AUDIT_ONLY_SHADOW"
            or not baseline_data.get("all_complete_trusted")):
        raise RuntimeError("R6 refuses incomplete R2 reference baseline")
    baseline = {row["group"]: row for row in baseline_data["cases"]}
    initially = tracked_snapshot(root)
    hashes = certify_reviewed_production(root)
    output.mkdir(parents=True)
    sys.path.insert(0, str(root))
    from phase165_r52_r9_shared_math import build_shared_typed_bridge
    from phase169_r10et_r1_definition_reference_dependency_audit.audit import inspect_case
    bridge = build_shared_typed_bridge()
    cases = REQUIRED + (PROBES if include_probes else ())
    report: dict[str, Any] = {
        "phase": "169 R10ET-R6", "mode": "AUDIT_ONLY",
        "head": git_text(root, "rev-parse", "HEAD"),
        "source_verified": bool(hashes), "source_blobs": hashes,
        "baseline": R2_BASELINE, "cases": [], "full_pytest_run": False,
        "production_changed": [], "tracked_unchanged": False,
        "mandatory_count": len(REQUIRED), "probe_count": len(PROBES) if include_probes else 0,
    }
    try:
        for n, k in cases:
            label = f"pi_{n+k}^{n}"
            required = (n, k) in REQUIRED
            print(f"R10ET_R6_CASE_START={label}", flush=True)
            try:
                details = inspect_case(bridge, n, k, output)
                assessment = summarize_dependency(
                    details, baseline.get(label),
                    stable_transport=(n, k) in STABLE_TRANSPORT,
                    required=required,
                )
            except Exception as exc:
                assessment = {
                    "case": label, "required": required, "status": "ERROR",
                    "trust": "ERROR", "canonical_image_steps": 0,
                    "remaining_eligible_cited_steps": 0,
                    "reference_locators": [], "problems": [f"{type(exc).__name__}: {exc}"],
                    "passed": False, "traceback": traceback.format_exc(),
                }
            report["cases"].append(assessment)
            print(f"R10ET_R6_{label}_TRUST={assessment['trust']}", flush=True)
            print(f"R10ET_R6_{label}_REMAINING={assessment['remaining_eligible_cited_steps']}", flush=True)
            print(f"R10ET_R6_{label}_CHECK={'PASS' if assessment['passed'] else 'REVIEW_REQUIRED'}", flush=True)
    finally:
        report["tracked_unchanged"] = tracked_snapshot(root) == initially
        report["required_pass"] = all(x["passed"] for x in report["cases"] if x["required"])
        report["probes_pass"] = all(x["passed"] for x in report["cases"] if not x["required"])
        (output / "audit.json").write_text(
            json.dumps(report, ensure_ascii=False, indent=2) + "\n", encoding="utf-8"
        )
        (output / "audit.md").write_text(markdown_report(report), encoding="utf-8")
        print(f"R10ET_R6_REPORT={output / 'audit.md'}", flush=True)
        print(f"R10ET_R6_TRACKED_INDEX_UNCHANGED={report['tracked_unchanged']}", flush=True)
        print(f"R10ET_R6_REQUIRED_PASS={report['required_pass']}", flush=True)
        print(f"R10ET_R6_PROBES_PASS={report['probes_pass']}", flush=True)
    return 0 if (report["required_pass"] and report["probes_pass"]
                 and report["tracked_unchanged"]) else 1


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--root", required=True, type=Path)
    parser.add_argument("--output", required=True, type=Path)
    parser.add_argument("--probes", choices=("on", "off"), default="on")
    args = parser.parse_args(argv)
    root = args.root.resolve()
    output = args.output.resolve()
    print("R10ET_R6_MODE=AUDIT_ONLY", flush=True)
    print(f"R10ET_R6_REPO={root}", flush=True)
    try:
        return run(root, output, args.probes == "on")
    except BaseException:
        print("R10ET_R6_ERROR=" + traceback.format_exc(), flush=True)
        return 1


if __name__ == "__main__":
    raise SystemExit(main())
