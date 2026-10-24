from web_group_proof_common import (
    WebGroupProofStepView,
    WebGroupProofInlineSegmentView,
    WebGroupProofRenderedLineView,
    WebGroupProofView,
    _group_proof_rule_name,
    _group_proof_statement_latex,
    _split_group_proof_rendered_line,
    _build_group_proof_inline_segments,
    _build_group_proof_rendered_lines,
)

from dataclasses import dataclass

from toda_human_readable_renderer import (
  render_toda_public_group_relation_latex,
)
from toda_proof_narrative_renderer import (
  render_toda_proof_statement_latex,
)

from toda_group_query import TodaGroupQuery
from toda_group_query_semantics import TodaGroupQueryDomainKind
from toda_group_query_semantics import classify_toda_group_query_domain
