# Phase 155-R3-2D — missing execution record audit

## Boundary

This audit investigates only missing execution records identified by R3-2C-r1.
It modifies no production code and no existing test.

- Repository root: `C:\Users\oomae\Dropbox\Python\fitz\ehp_proof`
- Git HEAD: `d1d57b3478feeb29fcb32c27670bfaf0dc537f57`
- Missing test references audited: 12

## Root causes

| root cause | records |
| --- | ---: |
| `parameterized_nodeid_all_pass` | 0 |
| `parameterized_nodeid_has_failure` | 12 |
| `collected_but_not_recorded` | 0 |
| `nonparameterized_execution_match` | 0 |
| `not_collected` | 0 |
| `unresolved` | 0 |

- Recorder-only records: 0
- Test-related records: 12

## Interpretation

`parameterized_nodeid_all_pass` means the original candidate test was specified as `file.py::test_name`, while pytest executed `file.py::test_name[param]` instances. R3-2 used exact-key lookup and therefore created a false missing record even though every parameter instance passed.

`collected_but_not_recorded` means pytest currently collects the test but the previous execution recorder did not save a matching result.

`not_collected` or `parameterized_nodeid_has_failure` requires test-side investigation before R3-2 closure.

Repository-wide pytest remains deferred until Phase 155 closure.
