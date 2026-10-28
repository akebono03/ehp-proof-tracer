"""R10ET-R6C guarded patch, focused tests, 19-case audit, rollback."""
from __future__ import annotations

import argparse
import datetime
import json
import os
import subprocess
import sys
import traceback
from pathlib import Path

sys.dont_write_bytecode = True

from patch import EXPECTED_GIT_BLOBS, MODEL, RENDERER, extract_whole_function, git_blob, transform

EXPECTED_HEAD = "232a92883b0cb009762b437cbb3cc550f00ab6bd"


def git(root: Path, *arguments: str) -> bytes:
    result = subprocess.run(("git", "-C", str(root), *arguments),
                            capture_output=True, check=True)
    return result.stdout


def snapshot(root: Path) -> dict[str, str]:
    return {"head":git(root,"rev-parse","HEAD").decode().strip(),
            "index":git(root,"diff","--cached","--raw","-z").hex(),
            "tracked":git(root,"diff","--raw","-z").hex(),
            "index_type":"raw staged blob diff"}


def guard(root: Path) -> None:
    if git(root,"branch","--show-current").decode().strip() != "develop":
        raise RuntimeError("R6C requires develop")
    if git(root,"rev-parse","HEAD").decode().strip() != EXPECTED_HEAD:
        raise RuntimeError("R6C refuses unreviewed HEAD; review GitHub sources first")
    for path, sha in EXPECTED_GIT_BLOBS.items():
        if git_blob((root/path).read_bytes()) != sha:
            raise RuntimeError(f"R6C refuses modified source before patch: {path}")
        if git_blob(git(root,"show",f"HEAD:{path}")) != sha:
            raise RuntimeError(f"R6C Git HEAD source differs: {path}")
    # Verify the existing R5 provider and four migrated tests without changing them.
    from phase169_r10et_r5d_staged_audit_guard.patch import EXPECTED_BLOBS, transform as r5_transform
    for path, expected in EXPECTED_BLOBS.items():
        baseline = git(root,"show",f"3a8014efb91ddf76060c4d07d73153e55ea52c75:{path}")
        from phase169_r10et_r5d_staged_audit_guard.patch import git_blob as r5_blob
        if r5_blob(baseline) != expected or (root/path).read_bytes() != r5_transform(path, baseline)[0]:
            raise RuntimeError(f"R6C existing R5 requirement failed: {path}")
    # No staged target source may be replaced, even if bytes match HEAD.
    staged = git(root,"diff","--cached","--name-only","-z").decode("utf-8").split("\0")
    if MODEL in staged or RENDERER in staged:
        raise RuntimeError("R6C refuses staged edits to its two target files")


def run_pytest(root: Path) -> None:
    packages = [
        "phase169_r10et_r6c_root_reachable_citations/tests/test_r6c_root_citations.py",
        "phase169_r10et_r6c_root_reachable_citations/tests/test_r6c_patch.py",
        "phase168_r3_3_narrative_model/tests/test_phase168_r3_3_proof_narrative_model.py",
        "phase168_r3_41p13_trust_boundary/tests/test_phase168_r3_41p13_trust_boundary.py",
        "phase169_r10a_verified_stable_chain_projection/tests/test_r10a_verified_stable_chain.py",
        "phase169_r10et_r4_cyclic_definition_projection/tests/test_r10et_r4_live.py",
        "phase169_r10et_r5_common_definition_provider/tests/test_r5_live.py",
        "phase169_r10ec_direct_sum_narrative_projection/tests/test_r10ec_projection.py",
    ]
    missing = [path for path in packages if not (root/path).is_file()]
    if missing:
        raise RuntimeError(f"focused tests absent: {missing}")
    env=os.environ.copy()
    env["PYTHONDONTWRITEBYTECODE"]="1"
    env["PYTHONPATH"]=str(root)+os.pathsep+env.get("PYTHONPATH","")
    print("R10ET_R6C_FOCUSED_PYTEST_START", flush=True)
    result=subprocess.run((sys.executable,"-m","pytest","-q",*packages),cwd=root,env=env)
    print(f"R10ET_R6C_FOCUSED_PYTEST_EXIT={result.returncode}",flush=True)
    if result.returncode:
        raise RuntimeError("R6C focused test failed")


def execute(root: Path) -> int:
    print("R10ET_R6C_MODE=IMPLEMENT_FOCUSED",flush=True)
    print(f"R10ET_R6C_HEAD={git(root,'rev-parse','HEAD').decode().strip()}",flush=True)
    sys.path.insert(0,str(root))
    guard(root)
    original = {path:(root/path).read_bytes() for path in EXPECTED_GIT_BLOBS}
    prepared = {path:transform(path,raw) for path,raw in original.items()}
    before = snapshot(root)
    backup_root = Path(os.environ.get("LOCALAPPDATA",os.environ.get("TEMP",str(root)))) / "EHPProofTracerRecovery"
    suffix = datetime.datetime.now().strftime("%Y%m%d_%H%M%S_%f")
    output=backup_root/f"r10et_r6c_{suffix}"
    output.mkdir(parents=True,exist_ok=False)
    for path,raw in original.items():
        (output/"before"/path).parent.mkdir(parents=True,exist_ok=True)
        (output/"before"/path).write_bytes(raw)
        (output/"after"/path).parent.mkdir(parents=True,exist_ok=True)
        (output/"after"/path).write_bytes(prepared[path])
    (output/"full_function_build_proof_narrative_model.py").write_text(
        extract_whole_function(prepared[MODEL],"build_proof_narrative_model"),encoding="utf-8")
    (output/"full_function_root_ancestor_step_indices.py").write_text(
        extract_whole_function(prepared[MODEL],"root_ancestor_step_indices"),encoding="utf-8")
    (output/"full_function_render_model_backed_narrative_markdown.py").write_text(
        extract_whole_function(prepared[RENDERER],"render_model_backed_narrative_markdown"),encoding="utf-8")
    (output/"scope.json").write_text(json.dumps({"mode":"R6C","head":EXPECTED_HEAD,
        "target_files":list(original),"before_index_snapshot":before},indent=2)+"\n",encoding="utf-8")
    print(f"R10ET_R6C_BACKUP={output}",flush=True)
    try:
        for path,data in prepared.items():
            (root/path).write_bytes(data)
        print("R10ET_R6C_PATCHED="+",".join(prepared),flush=True)
        run_pytest(root)
        from phase169_r10et_r6c_root_reachable_citations.audit import audit_real_cases
        report=audit_real_cases(root,output/"audit")
        if not report["success"]:
            raise RuntimeError("R6C 19-case audit rejected the repaired citations")
        after=snapshot(root)
        if before["head"]!=after["head"] or before["index"]!=after["index"]:
            raise RuntimeError("unexpected HEAD/staged index changes")
        expected_unstaged=sorted(path for path in prepared)
        current_names=set(git(root,"diff","--name-only","-z").decode().rstrip("\0").split("\0"))
        if not set(expected_unstaged).issubset(current_names):
            raise RuntimeError("patched target source missing from tracked diff")
        for path,data in prepared.items():
            if (root/path).read_bytes()!=data:
                raise RuntimeError(f"unexpected concurrent modification: {path}")
        print("R10ET_R6C_19_CASES=PASS",flush=True)
        print("R10ET_R6C_TRACKED_PREEXISTING_R5_PRESERVED=True",flush=True)
        print("R10ET_R6C_INDEX_PRESERVED=True",flush=True)
        print("R10ET_R6C_COMPLETE=PASS",flush=True)
        return 0
    except BaseException:
        print("R10ET_R6C_ERROR="+traceback.format_exc(),flush=True)
        for path,raw in original.items():
            (root/path).write_bytes(raw)
        print("R10ET_R6C_ROLLBACK=True",flush=True)
        return 1


def main() -> int:
    parser=argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--repo",type=Path,required=True)
    args=parser.parse_args()
    try:
        return execute(args.repo.resolve())
    except BaseException:
        print("R10ET_R6C_ERROR="+traceback.format_exc(),flush=True)
        return 1


if __name__=="__main__":
    raise SystemExit(main())
