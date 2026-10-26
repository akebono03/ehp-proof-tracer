def patch_renderer(func: str) -> str:
    original = func
    import_line = "    from phase165_r14_r14_diagonal_and_prop42 import GeneratorSuspension\n"
    if func.count(import_line) != 1:
        raise RuntimeError("R3K2 renderer import anchor changed")
    if "from phase165_r14_r6_generic_iso import GeneratorImage" not in func:
        func = func.replace(import_line, import_line +
                            "    from phase165_r14_r6_generic_iso import GeneratorImage\n", 1)
    locator = "        locator = citation.reference.locator or citation.reference.label\n"
    if func.count(locator) != 1:
        raise RuntimeError("R3K2 citation locator anchor changed")
    func = func.replace(locator, locator +
        '        if locator == "Chapter V, i)":\n'
        '            locator = "η 系列の定義（Chapter V, i）"\n', 1)
    if func.count(OLD_ETA_SOURCE) != 1:
        raise RuntimeError("R3K2 typed-eta citation anchor changed")
    func = func.replace(OLD_ETA_SOURCE, NEW_ETA_SOURCE, 1)
    # The former import-text anchor matches both 4-space and 8-space
    # indentation in R3K; locate the unique top-level body loop instead.
    body_loop = "    for index in order:\n"
    if func.splitlines(keepends=True).count(body_loop) != 1:
        raise RuntimeError("R3K2 body-loop anchor changed")
    if ("    def unique_step_index(premise):\n" not in func
            or "    def only_consumed_by(candidate, consumer):\n" not in func
            or "    displayed_cyclic_math = set()\n" not in func):
        raise RuntimeError("R3K2 R3K suppression dependencies changed")
    func = func.replace(body_loop, SUPPRESS_TRANSPORT_INTERMEDIATES + body_loop, 1)
    if func == original:
        raise RuntimeError("No renderer changes applied")
    ast.parse(func)
    return func
