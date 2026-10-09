# Recursive ProofStep trace with existing exactness reasons

注意: 理由が未対応の推論は証明文章として認証しない。

### [S001] GIVEN

前提: なし

事実: $\nu' \in \{\eta_{3}, 2\iota_{4}, \eta_{4}\}_{1}$

根拠区分: GIVEN (既知の前提)

### [S002] UNEXPLAINED

前提: [S001]

事実: $\nu' \in \{\eta_{3}, 2\iota_{4}, \eta_{4}\}_{1}$ が成り立つ.

推論理由: 未対応

### [S003] GIVEN

前提: なし

事実: $\pi_{3}^{2} = \mathbb{Z}\{\eta_{2}\}$

根拠区分: GIVEN (既知の前提)

### [S004] GIVEN

前提: なし

事実: $\pi_{5}^{5} = \mathbb{Z}\{\iota_{5}\}$

根拠区分: GIVEN (既知の前提)

### [S005] GIVEN

前提: なし

事実: `TodaDeltaMap`

根拠区分: GIVEN (既知の前提)

### [S006] UNEXPLAINED

前提: [S005]

事実: $\Delta\left(\iota_{5}\right) = \pm [\iota_{2}, \iota_{2}]$

推論理由: 未対応

### [S007] GIVEN

前提: なし

事実: $[\iota_{2}, \iota_{2}]$

根拠区分: GIVEN (既知の前提)

### [S008] UNEXPLAINED

前提: [S007]

事実: $H([\iota_{2}, \iota_{2}]) = \pm 2\iota_{3}$ が成り立つ.

推論理由: 未対応

### [S009] GIVEN

前提: なし

事実: $H(\eta_{2}) = \iota_{3}$ を満たす $\eta_{2} \in \pi_{3}^{2}$ を定める.

根拠区分: GIVEN (既知の前提)

### [S010] GIVEN

前提: なし

事実: $H\left(\eta_{2}\right) = \iota_{3}$

根拠区分: GIVEN (既知の前提)

### [S011] GIVEN

前提: なし

事実: $H: \pi_{3}^{2} \to \pi_{3}^{3}$ は単射である.

根拠区分: GIVEN (既知の前提)

### [S012] UNEXPLAINED

前提: [S008], [S009], [S010], [S011]

事実: Toda pi_3^2 Whitehead square equals twice eta_2 up to sign

推論理由: 未対応

### [S013] UNEXPLAINED

前提: [S004], [S006], [S012]

事実: $\operatorname{Im}\Delta = \mathbb{Z}\{2\eta_{2}\}$.

推論理由: 未対応

### [S014] GIVEN

前提: なし

事実: $\pi_{5}^{5} \xrightarrow{Δ} \pi_{3}^{2} \xrightarrow{E} \pi_{4}^{3}$ は完全である.

根拠区分: GIVEN (既知の前提)

### [S015] EXPLAINED

前提: [S013], [S014]

事実: $\ker E = \mathbb{Z}\{2\eta_{2}\}$.

推論理由: 完全性より, $\ker E=\operatorname{Im}Δ=\mathbb{Z}\{2\eta_{2}\}$.

### [S016] GIVEN

前提: なし

事実: $\pi_{4}^{5} = 0$

根拠区分: GIVEN (既知の前提)

### [S017] GIVEN

前提: なし

事実: $\pi_{3}^{2} \xrightarrow{E} \pi_{4}^{3} \xrightarrow{H} \pi_{4}^{5}$ は完全である.

根拠区分: GIVEN (既知の前提)

### [S018] EXPLAINED

前提: [S016], [S017]

事実: $E: \pi_{3}^{2} \to \pi_{4}^{3}$ は全射である.

推論理由: 完全性より, $E: \pi_{3}^{2} \to \pi_{4}^{3}$ は全射.

### [S019] UNEXPLAINED

前提: [S003], [S015], [S018]

事実: $\pi_{4}^{3} = \mathbb{Z}/2\{\eta_{3}\}$

推論理由: 未対応

### [S020] GIVEN

前提: なし

事実: `TodaEtaFamilyDefinitionStatement`

根拠区分: GIVEN (既知の前提)

### [S021] UNEXPLAINED

前提: [S020]

事実: $\eta_{3} = \eta_{3}$

推論理由: 未対応

### [S022] UNEXPLAINED

前提: [S019], [S021]

事実: $\pi_{4}^{3} = \mathbb{Z}/2\{\eta_{3}\}$

推論理由: 未対応

### [S023] UNEXPLAINED

前提: [S022]

事実: $2\eta_{3} = 0$

推論理由: 未対応

### [S024] UNEXPLAINED

前提: [S002], [S023]

事実: $H\left(\nu'\right) = \eta_{5}$

推論理由: 未対応

### [S025] GIVEN

前提: なし

事実: `TodaEtaFamilyDefinitionStatement`

根拠区分: GIVEN (既知の前提)

### [S026] GIVEN

前提: なし

事実: `TodaEtaFamilyDefinitionStatement`

根拠区分: GIVEN (既知の前提)

### [S027] UNEXPLAINED

前提: [S025], [S026]

事実: $\eta_{5} = \eta_{5}$

推論理由: 未対応

### [S028] UNEXPLAINED

前提: [S024], [S027]

事実: $H\left(\nu'\right) = \eta_{5}$

推論理由: 未対応

### [S029] GIVEN

前提: なし

事実: $\pi_{2}^{1} = 0$

根拠区分: GIVEN (既知の前提)

### [S030] GIVEN

前提: なし

事実: $\pi_{2}^{1} \xrightarrow{E} \pi_{3}^{2} \xrightarrow{H} \pi_{3}^{3}$ は完全である.

根拠区分: GIVEN (既知の前提)

### [S031] EXPLAINED

前提: [S029], [S030]

事実: $H: \pi_{3}^{2} \to \pi_{3}^{3}$ は単射である.

推論理由: 完全性より, $H: \pi_{3}^{2} \to \pi_{3}^{3}$ は単射.

### [S032] GIVEN

前提: なし

事実: $E: \pi_{1}^{1} \to \pi_{2}^{2}$ は同型写像である.

根拠区分: GIVEN (既知の前提)

### [S033] UNEXPLAINED

前提: [S032]

事実: $E: \pi_{1}^{1} \to \pi_{2}^{2}$ は単射である.

推論理由: 未対応

### [S034] GIVEN

前提: なし

事実: $\pi_{3}^{3} \xrightarrow{Δ} \pi_{1}^{1} \xrightarrow{E} \pi_{2}^{2}$ は完全である.

根拠区分: GIVEN (既知の前提)

### [S035] UNEXPLAINED

前提: [S033], [S034]

事実: $\Delta: \pi_{3}^{3} \to \pi_{1}^{1}$ は零写像である.

推論理由: 未対応

### [S036] GIVEN

前提: なし

事実: $\pi_{3}^{2} \xrightarrow{H} \pi_{3}^{3} \xrightarrow{Δ} \pi_{1}^{1}$ は完全である.

根拠区分: GIVEN (既知の前提)

### [S037] EXPLAINED

前提: [S035], [S036]

事実: $H: \pi_{3}^{2} \to \pi_{3}^{3}$ は全射である.

推論理由: 完全性より, $H: \pi_{3}^{2} \to \pi_{3}^{3}$ は全射.

### [S038] UNEXPLAINED

前提: [S031], [S037]

事実: $H: \pi_{3}^{2} \to \pi_{3}^{3}$ は同型写像である.

推論理由: 未対応

### [S039] GIVEN

前提: なし

事実: $\pi_{3}^{3} = \mathbb{Z}\{\iota_{3}\}$

根拠区分: GIVEN (既知の前提)

### [S040] UNEXPLAINED

前提: [S038], [S039]

事実: $H(\eta_{2}) = \iota_{3}$ を満たす $\eta_{2} \in \pi_{3}^{2}$ を定める.

推論理由: 未対応

### [S041] UNEXPLAINED

前提: [S038], [S039], [S040]

事実: $\pi_{3}^{2} = \mathbb{Z}\{\eta_{2}\}$

推論理由: 未対応

### [S042] UNEXPLAINED

前提: [S040]

事実: $H\left(\eta_{2}\right) = \iota_{3}$

推論理由: 未対応

### [S043] GIVEN

前提: なし

事実: `TodaDeltaMap`

根拠区分: GIVEN (既知の前提)

### [S044] UNEXPLAINED

前提: [S043]

事実: $\Delta\left(\iota_{5}\right) = \pm [\iota_{2}, \iota_{2}]$

推論理由: 未対応

### [S045] GIVEN

前提: なし

事実: $[\iota_{2}, \iota_{2}]$

根拠区分: GIVEN (既知の前提)

### [S046] UNEXPLAINED

前提: [S045]

事実: $H([\iota_{2}, \iota_{2}]) = \pm 2\iota_{3}$ が成り立つ.

推論理由: 未対応

### [S047] UNEXPLAINED

前提: [S046], [S040], [S042], [S031]

事実: Toda pi_3^2 Whitehead square equals twice eta_2 up to sign

推論理由: 未対応

### [S048] UNEXPLAINED

前提: [S044], [S047]

事実: $\Delta\left(\iota_{5}\right) = \pm 2\eta_{2}$

推論理由: 未対応

### [S049] GIVEN

前提: なし

事実: $\pi_{5}^{5} = \mathbb{Z}\{\iota_{5}\}$

根拠区分: GIVEN (既知の前提)

### [S050] UNEXPLAINED

前提: [S049], [S044], [S047]

事実: $\operatorname{Im}\Delta = \mathbb{Z}\{2\eta_{2}\}$.

推論理由: 未対応

### [S051] GIVEN

前提: なし

事実: $\pi_{5}^{5} \xrightarrow{Δ} \pi_{3}^{2} \xrightarrow{E} \pi_{4}^{3}$ は完全である.

根拠区分: GIVEN (既知の前提)

### [S052] EXPLAINED

前提: [S050], [S051]

事実: $\ker E = \mathbb{Z}\{2\eta_{2}\}$.

推論理由: 完全性より, $\ker E=\operatorname{Im}Δ=\mathbb{Z}\{2\eta_{2}\}$.

### [S053] GIVEN

前提: なし

事実: $\pi_{4}^{5} = 0$

根拠区分: GIVEN (既知の前提)

### [S054] GIVEN

前提: なし

事実: $\pi_{3}^{2} \xrightarrow{E} \pi_{4}^{3} \xrightarrow{H} \pi_{4}^{5}$ は完全である.

根拠区分: GIVEN (既知の前提)

### [S055] EXPLAINED

前提: [S053], [S054]

事実: $E: \pi_{3}^{2} \to \pi_{4}^{3}$ は全射である.

推論理由: 完全性より, $E: \pi_{3}^{2} \to \pi_{4}^{3}$ は全射.

### [S056] UNEXPLAINED

前提: [S041], [S052], [S055]

事実: $\pi_{4}^{3} = \mathbb{Z}/2\{\eta_{3}\}$

推論理由: 未対応

### [S057] GIVEN

前提: なし

事実: `TodaEtaFamilyDefinitionStatement`

根拠区分: GIVEN (既知の前提)

### [S058] UNEXPLAINED

前提: [S057]

事実: $\eta_{3} = \eta_{3}$

推論理由: 未対応

### [S059] UNEXPLAINED

前提: [S056], [S058]

事実: $\pi_{4}^{3} = \mathbb{Z}/2\{\eta_{3}\}$

推論理由: 未対応

### [S060] GIVEN

前提: なし

事実: `ScalarGreaterEqualStatement`

根拠区分: GIVEN (既知の前提)

### [S061] GIVEN

前提: なし

事実: `ScalarGreaterEqualStatement`

根拠区分: GIVEN (既知の前提)

### [S062] GIVEN

前提: なし

事実: `TodaIteratedSuspensionMap`

根拠区分: GIVEN (既知の前提)

### [S063] UNEXPLAINED

前提: [S060], [S061], [S062]

事実: $E^{n - 3}: \pi_{3 + 1}^{3} \to \pi_{n + 1}^{n}$ は同型写像である.

推論理由: 未対応

### [S064] UNEXPLAINED

前提: [S059], [S063]

事実: $\pi_{n + 1}^{n} = \mathbb{Z}/2\{E^{n - 3}\eta_{3}\}$

推論理由: 未対応

### [S065] GIVEN

前提: なし

事実: `TodaEtaFamilyDefinitionStatement`

根拠区分: GIVEN (既知の前提)

### [S066] UNEXPLAINED

前提: [S065], [S058]

事実: $E^{n - 3}\eta_{3} = \eta_{n}$

推論理由: 未対応

### [S067] UNEXPLAINED

前提: [S064], [S066]

事実: $\pi_{n + 1}^{n} = \mathbb{Z}/2\{\eta_{n}\}$

推論理由: 未対応

### [S068] UNEXPLAINED

前提: [S041], [S042], [S048], [S067]

事実: $\pi_{3}^{2} = \mathbb{Z}\{\eta_{2}\}$, $H\left(\eta_{2}\right) = \iota_{3}$, $\Delta\left(\iota_{5}\right) = \pm 2\eta_{2}$, $\pi_{n + 1}^{n} = \mathbb{Z}/2\{\eta_{n}\}$ が成り立つ.

推論理由: 未対応

### [S069] UNEXPLAINED

前提: [S028], [S068]

事実: $H: \pi_{6}^{3} \to \pi_{6}^{5}$ は全射である.

推論理由: 未対応

### [S070] GIVEN

前提: なし

事実: $\pi_{6}^{3} \xrightarrow{H} \pi_{6}^{5} \xrightarrow{Δ} \pi_{4}^{2}$ は完全である.

根拠区分: GIVEN (既知の前提)

### [S071] UNEXPLAINED

前提: [S069], [S070]

事実: $\Delta: \pi_{6}^{5} \to \pi_{4}^{2}$ は零写像である.

推論理由: 未対応

### [S072] GIVEN

前提: なし

事実: $\pi_{6}^{5} \xrightarrow{Δ} \pi_{4}^{2} \xrightarrow{E} \pi_{5}^{3}$ は完全である.

根拠区分: GIVEN (既知の前提)

### [S073] EXPLAINED

前提: [S071], [S072]

事実: $E: \pi_{4}^{2} \to \pi_{5}^{3}$ は単射である.

推論理由: 完全性より, $E: \pi_{4}^{2} \to \pi_{5}^{3}$ は単射.

### [S074] UNEXPLAINED

前提: [S068]

事実: $\Delta: \pi_{5}^{5} \to \pi_{3}^{2}$ は単射である.

推論理由: 未対応

### [S075] GIVEN

前提: なし

事実: $\pi_{5}^{3} \xrightarrow{H} \pi_{5}^{5} \xrightarrow{Δ} \pi_{3}^{2}$ は完全である.

根拠区分: GIVEN (既知の前提)

### [S076] UNEXPLAINED

前提: [S074], [S075]

事実: $H: \pi_{5}^{3} \to \pi_{5}^{5}$ は零写像である.

推論理由: 未対応

### [S077] GIVEN

前提: なし

事実: $\pi_{4}^{2} \xrightarrow{E} \pi_{5}^{3} \xrightarrow{H} \pi_{5}^{5}$ は完全である.

根拠区分: GIVEN (既知の前提)

### [S078] EXPLAINED

前提: [S076], [S077]

事実: $E: \pi_{4}^{2} \to \pi_{5}^{3}$ は全射である.

推論理由: 完全性より, $E: \pi_{4}^{2} \to \pi_{5}^{3}$ は全射.

### [S079] UNEXPLAINED

前提: [S073], [S078]

事実: $E: \pi_{4}^{2} \to \pi_{5}^{3}$ は同型写像である.

推論理由: 未対応

### [S080] GIVEN

前提: なし

事実: $\pi_{3}^{2} = \mathbb{Z}\{\eta_{2}\}$

根拠区分: GIVEN (既知の前提)

### [S081] GIVEN

前提: なし

事実: $\pi_{5}^{5} = \mathbb{Z}\{\iota_{5}\}$

根拠区分: GIVEN (既知の前提)

### [S082] GIVEN

前提: なし

事実: `TodaDeltaMap`

根拠区分: GIVEN (既知の前提)

### [S083] UNEXPLAINED

前提: [S082]

事実: $\Delta\left(\iota_{5}\right) = \pm [\iota_{2}, \iota_{2}]$

推論理由: 未対応

### [S084] GIVEN

前提: なし

事実: $[\iota_{2}, \iota_{2}]$

根拠区分: GIVEN (既知の前提)

### [S085] UNEXPLAINED

前提: [S084]

事実: $H([\iota_{2}, \iota_{2}]) = \pm 2\iota_{3}$ が成り立つ.

推論理由: 未対応

### [S086] GIVEN

前提: なし

事実: $H(\eta_{2}) = \iota_{3}$ を満たす $\eta_{2} \in \pi_{3}^{2}$ を定める.

根拠区分: GIVEN (既知の前提)

### [S087] GIVEN

前提: なし

事実: $H\left(\eta_{2}\right) = \iota_{3}$

根拠区分: GIVEN (既知の前提)

### [S088] GIVEN

前提: なし

事実: $H: \pi_{3}^{2} \to \pi_{3}^{3}$ は単射である.

根拠区分: GIVEN (既知の前提)

### [S089] UNEXPLAINED

前提: [S085], [S086], [S087], [S088]

事実: Toda pi_3^2 Whitehead square equals twice eta_2 up to sign

推論理由: 未対応

### [S090] UNEXPLAINED

前提: [S081], [S083], [S089]

事実: $\operatorname{Im}\Delta = \mathbb{Z}\{2\eta_{2}\}$.

推論理由: 未対応

### [S091] GIVEN

前提: なし

事実: $\pi_{5}^{5} \xrightarrow{Δ} \pi_{3}^{2} \xrightarrow{E} \pi_{4}^{3}$ は完全である.

根拠区分: GIVEN (既知の前提)

### [S092] EXPLAINED

前提: [S090], [S091]

事実: $\ker E = \mathbb{Z}\{2\eta_{2}\}$.

推論理由: 完全性より, $\ker E=\operatorname{Im}Δ=\mathbb{Z}\{2\eta_{2}\}$.

### [S093] GIVEN

前提: なし

事実: $\pi_{4}^{5} = 0$

根拠区分: GIVEN (既知の前提)

### [S094] GIVEN

前提: なし

事実: $\pi_{3}^{2} \xrightarrow{E} \pi_{4}^{3} \xrightarrow{H} \pi_{4}^{5}$ は完全である.

根拠区分: GIVEN (既知の前提)

### [S095] EXPLAINED

前提: [S093], [S094]

事実: $E: \pi_{3}^{2} \to \pi_{4}^{3}$ は全射である.

推論理由: 完全性より, $E: \pi_{3}^{2} \to \pi_{4}^{3}$ は全射.

### [S096] UNEXPLAINED

前提: [S080], [S092], [S095]

事実: $\pi_{4}^{3} = \mathbb{Z}/2\{\eta_{3}\}$

推論理由: 未対応

### [S097] GIVEN

前提: なし

事実: `TodaEtaFamilyDefinitionStatement`

根拠区分: GIVEN (既知の前提)

### [S098] UNEXPLAINED

前提: [S097]

事実: $\eta_{3} = \eta_{3}$

推論理由: 未対応

### [S099] UNEXPLAINED

前提: [S096], [S098]

事実: $\pi_{4}^{3} = \mathbb{Z}/2\{\eta_{3}\}$

推論理由: 未対応

### [S100] GIVEN

前提: なし

事実: `ScalarGreaterEqualStatement`

根拠区分: GIVEN (既知の前提)

### [S101] UNEXPLAINED

前提: [S100]

事実: $\pi_{i - 1}^{1} = 0$

推論理由: 未対応

### [S102] GIVEN

前提: なし

事実: $\pi_{2}^{1} = 0$

根拠区分: GIVEN (既知の前提)

### [S103] GIVEN

前提: なし

事実: $\pi_{2}^{1} \xrightarrow{E} \pi_{3}^{2} \xrightarrow{H} \pi_{3}^{3}$ は完全である.

根拠区分: GIVEN (既知の前提)

### [S104] EXPLAINED

前提: [S102], [S103]

事実: $H: \pi_{3}^{2} \to \pi_{3}^{3}$ は単射である.

推論理由: 完全性より, $H: \pi_{3}^{2} \to \pi_{3}^{3}$ は単射.

### [S105] GIVEN

前提: なし

事実: $E: \pi_{1}^{1} \to \pi_{2}^{2}$ は同型写像である.

根拠区分: GIVEN (既知の前提)

### [S106] UNEXPLAINED

前提: [S105]

事実: $E: \pi_{1}^{1} \to \pi_{2}^{2}$ は単射である.

推論理由: 未対応

### [S107] GIVEN

前提: なし

事実: $\pi_{3}^{3} \xrightarrow{Δ} \pi_{1}^{1} \xrightarrow{E} \pi_{2}^{2}$ は完全である.

根拠区分: GIVEN (既知の前提)

### [S108] UNEXPLAINED

前提: [S106], [S107]

事実: $\Delta: \pi_{3}^{3} \to \pi_{1}^{1}$ は零写像である.

推論理由: 未対応

### [S109] GIVEN

前提: なし

事実: $\pi_{3}^{2} \xrightarrow{H} \pi_{3}^{3} \xrightarrow{Δ} \pi_{1}^{1}$ は完全である.

根拠区分: GIVEN (既知の前提)

### [S110] EXPLAINED

前提: [S108], [S109]

事実: $H: \pi_{3}^{2} \to \pi_{3}^{3}$ は全射である.

推論理由: 完全性より, $H: \pi_{3}^{2} \to \pi_{3}^{3}$ は全射.

### [S111] UNEXPLAINED

前提: [S104], [S110]

事実: $H: \pi_{3}^{2} \to \pi_{3}^{3}$ は同型写像である.

推論理由: 未対応

### [S112] GIVEN

前提: なし

事実: $\pi_{3}^{3} = \mathbb{Z}\{\iota_{3}\}$

根拠区分: GIVEN (既知の前提)

### [S113] UNEXPLAINED

前提: [S111], [S112]

事実: $H(\eta_{2}) = \iota_{3}$ を満たす $\eta_{2} \in \pi_{3}^{2}$ を定める.

推論理由: 未対応

### [S114] UNEXPLAINED

前提: [S113]

事実: $H\left(\eta_{2}\right) = \iota_{3}$

推論理由: 未対応

### [S115] GIVEN

前提: なし

事実: `TodaProp44DecompositionMap`

根拠区分: GIVEN (既知の前提)

### [S116] UNEXPLAINED

前提: [S113], [S114], [S115]

事実: $(\beta, γ) \mapsto E\beta + \eta_{2}γ: \pi_{i - 1}^{1} \oplus \pi_{i}^{3} \to \pi_{i}^{2}$ は同型写像である.

推論理由: 未対応

### [S117] UNEXPLAINED

前提: [S116]

事実: 分解写像の第二成分は $\eta_{2}γ$ で与えられる.

推論理由: 未対応

### [S118] UNEXPLAINED

前提: [S101], [S116], [S117]

事実: $\eta_{2}\circ -: \pi_{i}^{3} \to \pi_{i}^{2}$ は同型写像である.

推論理由: 未対応

### [S119] UNEXPLAINED

前提: [S099], [S118]

事実: $\pi_{4}^{2} = \mathbb{Z}/2\{\eta_{2}^{2}\}$

推論理由: 未対応

### [S120] GIVEN

前提: なし

事実: `TodaEtaFamilyDefinitionStatement`

根拠区分: GIVEN (既知の前提)

### [S121] GIVEN

前提: なし

事実: `TodaEtaFamilyDefinitionStatement`

根拠区分: GIVEN (既知の前提)

### [S122] UNEXPLAINED

前提: [S120], [S121]

事実: $\eta_{3}\eta_{3} = \eta_{3}^{2}$

推論理由: 未対応

### [S123] EXPLAINED

前提: [S079], [S119], [S122]

事実: $\pi_{5}^{3} = \mathbb{Z}/2\{\eta_{3}^{2}\}$

推論理由: 群構造の移送に必要な前提を確認する. $E: \pi_{4}^{2} \xrightarrow{\cong} \pi_{5}^{3}$ は同型であり, $\pi_{4}^{2} = \mathbb{Z}/2\{\eta_{2}^{2}\}$ および $E\eta_{2}\eta_{3} = \eta_{3}\eta_{4}$ が成り立つ. したがって, 同型写像によって位数と生成元が移され, 移送先は指定された生成元を持つ同じ位数の巡回群である.
