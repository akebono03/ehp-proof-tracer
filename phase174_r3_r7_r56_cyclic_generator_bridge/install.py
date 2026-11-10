"""Source-guarded R56 installer; only common provider wiring is edited.

Git object bytes are pinned. All local file edits and EOL styles are preserved
unless they exactly match the reviewed baseline, and an idempotent re-run is
allowed. Existing mathematical and presentation modules are not rewritten.
"""
from __future__ import annotations

import argparse
import ast
import hashlib
import json
from pathlib import Path
import subprocess


ROOT = Path(__file__).resolve().parents[1]
PACKAGE = Path(__file__).resolve().parent
SHARED = "phase165_r52_r9_shared_math.py"
PINNED_SHA = "534b552856fefc8315b243fecc3170ee5792ebc7"
REVIEWED_ANCESTOR = "d923ff2a34b6ba9d4c23d3da0221402f0b815f46"
REVIEWED_GITHUB_HEAD = "0a5be29a4458cdffaa8a7ad4ad31c2e91f6941f9"

PROVIDER_BEFORE = '''    extra_providers = (
        expand_hopf_injective_from_zero_image,
        expand_upper_delta_surjectivity,
    ) + tuple(extra_providers)
'''
PROVIDER_AFTER = '''    extra_providers = (
        expand_hopf_injective_from_zero_image,
        expand_upper_delta_surjectivity,
    ) + tuple(extra_providers)
    # R56: two ordinary typed EHP consequences, shared by every root query.
    # Prefer the two-step generator route while preserving the old R37 rule.
    from phase174_r3_r7_r56_cyclic_generator_bridge.rule import (
        expand_cyclic_generator_from_hopf,
        expand_delta_surjectivity_from_generator,
    )
    extra_providers = (
        expand_delta_surjectivity_from_generator,
        expand_cyclic_generator_from_hopf,
    ) + tuple(extra_providers)
'''
SHARED_SEARCH_BEFORE = '''    if expansion_provider is None:
        expansion_provider = shared_expansion_provider(
            proof_context, proof_target=goal,
            prior_conclusions=tuple(item.root.conclusion for item in prior),
        )
    return search_registered_partial_proof(
'''
SHARED_SEARCH_AFTER = '''    if expansion_provider is None:
        expansion_provider = shared_expansion_provider(
            proof_context, proof_target=goal,
            prior_conclusions=tuple(item.root.conclusion for item in prior),
        )
        # Every ordinary (nonzero) group search needs the same cited R53
        # source-bound kernel candidate already used by the zero-group route.
        # This is a candidate ordering wrapper, not a new premise or GIVEN.
        from phase174_r3_r7_r53_public_source_bound_kernel.provider import (
            build_public_source_bound_kernel_provider,
        )
        expansion_provider = build_public_source_bound_kernel_provider(
            expansion_provider, proof_context,
        )
    return search_registered_partial_proof(
'''


def _git(*args: str, binary: bool = False):
    cmd = subprocess.run(("git",) + args, cwd=ROOT, check=False,
                         capture_output=True)
    if cmd.returncode:
        raise RuntimeError("git " + " ".join(args) + " failed: "
                           + cmd.stderr.decode("utf-8", "replace").strip())
    return cmd.stdout if binary else cmd.stdout.decode("utf-8", "replace").strip()


def _git_blob(raw: bytes) -> str:
    return hashlib.sha1(b"blob " + str(len(raw)).encode("ascii") + b"\0" + raw).hexdigest()


def _normalize(raw: bytes) -> tuple[str, bytes, str]:
    bom = b"\xef\xbb\xbf" if raw.startswith(b"\xef\xbb\xbf") else b""
    data = raw[len(bom):]
    if b"\r" in data.replace(b"\r\n", b""):
        raise RuntimeError("unsupported CR-only or mixed EOL")
    return data.decode("utf-8").replace("\r\n", "\n"), bom, ("\r\n" if b"\r\n" in data else "\n")


def _write_style(text: str, bom: bytes, eol: str) -> bytes:
    return bom + text.replace("\n", eol).encode("utf-8")


def _replace_once(text: str, before: str, after: str, name: str) -> str:
    if text.count(before) != 1:
        raise RuntimeError("missing or ambiguous reviewed patch anchor: " + name)
    return text.replace(before, after, 1)


def patch_shared(source: str) -> str:
    result = _replace_once(source, PROVIDER_BEFORE, PROVIDER_AFTER, "common provider")
    result = _replace_once(result, SHARED_SEARCH_BEFORE, SHARED_SEARCH_AFTER,
                           "ordinary group source-bound provider")
    ast.parse(result, filename=SHARED)
    return result


def _whole_function(source: str, name: str) -> str:
    tree = ast.parse(source)
    functions = [item for item in tree.body
                 if isinstance(item, ast.FunctionDef) and item.name == name]
    if len(functions) != 1:
        raise RuntimeError("cannot extract unique full function " + name)
    node = functions[0]
    return "".join(source.splitlines(keepends=True)[node.lineno - 1:node.end_lineno])


def review() -> dict[str, object]:
    if _git("branch", "--show-current") != "develop":
        raise RuntimeError("expected develop branch")
    if (_git("rev-parse", "--show-toplevel").replace("\\", "/").lower()
            != str(ROOT).replace("\\", "/").lower()):
        raise RuntimeError("extract the ZIP into repository root")
    status = subprocess.run(
        ("git", "merge-base", "--is-ancestor", REVIEWED_ANCESTOR, "HEAD"),
        cwd=ROOT, check=False,
    )
    if status.returncode:
        raise RuntimeError("HEAD does not descend from reviewed R55 baseline")
    committed_sha = _git("rev-parse", "HEAD:" + SHARED)
    if committed_sha != PINNED_SHA:
        raise RuntimeError("unreviewed committed provider module")
    raw_git = _git("show", "HEAD:" + SHARED, binary=True)
    if _git_blob(raw_git) != PINNED_SHA:
        raise RuntimeError("committed Git object byte check failed")
    base = _normalize(raw_git)[0]
    intended = patch_shared(base)
    local_path = ROOT / SHARED
    local = local_path.read_bytes()
    current, bom, eol = _normalize(local)
    if current not in (base, intended):
        raise RuntimeError("unreviewed user changes in provider module: " + SHARED)
    staged = _git("diff", "--cached", "--name-only", "--", SHARED)
    if staged:
        raise RuntimeError("provider file has staged modifications")
    code = (PACKAGE / "rule.py").read_text(encoding="utf-8")
    if "GIVEN" in code and "ProofRule.GIVEN" not in code:
        raise RuntimeError("unexpected rule source")
    ast.parse(code, filename="rule.py")
    return {
        "local_head": _git("rev-parse", "HEAD"),
        "github_reviewed_head": REVIEWED_GITHUB_HEAD,
        "source_guard": "PASS",
        "provider": SHARED,
        "current": current,
        "proposed": intended,
        "existing_bytes": local,
        "future_bytes": _write_style(intended, bom, eol),
        "new_givens": 0,
        "new_general_rules": 2,
        "changed_production_files": [SHARED],
    }


def install(*, dry_run: bool) -> dict[str, object]:
    state = review()
    changed = state["existing_bytes"] != state["future_bytes"]
    if not dry_run:
        if changed:
            (ROOT / SHARED).write_bytes(state["future_bytes"])
        new_source = _normalize((ROOT / SHARED).read_bytes())[0]
        if new_source != state["proposed"]:
            raise RuntimeError("post-install source mismatch")
        folder = PACKAGE / "output"
        folder.mkdir(exist_ok=True)
        (folder / "phase165_r52_r9_shared_math.FULL.py").write_text(
            new_source, encoding="utf-8")
        full = (
            "# R56 変更後の関数全文\n\n"
            "## phase165_r52_r9_shared_math.py : shared_expansion_provider\n\n"
            "```python\n" + _whole_function(new_source, "shared_expansion_provider")
            + "\n```\n\n"
            "## phase165_r52_r9_shared_math.py : search_shared_group_goal\n\n"
            "```python\n" + _whole_function(new_source, "search_shared_group_goal")
            + "\n```\n"
        )
        (folder / "CHANGED_FUNCTIONS_FULL_JA.md").write_text(full, encoding="utf-8")
    result = {key: value for key, value in state.items()
              if key not in ("current", "proposed", "existing_bytes", "future_bytes")}
    result["would_change" if dry_run else "changed"] = changed
    result["gate"] = "PASS_PREFLIGHT_ONLY" if dry_run else "PASS_R56_SHARED_PROVIDER_CONNECTED"
    return result


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--dry-run", action="store_true")
    args = parser.parse_args()
    report = install(dry_run=args.dry_run)
    print("PHASE174_R56_LOCAL_HEAD=" + str(report["local_head"]))
    print("PHASE174_R56_SOURCE_GUARD=" + str(report["source_guard"]))
    print("PHASE174_R56_NEW_GIVENS=0")
    print("PHASE174_R56_NEW_GENERAL_RULES=2")
    print("PHASE174_R56_GATE=" + str(report["gate"]))
    if not args.dry_run:
        print("PHASE174_R56_FUNCTIONS_FULL=" + str(
            PACKAGE / "output" / "CHANGED_FUNCTIONS_FULL_JA.md"
        ))
    print("(END)")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
