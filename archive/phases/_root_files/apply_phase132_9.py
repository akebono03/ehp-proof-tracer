from pathlib import Path
import shutil


ROOT = Path(__file__).resolve().parent
WEB_GROUP_PROOF_PATH = ROOT / "web_group_proof.py"
WEB_APP_PATH = ROOT / "web_app.py"
TEMPLATE_PATH = ROOT / "templates" / "index.html"


def replace_exact(
  text: str,
  old: str,
  new: str,
  label: str,
) -> str:
  count = text.count(old)

  if count != 1:
    raise RuntimeError(
      f"{label}: expected exactly one match, found {count}"
    )

  return text.replace(old, new, 1)


def backup_once(
  path: Path,
) -> None:
  backup = path.with_name(
    path.name + ".phase132_9_backup"
  )

  if not backup.exists():
    shutil.copy2(
      path,
      backup,
    )


def patch_web_group_proof() -> None:
  backup_once(
    WEB_GROUP_PROOF_PATH
  )

  text = WEB_GROUP_PROOF_PATH.read_text(
    encoding="utf-8",
  )

  old_imports = '''from toda_group_result_proof_replay import (
  build_toda_group_result_proof_replay,
)
from toda_proof_narrative_renderer import (
  render_toda_proof_statement_latex,
)
'''

  new_imports = '''from toda_group_proof_narrative_renderer import (
  render_toda_group_proof_narrative_markdown,
)
from toda_group_proof_outline_renderer import (
  render_toda_group_proof_outline_markdown,
)
from toda_group_proof_presentation import (
  build_toda_group_proof_presentation,
)
from toda_group_result_proof_replay import (
  build_toda_group_result_proof_replay,
)
from toda_proof_narrative_renderer import (
  render_toda_proof_statement_latex,
)
'''

  text = replace_exact(
    text,
    old_imports,
    new_imports,
    "web_group_proof imports",
  )

  anchor = '''@dataclass(frozen=True)
class WebGroupProofView:
'''

  rendered_line_class = '''@dataclass(frozen=True)
class WebGroupProofRenderedLineView:
  kind: str
  indent_level: int
  prefix: str
  statement_latex: str | None
  suffix: str

  def __post_init__(
    self,
  ) -> None:
    if self.kind not in (
      "heading",
      "text",
    ):
      raise ValueError(
        "kind must be heading or text"
      )

    if (
      isinstance(
        self.indent_level,
        bool,
      )
      or not isinstance(
        self.indent_level,
        int,
      )
    ):
      raise TypeError(
        "indent_level must be an int"
      )

    if self.indent_level < 0:
      raise ValueError(
        "indent_level must be nonnegative"
      )

    if not isinstance(
      self.prefix,
      str,
    ):
      raise TypeError(
        "prefix must be a str"
      )

    if (
      self.statement_latex is not None
      and not isinstance(
        self.statement_latex,
        str,
      )
    ):
      raise TypeError(
        "statement_latex must be a str or None"
      )

    if not isinstance(
      self.suffix,
      str,
    ):
      raise TypeError(
        "suffix must be a str"
      )


@dataclass(frozen=True)
class WebGroupProofView:
'''

  text = replace_exact(
    text,
    anchor,
    rendered_line_class,
    "WebGroupProofRenderedLineView insertion",
  )

  old_fields = '''  steps: tuple[
    WebGroupProofStepView,
    ...,
  ]
  max_depth: int

  def __post_init__(
'''

  new_fields = '''  steps: tuple[
    WebGroupProofStepView,
    ...,
  ]
  max_depth: int
  mode: str = "trace"
  rendered_lines: tuple[
    WebGroupProofRenderedLineView,
    ...,
  ] = ()

  def __post_init__(
'''

  text = replace_exact(
    text,
    old_fields,
    new_fields,
    "WebGroupProofView fields",
  )

  old_validation_tail = '''    if self.max_depth < 0:
      raise ValueError(
        "max_depth must be nonnegative"
      )


def _group_proof_rule_name(
'''

  new_validation_tail = '''    if self.max_depth < 0:
      raise ValueError(
        "max_depth must be nonnegative"
      )

    if self.mode not in (
      "trace",
      "outline",
      "narrative",
    ):
      raise ValueError(
        "mode must be trace, outline, or narrative"
      )

    if not isinstance(
      self.rendered_lines,
      tuple,
    ):
      raise TypeError(
        "rendered_lines must be a tuple"
      )

    for line in self.rendered_lines:
      if not isinstance(
        line,
        WebGroupProofRenderedLineView,
      ):
        raise TypeError(
          "rendered_lines must contain only "
          "WebGroupProofRenderedLineView values"
        )

    if (
      self.mode == "trace"
      and self.rendered_lines
    ):
      raise ValueError(
        "trace mode must not have rendered_lines"
      )

    if (
      self.mode != "trace"
      and not self.rendered_lines
    ):
      raise ValueError(
        "outline and narrative modes require "
        "rendered_lines"
      )


def _group_proof_rule_name(
'''

  text = replace_exact(
    text,
    old_validation_tail,
    new_validation_tail,
    "WebGroupProofView validation",
  )

  build_anchor = '''def build_standard_web_group_proof_view(
'''

  helper_functions = r'''def _split_group_proof_rendered_line(
  line: str,
) -> tuple[
  str,
  str | None,
  str,
]:
  first_math = line.find(
    "$"
  )

  if first_math < 0:
    return (
      line,
      None,
      "",
    )

  second_math = line.find(
    "$",
    first_math + 1,
  )

  if second_math < 0:
    return (
      line,
      None,
      "",
    )

  return (
    line[
      :first_math
    ],
    line[
      first_math + 1:
      second_math
    ],
    line[
      second_math + 1:
    ],
  )


def _build_group_proof_rendered_lines(
  markdown: str,
) -> tuple[
  WebGroupProofRenderedLineView,
  ...,
]:
  if not isinstance(
    markdown,
    str,
  ):
    raise TypeError(
      "markdown must be a str"
    )

  lines = []

  for raw_line in markdown.splitlines():
    if not raw_line:
      continue

    if raw_line.startswith(
      "# "
    ):
      continue

    stripped = raw_line.lstrip(
      " "
    )
    leading_spaces = (
      len(
        raw_line
      )
      - len(
        stripped
      )
    )
    indent_level = (
      leading_spaces // 2
    )

    if stripped.startswith(
      "## "
    ):
      lines.append(
        WebGroupProofRenderedLineView(
          kind="heading",
          indent_level=0,
          prefix=stripped[
            3:
          ],
          statement_latex=None,
          suffix="",
        )
      )
      continue

    (
      prefix,
      statement_latex,
      suffix,
    ) = _split_group_proof_rendered_line(
      stripped
    )

    lines.append(
      WebGroupProofRenderedLineView(
        kind="text",
        indent_level=indent_level,
        prefix=prefix,
        statement_latex=statement_latex,
        suffix=suffix,
      )
    )

  return tuple(
    lines
  )


def build_standard_web_group_proof_view(
'''

  text = replace_exact(
    text,
    build_anchor,
    helper_functions,
    "Web render adapter insertion",
  )

  old_signature = '''def build_standard_web_group_proof_view(
  n: int,
  k: int,
  max_depth: int = 1,
) -> WebGroupProofView:
'''

  new_signature = '''def build_standard_web_group_proof_view(
  n: int,
  k: int,
  max_depth: int = 1,
  mode: str = "trace",
) -> WebGroupProofView:
'''

  text = replace_exact(
    text,
    old_signature,
    new_signature,
    "build_standard_web_group_proof_view signature",
  )

  old_depth_validation = '''  if max_depth < 0:
    raise ValueError(
      "max_depth must be nonnegative"
    )

  report = (
'''

  new_depth_validation = '''  if max_depth < 0:
    raise ValueError(
      "max_depth must be nonnegative"
    )

  if mode not in (
    "trace",
    "outline",
    "narrative",
  ):
    raise ValueError(
      "mode must be trace, outline, or narrative"
    )

  report = (
'''

  text = replace_exact(
    text,
    old_depth_validation,
    new_depth_validation,
    "web group proof mode validation",
  )

  old_return = '''  return WebGroupProofView(
    n=n,
    k=k,
    conclusion_latex=conclusion_latex,
    theorem=replay.source_entry.theorem,
    phase=replay.source_entry.phase,
    key=replay.source_entry.key,
    steps=tuple(
      steps
    ),
    max_depth=replay.max_depth,
  )
'''

  new_return = '''  rendered_lines = ()

  if mode != "trace":
    presentation = (
      build_toda_group_proof_presentation(
        replay
      )
    )

    if mode == "outline":
      markdown = (
        render_toda_group_proof_outline_markdown(
          presentation
        )
      )
    else:
      markdown = (
        render_toda_group_proof_narrative_markdown(
          presentation
        )
      )

    rendered_lines = (
      _build_group_proof_rendered_lines(
        markdown
      )
    )

  return WebGroupProofView(
    n=n,
    k=k,
    conclusion_latex=conclusion_latex,
    theorem=replay.source_entry.theorem,
    phase=replay.source_entry.phase,
    key=replay.source_entry.key,
    steps=tuple(
      steps
    ),
    max_depth=replay.max_depth,
    mode=mode,
    rendered_lines=rendered_lines,
  )
'''

  text = replace_exact(
    text,
    old_return,
    new_return,
    "WebGroupProofView return",
  )

  WEB_GROUP_PROOF_PATH.write_text(
    text,
    encoding="utf-8",
  )


def patch_web_app() -> None:
  backup_once(
    WEB_APP_PATH
  )

  text = WEB_APP_PATH.read_text(
    encoding="utf-8",
  )

  old_value = '''    group_proof_depth_value = request.form.get(
      "group_proof_depth",
      "1",
    )
'''

  new_value = '''    group_proof_depth_value = request.form.get(
      "group_proof_depth",
      "1",
    )
    group_proof_mode_value = request.form.get(
      "group_proof_mode",
      "trace",
    )
'''

  text = replace_exact(
    text,
    old_value,
    new_value,
    "group_proof_mode_value",
  )

  old_builder_call = '''          group_proof_view = (
            build_standard_web_group_proof_view(
              n,
              k,
              max_depth=group_proof_depth,
            )
          )
'''

  new_builder_call = '''          group_proof_view = (
            build_standard_web_group_proof_view(
              n,
              k,
              max_depth=group_proof_depth,
              mode=group_proof_mode_value,
            )
          )
'''

  text = replace_exact(
    text,
    old_builder_call,
    new_builder_call,
    "group proof builder mode",
  )

  old_template_value = '''      group_proof_depth_value=(
        group_proof_depth_value
      ),
'''

  new_template_value = '''      group_proof_depth_value=(
        group_proof_depth_value
      ),
      group_proof_mode_value=(
        group_proof_mode_value
      ),
'''

  text = replace_exact(
    text,
    old_template_value,
    new_template_value,
    "group proof mode template value",
  )

  WEB_APP_PATH.write_text(
    text,
    encoding="utf-8",
  )


def patch_template() -> None:
  backup_once(
    TEMPLATE_PATH
  )

  text = TEMPLATE_PATH.read_text(
    encoding="utf-8",
  )

  old_form_tail = '''              </label>

              <button type="submit">
                Show proof
              </button>
'''

  new_form_tail = '''              </label>

              <label>
                Proof view
                <select name="group_proof_mode">
                  <option
                    value="trace"
                    {% if group_proof_mode_value == "trace" %}selected{% endif %}
                  >Trace</option>
                  <option
                    value="outline"
                    {% if group_proof_mode_value == "outline" %}selected{% endif %}
                  >Outline</option>
                  <option
                    value="narrative"
                    {% if group_proof_mode_value == "narrative" %}selected{% endif %}
                  >Narrative</option>
                </select>
              </label>

              <button type="submit">
                Show proof
              </button>
'''

  text = replace_exact(
    text,
    old_form_tail,
    new_form_tail,
    "group proof mode selector",
  )

  old_selected_depth = '''        <p>
          Selected depth:
          {{ group_proof_view.max_depth }}
        </p>

        <h3>
          Conclusion
        </h3>
'''

  new_selected_depth = '''        <p>
          Selected depth:
          {{ group_proof_view.max_depth }}
        </p>

        <p>
          Selected view:
          {{ group_proof_view.mode }}
        </p>

        <h3>
          Conclusion
        </h3>
'''

  text = replace_exact(
    text,
    old_selected_depth,
    new_selected_depth,
    "selected group proof mode",
  )

  old_proof_block = '''        <h3>
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
'''

  new_proof_block = '''        <h3>
          Proof
        </h3>

        {% if group_proof_view.mode == "trace" %}
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
        {% else %}
          <div
            id="group-proof-rendered-lines"
            data-proof-mode="{{ group_proof_view.mode }}"
          >
            {% for line in group_proof_view.rendered_lines %}
              {% if line.kind == "heading" %}
                <h4>
                  {{ line.prefix }}
                </h4>
              {% else %}
                <div
                  class="group-proof-rendered-line"
                  style="margin-left: {{ line.indent_level * 2 }}em;"
                >
                  {% if line.prefix %}
                    <span>{{ line.prefix }}</span>
                  {% endif %}

                  {% if line.statement_latex %}
                    <div
                      class="group-proof-rendered-math"
                      data-latex="{{ line.statement_latex }}"
                    >{{ line.statement_latex }}</div>
                  {% endif %}

                  {% if line.suffix %}
                    <span>{{ line.suffix }}</span>
                  {% endif %}
                </div>
              {% endif %}
            {% endfor %}
          </div>
        {% endif %}
'''

  text = replace_exact(
    text,
    old_proof_block,
    new_proof_block,
    "group proof mode rendering",
  )

  TEMPLATE_PATH.write_text(
    text,
    encoding="utf-8",
  )


def main() -> None:
  for path in (
    WEB_GROUP_PROOF_PATH,
    WEB_APP_PATH,
    TEMPLATE_PATH,
  ):
    if not path.exists():
      raise RuntimeError(
        f"required file not found: {path}"
      )

  patch_web_group_proof()
  patch_web_app()
  patch_template()

  print(
    "Phase 132-9 applied successfully."
  )
  print(
    "Backups created with .phase132_9_backup suffix."
  )


if __name__ == "__main__":
  main()
