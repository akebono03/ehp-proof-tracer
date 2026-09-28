from pathlib import Path

ROOT = Path.cwd()
multi_path = ROOT / "toda_group_proof_narrative_argument_multi_renderer.py"
body_path = ROOT / "toda_group_proof_narrative_argument_body_renderer.py"

multi = multi_path.read_text(encoding="utf-8-sig")
body = body_path.read_text(encoding="utf-8-sig")

# R16 incorrectly widened the semantic meaning of direct_derivation_premises.
r16 = """    direct_derivation_prerequisites = tuple(
      prerequisite_step
      for premise_step in direct_derivation_premises
      for prerequisite_step in premise_step.premises
      if all(
        prerequisite_step is not existing_step
        for existing_step in direct_derivation_premises
      )
    )
    direct_derivation_premises = (
      direct_derivation_prerequisites
      + direct_derivation_premises
    )
"""
if r16 not in multi:
    raise RuntimeError("R16 prerequisite widening block not found")
multi = multi.replace(r16, "", 1)

# Compute relocation support separately, preserving the existing API meaning.
anchor = """    direct_derivation_premises = (
      ()
      if conclusion_step is None
      else (
        extract_toda_group_proof_narrative_argument_conclusion_direct_derivation_premises(
          argument,
          arguments,
        )
      )
    )

    body = (
"""
replacement = """    direct_derivation_premises = (
      ()
      if conclusion_step is None
      else (
        extract_toda_group_proof_narrative_argument_conclusion_direct_derivation_premises(
          argument,
          arguments,
        )
      )
    )
    direct_derivation_support_steps = tuple(
      support_step
      for premise_step in direct_derivation_premises
      for support_step in premise_step.premises
      if all(
        support_step is not existing_step
        for existing_step in direct_derivation_premises
      )
    )

    body = (
"""
if anchor not in multi:
    raise RuntimeError("multi direct-premise anchor not found")
multi = multi.replace(anchor, replacement, 1)

call_anchor = """        direct_derivation_premises=direct_derivation_premises,
        context_hidden_step_ids=context_hidden_step_ids,
"""
call_replacement = """        direct_derivation_premises=direct_derivation_premises,
        direct_derivation_support_steps=direct_derivation_support_steps,
        context_hidden_step_ids=context_hidden_step_ids,
"""
if call_anchor not in multi:
    raise RuntimeError("multi body-call anchor not found")
multi = multi.replace(call_anchor, call_replacement, 1)

# A relocated support step has actually been rendered by the current argument.
# Record that fact for later cross-argument suppression.
seen_anchor = """    for block in local_body_blocks:
      if (
        block.role
        is not TodaGroupProofNarrativeMathematicalBlockRole
        .EXACTNESS
      ):
"""
seen_replacement = """    seen_non_exact_step_ids.update(
      id(
        support_step
      )
      for support_step in direct_derivation_support_steps
    )

    for block in local_body_blocks:
      if (
        block.role
        is not TodaGroupProofNarrativeMathematicalBlockRole
        .EXACTNESS
      ):
"""
if seen_anchor not in multi:
    raise RuntimeError("multi seen-step anchor not found")
multi = multi.replace(seen_anchor, seen_replacement, 1)

# Body renderer gets a separate support-step channel.
sig_anchor = """  direct_derivation_premises: tuple[
    ProofStep,
    ...,
  ] = (),
  context_hidden_step_ids: (
"""
sig_replacement = """  direct_derivation_premises: tuple[
    ProofStep,
    ...,
  ] = (),
  direct_derivation_support_steps: tuple[
    ProofStep,
    ...,
  ] = (),
  context_hidden_step_ids: (
"""
if sig_anchor not in body:
    raise RuntimeError("body signature anchor not found")
body = body.replace(sig_anchor, sig_replacement, 1)

validation_anchor = """  for premise_step in direct_derivation_premises:
    if not isinstance(
      premise_step,
      ProofStep,
    ):
      raise TypeError(
        "direct_derivation_premises must contain only "
        "ProofStep objects"
      )

  if (
    context_hidden_step_ids is not None
"""
validation_replacement = """  for premise_step in direct_derivation_premises:
    if not isinstance(
      premise_step,
      ProofStep,
    ):
      raise TypeError(
        "direct_derivation_premises must contain only "
        "ProofStep objects"
      )

  if not isinstance(
    direct_derivation_support_steps,
    tuple,
  ):
    raise TypeError(
      "direct_derivation_support_steps must be a tuple"
    )

  for support_step in direct_derivation_support_steps:
    if not isinstance(
      support_step,
      ProofStep,
    ):
      raise TypeError(
        "direct_derivation_support_steps must contain only "
        "ProofStep objects"
      )

  if (
    context_hidden_step_ids is not None
"""
if validation_anchor not in body:
    raise RuntimeError("body validation anchor not found")
body = body.replace(validation_anchor, validation_replacement, 1)

reloc_anchor = """          _relocatable_toda_group_proof_narrative_direct_derivation_premises(
            direct_derivation_premises,
            step_derivation_sources_by_target_id,
"""
reloc_replacement = """          _relocatable_toda_group_proof_narrative_direct_derivation_premises(
            (
              direct_derivation_support_steps
              + direct_derivation_premises
            ),
            step_derivation_sources_by_target_id,
"""
if reloc_anchor not in body:
    raise RuntimeError("body relocation anchor not found")
body = body.replace(reloc_anchor, reloc_replacement, 1)

multi_path.write_text(multi, encoding="utf-8")
body_path.write_text(body, encoding="utf-8")

print("Phase 144-6 R17 applied.")
print("Production:")
print("  toda_group_proof_narrative_argument_multi_renderer.py")
print("  toda_group_proof_narrative_argument_body_renderer.py")
print("Tests: no additional changes beyond R16 numbering-contract updates.")
