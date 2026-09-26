from pathlib import Path


ROOT = Path(__file__).resolve().parent.parent


def replace_once(path, old, new, label):
  text = path.read_text(encoding='utf-8')
  count = text.count(old)
  if count != 1:
    raise RuntimeError(
      f'{label}: expected exactly one match, found {count}'
    )
  path.write_text(text.replace(old, new, 1), encoding='utf-8')
  print(f'updated {path}')


def main():
  replace_once(
    ROOT / 'tests/test_phase143_51a_r_provenance_semantic_catalog.py',
    'def test_phase143_51a_r_pi8_5_suppresses_provenance_only_fallbacks():\n  rendered = _render_multi_argument(\n    5,\n    3,\n  )\n\n  for internal_name in (\n    "Toda Lemma 5.4 integration",\n    "Toda (5.6) nu_4 decomposition isomorphism semantics",\n  ):\n    assert internal_name not in rendered\n\n  assert (\n    "Toda Proposition 5.6 "\n    "pi_8^5 quotient by E^2 pi_6^3"\n    in rendered\n  )\n',
    'def test_phase143_51a_r_pi8_5_suppresses_provenance_only_fallbacks():\n  rendered = _render_multi_argument(\n    5,\n    3,\n  )\n\n  for internal_name in (\n    "Toda Lemma 5.4 integration",\n    "Toda (5.6) nu_4 decomposition isomorphism semantics",\n    (\n      "Toda Proposition 5.6 "\n      "pi_8^5 quotient by E^2 pi_6^3"\n    ),\n  ):\n    assert internal_name not in rendered\n\n  assert (\n    r"$\\pi_{8}^{5}/E^{2}\\left(\\pi_{6}^{3}\\right)"\n    r" \\cong \\mathbb{Z}/2$"\n    in rendered\n  )\n',
    '51A-R pi8_5',
  )
  replace_once(
    ROOT / 'tests/test_phase143_51a_r_provenance_semantic_catalog.py',
    'def test_phase143_51a_r_pi15_8_suppresses_provenance_only_fallbacks():\n  rendered = _render_multi_argument(\n    8,\n    7,\n  )\n\n  for internal_name in (\n    "Toda Proposition 5.15 sigma_8 "\n    "Proposition 4.4 specialization premises",\n    "Toda Lemma 5.14 sigma-prime branch",\n  ):\n    assert internal_name not in rendered\n\n  assert (\n    "Toda (5.14) second short exact sequence"\n    in rendered\n  )\n  assert (\n    "Toda Proposition 5.15 "\n    "sigma_8 transported decomposition"\n    in rendered\n  )\n',
    'def test_phase143_51a_r_pi15_8_suppresses_provenance_only_fallbacks():\n  rendered = _render_multi_argument(\n    8,\n    7,\n  )\n\n  for internal_name in (\n    "Toda Proposition 5.15 sigma_8 "\n    "Proposition 4.4 specialization premises",\n    "Toda Lemma 5.14 sigma-prime branch",\n    "Toda (5.14) second short exact sequence",\n    (\n      "Toda Proposition 5.15 "\n      "sigma_8 transported decomposition"\n    ),\n  ):\n    assert internal_name not in rendered\n\n  assert (\n    r"$0\\longrightarrow \\pi_{13}^{6}"\n    r"\\xrightarrow{E} \\pi_{14}^{7}"\n    r"\\xrightarrow{H} \\pi_{14}^{13}"\n    r"\\longrightarrow 0$"\n    in rendered\n  )\n  assert (\n    r"$\\pi_{15}^{8} \\cong "\n    r"\\mathbb{Z}/8\\{E\\sigma\'\\} "\n    r"\\oplus \\mathbb{Z}\\{\\sigma_{8}\\}$"\n    in rendered\n  )\n',
    '51A-R pi15_8',
  )
  replace_once(
    ROOT / 'tests/test_phase143_51a_r_provenance_semantic_catalog.py',
    'def test_phase143_51a_r_pi16_9_suppresses_provenance_only_fallbacks():\n  rendered = _render_multi_argument(\n    9,\n    7,\n  )\n\n  for internal_name in (\n    "Toda Lemma 5.14 sigma_8 branch",\n    "Toda Theorem 3.6 Lemma 5.14 "\n    "sigma double-prime bridge",\n    "Toda Lemma 5.14 sigma-prime branch",\n    "Toda Proposition 5.15 pi_12^5 Hopf isomorphism",\n    "Toda Lemma 5.13 sigma triple-prime definition",\n    "Toda Lemma 5.4 integration",\n    "Toda Proposition 5.11 finite-dimensional integration",\n    "Toda Proposition 5.8 finite-dimensional integration",\n    "Toda Lemma 5.14 sigma double-prime branch",\n  ):\n    assert internal_name not in rendered\n\n  assert (\n    "Toda (5.14) second short exact sequence"\n    in rendered\n  )\n  assert (\n    "Toda (4.8) pi_16^9 order sixteen and E4 injective"\n    in rendered\n  )\n',
    'def test_phase143_51a_r_pi16_9_suppresses_provenance_only_fallbacks():\n  rendered = _render_multi_argument(\n    9,\n    7,\n  )\n\n  for internal_name in (\n    "Toda Lemma 5.14 sigma_8 branch",\n    "Toda Theorem 3.6 Lemma 5.14 "\n    "sigma double-prime bridge",\n    "Toda Lemma 5.14 sigma-prime branch",\n    "Toda Proposition 5.15 pi_12^5 Hopf isomorphism",\n    "Toda Lemma 5.13 sigma triple-prime definition",\n    "Toda Lemma 5.4 integration",\n    "Toda Proposition 5.11 finite-dimensional integration",\n    "Toda Proposition 5.8 finite-dimensional integration",\n    "Toda Lemma 5.14 sigma double-prime branch",\n    "Toda (5.14) second short exact sequence",\n    "Toda (4.8) pi_16^9 order sixteen and E4 injective",\n  ):\n    assert internal_name not in rendered\n\n  assert (\n    r"$0\\longrightarrow \\pi_{13}^{6}"\n    r"\\xrightarrow{E} \\pi_{14}^{7}"\n    r"\\xrightarrow{H} \\pi_{14}^{13}"\n    r"\\longrightarrow 0$"\n    in rendered\n  )\n  assert (\n    r"$|\\pi_{16}^{9}| = 16$"\n    in rendered\n  )\n  assert (\n    r"$E^{4}: \\pi_{12}^{5} \\to \\pi_{16}^{9}$ は単射である."\n    in rendered\n  )\n',
    '51A-R pi16_9',
  )
  replace_once(
    ROOT / 'phase143_51A_impl/tests/test_phase143_51a_structured_fallback_and_provenance.py',
    'def test_phase143_51a_keeps_unhandled_aggregate_fallback_for_phase143_51b():\n  rendered = _render_multi_argument(\n    5,\n    3,\n  )\n\n  assert (\n    "Toda Proposition 5.6 "\n    "pi_8^5 quotient by E^2 pi_6^3"\n    in rendered\n  )\n',
    'def test_phase143_51a_aggregate_fallback_is_replaced_after_phase143_51b():\n  rendered = _render_multi_argument(\n    5,\n    3,\n  )\n\n  assert (\n    "Toda Proposition 5.6 "\n    "pi_8^5 quotient by E^2 pi_6^3"\n    not in rendered\n  )\n  assert (\n    r"$\\pi_{8}^{5}/E^{2}\\left(\\pi_{6}^{3}\\right)"\n    r" \\cong \\mathbb{Z}/2$"\n    in rendered\n  )\n',
    '51A aggregate boundary',
  )
  replace_once(
    ROOT / 'tests/test_phase143_50_generic_statement_prose_renderer.py',
    'def test_phase143_50_does_not_remove_internal_rule_fallback_yet():\n  rendered = _render_multi_argument(\n    5,\n    3,\n  )\n\n  assert (\n    "Toda Proposition 5.6 "\n    "pi_8^5 quotient by E^2 pi_6^3"\n    in rendered\n  )\n',
    'def test_phase143_50_structured_prose_remains_after_aggregate_rendering():\n  rendered = _render_multi_argument(\n    5,\n    3,\n  )\n\n  assert (\n    r"$E^{2}: \\pi_{6}^{3} \\to \\pi_{8}^{5}$ は単射である."\n    in rendered\n  )\n  assert (\n    r"$\\pi_{8}^{5}/E^{2}\\left(\\pi_{6}^{3}\\right)"\n    r" \\cong \\mathbb{Z}/2$"\n    in rendered\n  )\n',
    'Phase 50 post-51B contract',
  )


if __name__ == '__main__':
  main()
