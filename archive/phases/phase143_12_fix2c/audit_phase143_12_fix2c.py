import sys
from pathlib import Path

sys.path.insert(0, str(Path.cwd() / "tests"))

from test_phase143_12_purpose_subject import _arguments
from toda_group_proof_narrative_arguments import (
  extract_toda_group_proof_narrative_argument_purpose_subject,
)

for n, k in ((3, 3), (5, 3), (8, 7), (9, 7)):
  print("=" * 78)
  print(f"n={n}, k={k}")
  for index, argument in enumerate(_arguments(n, k), start=1):
    subject = extract_toda_group_proof_narrative_argument_purpose_subject(
      argument
    )
    print(
      f"A{index:02d} {argument.role.value}: {subject!r}"
    )
