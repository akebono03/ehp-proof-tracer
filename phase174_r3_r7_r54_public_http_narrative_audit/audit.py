"""R54: observe actual Flask Group query HTML without stubs or Renderer edits.

This is a real in-process HTTP request, not a live-host deployment or an
independent browser/KaTeX rendering test. Do not fabricate proven steps.
"""
from __future__ import annotations

import argparse
from html.parser import HTMLParser
import json
import os
from pathlib import Path
import tempfile
from typing import Any


class ProofHTMLParser(HTMLParser):
    """Read only the public proof's named HTML section and exact attributes."""

    _VOID_TAGS = frozenset((
        "area", "base", "br", "col", "embed", "hr", "img", "input",
        "link", "meta", "param", "source", "track", "wbr",
    ))

    def __init__(self) -> None:
        super().__init__(convert_charrefs=True)
        self.conclusion_latex: str | None = None
        self.proof_mode: str | None = None
        self.proof_expressions: list[str] = []
        self.proof_fragments: list[str] = []
        self.all_fragments: list[str] = []
        self._render_depth = 0
        self._proof_regions = 0
        self._conclusions = 0

    def handle_starttag(self, tag: str, attrs: list[tuple[str, str | None]]) -> None:
        attributes = dict(attrs)
        if attributes.get("id") == "group-proof-conclusion":
            self._conclusions += 1
            self.conclusion_latex = attributes.get("data-latex")
        if attributes.get("id") == "group-proof-rendered-lines":
            if self._render_depth:
                raise ValueError("Nested public proof region")
            self._proof_regions += 1
            self._render_depth = 1
            self.proof_mode = attributes.get("data-proof-mode")
        elif self._render_depth and tag not in self._VOID_TAGS:
            self._render_depth += 1
        if self._render_depth and attributes.get("data-latex") is not None:
            self.proof_expressions.append(attributes["data-latex"] or "")

    def handle_startendtag(self, tag: str, attrs: list[tuple[str, str | None]]) -> None:
        # A self-closing element cannot extend the proof-section nesting.
        attributes = dict(attrs)
        if self._render_depth and attributes.get("data-latex") is not None:
            self.proof_expressions.append(attributes["data-latex"] or "")

    def handle_endtag(self, tag: str) -> None:
        if self._render_depth and tag not in self._VOID_TAGS:
            self._render_depth -= 1

    def handle_data(self, data: str) -> None:
        if data.strip():
            self.all_fragments.append(data.strip())
            if self._render_depth:
                self.proof_fragments.append(data.strip())

    def verified_section(self) -> bool:
        return self._conclusions == 1 and self._proof_regions == 1 and self._render_depth == 0


def observe_response(response: object, *, form_kind: str) -> dict[str, Any]:
    """Check actual HTML, conclusion and verified narrative; record copy defects."""
    if not hasattr(response, "data") or not hasattr(response, "status_code"):
        raise TypeError("Flask HTTP response required")
    parser = ProofHTMLParser()
    parser.feed(response.data.decode("utf-8"))
    parser.close()
    expressions = parser.proof_expressions
    body = " ".join(parser.proof_fragments)
    full = " ".join(parser.all_fragments)
    required = (
        response.status_code == 200
        and parser.verified_section()
        and parser.conclusion_latex is not None
        and parser.conclusion_latex.replace(" ", "") == r"\pi_{12}^{7}=0"
        and parser.proof_mode == "narrative"
        and "generic-complete-proof" in full
        and "Conclusion" in full
        and "Proof target" not in full
        and "以上より" in body
        and "□" in body
        and "Proposition 2.7" in body
        and "Proposition 4.2" in body
        and "(5.10)" in body
        and "未解決 Goal" not in body
    )
    if not required:
        raise RuntimeError(
            "Public HTTP verified conclusion or reference tree missing: "
            + repr({"form_kind": form_kind, "http": response.status_code,
                    "conclusion": parser.conclusion_latex, "mode": parser.proof_mode,
                    "verified_section": parser.verified_section(),
                    "text_tail": body[-450:]})
        )
    intro_count = body.count("の群構造を決定するために")
    return {
        "form_kind": form_kind,
        "http_status": response.status_code,
        "public_proof_key": "generic-complete-proof",
        "conclusion_latex": parser.conclusion_latex,
        "proof_mode": parser.proof_mode,
        "proof_text_characters": len(body),
        "proof_latex_expressions": len(expressions),
        "verified_conclusion": True,
        "citation_references_visible": True,
        "proof_ends_with_box": "□" in body,
        "repeated_intro_count": intro_count,
        "duplicate_intro_observed": intro_count > 1,
        "browser_katex_checked": False,
    }


def inspect_public_http_proof() -> dict[str, object]:
    """Use Flask's real public POST routes with no proof/search monkeypatch."""
    from flask import Response
    from web_app import create_app
    app = create_app()
    app.config.update(TESTING=True)
    client = app.test_client()
    cases = (
        ("group", {"form_kind": "group", "n": "7", "k": "5"}),
        ("group_proof", {
            "form_kind": "group_proof", "n": "7", "k": "5",
            "group_proof_depth": "2", "group_proof_mode": "narrative",
        }),
    )
    results = []
    for name, payload in cases:
        response = client.post("/", data=payload)
        if not isinstance(response, Response):
            raise RuntimeError("Flask returned an invalid HTTP response")
        results.append(observe_response(response, form_kind=name))
    return {
        "root": "pi_12^7 = 0",
        "inprocess_http_verified": True,
        "checked_form_kinds": [x["form_kind"] for x in results],
        "cases": results,
        "both_http_200": all(x["http_status"] == 200 for x in results),
        "both_complete_proof": all(x["verified_conclusion"] for x in results),
        "narrative_duplicate_intro_observed": any(
            x["duplicate_intro_observed"] for x in results
        ),
        "production_files_changed": 0,
        "new_given": 0,
        "new_mathematical_rules": 0,
        "live_server_checked": False,
        "browser_katex_checked": False,
        "full_pytest": False,
    }


def report_path(dry_run: bool) -> Path:
    base = Path(os.environ.get("LOCALAPPDATA", tempfile.gettempdir()))
    return base / "EHPProofTracerAudit" / "phase174_r3_r7_r54" / (
        "preflight.json" if dry_run else "http_narrative_audit.json"
    )


def main() -> int:
    from phase174_r3_r7_r54_public_http_narrative_audit.source_guard import verify_checkout
    args = argparse.ArgumentParser(description=__doc__)
    args.add_argument("--dry-run", action="store_true")
    opts = args.parse_args()
    state = verify_checkout()
    observed = None if opts.dry_run else inspect_public_http_proof()
    gate = ("PASS_R54_R53_HTTP_PREFLIGHT" if opts.dry_run else
            "PASS_R54_INPROCESS_PUBLIC_HTTP_COMPLETE_DUPLICATE_RECORDED")
    result = {"phase": "174-R3-R7-R54", "state": state,
              "observations": observed, "gate": gate}
    path = report_path(opts.dry_run)
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(result, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    prefix = "PHASE174_R3R7R54_"
    for key, value in state.items():
        print(prefix + key.upper() + "=" + str(value))
    if observed is not None:
        for key, value in observed.items():
            print(prefix + key.upper() + "=" + str(value))
    print(prefix + "REPORT=" + str(path))
    print(prefix + "GATE=" + gate)
    print("(END)")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
