import runpy
import toda_proof_narrative_renderer as narrative

TARGETS = {
  "Toda211OrdinaryEHPApplicabilityStatement",
  "Toda515Sigma8Prop44SpecializationStatement",
  "Toda515Sigma8TransportedDecompositionStatement",
  "TodaLemma510Nu6OrdinaryCompositionReductionStatement",
  "TodaLemma510Nu6OrdinaryCompositionZeroStatement",
  "TodaLemma510OrdinaryIndeterminacyDoubleStatement",
}


def test_phase143_75ap_all_final_targets_render_semantically():
  captured = {}
  original = narrative.render_toda_proof_statement_latex

  def capture(statement):
    name = type(statement).__name__
    if name in TARGETS:
      captured.setdefault(name, statement)
    return original(statement)

  narrative.render_toda_proof_statement_latex = capture
  try:
    runpy.run_path(
      "phase143_75u/audit_phase143_75u_remaining_fallbacks.py",
      run_name="__main__",
    )
  finally:
    narrative.render_toda_proof_statement_latex = original

  assert set(captured) == TARGETS

  for name, statement in captured.items():
    rendered = original(statement)
    assert rendered is not None, name
    assert "Toda " not in rendered, (name, rendered)
    assert "transported decomposition" not in rendered
    assert "specialization premises" not in rendered
