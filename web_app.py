from flask import (
  Flask,
  render_template,
  request,
)

from web_group_query import (
  WebGroupQueryView,
  build_standard_web_group_query_view,
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
    n_value = request.form.get(
      "n",
      "",
    )
    k_value = request.form.get(
      "k",
      "",
    )

    view: WebGroupQueryView | None = None
    error_message: str | None = None

    if request.method == "POST":
      try:
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
      view=view,
      error_message=error_message,
    )

  return app
