from flask import (
  Flask,
  render_template,
  request,
)

from web_group_query import (
  WebGroupQueryView,
  build_standard_web_group_query_view,
)
from web_operation_query import (
  WebOperationQueryView,
  build_standard_web_operation_query_view,
)
from web_operation_query_proof import (
  WebOperationQueryProofView,
  build_standard_web_operation_query_proof_view,
)


def _parse_integer_form_value(
  value: str | None,
  field_name: str,
) -> int:
  if value is None or not value.strip():
    raise ValueError(
      f"{field_name} is required"
    )

  try:
    return int(
      value
    )
  except ValueError as error:
    raise ValueError(
      f"{field_name} must be an integer"
    ) from error


def create_app(
) -> Flask:
  app = Flask(
    __name__,
  )

  @app.route(
    "/",
    methods=(
      "GET",
      "POST",
    ),
  )
  def index(
  ) -> str:
    form_kind = request.form.get(
      "form_kind",
      "group",
    )

    n_value = request.form.get(
      "n",
      "",
    )
    k_value = request.form.get(
      "k",
      "",
    )
    operation_query_value = (
      request.form.get(
        "operation_query",
        "",
      )
    )
    proof_depth_value = request.form.get(
      "proof_depth",
      "1",
    )

    view: WebGroupQueryView | None = None
    operation_query_view: (
      WebOperationQueryView
      | None
    ) = None
    operation_query_proof_view: (
      WebOperationQueryProofView
      | None
    ) = None
    error_message: str | None = None

    if request.method == "POST":
      try:
        if form_kind == "operation":
          operation_query_view = (
            build_standard_web_operation_query_view(
              operation_query_value
            )
          )
        elif form_kind == "operation_proof":
          fact_number = (
            _parse_integer_form_value(
              request.form.get(
                "fact_number"
              ),
              "fact_number",
            )
          )
          proof_depth = (
            _parse_integer_form_value(
              proof_depth_value,
              "proof_depth",
            )
          )

          if proof_depth not in (
            0,
            1,
            2,
          ):
            raise ValueError(
              "proof_depth must be 0, 1, or 2"
            )

          operation_query_proof_view = (
            build_standard_web_operation_query_proof_view(
              operation_query_value,
              fact_number,
              max_depth=proof_depth,
            )
          )
        else:
          n = _parse_integer_form_value(
            n_value,
            "n",
          )
          k = _parse_integer_form_value(
            k_value,
            "k",
          )

          view = (
            build_standard_web_group_query_view(
              n=n,
              k=k,
            )
          )
      except (
        TypeError,
        ValueError,
      ) as error:
        error_message = str(
          error
        )

    return render_template(
      "index.html",
      n_value=n_value,
      k_value=k_value,
      operation_query_value=(
        operation_query_value
      ),
      proof_depth_value=(
        proof_depth_value
      ),
      view=view,
      operation_query_view=(
        operation_query_view
      ),
      operation_query_proof_view=(
        operation_query_proof_view
      ),
      error_message=error_message,
    )

  return app
