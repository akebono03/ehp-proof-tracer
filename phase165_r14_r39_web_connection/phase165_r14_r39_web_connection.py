"""Present the newly reconstructed registered pi_3(S^2) proof on the existing Web group-proof page."""
from __future__ import annotations
from pathlib import Path

from phase165_r14_r38_direct_registry import reconstruct_registered_pi32


def build_phase165_pi32_web_view(max_depth: int = 2, mode: str = "narrative"):
    """Make the existing Web view classes from the R38 registered backward proof."""
    from web_group_proof import (
        WebGroupProofStepView, WebGroupProofView,
        _build_group_proof_rendered_lines, _group_proof_statement_latex,
        _group_proof_rule_name,
    )
    if isinstance(max_depth, bool) or not isinstance(max_depth, int) or max_depth not in (0, 1, 2):
        raise ValueError("max_depth must be 0, 1, or 2")
    if mode not in ("trace", "outline", "narrative"):
        raise ValueError("mode must be trace, outline, or narrative")
    tex = Path(__file__).resolve().with_name("phase165_r14_r39_toda51.tex")
    registry, root = reconstruct_registered_pi32(tex)
    conclusion, fallback = _group_proof_statement_latex(root.conclusion)
    if conclusion is None:
        raise ValueError(f"cannot display the pi3^2 conclusion: {fallback}")
    steps = []
    visited = set()
    def visit(step, depth):
        key = id(step)
        if key in visited:
            return
        visited.add(key)
        statement, unknown = _group_proof_statement_latex(step.conclusion)
        steps.append(WebGroupProofStepView(
            depth=depth, statement_latex=statement,
            fallback_type_name=unknown,
            rule_name=_group_proof_rule_name(step),
            role_name="root" if depth == 0 else ("reference" if not step.premises else "inference"),
        ))
        if depth < max_depth:
            for premise in step.premises:
                visit(premise, depth + 1)
    visit(root, 0)
    if mode == "trace":
        rendered = ()
    else:
        # Render the registered backward proof, not a historical repository replay.
        # The Web markdown-to-inline-math renderer is deliberately reused.
        markdown = "\n".join((
            "## 証明対象",
            r"$\pi_3^2=\mathbb{Z}\{\eta_2\}$",
            "## 使用する結果",
            r"Toda (5.1): $\pi_2^1=0$, $\pi_n^n=\mathbb{Z}\{\iota_n\}$.",
            "Proposition 4.2: EHP 完全列 (4.4).",
            r"Proposition 5.1: $H(\eta_2)=\iota_3$.",
            r"基本事実: $E(\iota_1)=\iota_2$.",
            "---",
            "## 証明",
            r"$E:\pi_1^1\to\pi_2^2$ は同型である。",
            r"完全性より $\operatorname{Im}\Delta=\ker E=0$、したがって $\Delta=0$ である。",
            r"$\operatorname{Im}H=\ker\Delta=\pi_3^3$ より $H$ は全射である。",
            r"また $\pi_2^1=0$ と完全性から $\ker H=0$、したがって $H$ は単射である。",
            r"よって $H:\pi_3^2\xrightarrow{\cong}\pi_3^3$ である。",
            r"$\pi_3^3=\mathbb{Z}\{\iota_3\}$ と $H(\eta_2)=\iota_3$ より、",
            r"$\pi_3^2=\mathbb{Z}\{\eta_2\}$. □",
        ))
        rendered = _build_group_proof_rendered_lines(markdown)
    return WebGroupProofView(
        n=2, k=1, conclusion_latex=conclusion,
        theorem="Toda (5.1); Proposition 4.2; Proposition 5.1",
        phase="165", key="phase165:registered:pi3_2",
        steps=tuple(steps), max_depth=max_depth, mode=mode,
        rendered_lines=rendered,
    )
