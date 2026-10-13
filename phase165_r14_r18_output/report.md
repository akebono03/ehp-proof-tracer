# Phase 165 R14-R18 — 実装・出典監査

- phase: 165 R14-R18
- diagonal_obligations: ["Relation(lhs=TodaPrimaryGroup(group_dimension=1, sphere_dimension=1), rhs=FreeCyclicGroup(generator=HomotopyElement(name='ι₁', dimension=1, source=1, target=1, generator=GeneratorSymbol(family='ι', index=1, decoration=None))), relation_type=<RelationType.EQUALITY: 'equality'>, source=None, note=None)", "Relation(lhs=TodaPrimaryGroup(group_dimension=2, sphere_dimension=2), rhs=FreeCyclicGroup(generator=HomotopyElement(name='ι₂', dimension=2, source=2, target=2, generator=GeneratorSymbol(family='ι', index=2, decoration=None))), relation_type=<RelationType.EQUALITY: 'equality'>, source=None, note=None)", "GeneratorSuspension(map=TodaSuspensionMap(source_group=TodaPrimaryGroup(group_dimension=1, sphere_dimension=1), target_group=TodaPrimaryGroup(group_dimension=2, sphere_dimension=2)), source_generator=HomotopyElement(name='ι₁', dimension=1, source=1, target=1, generator=GeneratorSymbol(family='ι', index=1, decoration=None)), target_generator=HomotopyElement(name='ι₂', dimension=2, source=2, target=2, generator=GeneratorSymbol(family='ι', index=2, decoration=None)))"]
- foundational_step_available: True
- verified_toda_group_steps_supplied: 0
- diagonal_iso_in_production: False
- fail_closed_on_missing_group_steps: True
- prop42_candidate_count: 2
- prop42_semantics_certified: False
- new_toda_proof_steps: 0
- pi32_proved: False
- full_pytest_run: False
- status: FOUNDATIONAL_STEP_CONNECTED_CONDITIONALLY_TODA_LEAVES_MISSING

## Proposition 4.2 候補原文

### phase163:archive:toda:tex:ch4:0002

```tex
\begin{equation}\label{4.2}
% (4.2).\
\pis{i}{S^n}\ \text{は,} \ i=n \ \text{または} \ 
i=2n-1 \ \text{のとき以外は, 有限群である. }
\end{equation}
```

### phase163:archive:toda:tex:ch4:0005

```tex
\begin{proposition}[]\label{prop:4.2}
% Prop4.2.\
次の列は完全列である：
\begin{equation}\label{4.4}
% (4.4)
\cdots \longrightarrow
\pit{i}{n}\ \xrightarrow{\ \Ex\ }\ \pit{i+1}{n+1}\
\xrightarrow{\ H\ }\ \pit{i+1}{2n+1}\
\xrightarrow{\ \Delta\ }\ \pit{i-1}{n}\
\xrightarrow{\ \Ex\ }\ \pit{i}{n+1}\ \xrightarrow{\ H\ }\ \cdots.
\end{equation}
\end{proposition}
```
