def inspect_source_provider(root: Path) -> dict[str, Any]:
    """Compare against the pinned current HEAD or the exact reviewed new provider."""
    file = root / SOURCE_FILE
    source = file.read_bytes()
    parsed = ast.parse(source.decode("utf-8-sig"))
    functions = [
        node for node in parsed.body
        if isinstance(node, ast.FunctionDef)
        and node.name == "shared_expansion_provider"
    ]
    if len(functions) != 1:
        raise ValueError("shared_expansion_provider must have one definition")
    if source.count(DELTA_HOOK.encode("utf-8")) != 1:
        raise ValueError("R3-R4 general Delta-zero hook is absent or duplicated")
    import subprocess
    from phase174_r3_r6_r2_prop44_lemma54.patch import git_blob, normalize, patch_shared

    original = subprocess.run(
        ("git", "show", "HEAD:" + SOURCE_FILE),
        cwd=root, check=True, capture_output=True,
    ).stdout
    if git_blob(original) != "bf5bc76c842a6fcac65fc88846f96a95917d0624":
        raise ValueError("Unexpected committed R3-R6 source")
    original_text = normalize(original.decode("utf-8-sig"))
    expected = patch_shared(original_text)
    normalized_current = normalize(source.decode("utf-8-sig"))
    if normalized_current not in (original_text, expected):
        raise ValueError("Unreviewed production source modifications")
    state = "COMMITTED" if normalized_current == original_text else "WORKTREE_PATCHED"
    return {
        "state": state,
        "delta_provider_hook_present": True,
        "full_function_line_count": functions[0].end_lineno - functions[0].lineno + 1,
        "production_source_changed_by_this_audit": False,
    }
