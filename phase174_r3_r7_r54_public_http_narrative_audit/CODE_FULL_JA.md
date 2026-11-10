# R54 追加コード全文


追加位置: 全ファイルを `phase174_r3_r7_r54_public_http_narrative_audit/` 配下に新規追加する。既存ファイルへの差分はない。


## `__init__.py`（全文）

```python
"""R54 in-process HTTP and common narrative display audit."""
```


## `source_guard.py`（全文）

```python
"""R54: review both pre-merge and R53-merged public HTTP code strictly."""
from __future__ import annotations

from pathlib import Path

from phase174_r3_r7_r53_public_source_bound_kernel.install import patched_source
from phase174_r3_r7_r53_public_source_bound_kernel.source_guard import (
    ROOT, REVIEWED_HEAD as R52_MERGED_HEAD, git, git_blob, git_bytes, normalized,
    verify_checkout as verify_r53_unmerged,
)

R53_MERGED_HEAD = "e2598a3b4c865afea15b06b097c809333fabcc85"
TARGET = "phase165_r55_nk_only_goal.py"
ORIGINAL_TARGET_BLOB = "9aa232c8f98a7a75f27266044224eddfa98c5e04"
INSTALLED_TARGET_BLOB = "e436879f578148fe5c30f5a34974bea3425108b2"
PINNED_WEB_BLOBS = {
    "web_app.py": "6f95663df5cbf028bb16d1f05dca62db2e3fc00e",
    "templates/index.html": "7af2afa40b92b8c1ec3916cf9759516c158b989f",
    "phase165_r52_r4_flask_bridge.py": "aec7615671ea0b472d4f6093c06fc0f857632db7",
    "phase165_r52_r3_web_adapter.py": "dda215780c0468cf421592aff86c79b1f5482eed",
    "phase168_r3_5_model_renderer.py": "64e0570e8462ee0361ed07afab836c66ce8e7895",
    "phase168_r3_41p13_trust_boundary/verification.py": "547464846ce574d227092a4aacb895d2e2dfefca",
    "tests/test_phase145_group_proof_defaults.py": "914d045cfd9615afa90cd0e877c298b7fd994426",
    "test_phase165_r52_r4_flask_connection.py": "45e42093449f9b09dfbba5e86bcbd56d86bf3d80",
}


def verify_checkout() -> dict[str, object]:
    """Accept only two reviewed source states, with identical installed R53 bytes."""
    if Path(git("rev-parse", "--show-toplevel")).resolve() != ROOT.resolve():
        raise RuntimeError("R54 must be unpacked under the repository root")
    if git("branch", "--show-current") != "develop":
        raise RuntimeError("R54 expects the develop branch")
    head = git("rev-parse", "HEAD")
    remote = git("ls-remote", "origin", "refs/heads/develop")
    remote_head = remote.split()[0] if remote else ""
    if head != remote_head or head not in (R52_MERGED_HEAD, R53_MERGED_HEAD):
        raise RuntimeError("R54 GitHub HEAD must be the reviewed R52 or R53 commit")
    if git("diff", "--cached", "--name-only"):
        raise RuntimeError("R54 requires an unstaged and unmodified Git index")
    working_changes = tuple(git("diff", "--name-only").splitlines())
    mode = "R53_UNCOMMITTED" if head == R52_MERGED_HEAD else "R53_MERGED"
    allowed = (TARGET,) if mode == "R53_UNCOMMITTED" else ()
    if working_changes != allowed:
        raise RuntimeError("R54 found unreviewed tracked working changes: " + repr(working_changes))
    baseline = git_bytes("show", R52_MERGED_HEAD + ":" + TARGET)
    if git_blob(baseline) != ORIGINAL_TARGET_BLOB:
        raise RuntimeError("R52 reviewed public search target changed")
    updated = patched_source(normalized(baseline).decode("utf-8-sig"))
    current = normalized((ROOT / TARGET).read_bytes()).decode("utf-8-sig")
    if current != updated:
        raise RuntimeError("R53 public Source-bound implementation is not installed")
    head_target = git_bytes("show", "HEAD:" + TARGET)
    expected_head_blob = (
        ORIGINAL_TARGET_BLOB if mode == "R53_UNCOMMITTED" else INSTALLED_TARGET_BLOB
    )
    if git_blob(head_target) != expected_head_blob:
        raise RuntimeError("Unexpected committed public search function blob")
    if mode == "R53_UNCOMMITTED":
        verify_r53_unmerged()
    for relative, expected in PINNED_WEB_BLOBS.items():
        source = git_bytes("show", "HEAD:" + relative)
        if git_blob(source) != expected:
            raise RuntimeError("Unreviewed R54 HTTP source blob: " + relative)
        installed = (ROOT / relative).read_bytes()
        if normalized(installed) != normalized(source):
            raise RuntimeError("HTTP or narrative source changed: " + relative)
    return {
        "source_guard": "PASS",
        "local_head": head,
        "remote_head": remote_head,
        "handoff_mode": mode,
        "r53_public_wiring_installed": True,
        "reviewed_http_and_renderer_blobs": len(PINNED_WEB_BLOBS),
        "tracked_changes": working_changes,
        "production_files_changed_by_r54": 0,
        "new_given": 0,
        "new_math_rules": 0,
        "full_pytest": False,
    }
```


## `audit.py`（全文）

```python
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
```


## `tests/test_static.py`（全文）

```python
"""R54 read-only scope, source pinning, and no skipped implementation."""
from __future__ import annotations

import ast
from pathlib import Path

PACKAGE = Path(__file__).resolve().parents[1]


def test_r54_sources_parse_and_have_no_ellipsis() -> None:
    sources = tuple(PACKAGE.glob("*.py")) + tuple((PACKAGE / "tests").glob("test_*.py"))
    assert len(sources) >= 6
    for path in sources:
        tree = ast.parse(path.read_text(encoding="utf-8"))
        assert not any(isinstance(node, ast.Constant) and node.value is Ellipsis
                       for node in ast.walk(tree)), path


def test_run_script_is_read_only_and_focused() -> None:
    source = (PACKAGE / "run.ps1").read_text(encoding="utf-8")
    assert "--dry-run" in source
    assert "-p no:cacheprovider" in source
    assert "--import-mode=importlib" in source
    assert "FULL_PYTEST=False" in source
    for unwanted in ("git reset", "git clean", "git add", "git commit", "install.py"):
        assert unwanted not in source


def test_audit_uses_real_flask_and_no_proof_injection() -> None:
    source = (PACKAGE / "audit.py").read_text(encoding="utf-8")
    assert "from web_app import create_app" in source
    assert 'client.post("/", data=payload)' in source
    assert "form_kind" in source
    assert '"group_proof"' in source
    assert '"group"' in source
    assert "ProofStep(" not in source
    assert "monkeypatch.setattr(" not in source
    assert "patch.object" not in source
    assert '"browser_katex_checked": False' in source
```


## `tests/test_html_parser.py`（全文）

```python
"""Small, reproducible test fixtures for the HTML contract only."""
from __future__ import annotations

from dataclasses import dataclass

import pytest

from phase174_r3_r7_r54_public_http_narrative_audit.audit import (
    ProofHTMLParser, observe_response,
)


@dataclass
class FakeResponse:
    status_code: int
    data: bytes


def fixture_response(*, key: str = "generic-complete-proof", conclusion: str = r"\pi_{12}^{7}=0", duplicated: bool = False) -> FakeResponse:
    extra = " の群構造を決定するために" if duplicated else ""
    html = (
        "<html><body><h3>Conclusion</h3>"
        '<div id="group-proof-conclusion" data-latex="' + conclusion + '">result</div>'
        "<p>" + key + "</p>"
        '<div id="group-proof-rendered-lines" data-proof-mode="narrative">'
        "<h4>証明</h4><div><span>Proposition 2.7</span>"
        "<span>Proposition 4.2</span><span>(5.10)</span>"
        "<span>の群構造を決定するために</span>"
        "<span>" + extra + "</span>"
        '<span data-latex="\\pi_{12}^{13}=0">tex</span>'
        "<span>以上より</span><span>□</span></div></div></body></html>"
    )
    return FakeResponse(200, html.encode("utf-8"))


def test_html_parser_recovers_one_conclusion_and_section() -> None:
    parser = ProofHTMLParser()
    parser.feed(fixture_response().data.decode("utf-8"))
    assert parser.verified_section()
    assert parser.conclusion_latex == r"\pi_{12}^{7}=0"
    assert parser.proof_mode == "narrative"
    assert "Proposition 2.7" in parser.proof_fragments


def test_complete_html_contract_and_duplicate_reporting() -> None:
    outcome = observe_response(fixture_response(duplicated=True), form_kind="group")
    assert outcome["verified_conclusion"] is True
    assert outcome["duplicate_intro_observed"] is True
    assert outcome["repeated_intro_count"] == 2
    assert outcome["browser_katex_checked"] is False


def test_partial_proof_not_accepted_as_verified_completion() -> None:
    with pytest.raises(RuntimeError):
        observe_response(fixture_response(key="generic-partial-proof"), form_kind="group")


def test_wrong_conclusion_or_http_status_rejected() -> None:
    with pytest.raises(RuntimeError):
        observe_response(fixture_response(conclusion=r"\pi_{13}^{7}=0"), form_kind="group")
    page = fixture_response()
    page.status_code = 500
    with pytest.raises(RuntimeError):
        observe_response(page, form_kind="group")
```


## `tests/test_guard.py`（全文）

```python
"""The R53 public patch and the actual HTTP/Renderer files must match review."""
from __future__ import annotations

from phase174_r3_r7_r54_public_http_narrative_audit.source_guard import (
    PINNED_WEB_BLOBS, verify_checkout,
)


def test_reviewed_source_guard_allows_only_installed_r53() -> None:
    report = verify_checkout()
    assert report["source_guard"] == "PASS"
    assert report["r53_public_wiring_installed"] is True
    assert report["production_files_changed_by_r54"] == 0
    assert report["new_given"] == 0
    assert report["new_math_rules"] == 0


def test_fixed_pins_include_http_template_renderer_and_trust_gate() -> None:
    assert len(PINNED_WEB_BLOBS) == 8
    assert "web_app.py" in PINNED_WEB_BLOBS
    assert "templates/index.html" in PINNED_WEB_BLOBS
    assert "phase168_r3_5_model_renderer.py" in PINNED_WEB_BLOBS
    assert "phase168_r3_41p13_trust_boundary/verification.py" in PINNED_WEB_BLOBS
    assert all(len(value) == 40 for value in PINNED_WEB_BLOBS.values())
```


## `tests/test_http.py`（全文）

```python
"""R54 public Flask Group query; in-process HTTP, real source-backed search."""
from __future__ import annotations

from phase174_r3_r7_r54_public_http_narrative_audit.audit import (
    inspect_public_http_proof,
)


def test_group_and_group_proof_http_return_complete_cited_narrative() -> None:
    report = inspect_public_http_proof()
    assert report["inprocess_http_verified"] is True
    assert report["checked_form_kinds"] == ["group", "group_proof"]
    assert report["both_http_200"] is True
    assert report["both_complete_proof"] is True
    for observed in report["cases"]:
        assert observed["conclusion_latex"].replace(" ", "") == r"\pi_{12}^{7}=0"
        assert observed["public_proof_key"] == "generic-complete-proof"
        assert observed["citation_references_visible"] is True
        assert observed["proof_ends_with_box"] is True
        assert observed["proof_mode"] == "narrative"
    assert report["production_files_changed"] == 0
    assert report["live_server_checked"] is False
    assert report["browser_katex_checked"] is False
```


## `run.ps1`（全文）

```powershell
param([switch]$DryRun)
$ErrorActionPreference = 'Stop'
$Root = (Resolve-Path (Join-Path $PSScriptRoot '..')).Path
Push-Location $Root
try {
    python -B -m phase174_r3_r7_r54_public_http_narrative_audit.audit --dry-run
    if ($LASTEXITCODE -ne 0) { throw 'R54 Source Guard failed' }
    if ($DryRun) {
        Write-Output 'PHASE174_R3R7R54_RUN=DRYRUN_PASS'
        Write-Output '(END)'
        exit 0
    }
    python -B -m phase174_r3_r7_r54_public_http_narrative_audit.audit
    if ($LASTEXITCODE -ne 0) { throw 'R54 in-process HTTP audit failed' }
    $Groups = @(
        @{Name='R54_STATIC'; Path='phase174_r3_r7_r54_public_http_narrative_audit/tests/test_static.py'},
        @{Name='R54_PARSER'; Path='phase174_r3_r7_r54_public_http_narrative_audit/tests/test_html_parser.py'},
        @{Name='R54_GUARD'; Path='phase174_r3_r7_r54_public_http_narrative_audit/tests/test_guard.py'},
        @{Name='R54_HTTP'; Path='phase174_r3_r7_r54_public_http_narrative_audit/tests/test_http.py'},
        @{Name='R53_PUBLIC_REGRESSION'; Path='phase174_r3_r7_r53_public_source_bound_kernel/tests/test_public.py'}
    )
    foreach ($Group in $Groups) {
        Write-Output ('PHASE174_R3R7R54_TEST_GROUP=' + $Group.Name)
        python -B -m pytest -q --import-mode=importlib -p no:cacheprovider $Group.Path
        if ($LASTEXITCODE -ne 0) { throw ('R54 focused pytest failed: ' + $Group.Name) }
    }
    Write-Output 'PHASE174_R3R7R54_RUN=PASS'
    Write-Output 'PHASE174_R3R7R54_PRODUCTION_FILES_CHANGED=0'
    Write-Output 'PHASE174_R3R7R54_FULL_PYTEST=False'
    Write-Output '(END)'
} finally {
    Pop-Location
}
```
