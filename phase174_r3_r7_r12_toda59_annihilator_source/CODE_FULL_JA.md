# Phase 174 R3-R7-R12 — 完全コードと実行手順

このファイルは全ての新規 Python クラス・関数・テスト関数と import、
PowerShell 実行コードを省略せず収録する。既存の本番ファイルを置き換えない。

## 変更一覧

- 新規 `phase174_r3_r7_r12_toda59_annihilator_source/source.py` の
  `CitedFamilyAnnihilator` と `verify_toda59_annihilator_text()`、
  `reviewed_toda59_annihilator_schema()`。
- 新規 `rule.py` の `canonical_annihilator_instance()`、
  `annihilator_specialization_inputs()`、`cited_annihilator_specialization_rule()`、
  `expand_cited_annihilator_specialization()`。
- 新規 `audit.py` の Source Guard、R11 証拠照合、独立候補監査、出力。
- 新規 `tests/test_source.py`、`tests/test_rule.py`、`tests/test_audit.py`。
- 新規 `run.ps1`、新規パッケージ `README.md` と `AUDIT_PLAN_JA.md`。

## Windows PowerShell からの実行

```powershell
cd C:\Users\oomae\Dropbox\Python\fitz\ehp_proof
$ErrorActionPreference = 'Stop'
Expand-Archive -Path "$HOME\Downloads\R12.zip" -DestinationPath "." -Force
powershell -NoProfile -ExecutionPolicy Bypass -File ".\phase174_r3_r7_r12_toda59_annihilator_source\run.ps1" -DryRun
if ($LASTEXITCODE -ne 0) { throw "R12 DryRun failed" }
powershell -NoProfile -ExecutionPolicy Bypass -File ".\phase174_r3_r7_r12_toda59_annihilator_source\run.ps1"
if ($LASTEXITCODE -ne 0) { throw "R12 audit failed" }
git status -sb
git diff --stat
```

## 各ファイルの全文

### `source.py`

```python
"""Source-first, unadmitted general annihilator schema from Toda (5.9).

Source text and family metadata are checked independently. Returning a
schema does not register a GIVEN, a ProofStep, or a production rule.
"""
from __future__ import annotations

from dataclasses import dataclass
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
TODA_SOURCE = ROOT / "sources" / "toda" / "Toda_05_2.tex"
TODA_CLAUSE = r"\nu_n\circ \eta_{n+3}=0\ (n\ge6)"
PROPOSITION_START = r"\begin{proposition}\label{prop:5.9}"
SOURCE_ANNIHILATOR_LOCATOR = "Toda (5.9), in the proof of Proposition 5.9"


@dataclass(frozen=True)
class CitedFamilyAnnihilator:
    """An unadmitted, citation-qualified family-composition relation schema."""

    left_family_id: int
    right_family_id: int
    minimum_left_index: int
    right_index_offset: int
    citation_locator: str


def verify_toda59_annihilator_text(path: Path = TODA_SOURCE) -> dict[str, object]:
    """Check the exact general law within its position in the adopted TeX."""
    text = Path(path).read_text(encoding="utf-8-sig")
    start = text.find(PROPOSITION_START)
    if start < 0 or text.count(PROPOSITION_START) != 1:
        raise RuntimeError("Proposition 5.9 source boundary missing or ambiguous")
    end = text.find(r"\qed", start)
    if end < 0:
        raise RuntimeError("Proposition 5.9 proof end missing")
    excerpt = text[start:end]
    marker = r"\textbf{(5.9).}"
    if excerpt.count(marker) != 1 or excerpt.count(TODA_CLAUSE) != 1:
        raise RuntimeError("Reviewed Toda (5.9) general annihilator missing or repeated")
    relation_pos = excerpt.index(TODA_CLAUSE)
    direct_pos = excerpt.find(r"E\pi_{10}^5=0")
    if not (excerpt.index(marker) < relation_pos < direct_pos):
        raise RuntimeError("Toda general source is not prior to the derived zero-image claim")
    return {
        "source": "sources/toda/Toda_05_2.tex",
        "locator": SOURCE_ANNIHILATOR_LOCATOR,
        "general_relation": TODA_CLAUSE,
        "relative_position": relation_pos,
        "direct_image_zero_position": direct_pos,
        "printed_edition_independently_verified": False,
        "source_not_registered_as_given": True,
    }


def reviewed_toda59_annihilator_schema(
    path: Path = TODA_SOURCE,
    family_csv: Path | None = None,
) -> CitedFamilyAnnihilator:
    """Return an unproved general schema only after source and family checks."""
    verify_toda59_annihilator_text(path)
    from phase169_r10b_registered_stable_family_binding.family_registry import (
        read_registered_stable_families,
    )

    families = read_registered_stable_families(family_csv)
    left = tuple(x for x in families if x.family_id == 4)
    right = tuple(x for x in families if x.family_id == 2)
    if (len(left) != 1 or len(right) != 1
            or left[0].symbol_family != "ν" or left[0].stem != 3
            or left[0].minimum_n > 6 or right[0].symbol_family != "η"
            or right[0].stem != 1 or right[0].minimum_n > 9):
        raise RuntimeError("Typed ν/η metadata differs from reviewed Toda (5.9)")
    return CitedFamilyAnnihilator(
        left_family_id=left[0].family_id,
        right_family_id=right[0].family_id,
        minimum_left_index=6,
        right_index_offset=3,
        citation_locator=SOURCE_ANNIHILATOR_LOCATOR,
    )
```

### `rule.py`

```python
"""Generic instance inference from a separately certified family annihilator.

This candidate has no production wiring and creates no mathematical GIVEN.
The source schema must be independently admitted by an audited registry before
any real proof search can close the instance as an INFERENCE.
"""
from __future__ import annotations

from expression import Composition, GeneratorSymbol, HomotopyElement, Zero
from phase165_r3_recursive_search import GoalExpansion
from phase169_r10b_registered_stable_family_binding.family_registry import (
    read_registered_stable_families, registered_family_of,
)
from phase174_r3_r7_r12_toda59_annihilator_source.source import CitedFamilyAnnihilator
from proof import InferenceRule, PremisePattern, ProofRule, Relation, RelationType

RULE_NAME = "source-qualified general family annihilator specialization"


def canonical_annihilator_instance(
    source: object,
    left_index: object,
) -> Relation | None:
    """Construct a typed goal for any valid certified family-pair schema."""
    if not isinstance(source, CitedFamilyAnnihilator):
        return None
    if (type(left_index) is not int or type(source.minimum_left_index) is not int
            or left_index < max(2, source.minimum_left_index)
            or type(source.right_index_offset) is not int
            or source.right_index_offset < 1
            or type(source.left_family_id) is not int
            or type(source.right_family_id) is not int
            or not source.citation_locator):
        return None
    families = read_registered_stable_families()
    left = tuple(f for f in families if f.family_id == source.left_family_id)
    right = tuple(f for f in families if f.family_id == source.right_family_id)
    if len(left) != 1 or len(right) != 1:
        return None
    first, second = left[0], right[0]
    j = left_index + source.right_index_offset
    if (first.stem != source.right_index_offset
            or left_index < first.minimum_n or j < second.minimum_n
            or first.stem <= 0 or second.stem <= 0):
        return None

    def member(family: object, n: int) -> HomotopyElement:
        return HomotopyElement(
            name=family.name_at(n), dimension=n,
            source=n + family.stem, target=n,
            generator=GeneratorSymbol(family.symbol_family, n),
        )

    a, b = member(first, left_index), member(second, j)
    if (registered_family_of(a) != first or registered_family_of(b) != second
            or a.source != b.target):
        return None
    return Relation(
        lhs=Composition(a, b), rhs=Zero(), relation_type=RelationType.EQUALITY,
    )


def annihilator_specialization_inputs(
    goal: object,
    available: tuple[object, ...],
) -> tuple[CitedFamilyAnnihilator, ...]:
    """Find only explicitly available cited schemas; never create a source leaf."""
    if not isinstance(available, tuple):
        raise TypeError("available must be a tuple")
    if (not isinstance(goal, Relation)
            or goal.relation_type is not RelationType.EQUALITY
            or not isinstance(goal.rhs, Zero)
            or not isinstance(goal.lhs, Composition)
            or not isinstance(goal.lhs.left, HomotopyElement)):
        return ()
    n = goal.lhs.left.dimension
    found: list[CitedFamilyAnnihilator] = []
    for source in available:
        if not isinstance(source, CitedFamilyAnnihilator) or source in found:
            continue
        if canonical_annihilator_instance(source, n) == goal:
            found.append(source)
    return tuple(found)


def cited_annihilator_specialization_rule(
    goal: Relation,
    source: CitedFamilyAnnihilator,
) -> InferenceRule:
    """Require the exact certified general-source statement as a GIVEN step."""
    if annihilator_specialization_inputs(goal, (source,)) != (source,):
        raise ValueError("nonmatching source-qualified family relation")

    def guard(premises, bindings):
        return (
            len(premises) == 1
            and premises[0].rule is ProofRule.GIVEN
            and premises[0].conclusion == source
            and annihilator_specialization_inputs(goal, (source,)) == (source,)
        )

    return InferenceRule(
        name=RULE_NAME,
        description=(
            "A citation-screened general family annihilator may be instantiated "
            "at a type-compatible index. The cited law itself must be proved "
            "as a source leaf independently; this rule never creates one."
        ),
        premise_patterns=(PremisePattern(
            statement_type=CitedFamilyAnnihilator,
            statement_pattern=source,
            proof_rule=ProofRule.GIVEN,
        ),),
        conclusion_pattern=goal,
        match_guard=guard,
    )


def expand_cited_annihilator_specialization(
    goal: object,
    available: tuple[object, ...],
) -> tuple[GoalExpansion, ...]:
    """Return source-bound *unproved* goals without production registration."""
    source_options = annihilator_specialization_inputs(goal, available)
    return tuple(
        GoalExpansion(
            rule=cited_annihilator_specialization_rule(goal, source),
            subgoals=(source,),
        )
        for source in source_options
    )
```

### `audit.py`

```python
"""Phase 174 R3-R7-R12: isolated Toda (5.9) source-schema preflight.

Reads the certified R11 report and checks typed public goal proposals.
There is no production integration, no generated proof leaf, and no group GIVEN.
"""
from __future__ import annotations

import argparse
import hashlib
import json
import os
import subprocess
import tempfile
from pathlib import Path
from typing import Any

from phase174_r3_r7_r12_toda59_annihilator_source.source import (
    reviewed_toda59_annihilator_schema, verify_toda59_annihilator_text,
)

ROOT = Path(__file__).resolve().parents[1]
PHASE = "174-R3-R7-R12"
BASE_HEAD = "f260e157e69716a7021c02b49b6828359fba23d0"
REVIEWED_R11_HEAD = "162a72e42a7eadc16c62555de8239391bb5175cc"
ALLOWED_SUCCESSOR = "phase174_r3_r7_r11_canonical_fixture_audit/"
SOURCE_BLOBS = {
    "sources/toda/Toda_05_2.tex": "579661138928499ba04a51327f686d9b971b5314",
    "data/sphere.csv": "b7e98a4469e0dcf2c5ea16691a7225951fd36395",
    "data/HyoujiGen.csv": "26f33db0c83ba7f151433583fe861598399cbe6a",
    "expression.py": "7f7cd97468cd753643369f54774ee9892968c345",
    "homotopy_groups.py": "883faf1b4a067485c9127f14dbb575aaa195960e",
    "proof.py": "2eb683053eaf7146bd89afbc581a386af08b8060",
    "phase165_r14_r6_generic_iso.py": "8e8f5a4245f3dbbc5707b3a0042a1274e4b3e6b7",
    "phase165_r52_r9_shared_math.py": "0a06dcb0a721e5a79e866cd96909eeeec69303d6",
    "phase169_r10b_registered_stable_family_binding/family_registry.py": "4e461795954cc3e7a34fe9e3b47f77d00e5faeda",
    "phase169_r10d2_general_family_definition/family_citation.py": "b4b0c65e3eee85b557d5cfe7fa66a38a5386c3f8",
    "phase169_r10e2_unpositioned_citation/source_first.py": "b91b97a74d65b843fa8f9c19ffd082f684e461a7",
    "phase169_r10e5_composite_generator_image/rule.py": "01acace3eb273d47091421a61291ee54b51c369f",
    "phase174_r3_r7_r11_canonical_fixture_audit/audit.py": "348f0c805de2bdda156cbc40543e88de0ec3c11e",
    "phase174_r3_r7_r11_canonical_fixture_audit/tests/test_audit.py": "5f3dba359af7bccacb2f004ff03e05bef7b12817",
}


def git(*args: str, cwd: Path = ROOT) -> str:
    result = subprocess.run(
        ("git",) + args, cwd=cwd, capture_output=True, text=True,
        encoding="utf-8", errors="replace", check=True,
    )
    return result.stdout.strip()


def git_blob_sha(data: bytes) -> str:
    return hashlib.sha1(b"blob " + str(len(data)).encode("ascii") + b"\0" + data).hexdigest()


def source_blob_matches(data: bytes, expected_sha: str) -> bool:
    if (len(expected_sha) != 40
            or any(c not in "0123456789abcdef" for c in expected_sha)):
        return False
    normalized = data.replace(b"\r\n", b"\n")
    return any(git_blob_sha(item) == expected_sha for item in (
        data, normalized, normalized.replace(b"\n", b"\r\n"),
    ))


def reviewed_head_lineage(
    local: str, remote: str, successors: tuple[str, ...],
    changed: tuple[str, ...],
) -> str:
    if local != remote or len(local) != 40:
        raise RuntimeError("Local/remote develop mismatch")
    if local == BASE_HEAD and not successors and not changed:
        return "REVIEWED_BASE"
    if (local == REVIEWED_R11_HEAD
            and successors == (REVIEWED_R11_HEAD,)
            and bool(changed)
            and all(path.startswith(ALLOWED_SUCCESSOR) for path in changed)):
        return "REVIEWED_R11_ONLY_SUCCESSOR"
    raise RuntimeError("Unreviewed develop HEAD or source changes")


def verify_git_and_sources(root: Path = ROOT) -> dict[str, Any]:
    if Path(git("rev-parse", "--show-toplevel", cwd=root)).resolve() != root.resolve():
        raise RuntimeError("R12 package must be directly inside repository root")
    if git("branch", "--show-current", cwd=root) != "develop":
        raise RuntimeError("Expected develop branch")
    local = git("rev-parse", "HEAD", cwd=root)
    line = git("ls-remote", "origin", "refs/heads/develop", cwd=root)
    remote = line.split()[0] if line else ""
    if git("diff", "--cached", "--name-only", cwd=root):
        raise RuntimeError("Staged changes require review")
    if git("diff", "--name-only", cwd=root):
        raise RuntimeError("Tracked changes require review")
    if local == BASE_HEAD:
        commits: tuple[str, ...] = ()
        changed: tuple[str, ...] = ()
    else:
        subprocess.run(
            ("git", "merge-base", "--is-ancestor", BASE_HEAD, local),
            cwd=root, check=True, capture_output=True,
        )
        commits = tuple(git(
            "rev-list", "--reverse", f"{BASE_HEAD}..{local}", cwd=root,
        ).splitlines())
        changed = tuple(git(
            "diff", "--name-only", f"{BASE_HEAD}..{local}", cwd=root,
        ).splitlines())
    lineage = reviewed_head_lineage(local, remote, commits, changed)
    for relative, sha in SOURCE_BLOBS.items():
        file = root / relative
        if not file.is_file() or not source_blob_matches(file.read_bytes(), sha):
            raise RuntimeError("Pinned source changed: " + relative)
    return {
        "local_head": local,
        "remote_head": remote,
        "head_lineage": lineage,
        "source_guard": "PASS",
        "checked_blob_count": len(SOURCE_BLOBS),
        "working_tree_status": git(
            "status", "--porcelain=v1", "--untracked-files=normal", cwd=root,
        ).splitlines(),
    }


def prior_report_path() -> Path:
    root = Path(os.environ.get("LOCALAPPDATA", tempfile.gettempdir()))
    return root / "EHPProofTracerAudit" / "phase174_r3_r7_r11" / "canonical_fixture_audit.json"


def validate_r11_evidence(report: dict[str, Any]) -> dict[str, Any]:
    if (report.get("phase") != "174-R3-R7-R11"
            or report.get("gate") != "PASS_READ_ONLY_CANONICAL_FIXTURE_GAP"):
        raise RuntimeError("Certified R11 full live audit report is required")
    if (report.get("new_group_given") != 0
            or report.get("new_production_inference_rules") != 0
            or report.get("public_provider_changed") is not False
            or report.get("completion_claimed") is not False):
        raise RuntimeError("R11 proof trust contract changed")
    live = report.get("live") or {}
    if (live.get("canonical_full_composite_candidate_count") != 1
            or live.get("diagnostic_symbols_are_not_verified_aliases") is not True
            or live.get("canonical_source_from_explicit_database_goal") is not True
            or live.get("canonical_left_rule_names") != ["equality symmetry"]
            or live.get("transcription_not_promoted_to_proof") is not True
            or live.get("public_provider_unchanged") is not True
            or live.get("new_verified_steps") != 0):
        raise RuntimeError("R11 source or canonical-generator evidence changed")
    for key, expected in (
        ("public_canonical_full_image", 1),
        ("public_canonical_nu_image", 1),
        ("public_canonical_eta_square_image", 1),
        ("public_canonical_left_zero", 1),
    ):
        if (live.get(key) or {}).get("proposal_count") != expected:
            raise RuntimeError("R11 observed candidate count changed: " + key)
    return {"gate": report["gate"], "canonical_left_zero_only_symmetry": True}


def inspect_source_and_frontier() -> dict[str, Any]:
    from expression import Composition, Zero
    from homotopy_groups import TodaPrimaryGroup, TodaPrimaryGroupZeroStatement
    from phase165_r52_r9_shared_math import build_shared_typed_bridge, shared_expansion_provider
    from phase169_r10e2_unpositioned_citation.source_first import (
        screen_independent_sources_for_derived_goal,
    )
    from phase174_r3_r7_r12_toda59_annihilator_source.rule import (
        annihilator_specialization_inputs, canonical_annihilator_instance,
        expand_cited_annihilator_specialization,
    )
    from phase174_r3_r7_source_first_audit.audit import (
        is_exact_given, summarize_proposals,
    )
    from proof import ProofRule, Relation, RelationType
    from unified_statement_registry import AssertionOrigin

    reviewed = reviewed_toda59_annihilator_schema()
    left = canonical_annihilator_instance(reviewed, 6)
    if (not isinstance(left, Relation)
            or left.relation_type is not RelationType.EQUALITY
            or not isinstance(left.lhs, Composition)
            or left.rhs != Zero()
            or left.lhs.left.generator.index != 6
            or left.lhs.right.generator.index != 9):
        raise RuntimeError("General source does not produce the correct typed n=6 instance")
    target = TodaPrimaryGroupZeroStatement(TodaPrimaryGroup(12, 7))
    bridge = build_shared_typed_bridge()
    screened = screen_independent_sources_for_derived_goal(bridge, goal=target)
    admitted = tuple(
        link.step.conclusion for link in screened.proof_links
        if link.step is not None and link.step.rule is ProofRule.GIVEN
        and screened.registry.assertion(link.assertion_id).origin is AssertionOrigin.FIXED_STATEMENT
        and screened.registry.assertion(link.assertion_id).content == link.step.conclusion
    )
    provider = shared_expansion_provider(screened, proof_target=target)
    source_is_live = is_exact_given(reviewed, admitted)
    if source_is_live or is_exact_given(left, admitted) or is_exact_given(target, admitted):
        raise RuntimeError("Unreviewed annihilator or target assertion was admitted")
    isolated = expand_cited_annihilator_specialization(left, (reviewed,))
    without_source = expand_cited_annihilator_specialization(left, admitted)
    if (len(isolated) != 1 or isolated[0].subgoals != (reviewed,)
            or without_source or annihilator_specialization_inputs(left, ())):
        raise RuntimeError("Source-bound specialization did not preserve proof trust")
    public = summarize_proposals(provider, left, admitted)
    observed = tuple(provider(left))
    names = [str(getattr(option.rule, "name", "")) for option in observed]
    if public["proposal_count"] != 1 or names != ["equality symmetry"]:
        raise RuntimeError("R11 equality-symmetry-only gap changed")
    return {
        "source_screening": "adopted_toda_transcription_verified_but_not_admitted",
        "schema_type": type(reviewed).__name__,
        "schema_repr": repr(reviewed),
        "canonical_left_relation_repr": repr(left)[:1600],
        "independent_source_candidate_count": len(isolated),
        "production_source_given_count": int(source_is_live),
        "production_cited_specialization_count": len(without_source),
        "production_left_zero_proposals": public,
        "production_left_zero_rule_names": names,
        "source_as_proof_leaf_created": False,
        "new_verified_steps": 0,
        "public_provider_unchanged": True,
    }


def output_path() -> Path:
    base = Path(os.environ.get("LOCALAPPDATA", tempfile.gettempdir()))
    return base / "EHPProofTracerAudit" / "phase174_r3_r7_r12" / "toda59_annihilator.json"


def make_report(*, dry_run: bool, root: Path = ROOT) -> dict[str, Any]:
    github = verify_git_and_sources(root)
    transcription = verify_toda59_annihilator_text(root / "sources/toda/Toda_05_2.tex")
    previous = prior_report_path()
    if not previous.is_file():
        raise RuntimeError("Certified R11 report is required")
    prior = validate_r11_evidence(json.loads(previous.read_text(encoding="utf-8-sig")))
    live = None if dry_run else inspect_source_and_frontier()
    return {
        "phase": PHASE,
        "mode": "PREFLIGHT" if dry_run else "ISOLATED_CITED_ANNIHILATOR",
        "git_state": github,
        "source_review": transcription,
        "prior_evidence": prior,
        "live": live,
        "new_group_given": 0,
        "new_production_inference_rules": 0,
        "public_provider_changed": False,
        "completion_claimed": False,
        "full_pytest_run": False,
        "gate": (
            "PASS_PREFLIGHT" if dry_run
            else "PASS_ISOLATED_CITED_ANNIHILATOR_SOURCE_UNWIRED"
        ),
    }


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--dry-run", action="store_true")
    args = parser.parse_args()
    report = make_report(dry_run=args.dry_run)
    out = output_path()
    out.parent.mkdir(parents=True, exist_ok=True)
    out.write_text(
        json.dumps(report, ensure_ascii=False, indent=2) + "\n",
        encoding="utf-8",
    )
    prefix = "PHASE174_R3R7R12_"
    print(prefix + "LOCAL_HEAD=" + report["git_state"]["local_head"])
    print(prefix + "REMOTE_HEAD=" + report["git_state"]["remote_head"])
    print(prefix + "SOURCE_GUARD=PASS")
    print(prefix + "HEAD_LINEAGE=" + report["git_state"]["head_lineage"])
    print(prefix + "TODA59_GENERAL_ANNIHILATOR=VERIFIED_TRANSCRIPTION_NOT_GIVEN")
    if report["live"] is not None:
        live = report["live"]
        print(prefix + "ISOLATED_SOURCE_SPECIALIZATION_PROPOSALS=" + str(
            live["independent_source_candidate_count"]
        ))
        print(prefix + "PUBLIC_SOURCE_GIVEN_COUNT=" + str(
            live["production_source_given_count"]
        ))
        print(prefix + "PUBLIC_CITED_SPECIALIZATION_PROPOSALS=" + str(
            live["production_cited_specialization_count"]
        ))
        print(prefix + "PUBLIC_LEFT_ZERO_PROPOSALS=" + str(
            live["production_left_zero_proposals"]["proposal_count"]
        ))
        print(prefix + "PUBLIC_LEFT_ZERO_RULES=" + ",".join(
            live["production_left_zero_rule_names"]
        ))
        print(prefix + "PUBLIC_PROVIDER_UNCHANGED=True")
    print(prefix + "NEW_GROUP_GIVEN=0")
    print(prefix + "NEW_PRODUCTION_RULES=0")
    print(prefix + "FULL_PYTEST=False")
    print(prefix + "REPORT=" + str(out))
    print(prefix + "GATE=" + report["gate"])
    print("(END)")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
```

### `tests/test_source.py`

```python
"""Focused adopted-text boundary and source-only metadata tests."""
from __future__ import annotations

from pathlib import Path

import pytest

from phase174_r3_r7_r12_toda59_annihilator_source.source import (
    CitedFamilyAnnihilator, PROPOSITION_START, SOURCE_ANNIHILATOR_LOCATOR,
    TODA_CLAUSE, verify_toda59_annihilator_text,
)


def example_source() -> str:
    return (
        "before\n" + PROPOSITION_START + "\n"
        + r"\textbf{(5.9).}" + "\n"
        + TODA_CLAUSE + "\n"
        + r"E\pi_{10}^5=0" + "\n"
        + r"\qed" + "\n"
    )


def test_exact_general_citation_is_source_metadata_not_proof(tmp_path: Path) -> None:
    path = tmp_path / "toda.tex"
    path.write_text(example_source(), encoding="utf-8")
    result = verify_toda59_annihilator_text(path)
    assert result["source_not_registered_as_given"] is True
    assert result["printed_edition_independently_verified"] is False
    assert result["general_relation"] == TODA_CLAUSE
    assert result["relative_position"] < result["direct_image_zero_position"]


@pytest.mark.parametrize("mutator", (
    lambda s: s.replace(TODA_CLAUSE, ""),
    lambda s: s.replace(TODA_CLAUSE, TODA_CLAUSE + "\n" + TODA_CLAUSE),
    lambda s: s.replace("n\\ge6", "n\\ge5"),
    lambda s: s.replace(r"\textbf{(5.9).}", ""),
    lambda s: s.replace(PROPOSITION_START, ""),
    lambda s: s.replace(r"\qed", ""),
    lambda s: s.replace(TODA_CLAUSE, "PLACEHOLDER").replace(r"E\pi_{10}^5=0", TODA_CLAUSE).replace("PLACEHOLDER", r"E\pi_{10}^5=0"),
))
def test_modified_or_unpositioned_source_is_rejected(tmp_path: Path, mutator) -> None:
    path = tmp_path / "toda.tex"
    path.write_text(mutator(example_source()), encoding="utf-8")
    with pytest.raises(RuntimeError):
        verify_toda59_annihilator_text(path)


def test_general_schema_is_distinct_from_target_group_statement() -> None:
    claim = CitedFamilyAnnihilator(4, 2, 6, 3, SOURCE_ANNIHILATOR_LOCATOR)
    assert claim.left_family_id != claim.right_family_id
    assert claim.right_index_offset == 3
    assert claim.minimum_left_index == 6
    assert "Proposition 5.9" in claim.citation_locator
```

### `tests/test_rule.py`

```python
"""Typed general annihilator specialization: no target GIVEN and no aliasing."""
from __future__ import annotations

from dataclasses import replace

import pytest

from expression import Composition, HomotopyElement, Zero
from phase164_r8_proofstep_factory import derive_inference_proof_step
from phase174_r3_r7_r12_toda59_annihilator_source.rule import (
    RULE_NAME, annihilator_specialization_inputs, canonical_annihilator_instance,
    cited_annihilator_specialization_rule, expand_cited_annihilator_specialization,
)
from phase174_r3_r7_r12_toda59_annihilator_source.source import (
    CitedFamilyAnnihilator, SOURCE_ANNIHILATOR_LOCATOR,
)
from proof import InferenceRule, ProofRule, ProofStep, Relation, RelationType, find_inference_matches_for_rule


def schema() -> CitedFamilyAnnihilator:
    return CitedFamilyAnnihilator(4, 2, 6, 3, SOURCE_ANNIHILATOR_LOCATOR)


@pytest.mark.parametrize("n", (6, 7, 11, 20))
def test_any_permitted_index_uses_same_generic_cited_rule(n: int) -> None:
    claim = schema()
    goal = canonical_annihilator_instance(claim, n)
    assert isinstance(goal, Relation)
    assert goal.relation_type is RelationType.EQUALITY
    assert isinstance(goal.lhs, Composition)
    assert goal.lhs.left.generator.index == n
    assert goal.lhs.right.generator.index == n + 3
    assert goal.lhs.left.source == goal.lhs.right.target
    assert goal.rhs == Zero()
    options = expand_cited_annihilator_specialization(goal, (claim,))
    assert len(options) == 1
    assert options[0].subgoals == (claim,)
    assert options[0].rule.name == RULE_NAME


def test_proved_cited_schema_yields_inferred_instance_with_provenance() -> None:
    claim = schema()
    goal = canonical_annihilator_instance(claim, 6)
    assert goal is not None
    rule = cited_annihilator_specialization_rule(goal, claim)
    cited = ProofStep(
        conclusion=claim, premises=(), rule=ProofRule.GIVEN,
        inference_rule=InferenceRule(name="test-only source assertion"),
    )
    matches = find_inference_matches_for_rule(rule, (cited,))
    assert len(matches) == 1
    derived = derive_inference_proof_step(matches[0])
    assert derived.conclusion == goal
    assert derived.rule is ProofRule.INFERENCE
    assert derived.premises == (cited,)
    assert derived.inference_rule is rule


def test_without_screened_cited_schema_no_rule_is_proposed() -> None:
    claim = schema()
    goal = canonical_annihilator_instance(claim, 6)
    assert expand_cited_annihilator_specialization(goal, ()) == ()
    assert annihilator_specialization_inputs(goal, ()) == ()
    assert find_inference_matches_for_rule(
        cited_annihilator_specialization_rule(goal, claim), (),
    ) == ()


def test_the_cited_schema_requires_a_given_not_a_speculative_inference() -> None:
    claim = schema()
    goal = canonical_annihilator_instance(claim, 6)
    rule = cited_annihilator_specialization_rule(goal, claim)
    inferred = ProofStep(
        claim, (), ProofRule.INFERENCE,
        inference_rule=InferenceRule(name="test-only unauthenticated schema"),
    )
    assert find_inference_matches_for_rule(rule, (inferred,)) == ()


@pytest.mark.parametrize("n", (0, 1, 4, 5, True, "6", None))
def test_invalid_or_below_range_indices_fail_closed(n: object) -> None:
    assert canonical_annihilator_instance(schema(), n) is None


@pytest.mark.parametrize("modified", (
    CitedFamilyAnnihilator(4, 2, 6, 4, SOURCE_ANNIHILATOR_LOCATOR),
    CitedFamilyAnnihilator(4, 2, 9, 3, SOURCE_ANNIHILATOR_LOCATOR),
    CitedFamilyAnnihilator(4, 99, 6, 3, SOURCE_ANNIHILATOR_LOCATOR),
    CitedFamilyAnnihilator(99, 2, 6, 3, SOURCE_ANNIHILATOR_LOCATOR),
    CitedFamilyAnnihilator(4, 2, 6, -1, SOURCE_ANNIHILATOR_LOCATOR),
))
def test_incorrect_family_or_dimension_schema_never_generates_target(modified) -> None:
    claim = schema()
    goal = canonical_annihilator_instance(claim, 6)
    assert annihilator_specialization_inputs(goal, (modified,)) == ()


def test_noncanonical_nu_symbol_is_not_silently_equated() -> None:
    claim = schema()
    goal = canonical_annihilator_instance(claim, 6)
    assert goal is not None
    a = goal.lhs.left
    bad_nu = replace(a, name="nu_6")
    changed = Relation(
        Composition(bad_nu, goal.lhs.right), Zero(), RelationType.EQUALITY,
    )
    assert annihilator_specialization_inputs(changed, (claim,)) == ()
    assert expand_cited_annihilator_specialization(changed, (claim,)) == ()


def test_bad_right_eta_or_reversed_product_is_not_matched() -> None:
    claim = schema()
    goal = canonical_annihilator_instance(claim, 6)
    assert goal is not None
    wrong = Relation(
        Composition(goal.lhs.right, goal.lhs.left), Zero(), RelationType.EQUALITY,
    )
    assert expand_cited_annihilator_specialization(wrong, (claim,)) == ()
    changed = Relation(
        Composition(goal.lhs.left, replace(goal.lhs.right, name="eta_9")),
        Zero(), RelationType.EQUALITY,
    )
    assert expand_cited_annihilator_specialization(changed, (claim,)) == ()


def test_wrong_relation_type_and_forged_zero_are_rejected() -> None:
    claim = schema()
    goal = canonical_annihilator_instance(claim, 6)
    assert goal is not None
    assert expand_cited_annihilator_specialization(
        Relation(goal.lhs, Zero(), RelationType.ZERO), (claim,),
    ) == ()
    assert expand_cited_annihilator_specialization(
        Relation(goal.lhs, 0, RelationType.EQUALITY), (claim,),
    ) == ()


def test_no_direct_target_step_is_constructed_by_backward_expansion() -> None:
    claim = schema()
    goal = canonical_annihilator_instance(claim, 6)
    options = expand_cited_annihilator_specialization(goal, (claim,))
    assert len(options) == 1
    assert all(not isinstance(x, ProofStep) for x in options[0].subgoals)
    assert options[0].subgoals == (claim,)


def test_wrong_or_duplicate_source_objects_cannot_be_used_as_evidence() -> None:
    claim = schema()
    goal = canonical_annihilator_instance(claim, 6)
    wrong = CitedFamilyAnnihilator(4, 2, 7, 3, SOURCE_ANNIHILATOR_LOCATOR)
    assert annihilator_specialization_inputs(goal, (wrong,)) == ()
    assert annihilator_specialization_inputs(goal, (claim, claim)) == (claim,)
    with pytest.raises(TypeError):
        annihilator_specialization_inputs(goal, [claim])
```

### `tests/test_audit.py`

```python
"""Source, reviewed-HEAD, evidence and non-promotion contracts for R12."""
from __future__ import annotations

import ast
from pathlib import Path

import pytest

from phase174_r3_r7_r12_toda59_annihilator_source.audit import (
    ALLOWED_SUCCESSOR, BASE_HEAD, REVIEWED_R11_HEAD, SOURCE_BLOBS,
    git_blob_sha, reviewed_head_lineage, source_blob_matches,
    validate_r11_evidence,
)


def certified_r11_fixture() -> dict:
    return {
        "phase": "174-R3-R7-R11",
        "gate": "PASS_READ_ONLY_CANONICAL_FIXTURE_GAP",
        "new_group_given": 0,
        "new_production_inference_rules": 0,
        "public_provider_changed": False,
        "completion_claimed": False,
        "live": {
            "canonical_full_composite_candidate_count": 1,
            "diagnostic_symbols_are_not_verified_aliases": True,
            "canonical_source_from_explicit_database_goal": True,
            "canonical_left_rule_names": ["equality symmetry"],
            "transcription_not_promoted_to_proof": True,
            "public_provider_unchanged": True,
            "new_verified_steps": 0,
            "public_canonical_full_image": {"proposal_count": 1},
            "public_canonical_nu_image": {"proposal_count": 1},
            "public_canonical_eta_square_image": {"proposal_count": 1},
            "public_canonical_left_zero": {"proposal_count": 1},
        },
    }


def test_valid_r11_report_is_evidence_not_an_installed_source() -> None:
    checked = validate_r11_evidence(certified_r11_fixture())
    assert checked["canonical_left_zero_only_symmetry"] is True


@pytest.mark.parametrize("field,value", (
    ("gate", "PASS_PREFLIGHT"),
    ("new_group_given", 1),
    ("new_production_inference_rules", 1),
    ("public_provider_changed", True),
    ("completion_claimed", True),
))
def test_invalid_r11_certification_never_opens_r12(field: str, value: object) -> None:
    report = certified_r11_fixture()
    report[field] = value
    with pytest.raises(RuntimeError):
        validate_r11_evidence(report)


@pytest.mark.parametrize("field,value", (
    ("canonical_full_composite_candidate_count", 0),
    ("diagnostic_symbols_are_not_verified_aliases", False),
    ("canonical_left_rule_names", ["cited Toda (5.9)"]),
    ("transcription_not_promoted_to_proof", False),
    ("new_verified_steps", 1),
    ("public_provider_unchanged", False),
))
def test_r11_partial_proof_cannot_be_promoted(field: str, value: object) -> None:
    report = certified_r11_fixture()
    report["live"][field] = value
    with pytest.raises(RuntimeError):
        validate_r11_evidence(report)


@pytest.mark.parametrize("field", (
    "public_canonical_full_image", "public_canonical_nu_image",
    "public_canonical_eta_square_image", "public_canonical_left_zero",
))
def test_r11_root_counts_cannot_change_silently(field: str) -> None:
    report = certified_r11_fixture()
    report["live"][field]["proposal_count"] = 0
    with pytest.raises(RuntimeError):
        validate_r11_evidence(report)


def test_source_guard_accepts_normal_crlf_but_not_truncated_sha() -> None:
    text = b"one\ntwo\n"
    sha = git_blob_sha(text)
    assert source_blob_matches(text, sha)
    assert source_blob_matches(b"one\r\ntwo\r\n", sha)
    assert not source_blob_matches(text, sha[:-1])
    assert not source_blob_matches(text, "f" * 40)
    assert all(len(value) == 40 for value in SOURCE_BLOBS.values())
    assert len(SOURCE_BLOBS) == 14


def test_only_reviewed_base_or_r11_successor_is_allowed() -> None:
    assert reviewed_head_lineage(BASE_HEAD, BASE_HEAD, (), ()) == "REVIEWED_BASE"
    assert reviewed_head_lineage(
        REVIEWED_R11_HEAD, REVIEWED_R11_HEAD,
        (REVIEWED_R11_HEAD,), (ALLOWED_SUCCESSOR + "audit.py",),
    ) == "REVIEWED_R11_ONLY_SUCCESSOR"
    with pytest.raises(RuntimeError):
        reviewed_head_lineage(BASE_HEAD, "f" * 40, (), ())
    with pytest.raises(RuntimeError):
        reviewed_head_lineage("f" * 40, "f" * 40, ("f" * 40,),
                              (ALLOWED_SUCCESSOR + "audit.py",))
    with pytest.raises(RuntimeError):
        reviewed_head_lineage(REVIEWED_R11_HEAD, REVIEWED_R11_HEAD,
                              (REVIEWED_R11_HEAD,), ("proof.py",))
    with pytest.raises(RuntimeError):
        reviewed_head_lineage(REVIEWED_R11_HEAD, REVIEWED_R11_HEAD,
                              (REVIEWED_R11_HEAD,), ())


def test_audit_cannot_install_provider_or_mutate_existing_code() -> None:
    file = Path(__file__).resolve().parents[1] / "audit.py"
    tree = ast.parse(file.read_text(encoding="utf-8"))
    functions = {node.name for node in tree.body if isinstance(node, ast.FunctionDef)}
    assert {"verify_git_and_sources", "inspect_source_and_frontier", "make_report"} <= functions
    assert not {"install", "patch", "register_given", "mutate_production"} & functions


def test_inference_requires_source_step_not_relation_leaf() -> None:
    file = Path(__file__).resolve().parents[1] / "rule.py"
    code = file.read_text(encoding="utf-8")
    assert "proof_rule=ProofRule.GIVEN" in code
    assert "source_options" in code
    assert "subgoals=(source,)" in code
    assert "ProofStep(" not in code
```

### `run.ps1`

```powershell
param([switch]$DryRun)

$ErrorActionPreference = 'Stop'
$RepoRoot = (Resolve-Path (Join-Path $PSScriptRoot '..')).Path
$PriorPythonPath = $env:PYTHONPATH
$PriorNoBytecode = $env:PYTHONDONTWRITEBYTECODE

Push-Location -LiteralPath $RepoRoot
try {
    $env:PYTHONPATH = $RepoRoot
    $env:PYTHONDONTWRITEBYTECODE = '1'

    # Each Phase group runs in a separate Python process because older test
    # directories contain repeated test_audit.py and test_rule.py basenames.
    $Groups = @(
        @{ Name = 'R12'; Paths = @(
            '.\phase174_r3_r7_r12_toda59_annihilator_source\tests\test_source.py',
            '.\phase174_r3_r7_r12_toda59_annihilator_source\tests\test_rule.py',
            '.\phase174_r3_r7_r12_toda59_annihilator_source\tests\test_audit.py'
        ) },
        @{ Name = 'R11'; Paths = @(
            '.\phase174_r3_r7_r11_canonical_fixture_audit\tests\test_audit.py'
        ) },
        @{ Name = 'R10'; Paths = @(
            '.\phase174_r3_r7_r10_cited_family_gap_audit\tests\test_audit.py'
        ) },
        @{ Name = 'R9'; Paths = @(
            '.\phase174_r3_r7_r9_composition_associativity\tests\test_rule.py',
            '.\phase174_r3_r7_r9_composition_associativity\tests\test_audit.py'
        ) },
        @{ Name = 'R8'; Paths = @(
            '.\phase174_r3_r7_r8_composite_image_gap\tests\test_audit.py'
        ) },
        @{ Name = 'R7'; Paths = @(
            '.\phase174_r3_r7_r7_composite_zero_audit\tests\test_rule.py',
            '.\phase174_r3_r7_r7_composite_zero_audit\tests\test_audit.py'
        ) },
        @{ Name = 'R6'; Paths = @(
            '.\phase174_r3_r7_r6_cyclic_generator_zero_image\tests\test_rule.py',
            '.\phase174_r3_r7_r6_cyclic_generator_zero_image\tests\test_audit.py'
        ) },
        @{ Name = 'R5'; Paths = @(
            '.\phase174_r3_r7_r5_zero_image_hopf_injective\tests\test_rule.py',
            '.\phase174_r3_r7_r5_zero_image_hopf_injective\tests\test_audit.py'
        ) },
        @{ Name = 'R4'; Paths = @(
            '.\phase174_r3_r7_r4_delta_surjectivity_audit\tests\test_audit.py',
            '.\phase174_r3_r7_r4_delta_surjectivity_audit\tests\test_r4_runner_split.py'
        ) },
        @{ Name = 'R3'; Paths = @(
            '.\phase174_r3_r7_r3_ehp_zero_rule\tests\test_rule.py',
            '.\phase174_r3_r7_r3_ehp_zero_rule\tests\test_audit.py'
        ) },
        @{ Name = 'MATH_REGRESSION'; Paths = @(
            '.\phase165_r12_r11_prop42_unified\tests\test_phase165_r12_r11_prop42_unified.py',
            '.\phase165_r12_r12_ehp_consequences\tests\test_phase165_r12_r12_ehp_consequences.py',
            '.\phase165_r14_r9_ehp_exactness\test_phase165_r14_r9_ehp_exactness.py'
        ) },
        @{ Name = 'FAMILY_REGRESSION'; Paths = @(
            '.\phase169_r10d2_general_family_definition\tests\test_r10d2_general_family.py'
        ) }
    )

    foreach ($Group in $Groups) {
        foreach ($TestPath in $Group.Paths) {
            if (-not (Test-Path -LiteralPath $TestPath)) {
                throw "Missing focused test: $TestPath"
            }
        }
    }
    Write-Output 'PHASE174_R3R7R12_FOCUSED_PYTEST_START'
    foreach ($Group in $Groups) {
        Write-Output "PHASE174_R3R7R12_PYTEST_GROUP=$($Group.Name)"
        $Paths = [string[]]$Group.Paths
        & python -B -m pytest -q --import-mode=prepend -p no:cacheprovider @Paths
        if ($LASTEXITCODE -ne 0) {
            throw "Phase 174 R3-R7-R12 $($Group.Name) pytest failed: $LASTEXITCODE"
        }
    }
    Write-Output 'PHASE174_R3R7R12_FOCUSED_PYTEST=PASS'

    if ($DryRun) {
        & python -B -m phase174_r3_r7_r12_toda59_annihilator_source.audit --dry-run
    }
    else {
        & python -B -m phase174_r3_r7_r12_toda59_annihilator_source.audit
    }
    if ($LASTEXITCODE -ne 0) {
        throw "Phase 174 R3-R7-R12 audit failed: $LASTEXITCODE"
    }
}
finally {
    $env:PYTHONPATH = $PriorPythonPath
    $env:PYTHONDONTWRITEBYTECODE = $PriorNoBytecode
    Pop-Location
}
```

### `README.md`

```markdown
# Phase 174 R3-R7-R12 — Source-qualified general annihilator

This package isolates the **general family relation** in Toda equation (5.9):
`nu_n ∘ eta_{n+3} = 0` for `n >= 6`. It does not install the statement in the
public source registry or add any new group result as a `GIVEN` assertion.

The generic inference candidate requires an **independently certified cited
source leaf**. It cannot derive a zero relation from a database generator name,
a symmetric equality, a hand-written symbol alias, or a mere TeX quotation.

## Run in Windows PowerShell

Extract `R12.zip` directly into the root of `akebono03/ehp-proof-tracer` at a
reviewed `develop` HEAD. Run:

```powershell
powershell -NoProfile -ExecutionPolicy Bypass -File ".\phase174_r3_r7_r12_toda59_annihilator_source\run.ps1" -DryRun
if ($LASTEXITCODE -ne 0) { throw "R12 DryRun failed" }
powershell -NoProfile -ExecutionPolicy Bypass -File ".\phase174_r3_r7_r12_toda59_annihilator_source\run.ps1"
if ($LASTEXITCODE -ne 0) { throw "R12 audit failed" }
```

The script runs only focused pytest groups, then checks current remote/local
HEAD lineage and source blobs, the certified R11 JSON report, the adopted Toda
text, and the unproved typed inference proposal. The final report is placed in
`%LOCALAPPDATA%\EHPProofTracerAudit\phase174_r3_r7_r12\toda59_annihilator.json`.

A successful isolation audit is **not** a completed proof of `pi_12^7 = 0`.
Only the final Phase 174 closeout may run the entire pytest suite.
```

### `AUDIT_PLAN_JA.md`

```markdown
# Phase 174 R3-R7-R12 — Toda (5.9) 一般消滅関係の出典監査

## 現行コード・既存テストの確認

2026-11-06 に GitHub `akebono03/ehp-proof-tracer` の `develop` の
HEAD `162a72e42a7eadc16c62555de8239391bb5175cc` を確認した。
R11 の監査・テスト、R10 の出典監査、既存の型付き一般特殊化
`phase165_r57_r20_general_specialization.py`、
`phase169_r10d2_general_family_definition/family_citation.py`、
`phase169_r10b_registered_stable_family_binding/family_registry.py`、
`proof.py` と関連する tests を確認した。

## 変更対象

新設の `phase174_r3_r7_r12_toda59_annihilator_source/` 配下に限定。

- `source.py`：`CitedFamilyAnnihilator`（新設クラス）、`verify_toda59_annihilator_text()`、`reviewed_toda59_annihilator_schema()` を追加。
- `rule.py`：`canonical_annihilator_instance()`、`annihilator_specialization_inputs()`、`cited_annihilator_specialization_rule()`、`expand_cited_annihilator_specialization()` を追加。
- `audit.py`：Source Guard、R11 の認証済みレポート、公開候補数、未登録の出典命題を読み取り専用で照合。
- `tests/test_source.py`、`tests/test_rule.py`、`tests/test_audit.py`：否定条件を含む限定テスト。
- `run.ps1`：限定 pytest の別プロセス実行、DryRun と本実行。
- `README.md`：英語の実行説明。

既存の本番ソース、既存テスト、共通 Renderer、主要5文書は変更しない。

## 数学上の責務

採用転写 `sources/toda/Toda_05_2.tex` の Proposition 5.9 の証明中にある
(5.9) の一般関係は以下のとおり。

$$\nu_n\circ\eta_{n+3}=0\quad(n\ge6).$$

`HyoujiGen.csv` の ν（family ID 4）・η（family ID 2）は名前・型の
メタデータであって証明ではない。採用転写の照合だけでも `ProofStep` は作らない。
今回の一般推論規則は、正式に出典認証された一般命題が別途 `GIVEN`
として存在するときに限り、その型付き特殊化を `INFERENCE` として許可する。
今回は出典命題そのものを登録しない。群 `π₁₂⁷=0` の直接 GIVEN も禁止する。

## 完了条件・次段階

- Source Guard と R11 証拠検査 PASS、限定 pytest PASS。
- ν₆∘η₉=0 の型付き候補1件、公開に出典一般命題 GIVEN 0件を実測。
- 公開の左因子零関係が依然 `equality symmetry` のみなら未完成維持。
- 既存 Proof Search・Narrative・Web 非変更、全体 pytest は行わない。

次の R13 は、証明出典の参照・registry と接続するための設計監査とし、
Source-first の信頼境界を通らず直接目標を GIVEN にしない。
```

### `__init__.py`

```python
"""Phase 174 R3-R7-R12 cited annihilator source audit."""
```

