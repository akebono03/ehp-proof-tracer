from toda_group_proof_narrative_contribution_renderer import (
  normalize_toda_group_proof_narrative_connectors,
)


def test_phase159_exactness_connector_normalization_drops_redundant_koreyori():
  markdown = (
    "$\\pi_{4}^{5}=0$.\n\n"
    "これより,\n\n"
    "この完全性と $\\pi_{4}^{5}=0$ より, "
    "$\\operatorname{Im}E=\\ker H=\\pi_{4}^{3}$.\n\n"
    "$E: \\pi_{3}^{2} \\to \\pi_{4}^{3}$ は全射."
  )

  rendered = (
    normalize_toda_group_proof_narrative_connectors(
      markdown
    )
  )

  assert (
    "これより, この完全性と "
    not in rendered
  )
  assert (
    "この完全性と $\\pi_{4}^{5}=0$ より, "
    "$\\operatorname{Im}E=\\ker H=\\pi_{4}^{3}$."
    in rendered
  )


def test_phase159_exactness_connector_normalization_keeps_ordinary_koreyori():
  markdown = (
    "$\\Delta(\\iota_{5})=\\pm2\\eta_{2}$.\n\n"
    "これより,\n\n"
    "$\\operatorname{Im}\\Delta="
    "\\mathbb{Z}\\{2\\eta_{2}\\}$."
  )

  rendered = (
    normalize_toda_group_proof_narrative_connectors(
      markdown
    )
  )

  assert (
    "これより, "
    "$\\operatorname{Im}\\Delta="
    "\\mathbb{Z}\\{2\\eta_{2}\\}$."
    in rendered
  )


def test_phase159_exactness_connector_normalization_drops_before_kanzensei_yori():
  markdown = (
    "$\\operatorname{Im}\\Delta="
    "\\mathbb{Z}\\{2\\eta_{2}\\}$.\n\n"
    "これより,\n\n"
    "完全性より, "
    "$\\ker E=\\operatorname{Im}\\Delta="
    "\\mathbb{Z}\\{2\\eta_{2}\\}$."
  )

  rendered = (
    normalize_toda_group_proof_narrative_connectors(
      markdown
    )
  )

  assert (
    "これより, 完全性より,"
    not in rendered
  )
  assert (
    "完全性より, "
    "$\\ker E=\\operatorname{Im}\\Delta="
    "\\mathbb{Z}\\{2\\eta_{2}\\}$."
    in rendered
  )
