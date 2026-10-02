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


def test_phase117_2_web_and_cli_share_sigma11_result(
  capsys,
):
  client = _build_test_client()

  web_response = client.post(
    "/",
    data={
      "n": "11",
      "k": "7",
    },
  )

  cli_exit_code = cli_main.main(
    [
      "11",
      "7",
    ]
  )
  captured = capsys.readouterr()

  result_latex = (
    rb"\pi_{18}^{11} \cong "
    rb"\mathbb{Z}/16\{\sigma_{11}\}"
  )

  assert web_response.status_code == 200
  assert cli_exit_code == 0
  assert result_latex in web_response.data
  assert (
    result_latex.decode(
      "ascii"
    )
    in captured.out
  )


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


