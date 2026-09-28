from proof import (
  ProofRule,
  ProofStep,
)
from toda_group_proof_narrative_argument_body_renderer import (
  render_toda_group_proof_narrative_argument_body_markdown,
)
from toda_group_proof_narrative_blocks import (
  TodaGroupProofNarrativeBlock,
  TodaGroupProofNarrativeMathematicalBlockRole,
)
from toda_group_proof_presentation import (
  TodaGroupProofPresentation,
  TodaGroupProofPresentationNode,
)
from toda_rules import (
  Relation,
)


def _step(
  left,
  right,
  premises=(),
):
  return ProofStep(
    conclusion=Relation(
      left=left,
      right=right,
    ),
    premises=premises,
    rule=ProofRule.INFERENCE,
  )


def test_phase144_6_r25_9a_r1_hidden_relocated_premise_stays_hidden():
  hidden_support = _step(
    "hidden-support",
    "0",
  )
  direct_premise = _step(
    "direct-premise",
    "0",
    premises=(
      hidden_support,
    ),
  )
  conclusion = _step(
    "conclusion",
    "0",
    premises=(
      direct_premise,
    ),
  )

  support_block = TodaGroupProofNarrativeBlock(
    role=(
      TodaGroupProofNarrativeMathematicalBlockRole
      .CALCULATION
    ),
    steps=(
      hidden_support,
    ),
  )
  premise_block = TodaGroupProofNarrativeBlock(
    role=(
      TodaGroupProofNarrativeMathematicalBlockRole
      .CALCULATION
    ),
    steps=(
      direct_premise,
    ),
  )
  conclusion_block = TodaGroupProofNarrativeBlock(
    role=(
      TodaGroupProofNarrativeMathematicalBlockRole
      .CALCULATION
    ),
    steps=(
      conclusion,
    ),
  )
  blocks = (
    support_block,
    premise_block,
    conclusion_block,
  )

  presentation = TodaGroupProofPresentation(
    nodes=tuple(
      TodaGroupProofPresentationNode(
        depth=index,
        proof_step=step,
        role="test",
      )
      for index, step in enumerate(
        (
          conclusion,
          direct_premise,
          hidden_support,
        )
      )
    ),
    edges=(),
  )

  rendered = (
    render_toda_group_proof_narrative_argument_body_markdown(
      presentation,
      blocks,
      blocks,
      None,
      connector_before_block_id=id(
        conclusion_block
      ),
      connector_text="したがって、",
      conclusion_step=conclusion,
      direct_derivation_premises=(
        direct_premise,
      ),
      direct_derivation_support_steps=(
        hidden_support,
      ),
      context_hidden_step_ids=frozenset(
        {
          id(
            hidden_support
          ),
        }
      ),
    )
  )

  assert "hidden-support" not in rendered
  assert "direct-premise" in rendered
  assert "conclusion" in rendered
