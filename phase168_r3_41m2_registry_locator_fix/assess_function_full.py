def assess(name: str, proof: str) -> list[dict[str, object]]:
    """Explicit benchmark wording checks, not a mathematical proof validator."""
    flat = compact(proof)
    if name == "pi3_2":
        requirements = (
            ("exactness_for_injectivity", "完全性より", r"H:\pi_{3}^{2}\to\pi_{3}^{3}", "は単射"),
            ("delta_image_kernel_zero", r"\operatorname{Im}", r"\kerE=0", ""),
            ("hopf_iso_from_bijectivity", "単射性と全射性より", "", ""),
            ("no_generic_circle_in_proof", "", "", ""),
        )
        # For the first check, compare the immediate logical statement, not an
        # unrelated reference to exactness elsewhere in the proof.
        indices = [line for line in proof.splitlines() if "は単射" in line and "H:" in line]
        injectivity = any("完全性より" in line for line in indices)
        delta = (r"\operatorname{Im}" in flat and r"\kerE=0" in flat)
        iso = "単射性と全射性より" in proof
        circle = not bool(re.search(r"\\pi_\{?i\}?\^\{?1\}?", flat))
        return [
            {"key": requirements[0][0], "present": injectivity, "why": "H の単射を完全性から導いたことを明記"},
            {"key": requirements[1][0], "present": delta, "why": r"Im Δ = ker E = 0 を明記"},
            {"key": requirements[2][0], "present": iso, "why": "H の同型性を単射性と全射性から説明"},
            {"key": requirements[3][0], "present": circle, "why": "基準にない一般円周公式の本文再掲がない"},
        ]
    if name == "pi4_3":
        lines = [line for line in proof.splitlines() if "は全射" in line and "E:" in line]
        return [
            {"key": "surjectivity_from_exactness", "present": any("完全性より" in line for line in lines), "why": "E の全射を完全性から導いたことを明記"},
            {"key": "kernel_presentation", "present": r"\kerE=" in flat and r"\mathbb{Z}" in flat, "why": "ker E の具体的な表示"},
            {"key": "quotient_theorem", "present": "準同型定理より" in proof, "why": "準同型定理を明記"},
            {"key": "diagonal_general_only_in_reference", "present": not bool(re.search(r"\\pi_\{?n\}?\^\{?n\}?", flat)), "why": "一般の対角群構造は Reference に置き本文には重複させない"},
        ]
    if name == "pi5_4":
        match = re.search(r"\(n,m,k\)=\(3,4,1\)", flat)
        cited = re.search(r"\[R\d+\].{0,100}適用", proof)
        source = flat.find(r"\pi_{4}^{3}")
        image = flat.find(r"E(\eta_{3})=\eta_{4}")
        if image < 0:
            image = flat.find(r"E\eta_{3}=\eta_{4}")
        return [
            {"key": "toda45_explicit_substitution", "present": match is not None, "why": "(4.5) への (n,m,k)=(3,4,1) の代入"},
            {"key": "specialization_citation_in_proof", "present": cited is not None, "why": "(4.5) を引用して適用したことを明記"},
            {"key": "source_before_generator_image", "present": source >= 0 and image >= 0 and source < image, "why": "引用する群構造を生成元の像より先に示す"},
            {"key": "specific_map_isomorphism", "present": r"E:\pi_{4}^{3}\to\pi_{5}^{4}" in flat and "は同型" in proof, "why": "具体的な E 同型を表示"},
        ]
    raise ValueError("Unknown frozen comparison case: " + name)
