from pathlib import Path

package_root = Path(__file__).resolve().parent
repo_root = package_root.parent
target = repo_root / "toda_prop515_upper_bootstrap.py"

if not target.exists():
    raise SystemExit(
        "toda_prop515_upper_bootstrap.py was not found"
    )

text = target.read_text(
    encoding="utf-8"
)

old_block = """  higher_step = next(
    step
    for step in stable_result.steps
    if (
      isinstance(
        step.conclusion,
        Relation,
      )
      and step.conclusion.lhs
      == target_group
      and isinstance(
        step.conclusion.rhs,
        FiniteCyclicGroup,
      )
      and step.conclusion.rhs.order
      == 16
    )
  )
"""

new_block = """  higher_step = next(
    step
    for step in stable_result.steps
    if (
      isinstance(
        step.conclusion,
        Relation,
      )
      and step.conclusion.lhs
      == target_group
      and isinstance(
        step.conclusion.rhs,
        FiniteCyclicGroup,
      )
      and step.conclusion.rhs.order
      == 16
      and step.conclusion.rhs.generator
      == sigma_family_step.conclusion.element
    )
  )
"""

count = text.count(
    old_block
)

if count != 1:
    raise SystemExit(
        "expected exactly one Phase 160-R6 higher_step "
        f"selection block, found {count}"
    )

text = text.replace(
    old_block,
    new_block,
    1,
)

target.write_text(
    text,
    encoding="utf-8",
)

print("Applied Phase 160-R6 repair1:")
print("  toda_prop515_upper_bootstrap.py")
print("  higher_step now selects normalized sigma_n relation")
