from pathlib import Path
import ast

path = Path("toda_proof_narrative_renderer.py")
text = path.read_text(encoding="utf-8")

names = [
    "Toda211OrdinaryEHPApplicabilityStatement",
    "Toda515Sigma8Prop44SpecializationStatement",
    "Toda515Sigma8TransportedDecompositionStatement",
    "TodaLemma510Nu6OrdinaryCompositionReductionStatement",
    "TodaLemma510Nu6OrdinaryCompositionZeroStatement",
    "TodaLemma510OrdinaryIndeterminacyDoubleStatement",
]

broken = "".join("  " + name + r",\n" for name in names)
fixed = "".join("  " + name + ",\n" for name in names)

if broken in text:
    text = text.replace(broken, fixed, 1)
    path.write_text(text, encoding="utf-8")
    print("Repaired literal-backslash-n import damage.")
else:
    try:
        ast.parse(text)
    except SyntaxError as exc:
        raise RuntimeError(
            "Expected 75AP R1 damage not found, "
            "but renderer remains invalid."
        ) from exc
    print("No R1 import repair was needed.")

ast.parse(path.read_text(encoding="utf-8"))
print("Renderer syntax is valid after repair.")
