"""Phase 171 R20R11 minimal, guarded installer of verified-prior Hopf inference."""
from __future__ import annotations

import argparse
import ast
import hashlib
from pathlib import Path
import subprocess

HERE = Path(__file__).resolve().parent
ROOT = HERE.parent
OUTPUT = HERE / "output"
SOURCE_PATH = Path("phase171_r2j_r2_cyclic_hopf_surjective/source.py")
SHARED_PATH = Path("phase165_r52_r9_shared_math.py")
EXPECTED_BLOBS = {
    SOURCE_PATH: "0edd1d8d3aba7624d8c6a224259095b38e7662e0",
    SHARED_PATH: "cd85ba1e645c1ff9e10e834e74e99437b9988172",
}

ADDED_IMPORT = "from phase169_r10e4_ordered_db_prior.db_prior import admitted_db_step, verified_db_step\n"
IMPORT_ANCHOR = "from phase168_r2_8_4_generic_specialization.specialization import specialize_registered_higher_stem\n"
RULE_ANCHOR = "def expand_cited_cyclic_hopf_surjectivity(\n"
RULE = '''def verified_prior_cyclic_generator_image_surjectivity_rule(
    goal: MapSurjective, group: Relation, image: Relation, *,
    proof_target: object, bridge: object,
) -> InferenceRule:
    """Reuse a *rechecked* earlier DB group, never an arbitrary GIVEN.

    The Hopf image remains a separately reconstructed INFERENCE.  The database
    admission is revalidated by the existing Phase 169 provenance gate on the
    *actual* ProofStep selected by canonical public recursion.
    """
    if not _valid_surjective_pair(goal, group, image):
        raise ValueError("typed cyclic Hopf generator image does not match")
    if admitted_db_step(group, proof_target=proof_target, bridge=bridge) is None:
        raise ValueError("cyclic group is not an eligible earlier database result")

    def guard(premises, bindings):
        return (
            len(premises) == 2
            and premises[0].rule is ProofRule.GIVEN
            and premises[1].rule is ProofRule.INFERENCE
            and bool(premises[1].premises)
            and premises[0].conclusion == group
            and premises[1].conclusion == image
            and verified_db_step(
                premises[0], proof_target=proof_target, bridge=bridge,
            )
            and _valid_surjective_pair(goal, group, image)
        )

    return InferenceRule(
        name="verified earlier database cyclic generator in Hopf image implies surjectivity",
        premise_patterns=(
            PremisePattern(
                proof_rule=ProofRule.GIVEN,
                statement_type=Relation,
                relation_type=RelationType.EQUALITY,
                statement_pattern=group,
            ),
            PremisePattern(
                proof_rule=ProofRule.INFERENCE,
                statement_type=Relation,
                relation_type=RelationType.EQUALITY,
                statement_pattern=image,
            ),
        ),
        match_guard=guard,
        conclusion_pattern=goal,
    )


'''
OLD_PARAMS = "    goal: object, available: tuple[object, ...], *, proof_target: object = None,\n"
NEW_PARAMS = "    goal: object, available: tuple[object, ...], *,\n    proof_target: object = None, bridge: object = None,\n"
OLD_CANDIDATE = "            if not any(x.subgoals == candidate.subgoals for x in proposals):\n                proposals.append(candidate)\n"
NEW_CANDIDATE = OLD_CANDIDATE + '''            if bridge is not None and proof_target is not None:
                prior = admitted_db_step(
                    group, proof_target=proof_target, bridge=bridge,
                )
                if prior is not None:
                    proposals.append(GoalExpansion(
                        verified_prior_cyclic_generator_image_surjectivity_rule(
                            goal, group, chain.conclusion,
                            proof_target=proof_target, bridge=bridge,
                        ),
                        (group, chain.conclusion),
                    ))
'''
OLD_SHARED = '''        options.extend(expand_cited_cyclic_hopf_surjectivity(
            goal, tuple(available), proof_target=proof_target,
        ))
'''
NEW_SHARED = '''        options.extend(expand_cited_cyclic_hopf_surjectivity(
            goal, tuple(available), proof_target=proof_target,
            bridge=bridge,
        ))
'''


def git(*args: str) -> str:
    return subprocess.run(
        ["git", *args], cwd=ROOT, check=True, capture_output=True,
        text=True, encoding="utf-8", errors="replace",
    ).stdout.strip()


def git_blob_sha(data: bytes) -> str:
    return hashlib.sha1(
        b"blob " + str(len(data)).encode("ascii") + b"\0" + data
    ).hexdigest()


def matches_reviewed_blob(data: bytes, expected: str) -> bool:
    normalized = data.replace(b"\r\n", b"\n")
    return expected in (
        git_blob_sha(data), git_blob_sha(normalized),
        git_blob_sha(normalized.replace(b"\n", b"\r\n")),
    )


def _replace_once(source: str, old: str, new: str, name: str) -> str:
    if source.count(old) != 1:
        raise RuntimeError(name + " anchor must occur exactly once")
    return source.replace(old, new, 1)


def transform_source(original: str) -> str:
    source = _replace_once(original, IMPORT_ANCHOR, IMPORT_ANCHOR + ADDED_IMPORT, "import")
    source = _replace_once(source, RULE_ANCHOR, RULE + RULE_ANCHOR, "new rule position")
    source = _replace_once(source, OLD_PARAMS, NEW_PARAMS, "provider signature")
    source = _replace_once(source, OLD_CANDIDATE, NEW_CANDIDATE, "provider proposal")
    ast.parse(source)
    return source


def transform_shared(original: str) -> str:
    source = _replace_once(original, OLD_SHARED, NEW_SHARED, "shared provider wiring")
    ast.parse(source)
    return source


def preserve_file_format(original: bytes, normalized: str) -> bytes:
    has_bom = original.startswith(b"\xef\xbb\xbf")
    line_end = "\r\n" if b"\r\n" in original else "\n"
    return (b"\xef\xbb\xbf" if has_bom else b"") + normalized.replace("\n", line_end).encode("utf-8")


def full_function(source: str, name: str) -> str:
    tree = ast.parse(source)
    nodes = [node for node in tree.body
             if isinstance(node, (ast.FunctionDef, ast.AsyncFunctionDef))
             and node.name == name]
    if len(nodes) != 1:
        raise RuntimeError("expected exactly one changed function: " + name)
    node = nodes[0]
    lines = source.splitlines(keepends=True)
    return "".join(lines[node.lineno - 1:node.end_lineno])


def imports_complete(source: str) -> str:
    tree = ast.parse(source)
    imports = [node for node in tree.body if isinstance(node, (ast.Import, ast.ImportFrom))]
    if not imports:
        raise RuntimeError("no import block")
    lines = source.splitlines(keepends=True)
    return "".join(lines[imports[0].lineno - 1:imports[-1].end_lineno])


def preflight() -> tuple[str, dict[Path, bytes]]:
    if git("branch", "--show-current") != "develop":
        raise RuntimeError("develop branch required; nothing has been changed")
    head = git("rev-parse", "HEAD")
    original = {}
    for name, expected in EXPECTED_BLOBS.items():
        file_path = ROOT / name
        if not file_path.is_file():
            raise RuntimeError("production source missing: " + str(name))
        contents = file_path.read_bytes()
        if not matches_reviewed_blob(contents, expected):
            raise RuntimeError("unreviewed production source: " + str(name))
        committed = subprocess.run(
            ["git", "show", "HEAD:" + name.as_posix()],
            cwd=ROOT, check=True, capture_output=True,
        ).stdout
        if not matches_reviewed_blob(committed, expected):
            raise RuntimeError("unreviewed source at HEAD: " + str(name))
        if contents.replace(b"\r\n", b"\n") != committed.replace(b"\r\n", b"\n"):
            raise RuntimeError("local source is modified, refusing overwrite: " + str(name))
        original[name] = contents
    return head, original


def prepare_replacements(original: dict[Path, bytes]) -> dict[Path, bytes]:
    return {
        SOURCE_PATH: preserve_file_format(
            original[SOURCE_PATH],
            transform_source(original[SOURCE_PATH].decode("utf-8-sig").replace("\r\n", "\n")),
        ),
        SHARED_PATH: preserve_file_format(
            original[SHARED_PATH],
            transform_shared(original[SHARED_PATH].decode("utf-8-sig").replace("\r\n", "\n")),
        ),
    }


def write_code_document(replacements: dict[Path, bytes]) -> None:
    """Emit full imports, entire modified functions, and full replacement files."""
    replacements_dir = OUTPUT / "full_replacements"
    replacements_dir.mkdir(parents=True, exist_ok=True)
    source = replacements[SOURCE_PATH].decode("utf-8-sig").replace("\r\n", "\n")
    shared = replacements[SHARED_PATH].decode("utf-8-sig").replace("\r\n", "\n")
    (replacements_dir / SOURCE_PATH.name).write_text(source, encoding="utf-8")
    (replacements_dir / SHARED_PATH.name).write_text(shared, encoding="utf-8")
    document = (
        "# Phase 171 R20R11 — 完全な置換コード\n\n"
        "対象: `phase171_r2j_r2_cyclic_hopf_surjective/source.py`、"
        "`phase165_r52_r9_shared_math.py`。\n\n"
        "## source.py の変更後の import 全文\n\n```python\n"
        + imports_complete(source) + "```\n\n"
        "## source.py の新規関数全文（既存 surjectivity rule の直後）\n\n```python\n"
        + full_function(source, "verified_prior_cyclic_generator_image_surjectivity_rule")
        + "\n```\n\n"
        "## source.py の変更後の候補生成関数全文\n\n```python\n"
        + full_function(source, "expand_cited_cyclic_hopf_surjectivity")
        + "\n```\n\n"
        "## shared_math.py の変更後の関数全文\n\n```python\n"
        + full_function(shared, "shared_expansion_provider")
        + "\n```\n\n"
        "## 全ファイル\n\n"
        "`full_replacements/source.py` と `full_replacements/phase165_r52_r9_shared_math.py` を参照。\n"
        "実際の patch は元ファイルの改行コードを保持します。\n"
    )
    (OUTPUT / "CODE_FULL_JA.md").write_text(document, encoding="utf-8")


def run(dry_run: bool = False) -> None:
    head, originals = preflight()
    replacements = prepare_replacements(originals)
    print("PHASE171_R20R11_BRANCH=develop", flush=True)
    print("PHASE171_R20R11_HEAD=" + head, flush=True)
    print("PHASE171_R20R11_SOURCE_CONTENT_GUARD=PASS", flush=True)
    print("PHASE171_R20R11_CHANGED_FILES=" + ",".join(str(n) for n in EXPECTED_BLOBS), flush=True)
    if dry_run:
        print("PHASE171_R20R11_DRY_RUN=PASS", flush=True)
        return
    backup_dir = OUTPUT / "backup"
    backup_dir.mkdir(parents=True, exist_ok=True)
    for name, original in originals.items():
        (backup_dir / (name.name + (".source" if name == SOURCE_PATH else ".shared") + ".before")).write_bytes(original)
    changed = []
    try:
        for name, replacement in replacements.items():
            (ROOT / name).write_bytes(replacement)
            changed.append(name)
        write_code_document(replacements)
    except Exception:
        for name in reversed(changed):
            (ROOT / name).write_bytes(originals[name])
        raise
    print("PHASE171_R20R11_PATCHED=" + ",".join(str(n) for n in changed), flush=True)
    print("PHASE171_R20R11_FULL_CODE=" + str(OUTPUT / "CODE_FULL_JA.md"), flush=True)
    print("PHASE171_R20R11_RESULT=PASS_PATCHED", flush=True)


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--dry-run", action="store_true")
    arguments = parser.parse_args()
    run(dry_run=arguments.dry_run)


if __name__ == "__main__":
    main()
