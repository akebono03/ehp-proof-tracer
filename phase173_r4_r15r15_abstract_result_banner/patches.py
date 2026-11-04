"""Minimal status-driven Web presentation patch, no mathematical inference."""
from __future__ import annotations


COMMON_FIELD = "  partial_result: bool = False\n"
COMMON_FIELD_NEW = (
    "  partial_result: bool = False\n"
    "  abstract_structure_certified: bool = False\n"
)
COMMON_GUARD = (
    '    if not isinstance(self.partial_result, bool):\n'
    '      raise TypeError("partial_result must be a bool")\n'
)
COMMON_GUARD_NEW = COMMON_GUARD + (
    '\n'
    '    if not isinstance(self.abstract_structure_certified, bool):\n'
    '      raise TypeError("abstract_structure_certified must be a bool")\n'
    '\n'
    '    if self.abstract_structure_certified and not self.partial_result:\n'
    '      raise ValueError("abstract certificate cannot mark a complete named proof")\n'
)
ADAPTER_ANCHOR = (
    '        partial_result=(result.status is not ProofSearchStatus.COMPLETE),\n'
)
ADAPTER_REPLACEMENT = ADAPTER_ANCHOR + (
    '        abstract_structure_certified=(result.abstract_structure is not None),\n'
)
TEMPLATE_ANCHOR = '''      {% elif view.status.value == "not_found" %}
        {% if group_proof_view and not group_proof_view.partial_result %}
          <p>Typed proof search completed. See Group proof below.</p>
        {% else %}
        <p>
          No proof-backed result found for this query.
        </p>
        {% endif %}
'''
TEMPLATE_REPLACEMENT = '''      {% elif view.status.value == "not_found" %}
        {% if group_proof_view and not group_proof_view.partial_result %}
          <p>Typed proof search completed. See Group proof below.</p>
        {% elif group_proof_view and group_proof_view.abstract_structure_certified %}
          <p>
            A verified abstract group structure is available, but the
            named-generator proof is incomplete. See Group proof below.
          </p>
        {% else %}
          <p>No proof-backed result found for this query.</p>
        {% endif %}
'''


def _replace_once(source: str, old: str, new: str, path: str) -> str:
    if not isinstance(source, str):
        raise TypeError(f"{path}: source must be str")
    count = source.count(old)
    if count != 1:
        raise ValueError(f"{path}: reviewed anchor mismatch (count={count})")
    if new in source:
        raise ValueError(f"{path}: patch already present")
    return source.replace(old, new, 1)


def patch_common(source: str) -> str:
    """Add an explicit evidence flag to the existing Web view contract."""
    output = _replace_once(source, COMMON_FIELD, COMMON_FIELD_NEW, "web_group_proof_common.py")
    return _replace_once(output, COMMON_GUARD, COMMON_GUARD_NEW, "web_group_proof_common.py")


def patch_adapter(source: str) -> str:
    """Project the already-verified certificate from PartialProofResult."""
    return _replace_once(source, ADAPTER_ANCHOR, ADAPTER_REPLACEMENT,
                         "phase165_r52_r3_web_adapter.py")


def patch_template(source: str) -> str:
    """Display the three distinct existing proof states, with no source inference."""
    return _replace_once(source, TEMPLATE_ANCHOR, TEMPLATE_REPLACEMENT,
                         "templates/index.html")


TRANSFORMERS = {
    "web_group_proof_common.py": patch_common,
    "phase165_r52_r3_web_adapter.py": patch_adapter,
    "templates/index.html": patch_template,
}
