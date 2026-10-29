# R3-R6 HEAD 同期補正 — 変更コード全文

変更対象: `phase170_r3_r6_prop58_pi73_source/runner.py` のモジュール定数 `HEAD`、新規定数 `REVIEWED_COMMITTED_R3R5_BLOB`、および `preflight()` 関数全体。import は変更なし。本 ZIP には置換できる `runner.py` 全文と、追加テスト関数の全文を収録している。Proposition 5.8 数学的登録の本体や Web 検証は変更していない。

```python
HEAD = "970535190e160e9f2ae9e596a3ccb13abb9c913c"
REVIEWED_COMMITTED_R3R5_BLOB = "b3e104857e3a8129fb01df65ce3a38ff188ecd1f"
```

```python
def preflight(root: Path) -> dict:
    branch = git(root, "branch", "--show-current")
    head = git(root, "rev-parse", "HEAD")
    if branch != "develop" or head != HEAD:
        raise RuntimeError(f"unreviewed Git branch or HEAD: {branch} {head}")
    staged = git(root, "diff", "--cached", "--name-only")
    if staged:
        raise RuntimeError("staged tracked changes are not allowed")
    dirty = tuple(x for x in git(root, "diff", "--name-only").splitlines() if x)
    if dirty:
        raise RuntimeError(f"reviewed committed R3-R5 requires clean tracked worktree, found {dirty!r}")
    if git(root, "rev-parse", f"HEAD:{PREVIOUS_PATCH}") != REVIEWED_COMMITTED_R3R5_BLOB:
        raise RuntimeError("reviewed committed R3-R5 Toda (5.2) blob changed")
    if git(root, "rev-parse", f"HEAD:{REGISTRATION}") != ORIGINAL_REGISTRATION_BLOB:
        raise RuntimeError("reviewed registration module blob changed")
    previous = root / PREVIOUS_PATCH
    if hashlib.sha256(previous.read_bytes()).hexdigest() != PATCHED_R3R5_SHA256:
        raise RuntimeError("existing R3-R5 Toda (5.2) implementation changed")
    target = root / REGISTRATION
    if not target.is_file():
        raise RuntimeError("registration module missing")
    source = root / NEW_SOURCE
    if source.exists():
        raise RuntimeError("new source-binding module already exists; refusing overwrite")
    if git(root, "diff", "--", REGISTRATION):
        raise RuntimeError("registration module has preexisting changes")
    return {"branch": branch, "head": head, "committed_r3r5": PREVIOUS_PATCH,
            "committed_r3r5_blob": REVIEWED_COMMITTED_R3R5_BLOB,
            "committed_r3r5_sha256": PATCHED_R3R5_SHA256}

```
