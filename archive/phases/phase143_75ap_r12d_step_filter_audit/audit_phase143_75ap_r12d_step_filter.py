from pathlib import Path
import runpy

import toda_group_proof_narrative_argument_body_renderer as body
import toda_group_proof_narrative_argument_multi_renderer as multi

TARGET = "Toda515Sigma8TransportedDecompositionStatement"

original_redundant = (
  body.extract_toda_group_structure_narrative_redundant_direct_premise_step_ids
)
original_relocatable = (
  body._relocatable_toda_group_proof_narrative_direct_derivation_premises
)
original_body = (
  multi.render_toda_group_proof_narrative_argument_body_markdown
)

last_redundant_ids = frozenset()
last_relocated_ids = frozenset()


def statement_name(
  step,
):
  return type(
    step.conclusion
  ).__name__


def traced_redundant(
  conclusion_step,
):
  global last_redundant_ids
  result = original_redundant(
    conclusion_step
  )
  last_redundant_ids = frozenset(
    result
  )
  return result


def traced_relocatable(
  *args,
  **kwargs,
):
  global last_relocated_ids
  result = original_relocatable(
    *args,
    **kwargs,
  )
  last_relocated_ids = frozenset(
    id(
      step
    )
    for step in result
  )
  return result


body.extract_toda_group_structure_narrative_redundant_direct_premise_step_ids = (
  traced_redundant
)
body._relocatable_toda_group_proof_narrative_direct_derivation_premises = (
  traced_relocatable
)


def traced_body(
  *args,
  **kwargs,
):
  local_body_blocks = (
    args[
      2
    ]
    if len(
      args
    ) >= 3
    else kwargs.get(
      "local_body_blocks",
      (),
    )
  )
  context_hidden = kwargs.get(
    "context_hidden_step_ids",
  )
  direct_premises = kwargs.get(
    "direct_derivation_premises",
    (),
  )
  conclusion_step = kwargs.get(
    "conclusion_step",
  )

  target_steps = [
    step
    for block in local_body_blocks
    for step in block.steps
    if statement_name(
      step
    ) == TARGET
  ]

  if target_steps:
    print(
      "=" * 78
    )
    print(
      "TARGET STEP FILTER AUDIT"
    )
    print(
      "=" * 78
    )
    print(
      "context_hidden_step_ids:",
      context_hidden
    )
    print(
      "direct premise ids:",
      [
        id(
          step
        )
        for step in direct_premises
      ],
    )
    print(
      "direct premise types:",
      [
        statement_name(
          step
        )
        for step in direct_premises
      ],
    )
    print(
      "conclusion step id:",
      (
        None
        if conclusion_step is None
        else id(
          conclusion_step
        )
      ),
    )
    print(
      "conclusion type:",
      (
        None
        if conclusion_step is None
        else statement_name(
          conclusion_step
        )
      ),
    )

    # Run the real function first. The wrappers above capture the
    # redundant/relocatable results produced during that execution.
    result = original_body(
      *args,
      **kwargs,
    )

    for step in target_steps:
      step_id = id(
        step
      )
      print(
        "\ntarget step id:",
        step_id
      )
      print(
        "target in context_hidden:",
        (
          context_hidden is not None
          and step_id in context_hidden
        )
      )
      print(
        "target in redundant_direct_premise:",
        step_id in last_redundant_ids
      )
      print(
        "target in relocatable result:",
        step_id in last_relocated_ids
      )

    print(
      "captured redundant ids:",
      last_redundant_ids
    )
    print(
      "captured relocatable ids:",
      last_relocated_ids
    )
    return result

  return original_body(
    *args,
    **kwargs,
  )


multi.render_toda_group_proof_narrative_argument_body_markdown = (
  traced_body
)

test_globals = runpy.run_path(
  str(
    Path(
      "tests/test_phase143_51b_aggregate_statement_prose.py"
    )
  )
)
render = test_globals[
  "_render_multi_argument"
]
rendered = render(
  8,
  7,
)

print(
  "\nTARGET LATEX PRESENT:",
  r"$\pi_{15}^{8} \cong " in rendered,
)
