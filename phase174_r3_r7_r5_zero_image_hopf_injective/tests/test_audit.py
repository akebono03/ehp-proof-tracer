"""Source and evidence contracts for the isolated zero-image audit."""
from __future__ import annotations

import ast
from pathlib import Path

import pytest

from phase174_r3_r7_r5_zero_image_hopf_injective.audit import (
    REVIEWED_HEAD, REVIEWED_R4_SUCCESSOR_HEAD, SOURCE_BLOBS, TODA_CLAUSES,
    accepted_source_blob, blob_sha, reviewed_develop_head_pair,
    validate_r4_evidence, verify_git_and_sources,
)


def sample_r4() -> dict:
    return {
        "phase": "174-R3-R7-R4",
        "gate": "PASS_READ_ONLY_DELTA_SURJECTIVITY_GAP",
        "new_group_given": 0,
        "new_inference_rules": 0,
        "completion_claimed": False,
        "source_review": {"pi10_5_nonzero_but_suspension_zero": True},
        "live": {
            "candidate_obligations": {
                "delta_surjectivity": {"proposal_count": 0},
                "eh_exactness": {"proposal_count": 1},
                "hd_exactness": {"proposal_count": 1},
                "hopf_injectivity": {"proposal_count": 1},
                "false_pi10_5_zero_shortcut": {"proposal_count": 0},
            },
            "neighbor_groups": {
                "pi_10^5": {"search_status": "search_failed", "open_goals": [1, 2, 3]},
                "pi_9^5": {"search_status": "search_failed", "open_goals": [1, 2, 3]},
            },
        },
    }


def test_r4_certified_evidence_accepted_with_provenance_distinctions() -> None:
    checked = validate_r4_evidence(sample_r4())
    assert checked["observed_counts"]["delta_surjectivity"] == 0
    assert checked["source_zero_map_is_not_proven_step"]


def test_r4_dryrun_is_not_live_evidence() -> None:
    data = sample_r4()
    data["gate"] = "PASS_PREFLIGHT"
    with pytest.raises(RuntimeError, match="certified audit"):
        validate_r4_evidence(data)


def test_r4_new_given_and_completion_claim_fail_closed() -> None:
    data = sample_r4()
    data["new_group_given"] = 1
    with pytest.raises(RuntimeError, match="changed proof evidence"):
        validate_r4_evidence(data)
    data = sample_r4()
    data["completion_claimed"] = True
    with pytest.raises(RuntimeError, match="changed proof evidence"):
        validate_r4_evidence(data)


@pytest.mark.parametrize("name,count", (
    ("delta_surjectivity", 1), ("eh_exactness", 0),
    ("false_pi10_5_zero_shortcut", 1),
))
def test_observed_prior_counts_must_not_be_fabricated(name: str, count: int) -> None:
    data = sample_r4()
    data["live"]["candidate_obligations"][name]["proposal_count"] = count
    with pytest.raises(RuntimeError, match="frontier changed"):
        validate_r4_evidence(data)


def test_neighbor_group_completion_cannot_be_assumed() -> None:
    data = sample_r4()
    data["live"]["neighbor_groups"]["pi_10^5"]["search_status"] = "complete"
    with pytest.raises(RuntimeError, match="neighboring group"):
        validate_r4_evidence(data)


def test_source_blob_accepts_crlf_but_rejects_different_content() -> None:
    a = b"source\nline\n"
    assert accepted_source_blob(a, blob_sha(a))
    assert accepted_source_blob(b"source\r\nline\r\n", blob_sha(a))
    assert not accepted_source_blob(b"source\nchanged\n", blob_sha(a))


def test_toda_source_separates_nonzero_group_and_zero_image() -> None:
    assert r"\mathbb Z_2" in TODA_CLAUSES["nonzero_group"]
    assert TODA_CLAUSES["zero_suspension_image"] == r"E\pi_{10}^5=0"
    assert len(SOURCE_BLOBS) == 9
    assert len(REVIEWED_HEAD) == 40


def test_source_audit_contains_no_install_or_direct_given() -> None:
    source = Path(__file__).resolve().parents[1] / "audit.py"
    tree = ast.parse(source.read_text(encoding="utf-8"))
    funcs = {node.name for node in tree.body if isinstance(node, ast.FunctionDef)}
    assert "inspect_screened_zero_image_frontier" in funcs
    assert "verify_git_and_sources" in funcs
    assert "patch" not in funcs
    assert "install" not in funcs
    assert "create_given" not in funcs


@pytest.mark.parametrize("local,remote,accepted", (
    (REVIEWED_HEAD, REVIEWED_HEAD, True),
    (REVIEWED_R4_SUCCESSOR_HEAD, REVIEWED_R4_SUCCESSOR_HEAD, True),
    (REVIEWED_HEAD, REVIEWED_R4_SUCCESSOR_HEAD, False),
    (REVIEWED_R4_SUCCESSOR_HEAD, REVIEWED_HEAD, False),
    ("0" * 40, "0" * 40, False),
    ("0" * 40, REVIEWED_R4_SUCCESSOR_HEAD, False),
))
def test_reviewed_develop_head_pair_only_allows_identical_audited_commits(
    local: str, remote: str, accepted: bool,
) -> None:
    assert reviewed_develop_head_pair(local, remote) is accepted


def test_reviewed_successor_is_exact_and_pinned_sources_stay_strict() -> None:
    assert REVIEWED_R4_SUCCESSOR_HEAD == "db9ef1cd1560744352bced43d3b4e1b95003edfb"
    assert len(SOURCE_BLOBS) == 9
    assert "sources/toda/Toda_05_2.tex" in SOURCE_BLOBS
    assert "phase165_r52_r9_shared_math.py" in SOURCE_BLOBS
    assert "map_property_rules.py" in SOURCE_BLOBS


def test_verify_git_and_sources_accepts_reviewed_successor_with_pinned_blobs(
    tmp_path: Path, monkeypatch: pytest.MonkeyPatch,
) -> None:
    import phase174_r3_r7_r5_zero_image_hopf_injective.audit as audit_module

    for relative_path in SOURCE_BLOBS:
        target = tmp_path / relative_path
        target.parent.mkdir(parents=True, exist_ok=True)
        target.write_bytes(b"fixture reviewed source")

    def fake_git(*args: str, cwd: Path = tmp_path) -> str:
        commands = {
            ("rev-parse", "--show-toplevel"): str(tmp_path),
            ("branch", "--show-current"): "develop",
            ("rev-parse", "HEAD"): REVIEWED_R4_SUCCESSOR_HEAD,
            ("ls-remote", "origin", "refs/heads/develop"):
                REVIEWED_R4_SUCCESSOR_HEAD + "\trefs/heads/develop",
            ("diff", "--cached", "--name-only"): "",
            ("diff", "--name-only"): "",
            ("status", "--porcelain=v1", "--untracked-files=normal"): "",
        }
        if args not in commands:
            raise AssertionError("Unexpected Git invocation: " + repr(args))
        return commands[args]

    monkeypatch.setattr(audit_module, "git", fake_git)
    monkeypatch.setattr(audit_module, "accepted_source_blob", lambda data, expected: data == b"fixture reviewed source")
    result = verify_git_and_sources(tmp_path)
    assert result["local_head"] == REVIEWED_R4_SUCCESSOR_HEAD
    assert result["remote_head"] == REVIEWED_R4_SUCCESSOR_HEAD
    assert result["source_guard"] == "PASS"
    assert len(result["reviewed_files"]) == 9


def test_verify_git_and_sources_rejects_modified_pinned_source(
    tmp_path: Path, monkeypatch: pytest.MonkeyPatch,
) -> None:
    import phase174_r3_r7_r5_zero_image_hopf_injective.audit as audit_module

    for relative_path in SOURCE_BLOBS:
        target = tmp_path / relative_path
        target.parent.mkdir(parents=True, exist_ok=True)
        target.write_bytes(b"modified source")

    def fake_git(*args: str, cwd: Path = tmp_path) -> str:
        commands = {
            ("rev-parse", "--show-toplevel"): str(tmp_path),
            ("branch", "--show-current"): "develop",
            ("rev-parse", "HEAD"): REVIEWED_R4_SUCCESSOR_HEAD,
            ("ls-remote", "origin", "refs/heads/develop"):
                REVIEWED_R4_SUCCESSOR_HEAD + "\trefs/heads/develop",
            ("diff", "--cached", "--name-only"): "",
            ("diff", "--name-only"): "",
        }
        return commands[args]

    monkeypatch.setattr(audit_module, "git", fake_git)
    with pytest.raises(RuntimeError, match="Pinned source changed"):
        verify_git_and_sources(tmp_path)
