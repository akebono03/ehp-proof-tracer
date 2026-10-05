from toda_calculation_facade import (
  build_standard_toda_report,
)
from toda_group_proof_generic_narrative_renderer import (
  _GENERIC_ISOMORPHISM_STATEMENT_TYPES,
  _render_generic_narrative_step,
)
from toda_group_proof_narrative_semantics import (
  build_toda_group_proof_narrative_semantic_closure_presentation,
)
from toda_group_proof_presentation import (
  build_toda_group_proof_presentation,
)
from toda_group_result_proof_replay import (
  build_toda_group_result_proof_replay,
)
from toda_rules import (
  TodaPi32Eta2DefinitionStatement,
)


def main() -> None:
  report = build_standard_toda_report(
    n=2,
    k=1,
  )
  group_result = (
    report.candidates[0]
    .source_candidate
    .group_result
  )
  replay = (
    build_toda_group_result_proof_replay(
      group_result,
      max_depth=2,
    )
  )
  presentation = (
    build_toda_group_proof_presentation(
      replay
    )
  )
  semantic_presentation = (
    build_toda_group_proof_narrative_semantic_closure_presentation(
      presentation
    )
  )

  definition_nodes = [
    node
    for node in semantic_presentation.nodes
    if isinstance(
      node.proof_step.conclusion,
      TodaPi32Eta2DefinitionStatement,
    )
  ]

  print(
    "definition_node_count=",
    len(
      definition_nodes
    ),
    sep="",
  )

  for node_index, node in enumerate(
    definition_nodes
  ):
    proof_step = node.proof_step
    statement = proof_step.conclusion

    print()
    print(
      "definition_node_index=",
      node_index,
      sep="",
    )
    print(
      "rendered=",
      _render_generic_narrative_step(
        proof_step
      ),
      sep="",
    )
    print(
      "statement_type=",
      type(
        statement
      ).__name__,
      sep="",
    )
    print(
      "definition_map_type=",
      type(
        getattr(
          statement,
          "map",
          None,
        )
      ).__name__,
      sep="",
    )
    print(
      "definition_map_repr=",
      repr(
        getattr(
          statement,
          "map",
          None,
        )
      ),
      sep="",
    )
    print(
      "definition_map_name=",
      repr(
        getattr(
          getattr(
            statement,
            "map",
            None,
          ),
          "name",
          None,
        )
      ),
      sep="",
    )
    print(
      "premise_count=",
      len(
        proof_step.premises
      ),
      sep="",
    )

    for premise_index, premise in enumerate(
      proof_step.premises
    ):
      print()
      print(
        "premise_index=",
        premise_index,
        sep="",
      )
      print(
        "premise_object_type=",
        type(
          premise
        ).__name__,
        sep="",
      )

      premise_conclusion = getattr(
        premise,
        "conclusion",
        None,
      )

      print(
        "premise_conclusion_type=",
        type(
          premise_conclusion
        ).__name__,
        sep="",
      )
      print(
        "premise_conclusion_repr=",
        repr(
          premise_conclusion
        ),
        sep="",
      )
      print(
        "is_generic_isomorphism=",
        isinstance(
          premise_conclusion,
          _GENERIC_ISOMORPHISM_STATEMENT_TYPES,
        ),
        sep="",
      )

      premise_map = getattr(
        premise_conclusion,
        "map",
        None,
      )

      print(
        "premise_map_type=",
        type(
          premise_map
        ).__name__,
        sep="",
      )
      print(
        "premise_map_repr=",
        repr(
          premise_map
        ),
        sep="",
      )
      print(
        "same_map=",
        premise_map
        == getattr(
          statement,
          "map",
          None,
        ),
        sep="",
      )

  print()
  print(
    "all_semantic_nodes_with_eta2_rendering="
  )

  for node_index, node in enumerate(
    semantic_presentation.nodes
  ):
    rendered = _render_generic_narrative_step(
      node.proof_step
    )

    if (
      "eta_{2}" in rendered
      or r"\eta_{2}" in rendered
      or "η₂" in rendered
    ):
      print(
        node_index,
        type(
          node.proof_step.conclusion
        ).__name__,
        repr(
          rendered
        ),
      )


if __name__ == "__main__":
  main()
