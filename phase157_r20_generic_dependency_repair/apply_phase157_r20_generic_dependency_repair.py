from pathlib import Path
import re
import shutil
from datetime import datetime


ROOT = Path.cwd()

FILES = {
  "hopf_rules": ROOT / "hopf_rules.py",
  "toda_rules": ROOT / "toda_rules.py",
  "phase65": ROOT / "toda_phase65_bootstrap.py",
  "prop58": ROOT / "toda_prop58_zero_bootstrap.py",
  "dependency": ROOT / "toda_proof_dependency.py",
  "semantics": ROOT / "toda_group_proof_narrative_semantics.py",
  "boundary": ROOT / "toda_literature_statement_boundary.py",
  "references": ROOT / "toda_group_proof_narrative_references.py",
  "renderer": ROOT / "toda_group_proof_narrative_contribution_renderer.py",
  "phase65_test": ROOT / "tests" / "test_phase65_equation57_injectivity.py",
  "arch_test": ROOT / "tests" / "test_phase157_r20_generic_dependency_architecture.py",
}

HOPF_PROP22 = 'def toda_prop22_right_inference_rule(\n  alpha,\n  gamma,\n):\n  def conclusion_builder(\n    premises,\n  ):\n    suspended_gamma = Suspension(\n      expression=gamma,\n    )\n\n    return Relation(\n      lhs=MapApplication(\n        map=EHP_H_MAP,\n        expression=Composition(\n          left=alpha,\n          right=suspended_gamma,\n        ),\n      ),\n      rhs=Composition(\n        left=MapApplication(\n          map=EHP_H_MAP,\n          expression=alpha,\n        ),\n        right=suspended_gamma,\n      ),\n      relation_type=RelationType.EQUALITY,\n    )\n\n  return InferenceRule(\n    name="Toda Prop.2.2 right formula",\n    description=(\n      "Toda Prop.2.2 directly gives "\n      "H(alpha o E gamma) "\n      "= H(alpha) o E gamma."\n    ),\n    premise_patterns=(),\n    conclusion_builder=conclusion_builder,\n    literature_reference=LiteratureReference(\n      label="Toda Proposition 2.2",\n      locator="Proposition 2.2",\n    ),\n  )\n'
EQUATION57 = 'def toda_57_nu_prime_eta6_hopf_inference_rule():\n  def guard(\n    premises,\n    bindings,\n  ):\n    hopf_relation = (\n      premises[\n        0\n      ].conclusion\n    )\n\n    eta5_definition = (\n      premises[\n        1\n      ].conclusion\n    )\n\n    eta6_definition = (\n      premises[\n        2\n      ].conclusion\n    )\n\n    prop22_relation = (\n      premises[\n        3\n      ].conclusion\n    )\n\n    nu_prime = HomotopyElement(\n      name="ν′",\n      dimension=3,\n      source=6,\n      target=3,\n      generator=GeneratorSymbol(\n        family="ν",\n        decoration="′",\n      ),\n    )\n\n    canonical_eta_5 = HomotopyElement(\n      name="η₅",\n      dimension=5,\n      source=6,\n      target=5,\n      generator=GeneratorSymbol(\n        family="η",\n        index=5,\n      ),\n    )\n\n    expected_hopf_relation = Relation(\n      lhs=MapApplication(\n        map=EHP_H_MAP,\n        expression=nu_prime,\n      ),\n      rhs=canonical_eta_5,\n      relation_type=RelationType.EQUALITY,\n    )\n\n    if (\n      hopf_relation\n      != expected_hopf_relation\n    ):\n      return False\n\n    if (\n      eta5_definition.index\n      != 5\n    ):\n      return False\n\n    if (\n      eta6_definition.index\n      != 6\n    ):\n      return False\n\n    eta5_definition_element = (\n      eta5_definition.element\n    )\n\n    if not isinstance(\n      eta5_definition_element,\n      HomotopyElement,\n    ):\n      return False\n\n    if (\n      eta5_definition_element.dimension\n      != 5\n    ):\n      return False\n\n    if (\n      eta5_definition_element.source\n      != 6\n    ):\n      return False\n\n    if (\n      eta5_definition_element.target\n      != 5\n    ):\n      return False\n\n    if (\n      eta5_definition_element.generator\n      != GeneratorSymbol(\n        family="η",\n        index=5,\n      )\n    ):\n      return False\n\n    eta6_definition_element = (\n      eta6_definition.element\n    )\n\n    if not isinstance(\n      eta6_definition_element,\n      HomotopyElement,\n    ):\n      return False\n\n    if (\n      eta6_definition_element.dimension\n      != 6\n    ):\n      return False\n\n    if (\n      eta6_definition_element.source\n      != 7\n    ):\n      return False\n\n    if (\n      eta6_definition_element.target\n      != 6\n    ):\n      return False\n\n    if (\n      eta6_definition_element.generator\n      != GeneratorSymbol(\n        family="η",\n        index=6,\n      )\n    ):\n      return False\n\n    eta_2 = HomotopyElement(\n      name="η₂",\n      dimension=2,\n      source=3,\n      target=2,\n      generator=GeneratorSymbol(\n        family="η",\n        index=2,\n      ),\n    )\n\n    if (\n      eta5_definition.iterated_suspension\n      != IteratedSuspension(\n        expression=eta_2,\n        exponent=3,\n      )\n    ):\n      return False\n\n    if (\n      eta6_definition.iterated_suspension\n      != IteratedSuspension(\n        expression=eta_2,\n        exponent=4,\n      )\n    ):\n      return False\n\n    expected_prop22_relation = Relation(\n      lhs=MapApplication(\n        map=EHP_H_MAP,\n        expression=Composition(\n          left=nu_prime,\n          right=Suspension(\n            expression=eta5_definition_element,\n          ),\n        ),\n      ),\n      rhs=Composition(\n        left=MapApplication(\n          map=EHP_H_MAP,\n          expression=nu_prime,\n        ),\n        right=Suspension(\n          expression=eta5_definition_element,\n        ),\n      ),\n      relation_type=RelationType.EQUALITY,\n    )\n\n    if (\n      prop22_relation\n      != expected_prop22_relation\n    ):\n      return False\n\n    return True\n\n  def build_conclusion(\n    premises,\n  ):\n    hopf_relation = (\n      premises[\n        0\n      ].conclusion\n    )\n\n    nu_prime = (\n      hopf_relation\n      .lhs\n      .expression\n    )\n\n    eta_5 = HomotopyElement(\n      name="η₅",\n      dimension=5,\n      source=6,\n      target=5,\n      generator=GeneratorSymbol(\n        family="η",\n        index=5,\n      ),\n    )\n\n    eta_6 = HomotopyElement(\n      name="η₆",\n      dimension=6,\n      source=7,\n      target=6,\n      generator=GeneratorSymbol(\n        family="η",\n        index=6,\n      ),\n    )\n\n    eta_5_squared = Composition(\n      left=eta_5,\n      right=eta_6,\n    )\n\n    return Relation(\n      lhs=MapApplication(\n        map=EHP_H_MAP,\n        expression=Composition(\n          left=nu_prime,\n          right=eta_6,\n        ),\n      ),\n      rhs=eta_5_squared,\n      relation_type=RelationType.EQUALITY,\n    )\n\n  return InferenceRule(\n    name=(\n      "Toda Equation 5.7 "\n      "nu-prime eta_6 Hopf value"\n    ),\n    description=(\n      "Use H(nu-prime)=eta_5, the eta-family "\n      "definitions at indices 5 and 6, and the "\n      "actual Proposition 2.2 right-composition "\n      "proof step.  The result is "\n      "H(nu-prime eta_6)=eta_5 squared."\n    ),\n    premise_patterns=(\n      PremisePattern(\n        proof_rule=ProofRule.INFERENCE,\n        statement_type=Relation,\n        relation_type=(\n          RelationType.EQUALITY\n        ),\n      ),\n      PremisePattern(\n        proof_rule=ProofRule.GIVEN,\n        statement_type=(\n          TodaEtaFamilyDefinitionStatement\n        ),\n      ),\n      PremisePattern(\n        proof_rule=ProofRule.GIVEN,\n        statement_type=(\n          TodaEtaFamilyDefinitionStatement\n        ),\n      ),\n      PremisePattern(\n        proof_rule=ProofRule.INFERENCE,\n        statement_type=Relation,\n        relation_type=(\n          RelationType.EQUALITY\n        ),\n      ),\n    ),\n    conclusion_builder=build_conclusion,\n    match_guard=guard,\n  )\n'
EXCLUDE_ROOT = 'def exclude_toda_group_proof_narrative_root_reference(\n  entries: tuple[\n    TodaGroupProofNarrativeReferenceEntry,\n    ...,\n  ],\n  statement_lines_by_reference_number: dict[\n    int,\n    tuple[\n      str,\n      ...,\n    ],\n  ],\n  root_step: ProofStep,\n) -> tuple[\n  tuple[\n    TodaGroupProofNarrativeReferenceEntry,\n    ...,\n  ],\n  dict[\n    int,\n    tuple[\n      str,\n      ...,\n    ],\n  ],\n]:\n  if not isinstance(entries, tuple):\n    raise TypeError("entries must be a tuple")\n\n  if not all(\n    isinstance(\n      entry,\n      TodaGroupProofNarrativeReferenceEntry,\n    )\n    for entry in entries\n  ):\n    raise TypeError(\n      "entries must contain only "\n      "TodaGroupProofNarrativeReferenceEntry objects"\n    )\n\n  if not isinstance(\n    statement_lines_by_reference_number,\n    dict,\n  ):\n    raise TypeError(\n      "statement_lines_by_reference_number must be a dict"\n    )\n\n  if not isinstance(\n    root_step,\n    ProofStep,\n  ):\n    raise TypeError(\n      "root_step must be a ProofStep"\n    )\n\n  root_reference = (\n    extract_toda_group_proof_step_literature_reference(\n      root_step\n    )\n  )\n\n  if root_reference is None:\n    return (\n      entries,\n      statement_lines_by_reference_number,\n    )\n\n  root_boundary = (\n    classify_toda_literature_statement_step(\n      root_step\n    )\n  )\n\n  retained_entries = []\n\n  for entry in entries:\n    if not _same_toda_group_proof_literature_reference(\n      entry.reference,\n      root_reference,\n    ):\n      retained_entries.append(\n        entry\n      )\n      continue\n\n    if (\n      root_boundary is None\n      or root_boundary.classification\n      is not TodaLiteratureStatementClassification.FIXED_STATEMENT\n      or root_boundary.component_key is None\n    ):\n      continue\n\n    eligible_steps = []\n\n    for proof_step in entry.proof_steps:\n      boundary = (\n        classify_toda_literature_statement_step(\n          proof_step\n        )\n      )\n\n      if (\n        boundary is None\n        or boundary.classification\n        is not TodaLiteratureStatementClassification.FIXED_STATEMENT\n        or boundary.reference_locator\n        != root_boundary.reference_locator\n        or boundary.component_key is None\n      ):\n        continue\n\n      component = get_toda_fixed_statement_component(\n        boundary.reference_locator,\n        boundary.component_key,\n      )\n\n      if not (\n        is_toda_fixed_statement_component_reference_eligible(\n          component,\n          root_boundary.reference_locator,\n          root_boundary.component_key,\n        )\n      ):\n        continue\n\n      eligible_steps.append(\n        proof_step\n      )\n\n    if eligible_steps:\n      retained_entries.append(\n        replace(\n          entry,\n          proof_steps=tuple(\n            eligible_steps\n          ),\n        )\n      )\n\n  retained_entries = tuple(\n    retained_entries\n  )\n\n  number_map = {\n    entry.number: new_number\n    for new_number, entry in enumerate(\n      retained_entries,\n      start=1,\n    )\n  }\n\n  filtered_entries = tuple(\n    replace(\n      entry,\n      number=number_map[\n        entry.number\n      ],\n    )\n    for entry in retained_entries\n  )\n\n  filtered_statement_lines = {\n    number_map[\n      entry.number\n    ]: statement_lines_by_reference_number[\n      entry.number\n    ]\n    for entry in retained_entries\n    if entry.number\n    in statement_lines_by_reference_number\n  }\n\n  return (\n    filtered_entries,\n    filtered_statement_lines,\n  )\n'
HIDDEN_ZERO = 'def insert_toda_group_proof_narrative_hidden_zero_map_premises(\n  presentation: TodaGroupProofPresentation,\n  markdown: str,\n  reference_entries=(),\n) -> str:\n  if not isinstance(\n    presentation,\n    TodaGroupProofPresentation,\n  ):\n    raise TypeError(\n      "presentation must be a TodaGroupProofPresentation"\n    )\n\n  if not isinstance(\n    markdown,\n    str,\n  ):\n    raise TypeError(\n      "markdown must be a str"\n    )\n\n  if not isinstance(\n    reference_entries,\n    tuple,\n  ):\n    raise TypeError(\n      "reference_entries must be a tuple"\n    )\n\n  paragraphs = markdown.split(\n    "\\n\\n"\n  )\n\n  def match_key(\n    paragraph: str,\n  ) -> str:\n    stripped = paragraph.strip()\n\n    if stripped.startswith(\n      "[R"\n    ):\n      marker_end = stripped.find(\n        "]より, "\n      )\n\n      if marker_end >= 0:\n        stripped = stripped[\n          marker_end\n          + len(\n            "]より, "\n          ):\n        ]\n\n    return (\n      _phase157_r11_reference_statement_match_key(\n        stripped\n      )\n    )\n\n  def visible_index(\n    proof_step: ProofStep,\n  ) -> int | None:\n    rendered = (\n      _render_generic_narrative_step(\n        proof_step\n      )\n    )\n\n    if not rendered:\n      return None\n\n    target_key = (\n      _phase157_r11_reference_statement_match_key(\n        rendered\n      )\n    )\n\n    matches = tuple(\n      index\n      for index, paragraph in enumerate(\n        paragraphs\n      )\n      if match_key(\n        paragraph\n      ) == target_key\n    )\n\n    if len(matches) != 1:\n      return None\n\n    return matches[0]\n\n  def map_latex(\n    group_map,\n  ) -> str | None:\n    name = getattr(\n      group_map,\n      "name",\n      None,\n    )\n\n    if name is None:\n      return None\n\n    if name in (\n      "Δ",\n      "Delta",\n    ):\n      return r"\\Delta"\n\n    return str(\n      name\n    )\n\n  def exactness_reason(\n    zero_step: ProofStep,\n  ) -> str | None:\n    surjective_step = next(\n      (\n        premise\n        for premise in zero_step.premises\n        if (\n          "全射である."\n          in (\n            _render_generic_narrative_step(\n              premise\n            )\n            or ""\n          )\n        )\n      ),\n      None,\n    )\n\n    exactness_step = next(\n      (\n        premise\n        for premise in zero_step.premises\n        if classify_toda_proof_step_role(\n          premise\n        )\n        in (\n          TodaProofDependencyRole.EHP_EXACTNESS,\n          TodaProofDependencyRole.EHP_WINDOW,\n        )\n      ),\n      None,\n    )\n\n    if (\n      surjective_step is None\n      or exactness_step is None\n    ):\n      return None\n\n    exactness = (\n      exactness_step.conclusion\n    )\n    window = getattr(\n      exactness,\n      "window",\n      None,\n    )\n\n    if window is None:\n      return None\n\n    surjective_map = getattr(\n      surjective_step.conclusion,\n      "map",\n      None,\n    )\n    zero_map = getattr(\n      zero_step.conclusion,\n      "map",\n      None,\n    )\n\n    if (\n      surjective_map is None\n      or zero_map is None\n    ):\n      return None\n\n    if (\n      getattr(\n        surjective_map,\n        "source_group",\n        None,\n      )\n      != window.source_term\n      or getattr(\n        surjective_map,\n        "target_group",\n        None,\n      )\n      != window.middle_term\n      or getattr(\n        zero_map,\n        "source_group",\n        None,\n      )\n      != window.middle_term\n      or getattr(\n        zero_map,\n        "target_group",\n        None,\n      )\n      != window.target_term\n    ):\n      return None\n\n    first_map = map_latex(\n      window.first_map\n    )\n    second_map = map_latex(\n      window.second_map\n    )\n\n    if (\n      first_map is None\n      or second_map is None\n    ):\n      return None\n\n    return (\n      "完全性より, "\n      r"$\\ker "\n      + second_map\n      + r"=\\operatorname{Im}"\n      + first_map\n      + "="\n      + render_toda_primary_group_latex(\n        window.middle_term\n      )\n      + "$ である."\n    )\n\n  candidate_zero_steps = []\n  seen_zero_step_ids = set()\n\n  for node in presentation.nodes:\n    for proof_step in (\n      node.proof_step,\n      *node.proof_step.premises,\n    ):\n      rendered = (\n        _render_generic_narrative_step(\n          proof_step\n        )\n      )\n\n      if (\n        not rendered\n        or "零写像である."\n        not in rendered\n      ):\n        continue\n\n      proof_step_id = id(\n        proof_step\n      )\n\n      if proof_step_id in seen_zero_step_ids:\n        continue\n\n      seen_zero_step_ids.add(\n        proof_step_id\n      )\n      candidate_zero_steps.append(\n        proof_step\n      )\n\n  for zero_step in candidate_zero_steps:\n    zero_line = (\n      _render_generic_narrative_step(\n        zero_step\n      )\n    )\n\n    if not zero_line:\n      continue\n\n    zero_index = visible_index(\n      zero_step\n    )\n\n    if zero_index is None:\n      consumer_index = next(\n        (\n          visible_index(\n            node.proof_step\n          )\n          for node in presentation.nodes\n          if zero_step in node.proof_step.premises\n          and visible_index(\n            node.proof_step\n          )\n          is not None\n        ),\n        None,\n      )\n\n      if consumer_index is None:\n        continue\n\n      paragraphs.insert(\n        consumer_index,\n        zero_line,\n      )\n      zero_index = consumer_index\n\n    reason = exactness_reason(\n      zero_step\n    )\n\n    if reason is None:\n      continue\n\n    if any(\n      paragraph.strip() == reason\n      for paragraph in paragraphs\n    ):\n      continue\n\n    zero_index = next(\n      (\n        index\n        for index, paragraph in enumerate(\n          paragraphs\n        )\n        if match_key(\n          paragraph\n        )\n        == match_key(\n          zero_line\n        )\n      ),\n      zero_index,\n    )\n\n    paragraphs.insert(\n      zero_index,\n      reason,\n    )\n\n  return "\\n\\n".join(\n    paragraphs\n  )\n'
GENERIC_HELPERS = 'def _toda_group_proof_narrative_map_name_latex(\n  group_map,\n) -> str | None:\n  name = getattr(\n    group_map,\n    "name",\n    None,\n  )\n\n  if name is None:\n    return None\n\n  if name in (\n    "Δ",\n    "Delta",\n  ):\n    return r"\\Delta"\n\n  return str(\n    name\n  )\n\n\ndef merge_toda_group_proof_narrative_adjacent_ehp_exactness_windows(\n  presentation: TodaGroupProofPresentation,\n  markdown: str,\n) -> str:\n  if not isinstance(\n    presentation,\n    TodaGroupProofPresentation,\n  ):\n    raise TypeError(\n      "presentation must be a TodaGroupProofPresentation"\n    )\n\n  if not isinstance(\n    markdown,\n    str,\n  ):\n    raise TypeError(\n      "markdown must be a str"\n    )\n\n  paragraphs = markdown.split(\n    "\\n\\n"\n  )\n  exactness_steps = tuple(\n    node.proof_step\n    for node in presentation.nodes\n    if classify_toda_proof_step_role(\n      node.proof_step\n    )\n    is TodaProofDependencyRole.EHP_EXACTNESS\n  )\n\n  for left_step in exactness_steps:\n    left_window = getattr(\n      left_step.conclusion,\n      "window",\n      None,\n    )\n\n    if left_window is None:\n      continue\n\n    for right_step in exactness_steps:\n      if right_step is left_step:\n        continue\n\n      right_window = getattr(\n        right_step.conclusion,\n        "window",\n        None,\n      )\n\n      if right_window is None:\n        continue\n\n      if not (\n        left_window.middle_term\n        == right_window.source_term\n        and left_window.target_term\n        == right_window.middle_term\n        and _toda_group_proof_narrative_map_name_latex(\n          left_window.second_map\n        )\n        == _toda_group_proof_narrative_map_name_latex(\n          right_window.first_map\n        )\n      ):\n        continue\n\n      left_line = (\n        _render_generic_narrative_step(\n          left_step\n        )\n      )\n      right_line = (\n        _render_generic_narrative_step(\n          right_step\n        )\n      )\n\n      left_index = next(\n        (\n          index\n          for index, paragraph in enumerate(\n            paragraphs\n          )\n          if paragraph.strip()\n          == left_line.strip()\n        ),\n        None,\n      )\n      right_index = next(\n        (\n          index\n          for index, paragraph in enumerate(\n            paragraphs\n          )\n          if paragraph.strip()\n          == right_line.strip()\n        ),\n        None,\n      )\n\n      if (\n        left_index is None\n        or right_index is None\n      ):\n        continue\n\n      first_map = (\n        _toda_group_proof_narrative_map_name_latex(\n          left_window.first_map\n        )\n      )\n      second_map = (\n        _toda_group_proof_narrative_map_name_latex(\n          left_window.second_map\n        )\n      )\n      third_map = (\n        _toda_group_proof_narrative_map_name_latex(\n          right_window.second_map\n        )\n      )\n\n      if None in (\n        first_map,\n        second_map,\n        third_map,\n      ):\n        continue\n\n      merged = (\n        "$"\n        + render_toda_primary_group_latex(\n          left_window.source_term\n        )\n        + r" \\xrightarrow{"\n        + first_map\n        + "} "\n        + render_toda_primary_group_latex(\n          left_window.middle_term\n        )\n        + r" \\xrightarrow{"\n        + second_map\n        + "} "\n        + render_toda_primary_group_latex(\n          left_window.target_term\n        )\n        + r" \\xrightarrow{"\n        + third_map\n        + "} "\n        + render_toda_primary_group_latex(\n          right_window.target_term\n        )\n        + "$ は完全である."\n      )\n\n      insertion_index = min(\n        left_index,\n        right_index,\n      )\n\n      for index in sorted(\n        (\n          left_index,\n          right_index,\n        ),\n        reverse=True,\n      ):\n        paragraphs.pop(\n          index\n        )\n\n      paragraphs.insert(\n        insertion_index,\n        merged,\n      )\n\n      return "\\n\\n".join(\n        paragraphs\n      )\n\n  return markdown\n\n\ndef insert_toda_group_proof_narrative_adjacent_eta_suspension_bridges(\n  presentation: TodaGroupProofPresentation,\n  markdown: str,\n) -> str:\n  if not isinstance(\n    presentation,\n    TodaGroupProofPresentation,\n  ):\n    raise TypeError(\n      "presentation must be a TodaGroupProofPresentation"\n    )\n\n  if not isinstance(\n    markdown,\n    str,\n  ):\n    raise TypeError(\n      "markdown must be a str"\n    )\n\n  paragraphs = markdown.split(\n    "\\n\\n"\n  )\n\n  for node in presentation.nodes:\n    definition_steps = tuple(\n      premise\n      for premise in node.proof_step.premises\n      if type(\n        premise.conclusion\n      ).__name__\n      == "TodaEtaFamilyDefinitionStatement"\n    )\n\n    if len(\n      definition_steps\n    ) < 2:\n      continue\n\n    ordered = tuple(\n      sorted(\n        definition_steps,\n        key=lambda step: (\n          step.conclusion.index\n        ),\n      )\n    )\n\n    for lower_step, upper_step in zip(\n      ordered,\n      ordered[\n        1:\n      ],\n    ):\n      lower = lower_step.conclusion\n      upper = upper_step.conclusion\n\n      if (\n        not isinstance(\n          lower.index,\n          int,\n        )\n        or isinstance(\n          lower.index,\n          bool,\n        )\n        or not isinstance(\n          upper.index,\n          int,\n        )\n        or isinstance(\n          upper.index,\n          bool,\n        )\n        or upper.index\n        != lower.index + 1\n      ):\n        continue\n\n      bridge = (\n        "$"\n        + render_toda_expression_latex(\n          upper.element\n        )\n        + "=E"\n        + render_toda_expression_latex(\n          lower.element\n        )\n        + "$ である."\n      )\n\n      if any(\n        paragraph.strip() == bridge\n        for paragraph in paragraphs\n      ):\n        continue\n\n      dependent_line = (\n        _render_generic_narrative_step(\n          node.proof_step\n        )\n      )\n      dependent_index = next(\n        (\n          index\n          for index, paragraph in enumerate(\n            paragraphs\n          )\n          if paragraph.strip()\n          == dependent_line.strip()\n        ),\n        None,\n      )\n\n      if dependent_index is None:\n        continue\n\n      paragraphs.insert(\n        dependent_index,\n        bridge,\n      )\n\n  return "\\n\\n".join(\n    paragraphs\n  )\n'
ARCH_TEST = 'from pathlib import Path\n\nfrom hopf_rules import (\n  toda_prop22_right_inference_rule,\n)\nfrom tests.test_phase65_equation57_injectivity import (\n  build_phase65_3_data,\n)\n\n\ndef test_phase157_r20_prop22_is_first_class_literature_provenance():\n  rule = toda_prop22_right_inference_rule(\n    alpha=build_phase65_3_data()["nu_prime"],\n    gamma=build_phase65_3_data()["eta_5"],\n  )\n\n  assert rule.literature_reference is not None\n  assert (\n    rule.literature_reference.locator\n    == "Proposition 2.2"\n  )\n\n\ndef test_phase157_r20_equation57_depends_on_actual_prop22_step():\n  data = build_phase65_3_data()\n\n  assert (\n    data["prop22_step"]\n    in data["equation57_step"].premises\n  )\n  assert (\n    data["prop22_step"]\n    .inference_rule\n    .literature_reference\n    .locator\n    == "Proposition 2.2"\n  )\n\n\ndef test_phase157_r20_contribution_renderer_has_no_pi6_target_specialization():\n  source = Path(\n    "toda_group_proof_narrative_contribution_renderer.py"\n  ).read_text(\n    encoding="utf-8"\n  )\n\n  assert "_phase157_r19_" not in source\n  assert (\n    "filter_phase157_r3_pi6_3_reference_entries"\n    not in source\n  )\n  assert "is_pi6_3" not in source\n\n\ndef test_phase157_r20_reference_selection_has_no_pi6_root_specialization():\n  source = Path(\n    "toda_group_proof_narrative_references.py"\n  ).read_text(\n    encoding="utf-8"\n  )\n\n  assert "_phase157_r3_is_pi6_3_root" not in source\n  assert (\n    "filter_phase157_r3_pi6_3_reference_entries"\n    not in source\n  )\n'


def replace_function(source, name, replacement):
  marker = f"def {name}("
  start = source.find(marker)
  if start < 0:
    raise RuntimeError(f"function not found: {name}")

  match = re.search(
    r"^(?:def |class |@dataclass)",
    source[start + len(marker):],
    flags=re.MULTILINE,
  )
  if match is None:
    end = len(source)
  else:
    end = start + len(marker) + match.start()

  return (
    source[:start]
    + replacement.rstrip()
    + "\n\n\n"
    + source[end:]
  )


def remove_function_if_present(source, name):
  marker = f"def {name}("
  if marker not in source:
    return source
  return replace_function(source, name, "")


def remove_functions_by_prefix(source, prefix):
  while True:
    match = re.search(
      rf"^def {re.escape(prefix)}[A-Za-z0-9_]*\(",
      source,
      flags=re.MULTILINE,
    )
    if match is None:
      return source

    name_start = match.start() + len("def ")
    name_end = source.find("(", name_start)
    name = source[name_start:name_end]
    source = remove_function_if_present(
      source,
      name,
    )


def ensure_import_block(source, block, before):
  if block.strip() in source:
    return source
  index = source.find(before)
  if index < 0:
    raise RuntimeError(
      f"import insertion marker not found: {before}"
    )
  return (
    source[:index]
    + block
    + "\n"
    + source[index:]
  )


def patch_phase65_source(source):
  source = ensure_import_block(
    source,
    "from hopf_rules import (\n"
    "  toda_prop22_right_inference_rule,\n"
    ")\n",
    "from map_facts import (",
  )

  marker = "  equation57_result = (\n"
  if marker not in source:
    raise RuntimeError(
      "phase65 equation57 result marker not found"
    )

  insertion = """  hopf_relation = (
    hopf_nu_prime_step.conclusion
  )
  prop22_rule = (
    toda_prop22_right_inference_rule(
      alpha=(
        hopf_relation
        .lhs
        .expression
      ),
      gamma=hopf_relation.rhs,
    )
  )

"""
  if "  prop22_rule = (" not in source:
    source = source.replace(
      marker,
      insertion + marker,
      1,
    )

  old = """      (
        toda_57_nu_prime_eta6_hopf_inference_rule(),
"""
  new = """      (
        prop22_rule,
        toda_57_nu_prime_eta6_hopf_inference_rule(),
"""
  if old not in source:
    raise RuntimeError(
      "phase65 inference-rule tuple marker not found"
    )
  source = source.replace(
    old,
    new,
    1,
  )
  return source


def patch_prop58_source(source):
  source = ensure_import_block(
    source,
    "from hopf_rules import (\n"
    "  toda_prop22_right_inference_rule,\n"
    ")\n",
    "from map_facts import (",
  )

  function_marker = "def _build_equation57_steps("
  function_start = source.find(
    function_marker
  )
  if function_start < 0:
    raise RuntimeError(
      "prop58 equation57 builder not found"
    )

  result_marker = "  result = run_inference_until_stable_with_history(\n"
  result_index = source.find(
    result_marker,
    function_start,
  )
  if result_index < 0:
    raise RuntimeError(
      "prop58 result marker not found"
    )

  if (
    "prop22_rule = ("
    not in source[
      function_start:
      result_index
    ]
  ):
    insertion = """  hopf_relation = (
    support[
      "hopf_nu_prime_step"
    ].conclusion
  )
  prop22_rule = (
    toda_prop22_right_inference_rule(
      alpha=(
        hopf_relation
        .lhs
        .expression
      ),
      gamma=hopf_relation.rhs,
    )
  )

"""
    source = (
      source[:result_index]
      + insertion
      + source[result_index:]
    )

  tuple_marker = """    (
      toda_57_nu_prime_eta6_hopf_inference_rule(),
"""
  tuple_index = source.find(
    tuple_marker,
    function_start,
  )
  if tuple_index < 0:
    raise RuntimeError(
      "prop58 inference tuple marker not found"
    )

  source = (
    source[:tuple_index]
    + source[
      tuple_index:
    ].replace(
      tuple_marker,
      """    (
      prop22_rule,
      toda_57_nu_prime_eta6_hopf_inference_rule(),
""",
      1,
    )
  )
  return source


def patch_dependency_source(source):
  names = (
    "TodaDeltaZeroStatement",
    "TodaEtaFamilyDefinitionStatement",
    "TodaSuspensionInjectiveStatement",
  )

  for name in names:
    if f"  {name},\n" in source:
      continue

    marker = "from toda_rules import (\n"
    index = source.find(marker)
    if index < 0:
      raise RuntimeError(
        "toda_proof_dependency toda_rules import not found"
      )

    insert_at = index + len(marker)
    source = (
      source[:insert_at]
      + f"  {name},\n"
      + source[insert_at:]
    )

  old_tuple = """    (
      TodaDeltaImageUpToSignStatement,
      TodaDeltaInjectiveStatement,
      TodaHopfInvariantSurjectiveStatement,
      TodaHopfInvariantZeroStatement,
      TodaSuspensionSurjectiveStatement,
    ),
"""
  new_tuple = """    (
      TodaDeltaImageUpToSignStatement,
      TodaDeltaInjectiveStatement,
      TodaDeltaZeroStatement,
      TodaHopfInvariantSurjectiveStatement,
      TodaHopfInvariantZeroStatement,
      TodaSuspensionInjectiveStatement,
      TodaSuspensionSurjectiveStatement,
    ),
"""
  if old_tuple not in source:
    raise RuntimeError(
      "map-property classification tuple not found"
    )
  source = source.replace(
    old_tuple,
    new_tuple,
    1,
  )

  old_def = """  if isinstance(
    conclusion,
    TodaNuFamilyDefinitionStatement,
  ):
"""
  new_def = """  if isinstance(
    conclusion,
    (
      TodaEtaFamilyDefinitionStatement,
      TodaNuFamilyDefinitionStatement,
    ),
  ):
"""
  if old_def not in source:
    raise RuntimeError(
      "definition classification marker not found"
    )
  source = source.replace(
    old_def,
    new_def,
    1,
  )
  return source


def patch_semantics_source(source):
  source = ensure_import_block(
    source,
    "from toda_literature_statement_boundary import (\n"
    "  TodaLiteratureStatementClassification,\n"
    "  classify_toda_literature_statement_step,\n"
    ")\n",
    "from toda_proof_dependency import (",
  )

  marker = "  changed = True\n\n  while changed:\n"
  index = source.find(
    marker
  )
  if index < 0:
    raise RuntimeError(
      "semantic closure fixed-point marker not found"
    )

  generic_closure = """  map_property_frontier = [
    node.proof_step
    for node in provenance.nodes
    if (
      id(
        node.proof_step
      )
      in selected_step_ids
      and classify_toda_proof_step_role(
        node.proof_step
      )
      is TodaProofDependencyRole.MAP_PROPERTY
    )
  ]
  expanded_map_dependency_ids = set()

  while map_property_frontier:
    current_step = map_property_frontier.pop()
    current_step_id = id(
      current_step
    )

    if (
      current_step_id
      in expanded_map_dependency_ids
    ):
      continue

    expanded_map_dependency_ids.add(
      current_step_id
    )

    current_boundary = (
      classify_toda_literature_statement_step(
        current_step
      )
    )

    if (
      current_boundary is not None
      and current_boundary.classification
      is TodaLiteratureStatementClassification.FIXED_STATEMENT
    ):
      continue

    for edge in edges_by_parent_step_id.get(
      current_step_id,
      (),
    ):
      premise_step = edge.premise_step
      premise_step_id = id(
        premise_step
      )

      selected_step_ids.add(
        premise_step_id
      )

      premise_boundary = (
        classify_toda_literature_statement_step(
          premise_step
        )
      )

      if (
        premise_boundary is not None
        and premise_boundary.classification
        is TodaLiteratureStatementClassification.FIXED_STATEMENT
      ):
        continue

      premise_role = (
        classify_toda_proof_step_role(
          premise_step
        )
      )

      if premise_role in (
        TodaProofDependencyRole.MAP_PROPERTY,
        TodaProofDependencyRole.RELATION,
        TodaProofDependencyRole.EHP_EXACTNESS,
        TodaProofDependencyRole.EHP_WINDOW,
      ):
        map_property_frontier.append(
          premise_step
        )

"""
  if (
    "expanded_map_dependency_ids"
    not in source
  ):
    source = (
      source[:index]
      + generic_closure
      + source[index:]
    )

  return source


def patch_boundary_source(source):
  component_block = """
_PROPOSITION_22_COMPONENTS = (
  TodaFixedStatementComponent(
    reference_locator="Proposition 2.2",
    component_key="hopf_right_composition_formula",
    statement_role=TodaLiteratureStatementRole.RELATION,
    order=None,
    range_text=None,
    range_is_explicit_in_current_aggregate=True,
  ),
)


"""
  marker = "_PROPOSITION_51_COMPONENTS = ("
  if "_PROPOSITION_22_COMPONENTS" not in source:
    index = source.find(marker)
    if index < 0:
      raise RuntimeError(
        "Proposition 5.1 component marker not found"
      )
    source = (
      source[:index]
      + component_block
      + source[index:]
    )

  dict_marker = '_FIXED_COMPONENTS_BY_REFERENCE = {\n'
  if (
    '"Proposition 2.2": _PROPOSITION_22_COMPONENTS,'
    not in source
  ):
    source = source.replace(
      dict_marker,
      dict_marker
      + '  "Proposition 2.2": _PROPOSITION_22_COMPONENTS,\n',
      1,
    )

  fixed_marker = "_FIXED_RULE_COMPONENT_KEYS = {\n"
  if (
    '"Toda Prop.2.2 right formula":'
    not in source
  ):
    source = source.replace(
      fixed_marker,
      fixed_marker
      + '  "Toda Prop.2.2 right formula": '
        '"hopf_right_composition_formula",\n',
      1,
    )

  ref_marker = "_REFERENCE_LOCATOR_BY_FIXED_RULE_NAME = {\n"
  if (
    '"Toda Prop.2.2 right formula": "Proposition 2.2",'
    not in source
  ):
    source = source.replace(
      ref_marker,
      ref_marker
      + '  "Toda Prop.2.2 right formula": "Proposition 2.2",\n',
      1,
    )

  # Equation 5.7 is reconstructed from its actual premises in Narrative.
  source = source.replace(
    "    'Toda Equation 5.7 nu-prime eta_6 Hopf value': "
    "'nu_prime_eta6_hopf_relation',\n",
    "",
  )
  source = source.replace(
    "    'Toda Equation 5.7 nu-prime eta_6 Hopf value': "
    "'Equation 5.7',\n",
    "",
  )

  return source


def patch_references_source(source):
  source = remove_function_if_present(
    source,
    "_phase157_r3_is_pi6_3_root",
  )
  source = remove_function_if_present(
    source,
    "filter_phase157_r3_pi6_3_reference_entries",
  )
  source = replace_function(
    source,
    "exclude_toda_group_proof_narrative_root_reference",
    EXCLUDE_ROOT,
  )
  return source


def patch_renderer_imports(source):
  source = source.replace(
    "  filter_phase157_r3_pi6_3_reference_entries,\n",
    "",
  )

  if (
    "from toda_proof_narrative_renderer import (\n"
    not in source
  ):
    marker = "from toda_proof_dependency import (\n"
    block = (
      "from toda_proof_narrative_renderer import (\n"
      "  render_toda_primary_group_latex,\n"
      ")\n"
    )
    index = source.find(marker)
    if index < 0:
      raise RuntimeError(
        "renderer import insertion marker not found"
      )
    source = (
      source[:index]
      + block
      + source[index:]
    )
  elif (
    "  render_toda_primary_group_latex,\n"
    not in source
  ):
    source = source.replace(
      "from toda_proof_narrative_renderer import (\n",
      "from toda_proof_narrative_renderer import (\n"
      "  render_toda_primary_group_latex,\n",
      1,
    )

  if (
    "  render_toda_expression_latex,\n"
    not in source
  ):
    source = source.replace(
      "from toda_human_readable_renderer import (\n"
      "  _render_scalar_latex,\n",
      "from toda_human_readable_renderer import (\n"
      "  _render_scalar_latex,\n"
      "  render_toda_expression_latex,\n",
      1,
    )

  return source


def patch_reference_statement_renderer(source):
  name = "_phase153_r6_render_reference_statement"
  marker = f"def {name}("
  start = source.find(marker)
  if start < 0:
    raise RuntimeError(
      "reference statement renderer not found"
    )
  component_marker = """  component = (
    _phase153_r6_reference_aggregate_component(
"""
  component_index = source.find(
    component_marker,
    start,
  )
  if component_index < 0:
    raise RuntimeError(
      "reference statement component marker not found"
    )

  insertion = """  boundary = (
    classify_toda_literature_statement_step(
      proof_step
    )
  )

  if (
    boundary is not None
    and boundary.classification
    is TodaLiteratureStatementClassification.FIXED_STATEMENT
    and boundary.reference_locator
    == "Proposition 2.2"
    and boundary.component_key
    == "hopf_right_composition_formula"
  ):
    return (
      r"$H(\alpha\circ E\beta) = "
      r"H(\alpha)\circ E\beta$."
    )

"""
  function_slice = source[
    start:
    component_index
  ]
  if "hopf_right_composition_formula" not in function_slice:
    source = (
      source[:component_index]
      + insertion
      + source[component_index:]
    )
  return source


def patch_renderer_source(source):
  source = patch_renderer_imports(
    source
  )
  source = remove_functions_by_prefix(
    source,
    "_phase157_r19_",
  )
  for name in (
    "_phase157_r3_restore_pi6_3_earlier_prop56_reference",
    "_phase157_r3_restore_pi6_3_proof_internal_suspension_isomorphism",
  ):
    source = remove_function_if_present(
      source,
      name,
    )

  source = replace_function(
    source,
    "insert_toda_group_proof_narrative_hidden_zero_map_premises",
    HIDDEN_ZERO,
  )

  hidden_marker = (
    "def insert_toda_group_proof_narrative_hidden_zero_map_premises("
  )
  insert_index = source.find(
    hidden_marker
  )
  if insert_index < 0:
    raise RuntimeError(
      "hidden-zero function insertion point not found"
    )
  if (
    "def merge_toda_group_proof_narrative_adjacent_ehp_exactness_windows("
    not in source
  ):
    source = (
      source[:insert_index]
      + GENERIC_HELPERS.rstrip()
      + "\n\n\n"
      + source[insert_index:]
    )

  source = patch_reference_statement_renderer(
    source
  )

  special_reference_block = """  phase157_r19_reference_entries_before_pi6_filter = (
    reference_entries
  )
  reference_entries = (
    filter_phase157_r3_pi6_3_reference_entries(
      reference_entries,
      presentation.root_step,
    )
  )
  reference_entries = (
    _phase157_r19_restore_prop22_reference_for_pi6_3(
      presentation,
      phase157_r19_reference_entries_before_pi6_filter,
      reference_entries,
    )
  )
"""
  source = source.replace(
    special_reference_block,
    "",
  )

  source = source.replace(
    """  phase157_r3_entries_before_usage_filter = reference_entries
  phase157_r3_lines_before_usage_filter = (
    statement_lines_by_reference_number
  )

""",
    "",
  )

  restore_block_pattern = re.compile(
    r"""
  \(
    reference_entries,
    statement_lines_by_reference_number,
  \) = \(
    _phase157_r3_restore_pi6_3_earlier_prop56_reference\(
.*?
  \)

""",
    flags=re.DOTALL | re.VERBOSE,
  )
  source = restore_block_pattern.sub(
    "",
    source,
    count=1,
  )

  finalizer_pattern = re.compile(
    r"""
  \(
    reference_entries,
    statement_lines_by_reference_number,
    rendered,
  \) = \(
    _phase157_r19_finalize_pi6_3_public_narrative\(
.*?
  \)

  public_statement_lines_by_reference_number = \(
    _phase157_r19_public_reference_statement_lines\(
.*?
  \)
  reference_section = \(
    render_toda_group_proof_narrative_reference_entries_markdown\(
      reference_entries,
      public_statement_lines_by_reference_number,
    \)
  \)
""",
    flags=re.DOTALL | re.VERBOSE,
  )
  replacement = """  reference_section = (
    render_toda_group_proof_narrative_reference_entries_markdown(
      reference_entries,
      statement_lines_by_reference_number,
    )
  )
"""
  source, count = finalizer_pattern.subn(
    replacement,
    source,
    count=1,
  )
  if count == 0:
    # repair variants may already lack this exact block.
    source = source.replace(
      "      public_statement_lines_by_reference_number,\n",
      "      statement_lines_by_reference_number,\n",
    )

  hidden_call = """  rendered = (
    insert_toda_group_proof_narrative_hidden_zero_map_premises(
      presentation,
      rendered,
      reference_entries,
    )
  )
"""
  generic_calls = hidden_call + """  rendered = (
    insert_toda_group_proof_narrative_adjacent_eta_suspension_bridges(
      presentation,
      rendered,
    )
  )
  rendered = (
    merge_toda_group_proof_narrative_adjacent_ehp_exactness_windows(
      presentation,
      rendered,
    )
  )
"""
  if generic_calls not in source:
    if hidden_call not in source:
      raise RuntimeError(
        "hidden-zero call marker not found"
      )
    source = source.replace(
      hidden_call,
      generic_calls,
      1,
    )

  return source


def patch_phase65_test(source):
  source = ensure_import_block(
    source,
    "from hopf_rules import (\n"
    "  toda_prop22_right_inference_rule,\n"
    ")\n",
    "from map_facts import (",
  )

  rule_marker = """  equation57_rule = (
    toda_57_nu_prime_eta6_hopf_inference_rule()
  )
"""
  if "  prop22_rule = (" not in source:
    prop22_block = """  prop22_rule = (
    toda_prop22_right_inference_rule(
      alpha=nu_prime,
      gamma=eta_5,
    )
  )

"""
    source = source.replace(
      rule_marker,
      prop22_block + rule_marker,
      1,
    )

  source = source.replace(
    """  rules = (
    equation57_rule,
""",
    """  rules = (
    prop22_rule,
    equation57_rule,
""",
    1,
  )

  find_marker = """  equation57_step = next(
"""
  if "  prop22_step = next(" not in source:
    find_block = """  prop22_step = next(
    step
    for step in result.steps
    if step.inference_rule == prop22_rule
  )

"""
    source = source.replace(
      find_marker,
      find_block + find_marker,
      1,
    )

  source = source.replace(
    """    "equation57_rule": (
      equation57_rule
    ),
""",
    """    "prop22_rule": (
      prop22_rule
    ),
    "prop22_step": (
      prop22_step
    ),
    "equation57_rule": (
      equation57_rule
    ),
""",
    1,
  )

  old_match = """      data[
        "eta6_definition_step"
      ],
    ),
"""
  new_match = """      data[
        "eta6_definition_step"
      ],
      data[
        "prop22_step"
      ],
    ),
"""
  function_start = source.find(
    "def test_phase65_3_equation57_rule_matches_dependencies"
  )
  function_end = source.find(
    "\ndef ",
    function_start + 5,
  )
  segment = source[
    function_start:
    function_end
  ]
  if '"prop22_step"' not in segment:
    segment = segment.replace(
      old_match,
      new_match,
      1,
    )
    source = (
      source[:function_start]
      + segment
      + source[function_end:]
    )

  prov_start = source.find(
    "def test_phase65_3_equation57_provenance"
  )
  prov_end = source.find(
    "\ndef ",
    prov_start + 5,
  )
  prov_segment = source[
    prov_start:
    prov_end
  ]
  if '"prop22_step"' not in prov_segment:
    prov_segment = prov_segment.replace(
      """      data[
        "eta6_definition_step"
      ],
    )
""",
      """      data[
        "eta6_definition_step"
      ],
      data[
        "prop22_step"
      ],
    )
""",
      1,
    )
    source = (
      source[:prov_start]
      + prov_segment
      + source[prov_end:]
    )

  round_start = source.find(
    "def test_phase65_3_reaches_fixed_point_in_four_rounds"
  )
  if round_start >= 0:
    round_end = source.find(
      "\ndef ",
      round_start + 5,
    )
    if round_end < 0:
      round_end = len(source)
    round_segment = source[
      round_start:
      round_end
    ]
    round_segment = round_segment.replace(
      "def test_phase65_3_reaches_fixed_point_in_four_rounds():",
      "def test_phase65_3_reaches_fixed_point_in_five_rounds():",
      1,
    )
    round_segment = round_segment.replace(
      "assert result.round_count == 4",
      "assert result.round_count == 5",
      1,
    )
    round_segment = round_segment.replace(
      """  assert (
    data[
      "equation57_step"
    ]
    in result.round_results[
      0
    ].new_steps
  )
""",
      """  assert (
    data[
      "prop22_step"
    ]
    in result.round_results[
      0
    ].new_steps
  )

  assert (
    data[
      "equation57_step"
    ]
    in result.round_results[
      1
    ].new_steps
  )
""",
      1,
    )
    round_segment = round_segment.replace(
      """      1
    ].new_steps
""",
      """      2
    ].new_steps
""",
      1,
    )
    round_segment = round_segment.replace(
      """      2
    ].new_steps
""",
      """      3
    ].new_steps
""",
      1,
    )
    round_segment = round_segment.replace(
      """      3
    ].new_steps
""",
      """      4
    ].new_steps
""",
      1,
    )
    source = (
      source[:round_start]
      + round_segment
      + source[round_end:]
    )

  return source


def main():
  for key, path in FILES.items():
    if key == "arch_test":
      continue
    if not path.is_file():
      raise RuntimeError(
        f"missing file: {path}"
      )

  timestamp = datetime.now().strftime(
    "%Y%m%d_%H%M%S"
  )
  backup = ROOT / (
    "phase157_r20_generic_dependency_backup_"
    + timestamp
  )
  backup.mkdir(
    parents=True,
    exist_ok=False,
  )

  for key, path in FILES.items():
    if key == "arch_test":
      continue
    shutil.copy2(
      path,
      backup / path.name,
    )

  sources = {
    key: path.read_text(
      encoding="utf-8"
    )
    for key, path in FILES.items()
    if key != "arch_test"
  }

  sources["hopf_rules"] = replace_function(
    sources["hopf_rules"],
    "toda_prop22_right_inference_rule",
    HOPF_PROP22,
  )
  sources["toda_rules"] = replace_function(
    sources["toda_rules"],
    "toda_57_nu_prime_eta6_hopf_inference_rule",
    EQUATION57,
  )
  sources["phase65"] = patch_phase65_source(
    sources["phase65"]
  )
  sources["prop58"] = patch_prop58_source(
    sources["prop58"]
  )
  sources["dependency"] = patch_dependency_source(
    sources["dependency"]
  )
  sources["semantics"] = patch_semantics_source(
    sources["semantics"]
  )
  sources["boundary"] = patch_boundary_source(
    sources["boundary"]
  )
  sources["references"] = patch_references_source(
    sources["references"]
  )
  sources["renderer"] = patch_renderer_source(
    sources["renderer"]
  )
  sources["phase65_test"] = patch_phase65_test(
    sources["phase65_test"]
  )

  for key, source in sources.items():
    compile(
      source,
      str(
        FILES[
          key
        ]
      ),
      "exec",
    )

  for key, source in sources.items():
    FILES[
      key
    ].write_text(
      source,
      encoding="utf-8",
      newline="\n",
    )

  FILES[
    "arch_test"
  ].write_text(
    ARCH_TEST,
    encoding="utf-8",
    newline="\n",
  )

  compile(
    ARCH_TEST,
    str(
      FILES[
        "arch_test"
      ]
    ),
    "exec",
  )

  renderer_source = sources[
    "renderer"
  ]
  reference_source = sources[
    "references"
  ]

  print("Phase157-R20 generic dependency repair applied.")
  print(f"Backup: {backup}")
  print("Policy preflight:")
  print(
    "  renderer _phase157_r19_ occurrences:",
    renderer_source.count(
      "_phase157_r19_"
    ),
  )
  print(
    "  renderer is_pi6_3 occurrences:",
    renderer_source.count(
      "is_pi6_3"
    ),
  )
  print(
    "  reference pi6 filter occurrences:",
    reference_source.count(
      "filter_phase157_r3_pi6_3_reference_entries"
    ),
  )
  print("Changed:")
  for key in (
    "hopf_rules",
    "toda_rules",
    "phase65",
    "prop58",
    "dependency",
    "semantics",
    "boundary",
    "references",
    "renderer",
    "phase65_test",
    "arch_test",
  ):
    print(
      " ",
      FILES[
        key
      ],
    )


if __name__ == "__main__":
  main()
