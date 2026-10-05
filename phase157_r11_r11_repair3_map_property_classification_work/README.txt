Phase157 R11-R11 repair3 — map-property classification

原因
====

R11-R11 で semantic closure に追加した一般規則は MAP_PROPERTY を対象にするが、
現行 `classify_toda_proof_step_role()` は
`TodaHopfInvariantSurjectiveStatement` を MAP_PROPERTY に分類していなかった。

そのため H-surjectivity に対して closure 規則が発火していなかった。

また Reference の
`$nu' in pi_6^3$,`
と本文の
`$nu' in pi_6^3$.`
は末尾句読点だけ異なるため、Reference reuse が認識されていなかった。

repair3
=======

- `TodaHopfInvariantSurjectiveStatement` を dependency MAP_PROPERTY に追加。
- standalone Reference/body statement の比較では末尾 `,` / `.` を無視。
- Reference reuse は `[R#]より, ... .` と表示。
- H-surjectivity の dependency role regression test を追加。

full repository pytest は Phase157 closure まで実行しない。
