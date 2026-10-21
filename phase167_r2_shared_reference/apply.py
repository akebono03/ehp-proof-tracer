from __future__ import annotations
import ast
import json
import shutil
from pathlib import Path

repo = Path(__file__).resolve().parent.parent
target = repo / "toda_group_proof_narrative_references.py"
test = repo / "tests" / "test_phase167_r2_shared_reference.py"
folder = Path(__file__).resolve().parent
source = target.read_text(encoding="utf-8")
tree = ast.parse(source)
matches = [n for n in tree.body if isinstance(n, ast.FunctionDef)
           and n.name == "render_toda_group_proof_narrative_reference_entries_markdown"]
if len(matches) != 1:
    raise RuntimeError("Reference renderer function not unique")
node = matches[0]
parts = source.splitlines(keepends=True)
start = sum(len(x) for x in parts[:node.lineno-1])
end = sum(len(x) for x in parts[:node.end_lineno])
original = source[start:end]
a = original.find('    if entry.reference.locator == "(5.1)":')
b = original.find('    if entry.reference.locator == "Proposition 4.2":', a)
if a == -1 or b == -1:
    raise RuntimeError("Expected old branch missing; repo may have changed")
modified = original[:a] + original[b:]
anchor = "    for statement_line in statement_lines:\n"
fallback = r'''    # Typed universal connectivity assertion: render its general mathematical
    # statement through the same statement_lines pipeline as every reference.
    # The decision is based on the proven GIVEN statement, never on locator text.
    additional_lines = []
    for proof_step in entry.proof_steps:
      if (
        type(proof_step.conclusion).__name__ == "Toda51BelowDiagonalZeroStatement"
        and not proof_step.premises
        and getattr(proof_step.rule, "name", None) == "GIVEN"
      ):
        additional_lines.append(r"$\pi_{i}^{n} = 0\ (i < n)$")
    statement_lines = tuple(dict.fromkeys(
      (*statement_lines, *additional_lines)
    ))

'''
if modified.count(anchor) != 1:
    raise RuntimeError("Expected common reference iteration missing")
modified = modified.replace(anchor, fallback + anchor)
new_source = source[:start] + modified + source[end:]
ast.parse(new_source)
tests = r'''from web_group_proof import build_standard_web_group_proof_view
from toda_group_proof_narrative_references import (
    TodaGroupProofNarrativeReferenceEntry,
    render_toda_group_proof_narrative_reference_entries_markdown,
)
from proof import InferenceRule, LiteratureReference, ProofRule, ProofStep


def test_phase167_r2_pi43_reference_has_two_general_results():
    view = build_standard_web_group_proof_view(3, 1, 2, "narrative")
    text = "\n".join(
        str(line) if isinstance(line, str)
        else str(getattr(line, "statement_latex", "") or "")
        for line in view.rendered_lines
    )
    assert view.key == "generic-complete-proof"
    section = text.split("使用する結果", 1)[1].split("証明", 1)[0]
    assert r"\pi_{n}^{n}" in section
    assert r"\pi_{i}^{n}" in section
    assert "Proposition 5.1" in section


def test_phase167_r2_other_references_keep_common_statement_lines():
    ref = LiteratureReference(label="Generic source", locator="Generic source")
    step = ProofStep(
        conclusion="general claim",
        premises=(),
        rule=ProofRule.GIVEN,
        inference_rule=InferenceRule(name="generic", literature_reference=ref),
    )
    entry = TodaGroupProofNarrativeReferenceEntry(
        number=1, reference=ref, proof_steps=(step,)
    )
    rendered = render_toda_group_proof_narrative_reference_entries_markdown(
        (entry,), {1: ("$x=y$",)}
    )
    assert "$x=y$" in rendered
    assert "**[R1] Generic source.**" in rendered
'''
ast.parse(tests)
backup = folder / "backup" / target.name
backup.parent.mkdir(parents=True, exist_ok=True)
if not backup.exists():
    shutil.copy2(target, backup)
target.write_text(new_source, encoding="utf-8")
test.write_text(tests, encoding="utf-8")
(folder/"modified_function_full.py").write_text(modified, encoding="utf-8")
print(json.dumps({"modified":str(target),"backup":str(backup),
 "new_test":str(test),"full_function":str(folder/"modified_function_full.py")},ensure_ascii=False,indent=2))
