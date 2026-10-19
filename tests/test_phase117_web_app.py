import main as cli_main
import web_app as web_app_module

from toda_calculation_result import (
  TodaCalculationStatus,
)
from web_app import (
  create_app,
)
from web_group_query import (
  WebGroupQueryView,
)


def _build_test_client():
  app = create_app()
  app.config.update(
    TESTING=True,
  )
  return app.test_client()




def test_phase117_2_multiple_results_are_not_auto_selected(
  monkeypatch,
):
  def fake_build_standard_web_group_query_view(
    n: int,
    k: int,
  ) -> WebGroupQueryView:
    assert n == 11
    assert k == 7

    return WebGroupQueryView(
      n=n,
      k=k,
      status=(
        TodaCalculationStatus
        .MULTIPLE_RESULTS
      ),
      result_latex=None,
    )

  monkeypatch.setattr(
    web_app_module,
    "build_standard_web_group_query_view",
    fake_build_standard_web_group_query_view,
  )

  client = _build_test_client()

  response = client.post(
    "/",
    data={
      "n": "11",
      "k": "7",
    },
  )

  assert response.status_code == 200
  assert (
    b"Multiple proof-backed results were found."
    in response.data
  )
  assert (
    b'id="result-math"'
    not in response.data
  )


