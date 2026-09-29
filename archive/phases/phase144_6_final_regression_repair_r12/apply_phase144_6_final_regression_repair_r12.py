from pathlib import Path

ROOT = Path.cwd()

body_path = ROOT / "toda_group_proof_narrative_argument_body_renderer.py"
body = body_path.read_text(encoding="utf-8-sig")

old_sig = """  excluded_non_exact_block_ids: (
    frozenset[
      int
    ]
    | None
  ) = None,
  excluded_exactness_contribution_keys: (
"""
new_sig = """  excluded_non_exact_block_ids: (
    frozenset[
      int
    ]
    | None
  ) = None,
  excluded_non_exact_step_ids: (
    frozenset[
      int
    ]
    | None
  ) = None,
  excluded_exactness_contribution_keys: (
"""
if old_sig not in body:
    raise RuntimeError("body renderer signature anchor not found")
body = body.replace(old_sig, new_sig, 1)

old_validation = """  if (
    excluded_exactness_contribution_keys is not None
    and not isinstance(
      excluded_exactness_contribution_keys,
      frozenset,
    )
  ):
"""
new_validation = """  if (
    excluded_non_exact_step_ids is not None
    and not isinstance(
      excluded_non_exact_step_ids,
      frozenset,
    )
  ):
    raise TypeError(
      "excluded_non_exact_step_ids must be "
      "a frozenset or None"
    )

  if excluded_non_exact_step_ids is not None:
    for step_id in excluded_non_exact_step_ids:
      if (
        not isinstance(
          step_id,
          int,
        )
        or isinstance(
          step_id,
          bool,
        )
      ):
        raise TypeError(
          "excluded_non_exact_step_ids must contain "
          "only integers"
        )

  if (
    excluded_exactness_contribution_keys is not None
    and not isinstance(
      excluded_exactness_contribution_keys,
      frozenset,
    )
  ):
"""
if old_validation not in body:
    raise RuntimeError("body renderer validation anchor not found")
body = body.replace(old_validation, new_validation, 1)

old_display = """      display_steps = tuple(
        proof_step
        for proof_step in block.steps
        if (
          (
            context_hidden_step_ids is None
            or id(
              proof_step
            ) not in context_hidden_step_ids
          )
"""
new_display = """      display_steps = tuple(
        proof_step
        for proof_step in block.steps
        if (
          (
            excluded_non_exact_step_ids is None
            or id(
              proof_step
            ) not in excluded_non_exact_step_ids
          )
          and (
            context_hidden_step_ids is None
            or id(
              proof_step
            ) not in context_hidden_step_ids
          )
"""
if old_display not in body:
    raise RuntimeError("body renderer display-step anchor not found")
body = body.replace(old_display, new_display, 1)

body_path.write_text(body, encoding="utf-8")
print("Updated production body renderer:", body_path)

multi_path = ROOT / "toda_group_proof_narrative_argument_multi_renderer.py"
multi = multi_path.read_text(encoding="utf-8-sig")

multi = multi.replace(
    "  seen_non_exact_block_ids = set()\n  seen_exactness_contribution_keys = set()\n",
    "  seen_non_exact_block_ids = set()\n  seen_non_exact_step_ids = set()\n  seen_exactness_contribution_keys = set()\n",
    1,
)

old_call = """        excluded_non_exact_block_ids=frozenset(
          seen_non_exact_block_ids
        ),
        excluded_exactness_contribution_keys=frozenset(
"""
new_call = """        excluded_non_exact_block_ids=frozenset(
          seen_non_exact_block_ids
        ),
        excluded_non_exact_step_ids=frozenset(
          seen_non_exact_step_ids
        ),
        excluded_exactness_contribution_keys=frozenset(
"""
if old_call not in multi:
    raise RuntimeError("multi renderer body-call anchor not found")
multi = multi.replace(old_call, new_call, 1)

old_seen_r10 = """    for block in local_body_blocks:
      if (
        block.role
        is not TodaGroupProofNarrativeMathematicalBlockRole
        .EXACTNESS
      ):
        if not any(
          id(
            proof_step
          ) in context_hidden_step_ids
          for proof_step in block.steps
        ):
          seen_non_exact_block_ids.add(
            id(
              block
            )
          )
        continue
"""
old_seen_base = """    for block in local_body_blocks:
      if (
        block.role
        is not TodaGroupProofNarrativeMathematicalBlockRole
        .EXACTNESS
      ):
        seen_non_exact_block_ids.add(
          id(
            block
          )
        )
        continue
"""
new_seen = """    for block in local_body_blocks:
      if (
        block.role
        is not TodaGroupProofNarrativeMathematicalBlockRole
        .EXACTNESS
      ):
        visible_step_ids = {
          id(
            proof_step
          )
          for proof_step in block.steps
          if id(
            proof_step
          ) not in context_hidden_step_ids
        }
        seen_non_exact_step_ids.update(
          visible_step_ids
        )

        if (
          len(
            visible_step_ids
          )
          == len(
            block.steps
          )
        ):
          seen_non_exact_block_ids.add(
            id(
              block
            )
          )
        continue
"""
if old_seen_r10 in multi:
    multi = multi.replace(old_seen_r10, new_seen, 1)
elif old_seen_base in multi:
    multi = multi.replace(old_seen_base, new_seen, 1)
else:
    raise RuntimeError("multi renderer seen anchor not found")

multi_path.write_text(multi, encoding="utf-8")
print("Updated production multi renderer:", multi_path)
