# EHP Proof Tracer — Phase 174 R3-R7-R17

## Typed open map goals and the unresolved Delta-surjectivity frontier

This package makes `MapSurjective`, `MapInjective`, and `MapIsomorphism`
statements readable as typed mathematics in the common partial-proof
presentation. It applies to the three supported EHP map kinds (`Delta`, `E`,
`H`) without a special `(n,k)` rule or a dedicated narrative.

It does **not** change proof search, mathematical rules, accepted GIVENs,
proof trees, or proof completion status. In particular, the generic
isomorphism rule currently requires surjectivity as a premise; using
isomorphism to assert surjectivity without independent evidence would be
circular and is deliberately **not** implemented here.

The package includes a source-guarded PowerShell runner. Run from a local
Windows checkout with the already-applied Phase 174 R16 code. Both the
uncommitted R16 working-tree handoff and a fully merged R16 `develop`
checkout are supported, provided the content matches exactly.

```powershell
Expand-Archive -Path "$HOME\Downloads\EHP_Phase174_R3_R7_R17_TYPED_MAP_OPEN_GOAL.zip" -DestinationPath . -Force
powershell -NoProfile -ExecutionPolicy Bypass -File ".\phase174_r3_r7_r17_typed_map_open_goal\run.ps1" -DryRun
powershell -NoProfile -ExecutionPolicy Bypass -File ".\phase174_r3_r7_r17_typed_map_open_goal\run.ps1"
```

The runner performs focused tests only. No phase-wide `pytest` is run. The
R17 `MODIFIED_FUNCTION_FULL_JA.md` output is generated from the actual
source-guarded replacement function, including its complete in-function
imports. This package does not modify the root README or project documents.
