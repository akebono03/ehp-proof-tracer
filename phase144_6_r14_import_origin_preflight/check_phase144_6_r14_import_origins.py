import inspect
import sys

import toda_group_proof_narrative_argument_multi_renderer as multi
import toda_group_proof_narrative_argument_body_renderer as body
import tests.test_phase143_57c_step_derivation_connector as t57
import tests.test_phase143_61b_direct_premise_narrative as t61

print("sys.executable =", sys.executable)
print("sys.path:")
for item in sys.path:
    print(" ", item)

print()
for name, module in (
    ("multi_renderer", multi),
    ("body_renderer", body),
    ("test_phase143_57c", t57),
    ("test_phase143_61b", t61),
):
    print(name, "=", inspect.getfile(module))

print()
rendered=t57._render(3,3)
print("pi6 has first calculation =", r"$2\nu' = \eta_{3}E\eta_{3}\eta_{5}$" in rendered)
print("pi6 connector count =", rendered.count("これらより、"))

rendered8=t61._render(5,3)
pi6=r"$\pi_{6}^{3} = \mathbb{Z}/4\{\nu'\}$"
double=r"$2\nu_{5} = E^{2}\nu'$"
print("pi8 pi6 index =", rendered8.index(pi6))
print("pi8 double index =", rendered8.index(double))
