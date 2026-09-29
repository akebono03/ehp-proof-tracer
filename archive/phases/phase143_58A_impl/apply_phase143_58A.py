from pathlib import Path


ROOT = Path(__file__).resolve().parent.parent
RENDERER_PATH = (
  ROOT
  / "toda_human_readable_renderer.py"
)
TEST_SOURCE = (
  Path(__file__).resolve().parent
  / "tests"
  / "test_phase143_58a_negative_scalar_sum.py"
)
TEST_DESTINATION = (
  ROOT
  / "tests"
  / "test_phase143_58a_negative_scalar_sum.py"
)

START = "def _render_scalar_latex(\n"
END = "\n\ndef _render_generator_symbol_latex(\n"

NEW_FUNCTION = r'''def _render_scalar_latex(
  value,
) -> str:
  if isinstance(
    value,
    bool,
  ):
    raise TypeError(
      "scalar bool is not supported"
    )

  if isinstance(
    value,
    int,
  ):
    return str(
      value
    )

  if isinstance(
    value,
    ScalarSymbol,
  ):
    return _render_unicode_math_name_latex(
      value.name
    )

  if isinstance(
    value,
    ScalarSum,
  ):
    if (
      isinstance(
        value.right,
        int,
      )
      and not isinstance(
        value.right,
        bool,
      )
      and value.right < 0
    ):
      return (
        _render_scalar_latex(
          value.left
        )
        + " - "
        + _render_scalar_latex(
          -value.right
        )
      )

    return (
      _render_scalar_latex(
        value.left
      )
      + " + "
      + _render_scalar_latex(
        value.right
      )
    )

  if isinstance(
    value,
    ScalarProduct,
  ):
    return (
      _render_scalar_latex(
        value.left
      )
      + r"\,"
      + _render_scalar_latex(
        value.right
      )
    )

  if isinstance(
    value,
    ScalarPower,
  ):
    return (
      "{"
      + _render_scalar_latex(
        value.base
      )
      + "}^{"
      + _render_scalar_latex(
        value.exponent
      )
      + "}"
    )

  raise TypeError(
    "unsupported scalar value for LaTeX rendering"
  )
'''


def main() -> None:
  text = RENDERER_PATH.read_text(
    encoding="utf-8"
  )
  start_index = text.find(
    START
  )
  end_index = text.find(
    END,
    start_index,
  )

  if (
    start_index < 0
    or end_index < 0
  ):
    raise RuntimeError(
      "could not locate _render_scalar_latex "
      "replacement boundaries"
    )

  updated = (
    text[
      :start_index
    ]
    + NEW_FUNCTION
    + text[
      end_index:
    ]
  )
  RENDERER_PATH.write_text(
    updated,
    encoding="utf-8",
  )
  print(
    f"updated {RENDERER_PATH}"
  )

  TEST_DESTINATION.write_text(
    TEST_SOURCE.read_text(
      encoding="utf-8"
    ),
    encoding="utf-8",
  )
  print(
    f"updated {TEST_DESTINATION}"
  )


if __name__ == "__main__":
  main()
