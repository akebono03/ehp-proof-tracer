def certify_documents(root: Path, backup: Path) -> list[dict[str, Any]]:
    """Verify all five complete documents against the exact R2A output archive."""
    from phase169_r10et_closeout_r2_documentation.update_docs import (
        APPENDIX_PATHS, DOCUMENT_BLOBS, updated_document,
    )

    manifest = json.loads((backup / "manifest.json").read_text(encoding="utf-8"))
    if (manifest.get("head") != R2A_MANIFEST_HEAD
            or manifest.get("phase_169_closed") is not False
            or manifest.get("full_pytest_executed") is not False
            or manifest.get("index_modified") is not False):
        raise RuntimeError("Unexpected R2A backup manifest")
    records = manifest.get("documents")
    if not isinstance(records, list) or {x.get("path") for x in records} != set(DOCUMENT_BLOBS):
        raise RuntimeError("R2A manifest has missing or extra documents")
    archive = backup / "updated_five_documents_FULL.zip"
    import zipfile
    with zipfile.ZipFile(archive) as z:
        if z.testzip() is not None or set(z.namelist()) != set(DOCUMENT_BLOBS):
            raise RuntimeError("R2A full-document archive is incomplete or corrupt")
        for path in DOCUMENT_BLOBS:
            if z.read(path) != (backup / "AFTER_FULL" / path).read_bytes():
                raise RuntimeError("Archive and backed-up final document differ: " + path)

    output = []
    appendix_root = root / "phase169_r10et_closeout_r2_documentation" / "appendices"
    for path, expected_blob in DOCUMENT_BLOBS.items():
        record = next(x for x in records if x["path"] == path)
        before = (backup / "BEFORE_FULL" / path).read_bytes()
        after = (backup / "AFTER_FULL" / path).read_bytes()
        current = (root / path).read_bytes()
        appendix = (appendix_root / APPENDIX_PATHS[path]).read_text(encoding="utf-8")
        reproduced = updated_document(path, before, appendix)
        blob = git(root, "hash-object", f"--path={path}", "--stdin", input_bytes=before)
        if (blob != expected_blob
                or record.get("before_git_blob") != blob
                or hashlib.sha256(before).hexdigest() != record.get("before_sha256")
                or hashlib.sha256(after).hexdigest() != record.get("after_sha256")
                or reproduced != after
                or current != after):
            raise RuntimeError("Document bytes or baseline differ: " + path)
        output.append({"path": path, "after_sha256": hashlib.sha256(after).hexdigest()})
    return output
