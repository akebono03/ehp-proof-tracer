from collections import Counter

from audit_phase144_6_r5_43_6 import (
  build_hidden_bridge_inventory,
)
from test_phase144_6_r5_18_production_generic_proof_chain_foundation import (
  TARGETS,
  _context,
)
from toda_group_proof_narrative_hidden_bridge_semantics import (
  TodaGroupProofNarrativeHiddenBridgeSemanticRole,
  build_toda_group_proof_narrative_hidden_bridge_semantics,
)


_EXPECTED_ROLE_BY_AUDIT_CLASSIFICATION = {
  "transport_candidate": (
    TodaGroupProofNarrativeHiddenBridgeSemanticRole
    .TRANSPORT
  ),
  "integration_provenance_candidate": (
    TodaGroupProofNarrativeHiddenBridgeSemanticRole
    .INTEGRATION_PROVENANCE
  ),
}


def _semantic_by_signature():
  result = {}

  for n, k in TARGETS:
    presentation = _context(
      n,
      k,
    )[0]
    semantics = (
      build_toda_group_proof_narrative_hidden_bridge_semantics(
        presentation
      )
    )

    for semantic in semantics:
      rule = (
        semantic.proof_step.inference_rule
      )
      rule_name = (
        None
        if rule is None
        else rule.name
      )
      key = (
        type(
          semantic.proof_step.conclusion
        ).__name__,
        rule_name,
      )
      existing = result.get(
        key
      )

      if (
        existing is not None
        and existing is not semantic.role
      ):
        raise AssertionError(
          "semantic signature has conflicting roles"
        )

      result[
        key
      ] = semantic.role

  return result


def test_phase144_6_r5_43_7_reproduces_all_r5_43_6_hidden_bridge_signatures():
  audit_rows = (
    build_hidden_bridge_inventory()
  )
  semantic_by_signature = (
    _semantic_by_signature()
  )

  assert len(
    audit_rows
  ) == 64

  for row in audit_rows:
    signature = (
      row[
        "statement_type"
      ],
      row[
        "rule_name"
      ],
    )
    assert (
      semantic_by_signature[
        signature
      ]
      is _EXPECTED_ROLE_BY_AUDIT_CLASSIFICATION[
        row[
          "classification"
        ]
      ]
    )


def test_phase144_6_r5_43_7_r5_43_6_population_has_two_semantic_roles():
  audit_rows = (
    build_hidden_bridge_inventory()
  )
  semantic_by_signature = (
    _semantic_by_signature()
  )
  actual = Counter(
    semantic_by_signature[
      (
        row[
          "statement_type"
        ],
        row[
          "rule_name"
        ],
      )
    ]
    for row in audit_rows
  )

  assert actual == {
    (
      TodaGroupProofNarrativeHiddenBridgeSemanticRole
      .TRANSPORT
    ): 48,
    (
      TodaGroupProofNarrativeHiddenBridgeSemanticRole
      .INTEGRATION_PROVENANCE
    ): 16,
  }


def test_phase144_6_r5_43_7_builder_returns_deterministic_presentation_order():
  for n, k in TARGETS:
    presentation = _context(
      n,
      k,
    )[0]
    first = (
      build_toda_group_proof_narrative_hidden_bridge_semantics(
        presentation
      )
    )
    second = (
      build_toda_group_proof_narrative_hidden_bridge_semantics(
        presentation
      )
    )
    node_position = {
      id(
        node.proof_step
      ): index
      for index, node in enumerate(
        presentation.nodes
      )
    }

    assert tuple(
      id(
        semantic.proof_step
      )
      for semantic in first
    ) == tuple(
      id(
        semantic.proof_step
      )
      for semantic in second
    )
    assert tuple(
      node_position[
        id(
          semantic.proof_step
        )
      ]
      for semantic in first
    ) == tuple(
      sorted(
        node_position[
          id(
            semantic.proof_step
          )
        ]
        for semantic in first
      )
    )


def test_phase144_6_r5_43_7_production_module_does_not_import_audit_modules():
  import inspect
  import toda_group_proof_narrative_hidden_bridge_semantics as module

  source = inspect.getsource(
    module
  )

  assert "from audit_" not in source
  assert "import audit_" not in source


def test_phase144_6_r5_43_7_public_route_remains_unchanged_after_r5_43_10():
  import inspect
  import toda_group_proof_narrative_contribution_renderer as renderer

  renderer_source = inspect.getsource(
    renderer
  )

  assert (
    "toda_group_proof_narrative_hidden_bridge_semantics"
    in renderer_source
  )
  assert "inference_rule" not in renderer_source
  assert "n == 3" not in renderer_source
  assert "k == 3" not in renderer_source
