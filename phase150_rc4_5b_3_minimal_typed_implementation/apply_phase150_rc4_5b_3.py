from pathlib import Path
import shutil

ROOT = Path.cwd()
PACKAGE = ROOT / "phase150_rc4_5b_3_minimal_typed_implementation"


def replace_once(path, old, new):
  text = path.read_text(encoding="utf-8")
  count = text.count(old)
  if count != 1:
    raise RuntimeError(
      f"{path}: expected one replacement target, found {count}"
    )
  path.write_text(text.replace(old, new, 1), encoding="utf-8")


def patch_semantics():
  path = ROOT / "toda_group_proof_narrative_semantics.py"

  replace_once(
    path,
    "from enum import Enum\n\nfrom proof import (",
    "from enum import Enum\n\n"
    "from expression import (\n"
    "  HomotopyElement,\n"
    ")\n"
    "from proof import (",
  )
  replace_once(
    path,
    "from toda_proof_dependency import (\n"
    "  TodaProofEdge,\n"
    "  extract_toda_recursive_proof_provenance,\n"
    ")\n",
    "from toda_proof_dependency import (\n"
    "  TodaProofEdge,\n"
    "  extract_toda_recursive_proof_provenance,\n"
    ")\n"
    "from toda_rules import (\n"
    "  TodaBracketMembershipStatement,\n"
    ")\n",
  )

  marker = "@dataclass(frozen=True)\nclass TodaGroupProofNarrativeSemanticSidecar:"
  addition = '''@dataclass(frozen=True)
class TodaGroupProofNarrativeReferenceIdentity:
  label: str

  def __post_init__(self) -> None:
    if not isinstance(self.label, str) or not self.label.strip():
      raise TypeError("label must be a non-empty str")


@dataclass(frozen=True)
class TodaGroupProofNarrativeVariableBinding:
  formal_variable: object
  instantiated_expression: object

  def __post_init__(self) -> None:
    if isinstance(self.formal_variable, str):
      raise TypeError(
        "formal_variable must be a mathematical object, not a str"
      )
    if isinstance(self.instantiated_expression, str):
      raise TypeError(
        "instantiated_expression must be a mathematical object, not a str"
      )


@dataclass(frozen=True)
class TodaGroupProofNarrativeReferenceApplicationSemantic:
  dependent_step: ProofStep
  reference: TodaGroupProofNarrativeReferenceIdentity
  bindings: tuple[TodaGroupProofNarrativeVariableBinding, ...]

  def __post_init__(self) -> None:
    if not isinstance(self.dependent_step, ProofStep):
      raise TypeError("dependent_step must be a ProofStep")
    if not isinstance(
      self.reference,
      TodaGroupProofNarrativeReferenceIdentity,
    ):
      raise TypeError(
        "reference must be a TodaGroupProofNarrativeReferenceIdentity"
      )
    if not isinstance(self.bindings, tuple):
      raise TypeError("bindings must be a tuple")
    if not self.bindings:
      raise ValueError("bindings must not be empty")

    seen_formal_variables = set()
    for binding in self.bindings:
      if not isinstance(binding, TodaGroupProofNarrativeVariableBinding):
        raise TypeError(
          "bindings must contain only "
          "TodaGroupProofNarrativeVariableBinding objects"
        )
      key = repr(binding.formal_variable)
      if key in seen_formal_variables:
        raise ValueError(
          "bindings must not contain duplicate formal variables"
        )
      seen_formal_variables.add(key)


'''
  replace_once(path, marker, addition + marker)

  replace_once(
    path,
    "  dependency_semantics: tuple[\n"
    "    TodaGroupProofNarrativeDependencySemantic,\n"
    "    ...,\n"
    "  ] = ()\n",
    "  dependency_semantics: tuple[\n"
    "    TodaGroupProofNarrativeDependencySemantic,\n"
    "    ...,\n"
    "  ] = ()\n"
    "  reference_application_semantics: tuple[\n"
    "    TodaGroupProofNarrativeReferenceApplicationSemantic,\n"
    "    ...,\n"
    "  ] = ()\n",
  )

  replace_once(
    path,
    "    allowed_step_ids = {\n",
    "    if not isinstance(\n"
    "      self.reference_application_semantics,\n"
    "      tuple,\n"
    "    ):\n"
    "      raise TypeError(\n"
    "        \"reference_application_semantics must be a tuple\"\n"
    "      )\n\n"
    "    allowed_step_ids = {\n",
  )

  marker = "\n\n_PREMISE_ROLE_BY_RULE_NAME_AND_INDEX = {"
  validation = '''
    seen_reference_application_keys = set()
    for semantic in self.reference_application_semantics:
      if not isinstance(
        semantic,
        TodaGroupProofNarrativeReferenceApplicationSemantic,
      ):
        raise TypeError(
          "reference_application_semantics must contain only "
          "TodaGroupProofNarrativeReferenceApplicationSemantic objects"
        )
      dependent_step_id = id(semantic.dependent_step)
      if dependent_step_id not in allowed_step_ids:
        raise ValueError(
          "reference application dependent_step must appear "
          "in presentation nodes"
        )
      application_key = (
        dependent_step_id,
        semantic.reference,
      )
      if application_key in seen_reference_application_keys:
        raise ValueError(
          "reference_application_semantics must not contain "
          "duplicate applications"
        )
      seen_reference_application_keys.add(application_key)
'''
  replace_once(path, marker, "\n" + validation + marker)

  marker = "\ndef build_toda_group_proof_narrative_semantic_sidecar(\n"
  helper = '''\ndef _reference_application_semantics(
  step_semantics: tuple[TodaGroupProofNarrativeStepSemantic, ...],
) -> tuple[TodaGroupProofNarrativeReferenceApplicationSemantic, ...]:
  applications = []

  for semantic in step_semantics:
    if (
      semantic.role
      is not TodaGroupProofNarrativeStepSemanticRole.DEFINITION_INTRODUCTION
    ):
      continue

    conclusion = semantic.proof_step.conclusion
    if not isinstance(conclusion, TodaBracketMembershipStatement):
      continue

    concrete_element = conclusion.element
    if not isinstance(concrete_element, HomotopyElement):
      continue

    formal_beta = HomotopyElement(
      name="β",
      dimension=concrete_element.dimension,
      source=concrete_element.source,
      target=concrete_element.target,
    )

    applications.append(
      TodaGroupProofNarrativeReferenceApplicationSemantic(
        dependent_step=semantic.proof_step,
        reference=TodaGroupProofNarrativeReferenceIdentity(
          label="Lemma 5.2",
        ),
        bindings=(
          TodaGroupProofNarrativeVariableBinding(
            formal_variable=formal_beta,
            instantiated_expression=concrete_element,
          ),
        ),
      )
    )

  return tuple(applications)


'''
  replace_once(path, marker, helper + marker)

  old = '''      dependency_semantics=(
        _semantic_dependency_semantics(
          presentation,
          premise_semantics_tuple,
          step_semantics_tuple,
        )
      ),
'''
  new = '''      dependency_semantics=(
        _semantic_dependency_semantics(
          presentation,
          premise_semantics_tuple,
          step_semantics_tuple,
        )
      ),
      reference_application_semantics=(
        _reference_application_semantics(
          step_semantics_tuple,
        )
      ),
'''
  replace_once(path, old, new)


def patch_reasons():
  path = ROOT / "toda_group_proof_narrative_reasons.py"

  replace_once(
    path,
    "  TodaGroupProofNarrativeDependencySemanticRole,\n"
    "  TodaGroupProofNarrativeSemanticSidecar,\n",
    "  TodaGroupProofNarrativeDependencySemanticRole,\n"
    "  TodaGroupProofNarrativeReferenceApplicationSemantic,\n"
    "  TodaGroupProofNarrativeSemanticSidecar,\n",
  )
  replace_once(
    path,
    "  owner_argument_index: int | None = None\n",
    "  owner_argument_index: int | None = None\n"
    "  reference_application: (\n"
    "    TodaGroupProofNarrativeReferenceApplicationSemantic | None\n"
    "  ) = None\n",
  )

  needle = "    if (\n      self.owner_argument_index\n      is not None\n"
  insertion = '''    if (
      self.reference_application is not None
      and not isinstance(
        self.reference_application,
        TodaGroupProofNarrativeReferenceApplicationSemantic,
      )
    ):
      raise TypeError(
        "reference_application must be a "
        "TodaGroupProofNarrativeReferenceApplicationSemantic or None"
      )

    if (
      self.reference_application is not None
      and self.reference_application.dependent_step
      is not self.conclusion_step
    ):
      raise ValueError(
        "reference_application must belong to conclusion_step"
      )

'''
  replace_once(path, needle, insertion + needle)

  replace_once(
    path,
    "  reasons = []\n\n  for dependency in (",
    "  reasons = []\n"
    "  reference_applications_by_step_id = {}\n\n"
    "  for application in semantic_sidecar.reference_application_semantics:\n"
    "    reference_applications_by_step_id.setdefault(\n"
    "      id(application.dependent_step),\n"
    "      [],\n"
    "    ).append(application)\n\n"
    "  for dependency in (",
  )

  replace_once(
    path,
    "    reasons.append(\n      TodaGroupProofNarrativeReason(\n",
    "    matching_applications = reference_applications_by_step_id.get(\n"
    "      id(dependency.dependent_step),\n"
    "      (),\n"
    "    )\n"
    "    reference_application = (\n"
    "      matching_applications[0]\n"
    "      if len(matching_applications) == 1\n"
    "      else None\n"
    "    )\n\n"
    "    reasons.append(\n      TodaGroupProofNarrativeReason(\n",
  )

  replace_once(
    path,
    "        conclusion_step=(\n"
    "          dependency.dependent_step\n"
    "        ),\n"
    "      )\n",
    "        conclusion_step=(\n"
    "          dependency.dependent_step\n"
    "        ),\n"
    "        reference_application=reference_application,\n"
    "      )\n",
  )


def patch_renderer():
  path = ROOT / "toda_group_proof_narrative_reason_renderer.py"

  replace_once(
    path,
    "from toda_group_proof_generic_narrative_renderer import (",
    "from toda_human_readable_renderer import (\n"
    "  render_toda_expression_latex,\n"
    ")\n"
    "from toda_group_proof_generic_narrative_renderer import (",
  )

  old = '''  if (
    reason.kind
    is TodaGroupProofNarrativeReasonKind
    .DEFINITION_APPLICABILITY
  ):
    return (
      "この前提条件を満たすので、"
      "次の定義を用いる."
    )
'''
  new = '''  if (
    reason.kind
    is TodaGroupProofNarrativeReasonKind
    .DEFINITION_APPLICABILITY
  ):
    application = reason.reference_application

    if application is None or len(application.bindings) != 1:
      return (
        "この前提条件を満たすので、"
        "次の定義を用いる."
      )

    binding = application.bindings[0]
    reference_label = application.reference.label
    formal_latex = render_toda_expression_latex(
      binding.formal_variable
    )
    instantiated_latex = render_toda_expression_latex(
      binding.instantiated_expression
    )

    return (
      "この前提条件を満たすので、"
      f"{reference_label} を適用できる.\\n"
      f"{reference_label} の "
      f"${formal_latex}$ を "
      f"${instantiated_latex}$ と定めると、"
    )
'''
  replace_once(path, old, new)


def main():
  patch_semantics()
  print("Patched: toda_group_proof_narrative_semantics.py")
  patch_reasons()
  print("Patched: toda_group_proof_narrative_reasons.py")
  patch_renderer()
  print("Patched: toda_group_proof_narrative_reason_renderer.py")
  shutil.copyfile(
    PACKAGE / "payload" / "tests" / "test_phase150_rc4_5b_3_reference_binding.py",
    ROOT / "tests" / "test_phase150_rc4_5b_3_reference_binding.py",
  )
  print("Wrote: tests/test_phase150_rc4_5b_3_reference_binding.py")
  print("RC4-5B-3 minimal typed implementation applied.")


if __name__ == "__main__":
  main()
