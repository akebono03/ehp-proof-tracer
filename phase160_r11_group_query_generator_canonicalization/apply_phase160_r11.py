from pathlib import Path


package_root = Path(__file__).resolve().parent
repo_root = package_root.parent


def replace_function(
  path: Path,
  function_name: str,
  replacement: str,
) -> None:
  text = path.read_text(
    encoding="utf-8",
  )

  marker = (
    "def "
    + function_name
    + "("
  )

  start = text.find(
    marker
  )

  if start < 0:
    raise SystemExit(
      "function not found: "
      + function_name
      + " in "
      + str(
        path
      )
    )

  next_def = text.find(
    "\ndef ",
    start + len(
      marker
    ),
  )

  if next_def < 0:
    end = len(
      text
    )
  else:
    end = (
      next_def
      + 1
    )

  path.write_text(
    (
      text[
        :start
      ]
      + replacement.rstrip()
      + "\n\n"
      + text[
        end:
      ]
    ),
    encoding="utf-8",
  )


renderer = (
  repo_root
  / "toda_human_readable_renderer.py"
)

renderer_text = renderer.read_text(
  encoding="utf-8",
)

helper_marker = (
  "def _toda_public_eta_composition_factors("
)

if helper_marker not in renderer_text:
  insertion_marker = (
    "def render_toda_group_structure_latex("
  )
  insertion_index = (
    renderer_text.find(
      insertion_marker
    )
  )

  if insertion_index < 0:
    raise SystemExit(
      "group structure renderer insertion marker "
      "was not found"
    )

  helpers = (
    package_root
    / "files"
    / "public_group_generator_helpers.py"
  ).read_text(
    encoding="utf-8",
  ).rstrip()

  renderer_text = (
    renderer_text[
      :insertion_index
    ]
    + helpers
    + "\n\n\n"
    + renderer_text[
      insertion_index:
    ]
  )

  renderer.write_text(
    renderer_text,
    encoding="utf-8",
  )


replace_function(
  renderer,
  "render_toda_group_structure_latex",
  (
    package_root
    / "files"
    / "render_toda_group_structure_latex.py"
  ).read_text(
    encoding="utf-8",
  ),
)

renderer_text = renderer.read_text(
  encoding="utf-8",
)

if (
  "def render_toda_public_group_relation_latex("
  not in renderer_text
):
  insertion_marker = (
    "def render_toda_group_result_latex("
  )
  insertion_index = (
    renderer_text.find(
      insertion_marker
    )
  )

  if insertion_index < 0:
    raise SystemExit(
      "group result renderer insertion marker "
      "was not found"
    )

  relation_helper = (
    package_root
    / "files"
    / "render_toda_public_group_relation_latex.py"
  ).read_text(
    encoding="utf-8",
  ).rstrip()

  renderer_text = (
    renderer_text[
      :insertion_index
    ]
    + relation_helper
    + "\n\n\n"
    + renderer_text[
      insertion_index:
    ]
  )

  renderer.write_text(
    renderer_text,
    encoding="utf-8",
  )


web_group_proof = (
  repo_root
  / "web_group_proof.py"
)
web_text = web_group_proof.read_text(
  encoding="utf-8",
)

new_import = """from toda_human_readable_renderer import (
  render_toda_public_group_relation_latex,
)
"""

if new_import not in web_text:
  anchor = """from toda_group_result_proof_replay import (
  build_toda_group_result_proof_replay,
)
from toda_proof_narrative_renderer import (
"""

  replacement = """from toda_group_result_proof_replay import (
  build_toda_group_result_proof_replay,
)
from toda_human_readable_renderer import (
  render_toda_public_group_relation_latex,
)
from toda_proof_narrative_renderer import (
"""

  if web_text.count(
    anchor
  ) != 1:
    raise SystemExit(
      "web_group_proof import anchor "
      "was not found exactly once"
    )

  web_text = web_text.replace(
    anchor,
    replacement,
    1,
  )

  web_group_proof.write_text(
    web_text,
    encoding="utf-8",
  )


replace_function(
  web_group_proof,
  "_group_proof_statement_latex",
  (
    package_root
    / "files"
    / "group_proof_statement_latex.py"
  ).read_text(
    encoding="utf-8",
  ),
)


print("Applied Phase 160-R11:")
print("  toda_human_readable_renderer.py")
print("  web_group_proof.py")
print("")
print("No tests were run.")
