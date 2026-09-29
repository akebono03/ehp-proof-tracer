from pathlib import Path

TARGET = Path("toda_group_proof_narrative_argument_renderer.py")

OLD = r'''def render_toda_group_proof_narrative_argument_header_method_section(
  argument: TodaGroupProofNarrativeArgument,
  discourse_role: TodaGroupProofNarrativeArgumentDiscourseRole,
  primary_component: (
    TodaGroupProofNarrativeExactnessMethodComponent
    | None
  ),
) -> str:
  if not isinstance(
    argument,
    TodaGroupProofNarrativeArgument,
  ):
    raise TypeError(
      "argument must be a "
      "TodaGroupProofNarrativeArgument"
    )

  if not isinstance(
    discourse_role,
    TodaGroupProofNarrativeArgumentDiscourseRole,
  ):
    raise TypeError(
      "discourse_role must be a "
      "TodaGroupProofNarrativeArgumentDiscourseRole"
    )

  if (
    primary_component is not None
    and not isinstance(
      primary_component,
      TodaGroupProofNarrativeExactnessMethodComponent,
    )
  ):
    raise TypeError(
      "primary_component must be a "
      "TodaGroupProofNarrativeExactnessMethodComponent "
      "or None"
    )

  marker = (
    render_toda_group_proof_narrative_argument_discourse_marker(
      discourse_role
    )
  )
  purpose = (
    render_toda_group_proof_narrative_argument_purpose_sentence(
      argument
    )
  )

  lines = []

  if purpose is not None:
    lines.append(
      marker
      + purpose
    )

  transition = (
    render_toda_group_proof_narrative_exactness_method_transition(
      primary_component
    )
  )

  if transition is not None:
    if lines:
      lines[
        -1
      ] += (
        transition
      )
    else:
      lines.append(
        transition
      )

    lines.append(
      ""
    )
    lines.append(
      "$"
      + render_toda_group_proof_narrative_exactness_method_component_latex(
        primary_component
      )
      + "$"
    )

  return "\n".join(
    lines
  )
'''

NEW = r'''def render_toda_group_proof_narrative_argument_header_method_section(
  argument: TodaGroupProofNarrativeArgument,
  discourse_role: TodaGroupProofNarrativeArgumentDiscourseRole,
  primary_component: (
    TodaGroupProofNarrativeExactnessMethodComponent
    | None
  ),
) -> str:
  if not isinstance(
    argument,
    TodaGroupProofNarrativeArgument,
  ):
    raise TypeError(
      "argument must be a "
      "TodaGroupProofNarrativeArgument"
    )

  if not isinstance(
    discourse_role,
    TodaGroupProofNarrativeArgumentDiscourseRole,
  ):
    raise TypeError(
      "discourse_role must be a "
      "TodaGroupProofNarrativeArgumentDiscourseRole"
    )

  if (
    primary_component is not None
    and not isinstance(
      primary_component,
      TodaGroupProofNarrativeExactnessMethodComponent,
    )
  ):
    raise TypeError(
      "primary_component must be a "
      "TodaGroupProofNarrativeExactnessMethodComponent "
      "or None"
    )

  marker = (
    render_toda_group_proof_narrative_argument_discourse_marker(
      discourse_role
    )
  )
  purpose = (
    render_toda_group_proof_narrative_argument_purpose_sentence(
      argument
    )
  )
  transition = (
    render_toda_group_proof_narrative_exactness_method_transition(
      primary_component
    )
  )

  lines = []

  if (
    purpose is not None
    and transition is not None
    and purpose.endswith(
      "する."
    )
    and transition.startswith(
      "そのために、"
    )
  ):
    lines.append(
      marker
      + purpose[
        :-len(
          "する."
        )
      ]
      + "するために、"
      + transition[
        len(
          "そのために、"
        ):
      ]
    )
  elif purpose is not None:
    lines.append(
      marker
      + purpose
    )

    if transition is not None:
      lines[
        -1
      ] += (
        transition
      )
  elif transition is not None:
    lines.append(
      transition
    )

  if transition is not None:
    lines.append(
      ""
    )
    lines.append(
      "$"
      + render_toda_group_proof_narrative_exactness_method_component_latex(
        primary_component
      )
      + "$"
    )

  return "\n".join(
    lines
  )
'''

def main():
    text=TARGET.read_text(encoding="utf-8")
    if NEW in text:
        print("Phase 146-7 production change already applied.")
        return
    if OLD not in text:
        raise SystemExit("Expected current function not found; repository may have changed.")
    TARGET.write_text(text.replace(OLD,NEW),encoding="utf-8")
    print("Phase 146-7 production change applied.")
    print("Changed: toda_group_proof_narrative_argument_renderer.py")
    print("Function: render_toda_group_proof_narrative_argument_header_method_section")

if __name__=="__main__":
    main()
