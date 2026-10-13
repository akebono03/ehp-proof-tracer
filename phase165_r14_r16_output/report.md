# Phase 165 R14-R16 監査結果

- phase: 165 R14-R16
- foundational_claim: GeneratorSuspension(map=TodaSuspensionMap(source_group=TodaPrimaryGroup(group_dimension=1, sphere_dimension=1), target_group=TodaPrimaryGroup(group_dimension=2, sphere_dimension=2)), source_generator=HomotopyElement(name='ι₁', dimension=1, source=1, target=1, generator=GeneratorSymbol(family='ι', index=1, decoration=None)), target_generator=HomotopyElement(name='ι₂', dimension=2, source=2, target=2, generator=GeneratorSymbol(family='ι', index=2, decoration=None)))
- foundational_reference: foundational:suspension-identity
- foundational_justification: Under S(S^n) = S^(n+1), the reduced suspension of id_(S^n) is id_(S^(n+1)); hence E(iota_n)=iota_(n+1).
- classification: WELL_KNOWN_FOUNDATIONAL_NOT_TODA_LITERATURE
- foundational_claim_formulated: True
- foundational_claim_independently_reviewed: False
- foundational_claim_proof_eligible: False
- diagonal_obligation_count: 3
- prop42_candidate_count: 2
- prop42_clause_selected: False
- prop42_proof_eligible: False
- new_proof_steps: 0
- status: FOUNDATIONAL_IDENTITY_TYPED_PROP42_STILL_REQUIRES_REVIEW
- full_pytest_run: False

## Proposition 4.2 候補（原文）

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
