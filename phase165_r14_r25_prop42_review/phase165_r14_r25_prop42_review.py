"""Exact source-text review for Toda Proposition 4.2, without promotion."""
from __future__ import annotations
from dataclasses import dataclass,asdict
import json
from pathlib import Path

from phase165_r5_manifest_bridge import build_phase165_r5_manifest_bridge

CANDIDATE_IDS = (
    "phase163:archive:toda:tex:ch4:0002",
    "phase163:archive:toda:tex:ch4:0005",
)
# These are necessary scope checks, NOT sufficient certification.
TARGET_WINDOW = (
    "pi_3^3 --Delta--> pi_1^1 --E--> pi_2^2",
)

@dataclass(frozen=True)
class Prop42SourceReview:
    assertion_id: str
    locator: str
    source_text: str
    has_exactness_keyword: bool
    has_delta: bool
    has_suspension: bool
    has_index_range: bool
    source_text_present: bool
    certified: bool = False

def inspect_prop42_sources(bridge) -> tuple[Prop42SourceReview,...]:
    """Retrieve the actual archive records; never infer an EHP theorem by label."""
    records=[]
    for aid in CANDIDATE_IDS:
        assertion = bridge.registry._assertions.get(aid)
        if assertion is None:
            raise ValueError(f"missing recorded Proposition 4.2 candidate: {aid}")
        ref = bridge.registry.reference(assertion.reference_id)
        if "4.2" not in ref.locator:
            raise ValueError(f"unexpected proposition locator for {aid}: {ref.locator}")
        if not isinstance(assertion.content,dict):
            raise TypeError(f"unexpected source archive content for {aid}")
        raw=assertion.content.get("source_text")
        if not isinstance(raw,str) or not raw.strip():
            raise ValueError(f"missing original adopted source text for {aid}")
        low=raw.lower()
        records.append(Prop42SourceReview(
            assertion_id=aid,
            locator=ref.locator,
            source_text=raw,
            has_exactness_keyword=any(x in low for x in ("exact", "完全")),
            has_delta=any(x in raw for x in (r"\\Delta", "Δ", r"\\partial")),
            has_suspension=any(x in raw for x in (r"\\overset{E}",r"\\xrightarrow{E}",r"\\stackrel{E}",r"\\longrightarrow", "EHP")),
            has_index_range=any(x in raw for x in ("\\ge", "\\le", "\\forall", "n>", "i>", "n\\ge", "i\\ge")),
            source_text_present=True,
        ))
    return tuple(records)

def audit_r25() -> dict:
    bridge,summary = build_phase165_r5_manifest_bridge()
    before=(len(bridge.registry._assertions),len(bridge.proof_links))
    reviews=inspect_prop42_sources(bridge)
    after=(len(bridge.registry._assertions),len(bridge.proof_links))
    if before!=after:raise AssertionError("read-only review modified registry")
    return {
        "phase":"165 R14-R25",
        "candidate_count":len(reviews),
        "target_window":TARGET_WINDOW[0],
        "source_reviews":[asdict(r) for r in reviews],
        "source_assertions_preserved":summary.source_assertion_count,
        "semantic_application_certified":False,
        "proof_eligible_new":0,
        "new_proof_steps":0,
        "pi32_proved":False,
        "status":"PROP42_FULL_SOURCE_EXPORTED_MATHEMATICAL_SCOPE_REVIEW_PENDING",
        "full_pytest_run":False,
    }

def render_report(report:dict) -> str:
    lines=["# Phase 165 R14-R25 — Proposition 4.2 出典照合",
           "","## 対象の完全列","",f"`{report['target_window']}`","",
           "## 出典候補の全文と確認項目",""]
    for row in report["source_reviews"]:
        lines += [f"### {row['assertion_id']}","",
          f"- Locator: {row['locator']}",
          f"- 完全性語彙: {row['has_exactness_keyword']}",
          f"- Delta 記号: {row['has_delta']}",
          f"- E / 矢印記号: {row['has_suspension']}",
          f"- 次数条件らしき表記: {row['has_index_range']}",
          "- 数学的適用条件の確認: **未実施**","",
          "```tex",row["source_text"],"```",""]
    lines += ["## 判定","",
      "記号の出現だけでは exactness（完全性）・添字範囲を認証できない。",
      "該当文の原文と対象の Δ→E を照合するまでは ProofStep を作らない。"]
    return "\n".join(lines)+"\n"
