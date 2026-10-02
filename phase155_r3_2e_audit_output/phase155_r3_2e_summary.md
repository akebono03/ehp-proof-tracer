# Phase 155-R3-2E — parameterized failure decomposition

## Boundary

This step freshly executes only the unique base tests referenced by R3-2D.
It records pytest collection and all setup/call/teardown reports directly.
It changes no production code and no existing test.

- Repository root: `C:\Users\oomae\Dropbox\Python\fitz\ehp_proof`
- Git HEAD: `3917df4a7df8633f84754584913b43d4b2f0e41a`
- Unique base tests: 11
- Fresh focused pytest exit code: 0
- Fresh call instances: 62
- Passed call instances: 62
- Failed call instances: 0
- Blocking base tests: 0

## Root causes

| root cause | base tests |
| --- | ---: |
| `all_parameterized_instances_pass` | 11 |
| `parameterized_instance_failure` | 0 |
| `setup_or_teardown_failure` | 0 |
| `not_collected` | 0 |
| `collected_without_call_report` | 0 |
| `unresolved` | 0 |

## Interpretation

`all_parameterized_instances_pass` proves that R3-2D's earlier `parameterized with failure` classification was false for that base test.
The reason is structural: R3-2 wrote a synthetic base-level `missing` row when exact lookup failed, while actual pytest parameter instances were not written to that CSV.

Only a fresh call-phase `failed`, setup/teardown failure, collection failure, or unresolved record blocks R3-2 closure.

Repository-wide pytest remains deferred until Phase 155 closure.
