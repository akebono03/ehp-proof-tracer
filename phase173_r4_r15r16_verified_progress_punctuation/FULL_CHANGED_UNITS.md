# R15R16 変更後のコード全文（関数単位）

## 変更対象

- `phase173_r4_r15r9_shared_abstract_renderer/projection.py` の `_render_abstract_claim`（全文置換）と新規 `_verified_abstract_progress_lines`（直前に追加）.
- `phase173_r4_r15r13_unified_presentation/layout.py` の `canonicalize_proof_layout` の末尾を修正し, 新規 `_normalize_narrative_punctuation` をファイル末尾へ追加.
- import 文の変更なし.

## `_verified_abstract_progress_lines` と `_render_abstract_claim`

```python
def _verified_abstract_progress_lines(
    structure: CertifiedAbstractStructure,
) -> tuple[str, ...]:
    """Present actual certified premises, without adopting named-generator goals.

    The certificate's original typed inference guard has already checked its
    four premises. Their registered source metadata is used only for display.
    No new proof step, citation identity, or mathematical conclusion is made.
    """
    from web_group_proof_common import _group_proof_statement_latex

    root = structure.proof_step
    if len(root.premises) != 4:
        raise ValueError("verified abstract inference requires four premises")
    theorem_step, first_prior, second_prior, hopf_step = root.premises

    def source_label(step: object) -> str | None:
        rule = getattr(step, "inference_rule", None)
        reference = getattr(rule, "literature_reference", None)
        if reference is None:
            return None
        label = reference.locator or reference.label
        return label if isinstance(label, str) and label.strip() else None

    def verified_math(step: object) -> str | None:
        try:
            latex, fallback = _group_proof_statement_latex(step.conclusion)
        except (TypeError, ValueError):
            return None
        return f"${latex}$" if latex is not None and fallback is None else None

    theorem_label = source_label(root)
    theorem_description = (
        f"{theorem_label} の適用前提となる定理を検証した."
        if theorem_label is not None else "一般定理の前提を検証した."
    )
    lines = [theorem_description]
    for prior in (first_prior, second_prior):
        formula = verified_math(prior)
        locator = source_label(prior)
        if formula is not None and locator is not None:
            lines.append(f"先行データベースの {formula} を {locator} により確認した.")
        elif formula is not None:
            lines.append(f"先行データベースの検証済み結果 {formula} を確認した.")
        else:
            lines.append("先行データベースの型付き結果を検証した.")

    hopf_formula = verified_math(hopf_step)
    hopf_locator = source_label(hopf_step)
    if hopf_formula is not None and hopf_locator is not None:
        lines.append(f"{hopf_locator} から {hopf_formula} を導いた.")
    elif hopf_formula is not None:
        lines.append(f"検証済みの Hopf 関係 {hopf_formula} を導いた.")
    else:
        lines.append("検証済みの Hopf 関係を前提として確認した.")

    theorem_reference = theorem_label or "検証済みの一般定理"
    lines.append(
        f"これらの検証済み前提を使い, {theorem_reference} により"
        "抽象群構造を導いた."
    )
    return tuple(lines)


def _render_abstract_claim(target: object, structure: CertifiedAbstractStructure) -> str:
    """Show certified progress and the abstract claim, never named generators."""
    if type(target.group_dimension) is not int or type(target.sphere_dimension) is not int:
        raise ValueError("abstract result has nonconcrete group dimensions")
    invariant_latex = abstract_invariants_latex(structure.invariant_summands)
    target_latex = rf"\pi_{{{target.group_dimension}}}^{{{target.sphere_dimension}}}"
    progress = "\n\n".join(_verified_abstract_progress_lines(structure))
    return (
        "## 検証済みの途中経過\n\n"
        + progress
        + "\n\n"
        + "## 証明済みの抽象群構造\n\n"
        + rf"${target_latex} \cong {invariant_latex}$."
        + "\n\n"
        + "これは出典検査済みの抽象群 ProofStep による結論であり、"
        + "登録済みの先行 DB 群を前提とする。"
        + "記名生成元の対応は未証明であり、上記の未解決 Goal と探索状態は変わらない。"
    )
```

## `canonicalize_proof_layout` の完全な定義

```python
def canonicalize_proof_layout(markdown: str) -> str:
    """Use one Reference/Proof section layout, preserving proof body verbatim.

    Both historical Markdown spellings (plain and ## headings) represent the
    same semantic sections. Only the outer Web-owned target and Proof headers
    are suppressed when duplicates are present inside the narrative. This
    transformation never reads status, n, k, references, or mathematical data.
    """
    if not isinstance(markdown, str):
        raise TypeError("markdown must be str")
    lines = markdown.splitlines()
    reference_indices = [
        i for i, line in enumerate(lines)
        if line.strip() in ("使用する結果", "## 使用する結果")
    ]
    if len(reference_indices) != 1:
        return markdown
    reference_index = reference_indices[0]
    proof_indices = [
        i for i in range(reference_index + 1, len(lines))
        if lines[i].strip() in ("証明", "## 証明")
    ]
    if len(proof_indices) != 1:
        return markdown
    proof_index = proof_indices[0]

    prelude = list(lines[:reference_index])
    # WebGroupProofView already presents the group target above the narrative.
    # Remove the second copy only when the entire prelude consists of that
    # exact heading and one displayable math target. Leave unknown preludes
    # intact rather than silently discarding source content.
    meaningful = [line.strip() for line in prelude if line.strip()]
    if (len(meaningful) == 2 and meaningful[0] == "## 証明対象"
            and meaningful[1].startswith("$") and meaningful[1].endswith("$")):
        prelude = []

    reference_body = list(lines[reference_index + 1:proof_index])
    while reference_body and not reference_body[-1].strip():
        reference_body.pop()
    if reference_body and reference_body[-1].strip() == "---":
        reference_body.pop()
    while reference_body and not reference_body[-1].strip():
        reference_body.pop()
    while reference_body and not reference_body[0].strip():
        reference_body.pop(0)

    proof_body = list(lines[proof_index + 1:])
    while proof_body and not proof_body[0].strip():
        proof_body.pop(0)

    # The outer Web Proof heading owns the proof section title. All narratives
    # receive the same inner Reference heading and the same section separator.
    # Only headings and redundant duplicate-target presentation are modified.
    normalized = [*prelude, "## 使用する結果", "", *reference_body,
                  "", "---", "", *proof_body]
    in_search_diagnostics = False
    for index, line in enumerate(normalized):
        if line.startswith(("## ", "### ")):
            in_search_diagnostics = line.strip() == "## 探索診断"
        elif in_search_diagnostics and line.startswith("- "):
            normalized[index] = _public_search_diagnostic_line(line)
    normalized = _normalize_narrative_punctuation(normalized)
    result = "\n".join(normalized)
    return result.rstrip("\n") + ("\n" if markdown.endswith("\n") else "")

```

## 新規 `_normalize_narrative_punctuation`（ファイル末尾）

```python


def _normalize_narrative_punctuation(lines: list[str]) -> list[str]:
    """Apply uniform prose punctuation to the common Web narrative layout.

    Math and inline-code spans remain untouched. Numbered source locators,
    decimal points, headings, and display math remain intact. Sentence-final
    periods create physical line breaks, not new proof steps.
    """
    result: list[str] = []
    in_display_math = False
    in_code_fence = False
    for line in lines:
        stripped = line.strip()
        if stripped.startswith("```"):
            in_code_fence = not in_code_fence
            result.append(line)
            continue
        if stripped == r"\[":
            in_display_math = True
            result.append(line)
            continue
        if stripped == r"\]":
            in_display_math = False
            result.append(line)
            continue
        if (in_code_fence or in_display_math
                or stripped.startswith(("# ", "## ", "### "))):
            result.append(line)
            continue

        chunks: list[str] = []
        current: list[str] = []
        in_inline_math = False
        in_inline_code = False
        for index, raw in enumerate(line):
            if raw == "$" and not in_inline_code and (index == 0 or line[index - 1] != "\\"):
                in_inline_math = not in_inline_math
            elif raw == "`" and not in_inline_math and (index == 0 or line[index - 1] != "\\"):
                in_inline_code = not in_inline_code

            protected = in_inline_math or in_inline_code or raw in ("$", "`")
            character = raw
            if not protected and raw in ("、", "，"):
                character = "," if (index + 1 < len(line) and line[index + 1].isspace()) else ", "
            elif not protected and raw == "。":
                character = "."
            current.append(character)

            if protected or character != ".":
                continue
            remaining = line[index + 1:]
            next_word = remaining.lstrip()
            if not next_word:
                continue
            # The dot in 4.4, 0.5, or an enumerated item is not a full stop.
            if raw == "." and remaining[0].isdigit():
                continue
            if raw == "." and "".join(current[:-1]).strip().isdigit():
                continue
            next_char = next_word[0]
            is_japanese = (
                "\u3040" <= next_char <= "\u30ff"
                or "\u3400" <= next_char <= "\u9fff"
            )
            sentence_boundary = raw == "。" or is_japanese or (
                remaining[0].isspace()
                and (next_char.isupper() or next_char in "（[「")
            )
            if sentence_boundary:
                chunks.append("".join(current).rstrip())
                current = []
        final = "".join(current).strip()
        if final:
            chunks.append(final)
        if chunks:
            result.extend(chunks)
        else:
            result.append("")
    return result
```
