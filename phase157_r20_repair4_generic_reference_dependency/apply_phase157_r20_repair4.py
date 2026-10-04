from __future__ import annotations

import ast
import re
import shutil
from datetime import datetime
from pathlib import Path


ROOT = Path.cwd()

GENERIC_RENDERER = (
  ROOT
  / "toda_group_proof_generic_narrative_renderer.py"
)
CONTRIBUTION_RENDERER = (
  ROOT
  / "toda_group_proof_narrative_contribution_renderer.py"
)
R19_TEST = (
  ROOT
  / "tests"
  / "test_phase157_r19_pi6_3_reference_dependency_restoration.py"
)
R20_TEST = (
  ROOT
  / "tests"
  / "test_phase157_r20_generic_dependency_rendering.py"
)

EXPR_RENDERER = 'def _normalize_generic_eta_family_latex(\n  latex: str,\n) -> str:\n  if not isinstance(\n    latex,\n    str,\n  ):\n    raise TypeError(\n      "latex must be a str"\n    )\n\n  suspension_pattern = re.compile(\n    r"E(?:\\^\\{(?P<exponent>[0-9]+)\\})?"\n    r"\\\\eta_\\{(?P<index>[0-9]+)\\}"\n  )\n\n  def replace_suspension(\n    match,\n  ):\n    exponent_text = match.group(\n      "exponent"\n    )\n    exponent = (\n      1\n      if exponent_text is None\n      else int(\n        exponent_text\n      )\n    )\n    index = int(\n      match.group(\n        "index"\n      )\n    )\n\n    return (\n      r"\\eta_{"\n      + str(\n        index + exponent\n      )\n      + "}"\n    )\n\n  normalized = suspension_pattern.sub(\n    replace_suspension,\n    latex,\n  )\n\n  factor_pattern = re.compile(\n    r"\\\\eta_\\{([0-9]+)\\}"\n  )\n  matches = tuple(\n    factor_pattern.finditer(\n      normalized\n    )\n  )\n\n  if not matches:\n    return normalized\n\n  replacements = []\n  run_start = 0\n\n  while run_start < len(\n    matches\n  ):\n    run_end = run_start + 1\n    first_index = int(\n      matches[\n        run_start\n      ].group(\n        1\n      )\n    )\n\n    while run_end < len(\n      matches\n    ):\n      previous = matches[\n        run_end - 1\n      ]\n      current = matches[\n        run_end\n      ]\n\n      between = normalized[\n        previous.end():\n        current.start()\n      ]\n\n      if between:\n        break\n\n      current_index = int(\n        current.group(\n          1\n        )\n      )\n\n      if (\n        current_index\n        != first_index\n        + (\n          run_end\n          - run_start\n        )\n      ):\n        break\n\n      run_end += 1\n\n    run_length = (\n      run_end\n      - run_start\n    )\n\n    if run_length >= 2:\n      replacements.append(\n        (\n          matches[\n            run_start\n          ].start(),\n          matches[\n            run_end - 1\n          ].end(),\n          (\n            r"\\eta_{"\n            + str(\n              first_index\n            )\n            + r"}^{"\n            + str(\n              run_length\n            )\n            + "}"\n          ),\n        )\n      )\n\n    run_start = run_end\n\n  for start, end, replacement in reversed(\n    replacements\n  ):\n    normalized = (\n      normalized[\n        :start\n      ]\n      + replacement\n      + normalized[\n        end:\n      ]\n    )\n\n  return normalized\n\n\ndef _render_generic_narrative_expression_latex(\n  expression,\n) -> str:\n  compact = _render_generic_eta_composition_latex(\n    expression\n  )\n  if compact is not None:\n    return compact\n\n  if isinstance(\n    expression,\n    Suspension,\n  ):\n    suspended = expression.expression\n\n    if isinstance(\n      suspended,\n      HomotopyElement,\n    ):\n      generator = suspended.generator\n\n      if (\n        generator is not None\n        and generator.family == "η"\n        and isinstance(\n          generator.index,\n          int,\n        )\n        and not isinstance(\n          generator.index,\n          bool,\n        )\n        and generator.decoration is None\n      ):\n        return (\n          r"\\eta_{"\n          + str(\n            generator.index + 1\n          )\n          + "}"\n        )\n\n  if isinstance(\n    expression,\n    IteratedSuspension,\n  ):\n    suspended = expression.expression\n    exponent = expression.exponent\n\n    if (\n      isinstance(\n        suspended,\n        HomotopyElement,\n      )\n      and isinstance(\n        exponent,\n        int,\n      )\n      and not isinstance(\n        exponent,\n        bool,\n      )\n    ):\n      generator = suspended.generator\n\n      if (\n        generator is not None\n        and generator.family == "η"\n        and isinstance(\n          generator.index,\n          int,\n        )\n        and not isinstance(\n          generator.index,\n          bool,\n        )\n        and generator.decoration is None\n      ):\n        return (\n          r"\\eta_{"\n          + str(\n            generator.index\n            + exponent\n          )\n          + "}"\n        )\n\n  if isinstance(\n    expression,\n    Composition,\n  ):\n    return (\n      _render_generic_narrative_expression_latex(\n        expression.left\n      )\n      + _render_generic_narrative_expression_latex(\n        expression.right\n      )\n    )\n\n  return (\n    _normalize_generic_eta_family_latex(\n      render_toda_expression_latex(\n        expression\n      )\n    )\n  )\n'
NORMALIZE_STATEMENT = 'def _normalize_generic_narrative_statement_latex(\n  statement,\n  latex: str,\n) -> str:\n  if not isinstance(\n    latex,\n    str,\n  ):\n    raise TypeError(\n      "latex must be a str"\n    )\n\n  normalized = (\n    _normalize_generic_eta_family_latex(\n      latex\n    )\n  )\n\n  if not hasattr(\n    statement,\n    "lhs",\n  ):\n    return normalized\n\n  if not hasattr(\n    statement,\n    "rhs",\n  ):\n    return normalized\n\n  replacements = []\n  search_start = 0\n\n  for expression in (\n    statement.lhs,\n    statement.rhs,\n  ):\n    rendered_expression = (\n      _try_render_generic_narrative_expression_latex(\n        expression\n      )\n    )\n\n    if rendered_expression is None:\n      continue\n\n    normalized_expression = (\n      _render_generic_narrative_expression_latex(\n        expression\n      )\n    )\n\n    expression_start = normalized.find(\n      rendered_expression,\n      search_start,\n    )\n\n    if expression_start < 0:\n      continue\n\n    expression_end = (\n      expression_start\n      + len(\n        rendered_expression\n      )\n    )\n    search_start = expression_end\n\n    if (\n      normalized_expression\n      == rendered_expression\n    ):\n      continue\n\n    replacements.append(\n      (\n        expression_start,\n        expression_end,\n        normalized_expression,\n      )\n    )\n\n  for (\n    expression_start,\n    expression_end,\n    normalized_expression,\n  ) in reversed(\n    replacements\n  ):\n    normalized = (\n      normalized[\n        :expression_start\n      ]\n      + normalized_expression\n      + normalized[\n        expression_end:\n      ]\n    )\n\n  return (\n    _normalize_generic_eta_family_latex(\n      normalized\n    )\n  )\n'
NORMALIZE_STEP = 'def _normalize_generic_narrative_step_latex(\n  proof_step: ProofStep,\n  latex: str,\n) -> str:\n  return (\n    _normalize_generic_narrative_statement_latex(\n      proof_step.conclusion,\n      latex,\n    )\n  )\n'
COMPONENT_LATEX = 'def _render_phase153_r3_6_component_latex(\n  component,\n) -> str | None:\n  if isinstance(\n    component,\n    ScalarGreaterEqualStatement,\n  ):\n    return (\n      _render_scalar_latex(\n        component.left\n      )\n      + r" \\ge "\n      + _render_scalar_latex(\n        component.right\n      )\n    )\n\n  try:\n    latex = (\n      render_repository_conclusion_latex(\n        component\n      )\n    )\n  except (\n    TypeError,\n    ValueError,\n  ):\n    latex = None\n\n  if latex is not None:\n    return (\n      _normalize_generic_narrative_statement_latex(\n        component,\n        latex,\n      )\n    )\n\n  try:\n    latex = (\n      render_toda_proof_statement_latex(\n        component\n      )\n    )\n  except (\n    TypeError,\n    ValueError,\n  ):\n    return None\n\n  return (\n    _normalize_generic_narrative_statement_latex(\n      component,\n      latex,\n    )\n  )\n'
ETA_BRIDGE = 'def insert_toda_group_proof_narrative_adjacent_eta_suspension_bridges(\n  presentation: TodaGroupProofPresentation,\n  markdown: str,\n) -> str:\n  if not isinstance(\n    presentation,\n    TodaGroupProofPresentation,\n  ):\n    raise TypeError(\n      "presentation must be a TodaGroupProofPresentation"\n    )\n\n  if not isinstance(\n    markdown,\n    str,\n  ):\n    raise TypeError(\n      "markdown must be a str"\n    )\n\n  paragraphs = markdown.split(\n    "\\n\\n"\n  )\n\n  def match_key(\n    paragraph: str,\n  ) -> str:\n    stripped = paragraph.strip()\n\n    if stripped.startswith(\n      "[R"\n    ):\n      marker_end = stripped.find(\n        "]より, "\n      )\n\n      if marker_end >= 0:\n        stripped = stripped[\n          marker_end\n          + len(\n            "]より, "\n          ):\n        ]\n\n    return (\n      _phase157_r11_reference_statement_match_key(\n        stripped\n      )\n    )\n\n  for node in presentation.nodes:\n    definition_steps = tuple(\n      premise\n      for premise in node.proof_step.premises\n      if type(\n        premise.conclusion\n      ).__name__\n      == "TodaEtaFamilyDefinitionStatement"\n    )\n\n    if len(\n      definition_steps\n    ) < 2:\n      continue\n\n    ordered = tuple(\n      sorted(\n        definition_steps,\n        key=lambda step: (\n          step.conclusion.index\n        ),\n      )\n    )\n\n    for lower_step, upper_step in zip(\n      ordered,\n      ordered[\n        1:\n      ],\n    ):\n      lower = lower_step.conclusion\n      upper = upper_step.conclusion\n\n      if (\n        not isinstance(\n          lower.index,\n          int,\n        )\n        or isinstance(\n          lower.index,\n          bool,\n        )\n        or not isinstance(\n          upper.index,\n          int,\n        )\n        or isinstance(\n          upper.index,\n          bool,\n        )\n        or upper.index\n        != lower.index + 1\n      ):\n        continue\n\n      bridge = (\n        "$"\n        + render_toda_expression_latex(\n          upper.element\n        )\n        + "=E"\n        + render_toda_expression_latex(\n          lower.element\n        )\n        + "$ である."\n      )\n\n      bridge = (\n        _normalize_generic_eta_family_latex(\n          bridge\n        )\n      )\n\n      if any(\n        match_key(\n          paragraph\n        )\n        == match_key(\n          bridge\n        )\n        for paragraph in paragraphs\n      ):\n        continue\n\n      dependent_line = (\n        _render_generic_narrative_step(\n          node.proof_step\n        )\n      )\n\n      if not dependent_line:\n        continue\n\n      dependent_key = match_key(\n        dependent_line\n      )\n      dependent_index = next(\n        (\n          index\n          for index, paragraph in enumerate(\n            paragraphs\n          )\n          if match_key(\n            paragraph\n          )\n          == dependent_key\n        ),\n        None,\n      )\n\n      if dependent_index is None:\n        continue\n\n      paragraphs.insert(\n        dependent_index,\n        bridge,\n      )\n\n  return "\\n\\n".join(\n    paragraphs\n  )\n'
MAP_DEPENDENCIES = 'def insert_toda_group_proof_narrative_map_property_dependencies(\n  presentation: TodaGroupProofPresentation,\n  markdown: str,\n  reference_entries=(),\n) -> str:\n  if not isinstance(\n    presentation,\n    TodaGroupProofPresentation,\n  ):\n    raise TypeError(\n      "presentation must be a TodaGroupProofPresentation"\n    )\n\n  if not isinstance(\n    markdown,\n    str,\n  ):\n    raise TypeError(\n      "markdown must be a str"\n    )\n\n  if not isinstance(\n    reference_entries,\n    tuple,\n  ):\n    raise TypeError(\n      "reference_entries must be a tuple"\n    )\n\n  paragraphs = markdown.split(\n    "\\n\\n"\n  )\n\n  def match_key(\n    paragraph: str,\n  ) -> str:\n    stripped = paragraph.strip()\n\n    if stripped.startswith(\n      "[R"\n    ):\n      marker_end = stripped.find(\n        "]より, "\n      )\n\n      if marker_end >= 0:\n        stripped = stripped[\n          marker_end\n          + len(\n            "]より, "\n          ):\n        ]\n\n    return (\n      _phase157_r11_reference_statement_match_key(\n        stripped\n      )\n    )\n\n  def reference_number_for_step(\n    proof_step: ProofStep,\n  ) -> int | None:\n    direct = tuple(\n      entry.number\n      for entry in reference_entries\n      if any(\n        candidate is proof_step\n        for candidate in entry.proof_steps\n      )\n    )\n\n    if len(\n      direct\n    ) == 1:\n      return direct[\n        0\n      ]\n\n    reference = (\n      extract_toda_group_proof_step_literature_reference(\n        proof_step\n      )\n    )\n\n    if (\n      reference is None\n      or reference.locator is None\n    ):\n      return None\n\n    by_locator = tuple(\n      entry.number\n      for entry in reference_entries\n      if (\n        entry.reference.locator\n        == reference.locator\n      )\n    )\n\n    if len(\n      by_locator\n    ) != 1:\n      return None\n\n    return by_locator[\n      0\n    ]\n\n  def display_line(\n    proof_step: ProofStep,\n  ) -> str | None:\n    rendered = (\n      _render_generic_narrative_step(\n        proof_step\n      )\n    )\n\n    if not rendered:\n      return None\n\n    reference_number = (\n      reference_number_for_step(\n        proof_step\n      )\n    )\n\n    if reference_number is None:\n      return rendered\n\n    return (\n      "[R"\n      + str(\n        reference_number\n      )\n      + "]より, "\n      + rendered\n    )\n\n  def paragraph_index_for_step(\n    proof_step: ProofStep,\n  ) -> int | None:\n    rendered = (\n      _render_generic_narrative_step(\n        proof_step\n      )\n    )\n\n    if not rendered:\n      return None\n\n    target_key = match_key(\n      rendered\n    )\n    matches = tuple(\n      index\n      for index, paragraph in enumerate(\n        paragraphs\n      )\n      if match_key(\n        paragraph\n      )\n      == target_key\n    )\n\n    if len(\n      matches\n    ) != 1:\n      return None\n\n    return matches[\n      0\n    ]\n\n  relevant_roles = {\n    TodaProofDependencyRole.EHP_EXACTNESS,\n    TodaProofDependencyRole.EHP_WINDOW,\n    TodaProofDependencyRole.GROUP_STRUCTURE,\n    TodaProofDependencyRole.MAP_PROPERTY,\n    TodaProofDependencyRole.RELATION,\n  }\n\n  visiting = set()\n\n  def ensure_before(\n    proof_step: ProofStep,\n    anchor_index: int,\n  ) -> int:\n    proof_step_id = id(\n      proof_step\n    )\n\n    if proof_step_id in visiting:\n      return anchor_index\n\n    visiting.add(\n      proof_step_id\n    )\n\n    boundary = (\n      classify_toda_literature_statement_step(\n        proof_step\n      )\n    )\n    is_fixed_boundary = (\n      boundary is not None\n      and boundary.classification\n      is TodaLiteratureStatementClassification.FIXED_STATEMENT\n    )\n\n    if not is_fixed_boundary:\n      for premise in proof_step.premises:\n        premise_role = (\n          classify_toda_proof_step_role(\n            premise\n          )\n        )\n\n        if premise_role not in relevant_roles:\n          continue\n\n        anchor_index = ensure_before(\n          premise,\n          anchor_index,\n        )\n\n    line = display_line(\n      proof_step\n    )\n\n    if line is None:\n      visiting.remove(\n        proof_step_id\n      )\n      return anchor_index\n\n    current_index = (\n      paragraph_index_for_step(\n        proof_step\n      )\n    )\n\n    if current_index is not None:\n      reference_number = (\n        reference_number_for_step(\n          proof_step\n        )\n      )\n\n      if (\n        reference_number is not None\n        and not paragraphs[\n          current_index\n        ].strip().startswith(\n          "[R"\n        )\n      ):\n        paragraphs[\n          current_index\n        ] = line\n\n      if current_index < anchor_index:\n        visiting.remove(\n          proof_step_id\n        )\n        return anchor_index\n\n      paragraph = paragraphs.pop(\n        current_index\n      )\n\n      if current_index < anchor_index:\n        anchor_index -= 1\n\n      paragraphs.insert(\n        anchor_index,\n        paragraph,\n      )\n\n      visiting.remove(\n        proof_step_id\n      )\n      return anchor_index + 1\n\n    paragraphs.insert(\n      anchor_index,\n      line,\n    )\n\n    visiting.remove(\n      proof_step_id\n    )\n    return anchor_index + 1\n\n  visible_map_steps = []\n\n  for node in presentation.nodes:\n    proof_step = node.proof_step\n\n    if (\n      classify_toda_proof_step_role(\n        proof_step\n      )\n      is not TodaProofDependencyRole.MAP_PROPERTY\n    ):\n      continue\n\n    if (\n      paragraph_index_for_step(\n        proof_step\n      )\n      is None\n    ):\n      continue\n\n    visible_map_steps.append(\n      proof_step\n    )\n\n  for map_step in visible_map_steps:\n    map_index = paragraph_index_for_step(\n      map_step\n    )\n\n    if map_index is None:\n      continue\n\n    for premise in map_step.premises:\n      role = classify_toda_proof_step_role(\n        premise\n      )\n\n      if role not in relevant_roles:\n        continue\n\n      map_index = ensure_before(\n        premise,\n        map_index,\n      )\n\n  return "\\n\\n".join(\n    paragraphs\n  )\n'
HIDDEN_ZERO = 'def insert_toda_group_proof_narrative_hidden_zero_map_premises(\n  presentation: TodaGroupProofPresentation,\n  markdown: str,\n  reference_entries=(),\n) -> str:\n  if not isinstance(\n    presentation,\n    TodaGroupProofPresentation,\n  ):\n    raise TypeError(\n      "presentation must be a TodaGroupProofPresentation"\n    )\n\n  if not isinstance(\n    markdown,\n    str,\n  ):\n    raise TypeError(\n      "markdown must be a str"\n    )\n\n  if not isinstance(\n    reference_entries,\n    tuple,\n  ):\n    raise TypeError(\n      "reference_entries must be a tuple"\n    )\n\n  paragraphs = markdown.split(\n    "\\n\\n"\n  )\n\n  def match_key(\n    paragraph: str,\n  ) -> str:\n    stripped = paragraph.strip()\n\n    if stripped.startswith(\n      "[R"\n    ):\n      marker_end = stripped.find(\n        "]より, "\n      )\n\n      if marker_end >= 0:\n        stripped = stripped[\n          marker_end\n          + len(\n            "]より, "\n          ):\n        ]\n\n    return (\n      _phase157_r11_reference_statement_match_key(\n        stripped\n      )\n    )\n\n  def visible_index(\n    proof_step: ProofStep,\n  ) -> int | None:\n    rendered = (\n      _render_generic_narrative_step(\n        proof_step\n      )\n    )\n\n    if not rendered:\n      return None\n\n    target_key = match_key(\n      rendered\n    )\n    matches = tuple(\n      index\n      for index, paragraph in enumerate(\n        paragraphs\n      )\n      if match_key(\n        paragraph\n      )\n      == target_key\n    )\n\n    if len(\n      matches\n    ) != 1:\n      return None\n\n    return matches[\n      0\n    ]\n\n  def map_latex(\n    group_map,\n  ) -> str | None:\n    name = getattr(\n      group_map,\n      "name",\n      None,\n    )\n\n    if name is None:\n      return None\n\n    if name in (\n      "Δ",\n      "Delta",\n    ):\n      return r"\\Delta"\n\n    return str(\n      name\n    )\n\n  def exactness_reason(\n    zero_step: ProofStep,\n  ) -> str | None:\n    surjective_step = next(\n      (\n        premise\n        for premise in zero_step.premises\n        if (\n          classify_toda_proof_step_role(\n            premise\n          )\n          is TodaProofDependencyRole.MAP_PROPERTY\n          and "全射である."\n          in (\n            _render_generic_narrative_step(\n              premise\n            )\n            or ""\n          )\n        )\n      ),\n      None,\n    )\n\n    exactness_step = next(\n      (\n        premise\n        for premise in zero_step.premises\n        if classify_toda_proof_step_role(\n          premise\n        )\n        in (\n          TodaProofDependencyRole.EHP_EXACTNESS,\n          TodaProofDependencyRole.EHP_WINDOW,\n        )\n      ),\n      None,\n    )\n\n    if (\n      surjective_step is None\n      or exactness_step is None\n    ):\n      return None\n\n    window = getattr(\n      exactness_step.conclusion,\n      "window",\n      None,\n    )\n\n    if window is None:\n      return None\n\n    first_map = map_latex(\n      window.first_map\n    )\n    second_map = map_latex(\n      window.second_map\n    )\n\n    if (\n      first_map is None\n      or second_map is None\n    ):\n      return None\n\n    return (\n      "完全性より, "\n      r"$\\ker "\n      + second_map\n      + r"=\\operatorname{Im}"\n      + first_map\n      + "="\n      + render_toda_primary_group_latex(\n        window.middle_term\n      )\n      + "$ である."\n    )\n\n  candidate_zero_steps = []\n  seen_zero_step_ids = set()\n\n  for node in presentation.nodes:\n    for proof_step in (\n      node.proof_step,\n      *node.proof_step.premises,\n    ):\n      rendered = (\n        _render_generic_narrative_step(\n          proof_step\n        )\n      )\n\n      if (\n        not rendered\n        or "零写像である."\n        not in rendered\n      ):\n        continue\n\n      proof_step_id = id(\n        proof_step\n      )\n\n      if proof_step_id in seen_zero_step_ids:\n        continue\n\n      seen_zero_step_ids.add(\n        proof_step_id\n      )\n      candidate_zero_steps.append(\n        proof_step\n      )\n\n  for zero_step in candidate_zero_steps:\n    zero_line = (\n      _render_generic_narrative_step(\n        zero_step\n      )\n    )\n\n    if not zero_line:\n      continue\n\n    zero_index = visible_index(\n      zero_step\n    )\n\n    if zero_index is None:\n      consumer_index = next(\n        (\n          visible_index(\n            node.proof_step\n          )\n          for node in presentation.nodes\n          if zero_step in node.proof_step.premises\n          and visible_index(\n            node.proof_step\n          )\n          is not None\n        ),\n        None,\n      )\n\n      if consumer_index is None:\n        continue\n\n      insertion_index = consumer_index\n\n      if insertion_index > 0:\n        previous = paragraphs[\n          insertion_index - 1\n        ]\n\n        if (\n          "零写像"\n          in previous\n          or "Δ=0"\n          in previous\n          or r"\\Delta=0"\n          in previous\n          or (\n            r"\\ker E"\n            in previous\n            and r"\\operatorname{Im}"\n            in previous\n          )\n        ):\n          insertion_index -= 1\n\n      paragraphs.insert(\n        insertion_index,\n        zero_line,\n      )\n      zero_index = insertion_index\n\n    reason = exactness_reason(\n      zero_step\n    )\n\n    if reason is None:\n      continue\n\n    if any(\n      paragraph.strip()\n      == reason\n      for paragraph in paragraphs\n    ):\n      continue\n\n    zero_index = next(\n      (\n        index\n        for index, paragraph in enumerate(\n          paragraphs\n        )\n        if match_key(\n          paragraph\n        )\n        == match_key(\n          zero_line\n        )\n      ),\n      zero_index,\n    )\n\n    paragraphs.insert(\n      zero_index,\n      reason,\n    )\n\n  return "\\n\\n".join(\n    paragraphs\n  )\n'
TEST2 = 'def test_phase157_r19_pi6_3_delta_zero_has_shallow_dependency_support():\n  _, body = _reference_and_body()\n\n  full_exactness = (\n    r"$\\pi_{7}^{3} \\xrightarrow{H} "\n    r"\\pi_{7}^{5} \\xrightarrow{\\Delta} "\n    r"\\pi_{5}^{2} \\xrightarrow{E} "\n    r"\\pi_{6}^{3}$ は完全である."\n  )\n  eta6_definition = (\n    r"$\\eta_{6}=E\\eta_{5}$ である."\n  )\n  pi7_5 = (\n    r"$\\pi_{7}^{5} = "\n    r"\\mathbb{Z}/2\\{\\eta_{5}^{2}\\}$."\n  )\n  surjective = (\n    r"$H: \\pi_{7}^{3} \\to \\pi_{7}^{5}$ は全射である."\n  )\n  kernel_reason = (\n    "完全性より, "\n    r"$\\ker \\Delta=\\operatorname{Im}H="\n    r"\\pi_{7}^{5}$ である."\n  )\n  delta_zero = (\n    r"$\\Delta: \\pi_{7}^{5} \\to \\pi_{5}^{2}$ は零写像である."\n  )\n  injective = (\n    r"$E: \\pi_{5}^{2} \\to \\pi_{6}^{3}$ は単射である."\n  )\n\n  assert full_exactness in body\n  assert eta6_definition in body\n  assert "[R5]より" in body\n  assert "[R3]より" in body\n  assert pi7_5 in body\n  assert surjective in body\n  assert kernel_reason in body\n  assert delta_zero in body\n  assert injective in body\n  assert (\n    r"H\\left(\\nu\'\\eta_{6}\\right)"\n    in body\n  )\n  assert (\n    r"\\eta_{5}^{2}"\n    in body\n  )\n\n  assert body.index(\n    full_exactness\n  ) < body.index(\n    eta6_definition\n  )\n  assert body.index(\n    eta6_definition\n  ) < body.index(\n    "[R5]より"\n  )\n  assert body.index(\n    "[R5]より"\n  ) < body.index(\n    "[R3]より"\n  )\n  assert body.index(\n    "[R3]より"\n  ) < body.index(\n    surjective\n  )\n  assert body.index(\n    surjective\n  ) < body.index(\n    kernel_reason\n  )\n  assert body.index(\n    kernel_reason\n  ) < body.index(\n    delta_zero\n  )\n  assert body.index(\n    delta_zero\n  ) < body.index(\n    injective\n  )\n'
TEST3 = 'def test_phase157_r19_pi6_3_uses_canonical_reference_consequences():\n  _, body = _reference_and_body()\n\n  assert (\n    r"$2\\nu\' = \\eta_{3}^{3}"\n    in body\n  )\n  assert (\n    r"$H\\left(\\nu\'\\right) = \\eta_{5}"\n    in body\n    or r"$H\\left(\\nu\'\\right)=\\eta_{5}"\n    in body\n  )\n  assert (\n    "[R4]より" in body\n  )\n  assert (\n    r"$\\pi_{6}^{5} = \\mathbb{Z}/2\\{\\eta_{5}\\}$."\n    in body\n  )\n\n  forbidden = (\n    "`TodaEtaFamilyDefinitionStatement`",\n    "`TodaDeltaMap`",\n    "`ScalarGreaterEqualStatement`",\n    "`TodaPrimaryGroupMembershipStatement`",\n    r"$E^{2}\\eta_{3} = \\eta_{5}\\tag{5}$.",\n    r"\\eta_{2}\\eta_{3}\\eta_{4}",\n    r"\\eta_{3}\\eta_{4}\\eta_{5}",\n  )\n\n  for text in forbidden:\n    assert text not in body\n'
NEW_TEST = 'from toda_calculation_facade import (\n  build_standard_toda_report,\n)\nfrom toda_group_proof_narrative_renderer import (\n  render_toda_group_proof_narrative_markdown,\n)\nfrom toda_group_proof_presentation import (\n  build_toda_group_proof_presentation,\n)\nfrom toda_group_result_proof_replay import (\n  build_toda_group_result_proof_replay,\n)\n\n\ndef _render_pi6_3_r20() -> str:\n  report = build_standard_toda_report(\n    n=3,\n    k=3,\n  )\n  group_result = (\n    report\n    .candidates[0]\n    .source_candidate\n    .group_result\n  )\n  replay = build_toda_group_result_proof_replay(\n    group_result,\n    max_depth=2,\n  )\n  presentation = build_toda_group_proof_presentation(\n    replay\n  )\n\n  return render_toda_group_proof_narrative_markdown(\n    presentation\n  )\n\n\ndef test_phase157_r20_reference_dependencies_are_recovered_from_graph():\n  rendered = _render_pi6_3_r20()\n\n  for reference in (\n    "Proposition 5.6",\n    "(5.3)",\n    "Proposition 5.3",\n    "Proposition 5.1",\n    "Proposition 2.2",\n  ):\n    assert reference in rendered\n\n  assert (\n    rendered.index(\n      "[R5]より"\n    )\n    < rendered.index(\n      "[R3]より"\n    )\n  )\n\n\ndef test_phase157_r20_eta_family_is_canonicalized_generically():\n  rendered = _render_pi6_3_r20()\n\n  assert r"\\eta_{2}^{3}" in rendered\n  assert r"\\eta_{3}^{3}" in rendered\n  assert r"\\eta_{5}" in rendered\n\n  assert (\n    r"\\eta_{2}\\eta_{3}\\eta_{4}"\n    not in rendered\n  )\n  assert (\n    r"\\eta_{3}\\eta_{4}\\eta_{5}"\n    not in rendered\n  )\n  assert (\n    r"E^{2}\\eta_{3}"\n    not in rendered\n  )\n'


def function_range(
  source: str,
  name: str,
) -> tuple[int, int]:
  tree = ast.parse(
    source
  )
  lines = source.splitlines(
    keepends=True
  )

  for node in tree.body:
    if (
      isinstance(
        node,
        (
          ast.FunctionDef,
          ast.AsyncFunctionDef,
        ),
      )
      and node.name == name
    ):
      start = sum(
        len(line)
        for line in lines[
          :node.lineno - 1
        ]
      )
      end = sum(
        len(line)
        for line in lines[
          :node.end_lineno
        ]
      )

      while (
        end < len(source)
        and source[
          end:
          end + 1
        ] == "\n"
      ):
        end += 1

      return (
        start,
        end,
      )

  raise RuntimeError(
    f"function not found: {name}"
  )


def replace_function(
  source: str,
  name: str,
  replacement: str,
) -> str:
  start, end = function_range(
    source,
    name,
  )

  return (
    source[:start]
    + replacement.rstrip()
    + "\n\n\n"
    + source[end:]
  )


def insert_before_function(
  source: str,
  before_name: str,
  addition: str,
) -> str:
  start, _end = function_range(
    source,
    before_name,
  )

  return (
    source[:start]
    + addition.rstrip()
    + "\n\n\n"
    + source[start:]
  )


def ensure_import(
  source: str,
  module: str,
  name: str,
) -> str:
  if module == "re":
    if re.search(
      r"^import re$",
      source,
      flags=re.MULTILINE,
    ):
      return source

    return (
      "import re\n"
      + source
    )

  pattern = re.compile(
    rf"from {re.escape(module)} import \(\n"
    rf"(?P<body>.*?)\n\)",
    flags=re.DOTALL,
  )
  match = pattern.search(
    source
  )

  if match is None:
    raise RuntimeError(
      f"import block not found: {module}"
    )

  body = match.group(
    "body"
  )

  if re.search(
    rf"^\s*{re.escape(name)},\s*$",
    body,
    flags=re.MULTILINE,
  ):
    return source

  new_body = (
    body
    + "\n  "
    + name
    + ","
  )

  return (
    source[:match.start("body")]
    + new_body
    + source[match.end("body"):]
  )


def patch_generic_renderer(
  source: str,
) -> str:
  source = ensure_import(
    source,
    "re",
    "",
  )
  source = ensure_import(
    source,
    "expression",
    "IteratedSuspension",
  )

  source = replace_function(
    source,
    "_render_generic_narrative_expression_latex",
    EXPR_RENDERER,
  )

  if (
    "def _normalize_generic_narrative_statement_latex("
    not in source
  ):
    source = insert_before_function(
      source,
      "_normalize_generic_narrative_step_latex",
      NORMALIZE_STATEMENT,
    )
  else:
    source = replace_function(
      source,
      "_normalize_generic_narrative_statement_latex",
      NORMALIZE_STATEMENT,
    )

  source = replace_function(
    source,
    "_normalize_generic_narrative_step_latex",
    NORMALIZE_STEP,
  )
  source = replace_function(
    source,
    "_render_phase153_r3_6_component_latex",
    COMPONENT_LATEX,
  )

  return source


def patch_contribution_renderer(
  source: str,
) -> str:
  source = replace_function(
    source,
    "insert_toda_group_proof_narrative_hidden_zero_map_premises",
    HIDDEN_ZERO,
  )
  source = replace_function(
    source,
    "insert_toda_group_proof_narrative_adjacent_eta_suspension_bridges",
    ETA_BRIDGE,
  )

  if (
    "def insert_toda_group_proof_narrative_map_property_dependencies("
    not in source
  ):
    source = insert_before_function(
      source,
      "insert_toda_group_proof_narrative_hidden_zero_map_premises",
      MAP_DEPENDENCIES,
    )
  else:
    source = replace_function(
      source,
      "insert_toda_group_proof_narrative_map_property_dependencies",
      MAP_DEPENDENCIES,
    )

  hidden_call = """  rendered = (
    insert_toda_group_proof_narrative_hidden_zero_map_premises(
      presentation,
      rendered,
      reference_entries,
    )
  )
"""
  dependency_call = hidden_call + """  rendered = (
    insert_toda_group_proof_narrative_map_property_dependencies(
      presentation,
      rendered,
      reference_entries,
    )
  )
"""

  if dependency_call not in source:
    if source.count(
      hidden_call
    ) != 1:
      raise RuntimeError(
        "hidden-zero render call was not found exactly once"
      )

    source = source.replace(
      hidden_call,
      dependency_call,
      1,
    )

  forbidden = (
    "_phase157_r19_",
    "is_pi6_3",
    "_phase157_r3_restore_pi6_3_",
  )

  for token in forbidden:
    if token in source:
      raise RuntimeError(
        "target-specific token reappeared: "
        + token
      )

  return source


def patch_r19_test(
  source: str,
) -> str:
  source = replace_function(
    source,
    "test_phase157_r19_pi6_3_delta_zero_has_shallow_dependency_support",
    TEST2,
  )
  source = replace_function(
    source,
    "test_phase157_r19_pi6_3_uses_canonical_reference_consequences",
    TEST3,
  )

  return source


def main() -> int:
  for path in (
    GENERIC_RENDERER,
    CONTRIBUTION_RENDERER,
    R19_TEST,
  ):
    if not path.is_file():
      raise RuntimeError(
        f"missing file: {path}"
      )

  timestamp = datetime.now().strftime(
    "%Y%m%d_%H%M%S"
  )
  backup = (
    ROOT
    / (
      "phase157_r20_repair4_backup_"
      + timestamp
    )
  )
  backup.mkdir(
    parents=True,
    exist_ok=False,
  )

  for path in (
    GENERIC_RENDERER,
    CONTRIBUTION_RENDERER,
    R19_TEST,
  ):
    shutil.copy2(
      path,
      backup / path.name,
    )

  generic_source = (
    GENERIC_RENDERER.read_text(
      encoding="utf-8"
    )
  )
  contribution_source = (
    CONTRIBUTION_RENDERER.read_text(
      encoding="utf-8"
    )
  )
  r19_test_source = (
    R19_TEST.read_text(
      encoding="utf-8"
    )
  )

  generic_source = (
    patch_generic_renderer(
      generic_source
    )
  )
  contribution_source = (
    patch_contribution_renderer(
      contribution_source
    )
  )
  r19_test_source = (
    patch_r19_test(
      r19_test_source
    )
  )

  for path, source in (
    (
      GENERIC_RENDERER,
      generic_source,
    ),
    (
      CONTRIBUTION_RENDERER,
      contribution_source,
    ),
    (
      R19_TEST,
      r19_test_source,
    ),
  ):
    compile(
      source,
      str(
        path
      ),
      "exec",
    )

  compile(
    NEW_TEST,
    str(
      R20_TEST
    ),
    "exec",
  )

  GENERIC_RENDERER.write_text(
    generic_source,
    encoding="utf-8",
    newline="\n",
  )
  CONTRIBUTION_RENDERER.write_text(
    contribution_source,
    encoding="utf-8",
    newline="\n",
  )
  R19_TEST.write_text(
    r19_test_source,
    encoding="utf-8",
    newline="\n",
  )
  R20_TEST.write_text(
    NEW_TEST,
    encoding="utf-8",
    newline="\n",
  )

  print(
    "Phase157-R20 repair4 applied."
  )
  print(
    "Backup:",
    backup,
  )
  print(
    "Architecture preflight:"
  )
  print(
    "  _phase157_r19_:",
    contribution_source.count(
      "_phase157_r19_"
    ),
  )
  print(
    "  is_pi6_3:",
    contribution_source.count(
      "is_pi6_3"
    ),
  )
  print(
    "  pi6 restore:",
    contribution_source.count(
      "_phase157_r3_restore_pi6_3_"
    ),
  )

  return 0


if __name__ == "__main__":
  raise SystemExit(
    main()
  )
