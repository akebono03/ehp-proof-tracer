from __future__ import annotations

import ast
import re
import shutil
from datetime import datetime
from pathlib import Path

ROOT = Path.cwd()

FILES = {
    "phase65": ROOT / "toda_phase65_bootstrap.py",
    "prop58": ROOT / "toda_prop58_zero_bootstrap.py",
    "references": ROOT / "toda_group_proof_narrative_references.py",
    "renderer": ROOT / "toda_group_proof_narrative_contribution_renderer.py",
    "phase65_test": ROOT / "tests" / "test_phase65_equation57_injectivity.py",
    "arch_test": ROOT / "tests" / "test_phase157_r20_generic_dependency_architecture.py",
}

def ensure_import_name(source: str, module: str, name: str) -> str:
    pattern = re.compile(
        rf"from {re.escape(module)} import \(\n(?P<body>.*?)\n\)",
        flags=re.DOTALL,
    )
    match = pattern.search(source)
    if match is None:
        raise RuntimeError(f"import block not found: {module}")
    body = match.group("body")
    if re.search(rf"^\s*{re.escape(name)},\s*$", body, flags=re.MULTILINE):
        return source
    new_body = body + "\n  " + name + ","
    return source[:match.start("body")] + new_body + source[match.end("body"):]

def remove_import_name(source: str, module: str, name: str) -> str:
    pattern = re.compile(
        rf"from {re.escape(module)} import \(\n(?P<body>.*?)\n\)",
        flags=re.DOTALL,
    )
    match = pattern.search(source)
    if match is None:
        return source
    new_body = "\n".join(
        line for line in match.group("body").splitlines()
        if line.strip() != f"{name},"
    )
    return source[:match.start("body")] + new_body + source[match.end("body"):]

def top_level_function_ranges(source: str) -> dict[str, tuple[int, int]]:
    tree = ast.parse(source)
    lines = source.splitlines(keepends=True)
    offsets = [0]
    total = 0
    for line in lines:
        total += len(line)
        offsets.append(total)
    result = {}
    for node in tree.body:
        if isinstance(node, (ast.FunctionDef, ast.AsyncFunctionDef)):
            start = offsets[node.lineno - 1]
            end = offsets[getattr(node, "end_lineno", node.lineno)]
            while end < len(source) and source[end:end + 1] == "\n":
                end += 1
            result[node.name] = (start, end)
    return result

def remove_top_level_functions(source: str, names_or_prefixes) -> str:
    while True:
        ranges = top_level_function_ranges(source)
        match = None
        for name, (start, end) in ranges.items():
            if any(name == item or name.startswith(item) for item in names_or_prefixes):
                match = (start, end)
                break
        if match is None:
            return source
        start, end = match
        source = source[:start] + source[end:]

def replace_once(source: str, old: str, new: str, label: str) -> str:
    count = source.count(old)
    if count != 1:
        raise RuntimeError(f"{label}: expected 1 occurrence, found {count}")
    return source.replace(old, new, 1)

def patch_phase65(source: str) -> str:
    source = ensure_import_name(source, "proof", "apply_inference_match")
    source = ensure_import_name(source, "proof", "find_inference_match")
    source = replace_once(
        source,
        """      (
        prop22_rule,
        toda_57_nu_prime_eta6_hopf_inference_rule(),
        toda_prop56_pi7_3_hopf_surjective_inference_rule(),
        toda_prop56_pi7_5_delta_zero_inference_rule(),
        toda_prop56_pi5_2_suspension_injective_inference_rule(),
      ),
""",
        """      (
        toda_57_nu_prime_eta6_hopf_inference_rule(),
        toda_prop56_pi7_3_hopf_surjective_inference_rule(),
        toda_prop56_pi7_5_delta_zero_inference_rule(),
        toda_prop56_pi5_2_suspension_injective_inference_rule(),
      ),
""",
        "phase65 rules",
    )
    marker = """  equation57_result = (
    run_inference_until_stable_with_history(
"""
    if marker not in source:
        raise RuntimeError("phase65 result marker not found")
    if "  prop22_match = (\n    find_inference_match(" not in source:
        source = source.replace(
            marker,
            """  prop22_match = (
    find_inference_match(
      prop22_rule,
      (),
    )
  )

  if prop22_match is None:
    raise ValueError(
      "Toda Proposition 2.2 must be directly applicable"
    )

  prop22_step = (
    apply_inference_match(
      prop22_match
    )
  )

""" + marker,
            1,
        )
    source = replace_once(
        source,
        """        eta5_definition_step,
        eta6_definition_step,
        h_delta_exactness_step,
""",
        """        eta5_definition_step,
        eta6_definition_step,
        prop22_step,
        h_delta_exactness_step,
""",
        "phase65 premises",
    )
    return source

def patch_prop58(source: str) -> str:
    source = ensure_import_name(source, "proof", "apply_inference_match")
    source = ensure_import_name(source, "proof", "find_inference_match")
    source = replace_once(
        source,
        """    (
      prop22_rule,
      toda_57_nu_prime_eta6_hopf_inference_rule(),
      toda_prop56_pi7_3_hopf_surjective_inference_rule(),
      toda_prop56_pi7_5_delta_zero_inference_rule(),
      toda_prop56_pi5_2_suspension_injective_inference_rule(),
    ),
""",
        """    (
      toda_57_nu_prime_eta6_hopf_inference_rule(),
      toda_prop56_pi7_3_hopf_surjective_inference_rule(),
      toda_prop56_pi7_5_delta_zero_inference_rule(),
      toda_prop56_pi5_2_suspension_injective_inference_rule(),
    ),
""",
        "prop58 rules",
    )
    start = source.find("def _build_equation57_steps(")
    marker = "  result = run_inference_until_stable_with_history(\n"
    idx = source.find(marker, start)
    if idx < 0:
        raise RuntimeError("prop58 result marker not found")
    prefix = source[start:idx]
    if "  prop22_match = (\n    find_inference_match(" not in prefix:
        source = source[:idx] + """  prop22_match = (
    find_inference_match(
      prop22_rule,
      (),
    )
  )

  if prop22_match is None:
    raise ValueError(
      "Toda Proposition 2.2 must be directly applicable"
    )

  prop22_step = (
    apply_inference_match(
      prop22_match
    )
  )

""" + source[idx:]
    source = replace_once(
        source,
        """      eta5_definition_step,
      eta6_definition_step,
      ProofStep(
""",
        """      eta5_definition_step,
      eta6_definition_step,
      prop22_step,
      ProofStep(
""",
        "prop58 premises",
    )
    return source

def patch_phase65_test(source: str) -> str:
    source = ensure_import_name(source, "proof", "apply_inference_match")
    source = replace_once(
        source,
        """  rules = (
    prop22_rule,
    equation57_rule,
    hopf_surjective_rule,
    delta_zero_rule,
    suspension_injective_rule,
  )
""",
        """  rules = (
    equation57_rule,
    hopf_surjective_rule,
    delta_zero_rule,
    suspension_injective_rule,
  )
""",
        "test rules",
    )
    marker = "  premise_steps = (\n"
    if marker not in source:
        raise RuntimeError("test premise marker not found")
    if "  prop22_match = (\n    find_inference_match(" not in source:
        source = source.replace(
            marker,
            """  prop22_match = (
    find_inference_match(
      prop22_rule,
      (),
    )
  )

  assert prop22_match is not None

  prop22_step = (
    apply_inference_match(
      prop22_match
    )
  )

""" + marker,
            1,
        )
    source = replace_once(
        source,
        """    eta5_definition_step,
    eta6_definition_step,
    h_delta_exactness_step,
""",
        """    eta5_definition_step,
    eta6_definition_step,
    prop22_step,
    h_delta_exactness_step,
""",
        "test premises",
    )
    source = source.replace(
        """  prop22_step = next(
    step
    for step in result.steps
    if step.inference_rule == prop22_rule
  )

""",
        "",
        1,
    )

    start = source.find("def test_phase65_3_reaches_fixed_point_in_five_rounds():")
    if start < 0:
        start = source.find("def test_phase65_3_reaches_fixed_point_in_four_rounds():")
    if start < 0:
        raise RuntimeError("fixed-point test not found")
    end = source.find("\ndef ", start + 5)
    if end < 0:
        end = len(source)
    new_func = """def test_phase65_3_reaches_fixed_point_in_four_rounds():
  data = build_phase65_3_data()

  result = data[
    "result"
  ]

  assert (
    result.termination_reason
    == InferenceTerminationReason.FIXED_POINT
  )

  assert result.round_count == 4

  assert (
    data[
      "equation57_step"
    ]
    in result.round_results[
      0
    ].new_steps
  )

  assert (
    data[
      "hopf_surjective_step"
    ]
    in result.round_results[
      1
    ].new_steps
  )

  assert (
    data[
      "delta_zero_step"
    ]
    in result.round_results[
      2
    ].new_steps
  )

  assert (
    data[
      "suspension_injective_step"
    ]
    in result.round_results[
      3
    ].new_steps
  )
"""
    source = source[:start] + new_func + source[end:]
    return source

def remove_reference_specializations(source: str) -> str:
    return remove_top_level_functions(
        source,
        (
            "_phase157_r3_is_pi6_3_root",
            "filter_phase157_r3_pi6_3_reference_entries",
            "restore_phase157_r3_pi6_3_required_reference_entries_after_body_usage",
        ),
    )

def remove_renderer_specializations(source: str) -> str:
    source = remove_top_level_functions(
        source,
        (
            "_phase157_r19_",
            "_phase157_r3_restore_pi6_3_earlier_prop56_reference",
            "_phase157_r3_restore_pi6_3_proof_internal_suspension_isomorphism",
        ),
    )
    source = remove_import_name(
        source,
        "toda_group_proof_narrative_references",
        "filter_phase157_r3_pi6_3_reference_entries",
    )
    source = re.sub(
        r"""  phase157_r19_reference_entries_before_pi6_filter = \(\n    reference_entries\n  \)\n  reference_entries = \(\n    filter_phase157_r3_pi6_3_reference_entries\(\n      reference_entries,\n      presentation\.root_step,\n    \)\n  \)\n  reference_entries = \(\n    _phase157_r19_restore_prop22_reference_for_pi6_3\(\n      presentation,\n      phase157_r19_reference_entries_before_pi6_filter,\n      reference_entries,\n    \)\n  \)\n""",
        "",
        source,
    )
    source = source.replace(
        """  phase157_r3_entries_before_usage_filter = reference_entries
  phase157_r3_lines_before_usage_filter = (
    statement_lines_by_reference_number
  )

""",
        "",
    )
    source = re.sub(
        r"""  \(\n    reference_entries,\n    statement_lines_by_reference_number,\n  \) = \(\n    _phase157_r3_restore_pi6_3_earlier_prop56_reference\(\n      presentation,\n.*?    \)\n  \)\n\n""",
        "",
        source,
        flags=re.DOTALL,
    )
    source = re.sub(
        r"""  \(\n    reference_entries,\n    statement_lines_by_reference_number,\n    rendered,\n  \) = \(\n    _phase157_r19_finalize_pi6_3_public_narrative\(\n      presentation,\n.*?    \)\n  \)\n\n  public_statement_lines_by_reference_number = \(\n    _phase157_r19_public_reference_statement_lines\(\n      presentation,\n      reference_entries,\n      statement_lines_by_reference_number,\n    \)\n  \)\n""",
        "",
        source,
        flags=re.DOTALL,
    )
    source = source.replace(
        "      public_statement_lines_by_reference_number,\n",
        "      statement_lines_by_reference_number,\n",
    )
    return source

def patch_arch_test(source: str) -> str:
    return source.replace(
        """def test_phase157_r20_prop22_is_first_class_literature_provenance():
  rule = toda_prop22_right_inference_rule(
    alpha=build_phase65_3_data()["nu_prime"],
    gamma=build_phase65_3_data()["eta_5"],
  )

  assert rule.literature_reference is not None
""",
        """def test_phase157_r20_prop22_is_first_class_literature_provenance():
  data = build_phase65_3_data()
  rule = data["prop22_rule"]

  assert rule.literature_reference is not None
""",
        1,
    )

def preflight(renderer: str, references: str) -> None:
    forbidden_renderer = (
        "_phase157_r19_",
        "filter_phase157_r3_pi6_3_reference_entries",
        "_phase157_r3_restore_pi6_3_",
        "is_pi6_3",
    )
    forbidden_references = (
        "_phase157_r3_is_pi6_3_root",
        "filter_phase157_r3_pi6_3_reference_entries",
        "restore_phase157_r3_pi6_3_required_reference_entries_after_body_usage",
    )
    failures = []
    for token in forbidden_renderer:
        count = renderer.count(token)
        if count:
            failures.append(f"renderer: {token} x{count}")
    for token in forbidden_references:
        count = references.count(token)
        if count:
            failures.append(f"references: {token} x{count}")
    if failures:
        raise RuntimeError(
            "target-specific code remains:\n"
            + "\n".join(failures)
        )

def main() -> int:
    for path in FILES.values():
        if not path.is_file():
            raise RuntimeError(f"missing file: {path}")

    backup = ROOT / (
        "phase157_r20_repair1_backup_"
        + datetime.now().strftime("%Y%m%d_%H%M%S")
    )
    backup.mkdir(parents=True, exist_ok=False)

    for path in FILES.values():
        shutil.copy2(path, backup / path.name)

    sources = {
        key: path.read_text(encoding="utf-8")
        for key, path in FILES.items()
    }

    sources["phase65"] = patch_phase65(sources["phase65"])
    sources["prop58"] = patch_prop58(sources["prop58"])
    sources["phase65_test"] = patch_phase65_test(sources["phase65_test"])
    sources["references"] = remove_reference_specializations(sources["references"])
    sources["renderer"] = remove_renderer_specializations(sources["renderer"])
    sources["arch_test"] = patch_arch_test(sources["arch_test"])

    for key, source in sources.items():
        compile(source, str(FILES[key]), "exec")

    preflight(
        sources["renderer"],
        sources["references"],
    )

    for key, source in sources.items():
        FILES[key].write_text(
            source,
            encoding="utf-8",
            newline="\n",
        )

    print("Phase157-R20 repair1 applied.")
    print("Backup:", backup)
    print("Architecture preflight:")
    print("  renderer _phase157_r19_:", sources["renderer"].count("_phase157_r19_"))
    print("  renderer is_pi6_3:", sources["renderer"].count("is_pi6_3"))
    print("  renderer pi6 restore:", sources["renderer"].count("_phase157_r3_restore_pi6_3_"))
    print("  references pi6 root:", sources["references"].count("_phase157_r3_is_pi6_3_root"))
    print("  references pi6 filter:", sources["references"].count("filter_phase157_r3_pi6_3_reference_entries"))
    print("  references pi6 restore:", sources["references"].count("restore_phase157_r3_pi6_3_required_reference_entries_after_body_usage"))
    return 0

if __name__ == "__main__":
    raise SystemExit(main())
