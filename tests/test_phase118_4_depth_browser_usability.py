from pathlib import Path

import pytest

from web_app import (
  create_app,
)
from web_operation_query_proof import (
  build_standard_web_operation_query_proof_view,
)


def _build_test_client():
  app = create_app()
  app.config.update(
    TESTING=True,
  )
  return app.test_client()








def test_phase118_4_negative_depth_is_rejected_by_web_adapter():
  with pytest.raises(
    ValueError,
    match="max_depth must be nonnegative",
  ):
    build_standard_web_operation_query_proof_view(
      "H(nu_prime)",
      fact_number=1,
      max_depth=-1,
    )






def test_phase118_4_katex_smoke_targets_all_data_latex_elements():
  script = Path(
    "static/web_math.js"
  ).read_text(
    encoding="utf-8"
  )

  assert (
    'querySelectorAll(\n        "[data-latex]"'
    in script
  )

  assert (
    "throwOnError: false"
    in script
  )

  assert (
    "displayMode: displayMode"
    in script
  )
