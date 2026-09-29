from pathlib import Path


def replace_once(
  text: str,
  old: str,
  new: str,
  label: str,
) -> str:
  if old not in text:
    raise RuntimeError(
      f"Phase 131-5 patch target not found: {label}"
    )

  return text.replace(
    old,
    new,
    1,
  )


def patch_web_group_query() -> None:
  path = Path(
    "web_group_query.py"
  )
  text = path.read_text(
    encoding="utf-8"
  )

  text = replace_once(
    text,
    """  result_latex: str | None

  def __post_init__(
""",
    """  result_latex: str | None
  proof_available: bool = False

  def __post_init__(
""",
    "WebGroupQueryView field",
  )

  text = replace_once(
    text,
    """    if (
      self.status
      is TodaCalculationStatus.FOUND
    ):
""",
    """    if not isinstance(
      self.proof_available,
      bool,
    ):
      raise TypeError(
        "proof_available must be a bool"
      )

    if (
      self.status
      is TodaCalculationStatus.FOUND
    ):
""",
    "WebGroupQueryView validation",
  )

  text = replace_once(
    text,
    """      result_latex=(
        render_toda_group_query_domain_latex(
          domain
        )
      ),
    )
""",
    """      result_latex=(
        render_toda_group_query_domain_latex(
          domain
        )
      ),
      proof_available=False,
    )
""",
    "domain-only view",
  )

  text = replace_once(
    text,
    """  return WebGroupQueryView(
    n=n,
    k=k,
    status=report.status,
    result_latex=result_latex,
  )
""",
    """  return WebGroupQueryView(
    n=n,
    k=k,
    status=report.status,
    result_latex=result_latex,
    proof_available=(
      report.status
      is TodaCalculationStatus.FOUND
    ),
  )
""",
    "repository-backed view",
  )

  path.write_text(
    text,
    encoding="utf-8",
  )


def patch_web_app() -> None:
  path = Path(
    "web_app.py"
  )
  text = path.read_text(
    encoding="utf-8"
  )

  text = replace_once(
    text,
    """from web_group_query import (
  WebGroupQueryView,
  build_standard_web_group_query_view,
)
""",
    """from web_group_proof import (
  WebGroupProofView,
  build_standard_web_group_proof_view,
)
from web_group_query import (
  WebGroupQueryView,
  build_standard_web_group_query_view,
)
""",
    "web_group_proof import",
  )

  text = replace_once(
    text,
    """    proof_depth_value = request.form.get(
      "proof_depth",
      "1",
    )
""",
    """    proof_depth_value = request.form.get(
      "proof_depth",
      "1",
    )
    group_proof_depth_value = request.form.get(
      "group_proof_depth",
      "1",
    )
""",
    "group proof depth value",
  )

  text = replace_once(
    text,
    """    operation_query_view: (
      WebOperationQueryView
      | None
    ) = None
""",
    """    group_proof_view: (
      WebGroupProofView
      | None
    ) = None
    operation_query_view: (
      WebOperationQueryView
      | None
    ) = None
""",
    "group proof view variable",
  )

  text = replace_once(
    text,
    """        if form_kind == "operation":
""",
    """        if form_kind == "group_proof":
          n = _parse_integer_form_value(
            n_value,
            "n",
          )
          k = _parse_integer_form_value(
            k_value,
            "k",
          )
          group_proof_depth = (
            _parse_integer_form_value(
              group_proof_depth_value,
              "group_proof_depth",
            )
          )

          if group_proof_depth not in (
            0,
            1,
            2,
          ):
            raise ValueError(
              "group_proof_depth must be 0, 1, or 2"
            )

          view = (
            build_standard_web_group_query_view(
              n=n,
              k=k,
            )
          )
          group_proof_view = (
            build_standard_web_group_proof_view(
              n,
              k,
              max_depth=group_proof_depth,
            )
          )
        elif form_kind == "operation":
""",
    "group proof POST branch",
  )

  text = replace_once(
    text,
    """      proof_depth_value=(
        proof_depth_value
      ),
""",
    """      proof_depth_value=(
        proof_depth_value
      ),
      group_proof_depth_value=(
        group_proof_depth_value
      ),
""",
    "group proof depth template value",
  )

  text = replace_once(
    text,
    """      view=view,
      operation_query_view=(
""",
    """      view=view,
      group_proof_view=(
        group_proof_view
      ),
      operation_query_view=(
""",
    "group proof template view",
  )

  path.write_text(
    text,
    encoding="utf-8",
  )


def patch_template() -> None:
  path = Path(
    "templates/index.html"
  )
  text = path.read_text(
    encoding="utf-8"
  )

  old = """          <div
            id="result-math"
            data-latex="{{ view.result_latex }}"
          >{{ view.result_latex }}</div>
        </section>
"""

  new = """          <div
            id="result-math"
            data-latex="{{ view.result_latex }}"
          >{{ view.result_latex }}</div>

          {% if view.proof_available %}
            <form method="post">
              <input
                type="hidden"
                name="form_kind"
                value="group_proof"
              >
              <input
                type="hidden"
                name="n"
                value="{{ view.n }}"
              >
              <input
                type="hidden"
                name="k"
                value="{{ view.k }}"
              >

              <label>
                Proof depth
                <select name="group_proof_depth">
                  <option
                    value="0"
                    {% if group_proof_depth_value == "0" %}selected{% endif %}
                  >0</option>
                  <option
                    value="1"
                    {% if group_proof_depth_value == "1" %}selected{% endif %}
                  >1</option>
                  <option
                    value="2"
                    {% if group_proof_depth_value == "2" %}selected{% endif %}
                  >2</option>
                </select>
              </label>

              <button type="submit">
                Show proof
              </button>
            </form>
          {% endif %}
        </section>
"""

  text = replace_once(
    text,
    old,
    new,
    "group result proof form",
  )

  anchor = """    {% if operation_query_view %}
"""

  proof_section = """    {% if group_proof_view %}
      <section
        aria-labelledby="group-proof-heading"
      >
        <h2 id="group-proof-heading">
          Group proof
        </h2>

        <p>
          Selected depth:
          {{ group_proof_view.max_depth }}
        </p>

        <h3>
          Conclusion
        </h3>

        <div
          id="group-proof-conclusion"
          data-latex="{{ group_proof_view.conclusion_latex }}"
        >{{ group_proof_view.conclusion_latex }}</div>

        <h3>
          Provenance
        </h3>

        <p>
          {% if group_proof_view.theorem %}
            {{ group_proof_view.theorem }}
            {% if group_proof_view.phase %}
              — Phase {{ group_proof_view.phase }}
            {% endif %}
          {% else %}
            {{ group_proof_view.key }}
          {% endif %}
        </p>

        <h3>
          Proof
        </h3>

        <ol>
          {% for step in group_proof_view.steps %}
            <li class="group-proof-step">
              <p>
                Depth {{ step.depth }}
              </p>

              {% if step.statement_latex %}
                <div
                  class="group-proof-step-math"
                  data-latex="{{ step.statement_latex }}"
                >{{ step.statement_latex }}</div>
              {% else %}
                <p>
                  <code>
                    {{ step.fallback_type_name }}
                  </code>
                </p>
              {% endif %}

              <p>
                Role:
                {{ step.role_name }}
              </p>

              <p>
                Rule:
                {{ step.rule_name }}
              </p>
            </li>
          {% endfor %}
        </ol>
      </section>
    {% endif %}

"""

  text = replace_once(
    text,
    anchor,
    proof_section + anchor,
    "group proof result section",
  )

  path.write_text(
    text,
    encoding="utf-8",
  )


def main() -> None:
  patch_web_group_query()
  patch_web_app()
  patch_template()

  print(
    "Phase 131-5 Web group-proof patch applied."
  )


if __name__ == "__main__":
  main()
