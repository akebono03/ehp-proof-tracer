"""Phase 173 R15R17-R2: suppress only unrenderable display placeholders."""
from __future__ import annotations

OLD = '''                else:
                    # Preserve a truthful placeholder, not a guessed formula.
                    latex, fallback = _group_proof_statement_latex(statement)
                    statement_text = (f"${latex}$" if latex is not None and fallback is None
                                      else type(statement).__name__ + "（数式表示未対応）")
'''
NEW = '''                else:
                    # Keep every verified ProofStep and its provenance in the
                    # unified Model, but never expose internal Python type names
                    # as a mathematical proof sentence. Unsupported statements
                    # remain part of the proof tree and of cited References.
                    latex, fallback = _group_proof_statement_latex(statement)
                    if latex is None or fallback is not None:
                        continue
                    statement_text = f"${latex}$"
'''


def transform(source: str) -> str:
    """Replace one reviewed incomplete-proof fallback, never any other branch."""
    if not isinstance(source, str):
        raise TypeError("source must be str")
    if source.count(OLD) != 1:
        raise RuntimeError("R15R17-R2 unreviewed renderer or already installed")
    return source.replace(OLD, NEW, 1)
