# GitHub baseline — Phase 155-R3-3B

Repository: `akebono03/ehp-proof-tracer`
Branch: `main`
Observed public baseline commit: `8301520a7434f3836b1dbc7e8fa08a60c024225a`

Inspected before R3-3B:

- representative Phase 143, Phase 150, Phase 153, and Phase 154 test files,
- repository imports from `tests.test_phase143_*`,
- repository imports from `tests.test_phase150_*`,
- repository imports from `tests.test_phase153_*`,
- repository imports from `tests.test_phase154_*`.

GitHub confirms that test modules can be active dependency providers.
A prominent example is:

`from tests.test_phase143_19_method_evidence import _method_evidence_data`

used by later tests and audit code.

Therefore R3-3B does not equate "all tests in a file are duplicate
candidates" with "the file can be deleted."

The local R3-3A result is the authoritative candidate input:
- 164 removable pairs,
- 64 connected components,
- 227 tests in the removable graph,
- 161 unique deletion candidates,
- 0 cycle components,
- 0 manual-review components.

R3-3B audits those 161 candidates against the user's CURRENT local source
tree, including the R3-2F-r1 test repairs.
