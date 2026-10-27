def verify_prop44_hopf_fibration_source(source_path: Path | None = None) -> None:
    """Verify the actual Chapter IV paragraph immediately before Proposition 4.4.

    The frozen Git blob is an independently reviewed source identity; no
    assertion can be introduced from a modified or incomplete passage.
    """
    if source_path is None:
        source_path = Path(__file__).resolve().parent / "sources" / "toda" / "Toda_04_2.tex"
    if not isinstance(source_path, Path):
        raise TypeError("source_path must be a pathlib.Path")
    original = source_path.read_bytes()
    normalized = original.replace(b"\r\n", b"\n")
    candidates = (original, normalized, normalized.replace(b"\n", b"\r\n"))
    def actual_sha(content: bytes) -> str:
        return sha1(b"blob " + str(len(content)).encode("ascii") + b"\x00" + content).hexdigest()
    if not any(actual_sha(candidate) == "4d0c32b196f4bd51c04650dd26b0fd7133b6d4f7"
               for candidate in candidates):
        raise ValueError("unverified Toda Chapter IV source file for Hopf fibration")
    text = normalized.decode("utf-8")
    start_marker = "$n=2,4,8$ のとき, Hopf fibration"
    end_marker = r"\begin{proposition}\label{prop:4.4}"
    start = text.find(start_marker)
    end = text.find(end_marker)
    if start < 0 or end <= start or text.count(start_marker) != 1 or text.count(end_marker) != 1:
        raise ValueError("Proposition 4.4 Hopf-fibration source position is invalid")
    passage = text[start:end]
    required = (
        r"S^{2n-1}\xrightarrow{h} S^n",
        "Hopf 不変量",
        r"$\pm1$",
        r"\cite{Steenrod1951}",
    )
    if any(fragment not in passage for fragment in required):
        raise ValueError("the reviewed Hopf-fibration prelude is missing")

