# Phase 163 R4-R75：出典帰属の重点監査案

保留7件と番号なし主張候補4件を確認。帰属案であって原本・数学的境界の検証ではない。

## 集約案

- `ch1:coset-comparison:1004-1027`: #67, #68, #69
- `ch1:preceding-proposition:at-953`: #66
- `ch2:cohomology-maps:560-578`: #122, #123
- `ch2:cup-product-by-parity:549-559`: #120
- `ch2:delta-proof:1021-1026`: #142
- `ch2:relative-composition:991-999`: #140
- `ch2:spectral-sequence:705-818`: #133
- `ch4:ehp-proof:283-291`: #256

## 原文と判断根拠

### R48 #133（第2章 741行）

- 帰属案: `PROOF_SPECTRAL_SEQUENCE_STEP`
- 集約先（暫定）: `ch2:spectral-sequence:705-818`
- 根拠: スペクトル列の計算中の分解式。番号付き命題との境界は未確認。

```tex
\[
H^{*}(X;\Lambda)\ \cong\ p^{*}H^{*}\!\bigl((S^{pm})_\infty;\Lambda\bigr)\ \otimes\ G
\]
```

```text
738: \]
739: $E_\infty^{*}$ における $B^{*}\otimes G_0$ の極限を考えると, 
740: それは,
741: \[
742: H^{*}(X;\Lambda)\ \cong\ p^{*}H^{*}\!\bigl((S^{pm})_\infty;\Lambda\bigr)\ \otimes\ G
743: \]
744: に付随する graded module である. \\
745: よって, $B^{*}\otimes G_0 \cong E_\infty^{*}$ かつ,
746: $H^{*}(X;\Lambda)\otimes G_0$ に module として同型である. \\
```

### R48 #66（第1章 956行）

- 帰属案: `PARAPHRASE_OF_PRECEDING_PROPOSITION`
- 集約先（暫定）: `ch1:preceding-proposition:at-953`
- 根拠: 直前の proposition 終了後の『要するに』による言い換え。独立 Reference の新設を保留。

```tex
\[
\{\{\alpha,\beta,\gamma\},\ E\delta,\ E\varepsilon\}
+\{\alpha,\ \{\beta,\gamma,\delta\},\ E\varepsilon\}
+\{\alpha,\ \beta,\ \{\gamma,\delta,\varepsilon\}\}
\equiv0 .
\]
```

```text
953: \end{proposition}
954: 
955: \noindent (要するに) 
956: \[
957: \{\{\alpha,\beta,\gamma\},\ E\delta,\ E\varepsilon\}
958: +\{\alpha,\ \{\beta,\gamma,\delta\},\ E\varepsilon\}
959: +\{\alpha,\ \beta,\ \{\gamma,\delta,\varepsilon\}\}
960: \equiv0 .
961: \]
```

### R48 #67（第1章 1007行）

- 帰属案: `PROOF_COSET_EXPRESSION`
- 集約先（暫定）: `ch1:coset-comparison:1004-1027`
- 根拠: coset 比較の一方の部分群を記述。関連する #68, #69 と同じ議論に属する候補。

```tex
\[
(\alpha+\alpha')\circ \Ex^{n+1}\!\bigl([W, Y]\bigr) 
+ [\Ex^{n+1}X, Z]\circ \Ex^{n+1}\gamma.
\]
```

```text
1004: \{\alpha+\alpha',\Ex^n\beta,\Ex^n\gamma\}_n
1005: \)
1006: は, 次の部分群の coset である. 
1007: \[
1008: (\alpha+\alpha')\circ \Ex^{n+1}\!\bigl([W, Y]\bigr) 
1009: + [\Ex^{n+1}X, Z]\circ \Ex^{n+1}\gamma.
1010: \]
1011: 他方, 
1012: \(
```

### R48 #68（第1章 1016行）

- 帰属案: `PROOF_COSET_EXPRESSION`
- 集約先（暫定）: `ch1:coset-comparison:1004-1027`
- 根拠: 同じ coset 比較の他方の部分群。#67, #69 と独立に登録しない。

```tex
\[
\alpha\circ E^{n+1}[W,X]
+ \alpha'\circ E^{n+1}[W,X]
+ [E^{n+1}X,Z].
\]
```

```text
1013: \{\alpha,\Ex^n\beta,\Ex^n\gamma\}_n + \{\alpha',\Ex^n\beta,\Ex^n\gamma\}_n
1014: \)
1015: は, 次の部分群の coset である.
1016: \[
1017: \alpha\circ E^{n+1}[W,X]
1018: + \alpha'\circ E^{n+1}[W,X]
1019: + [E^{n+1}X,Z].
1020: \]
1021: この群は, 次の元を含んでいる.
```

### R48 #69（第1章 1022行）

- 帰属案: `PROOF_COSET_EXPRESSION`
- 集約先（暫定）: `ch1:coset-comparison:1004-1027`
- 根拠: 前の二つの部分群を比較する包含部分。TeX 誤記候補 E^[n+1] を要確認。

```tex
\[
(\alpha + \alpha') \circ E^{n+1}[W,X]
+ [E^[n+1]X,Z] \circ E^{n+1}\gamma.
\]
```

```text
1019: + [E^{n+1}X,Z].
1020: \]
1021: この群は, 次の元を含んでいる.
1022: \[
1023: (\alpha + \alpha') \circ E^{n+1}[W,X]
1024: + [E^[n+1]X,Z] \circ E^{n+1}\gamma.
1025: \]
1026: よって,
1027: \(
```

### R48 #120（第2章 557行）

- 帰属案: `UNNUMBERED_ASSERTION_CASE`
- 集約先（暫定）: `ch2:cup-product-by-parity:549-559`
- 根拠: m 偶数の積の公式。直前の m 奇数の場合との一体的登録を要確認。

```tex
\[
u_k\,u_h=\binom{k+h}{k}\,u_{k+h}.
\]
```

```text
554: u_{2k}\,u_{2h}=\binom{k+h}{k}\,u_{2(k+h)}.
555: \]
556: $m$ が偶数のとき, 
557: \[
558: u_k\,u_h=\binom{k+h}{k}\,u_{k+h}.
559: \]
560: 係数体を,
561: \[
562: \Lambda=
```

### R48 #122（第2章 569行）

- 帰属案: `UNNUMBERED_ASSERTION_CASE`
- 集約先（暫定）: `ch2:cohomology-maps:560-578`
- 根拠: 条件付き i* 同型。#123 と同じ周辺段落でも Assertion は別にする案。

```tex
\[
i^*:H^i\bigl((S^m)_\infty;\Lambda\bigr)\to H^i\bigl((S^m)_{p-1};\Lambda\bigr)
\ \ \text{は} \ 
i<pm \ \text{で同型 .}
\]
```

```text
566: \end{cases}
567: \]
568: とする. このとき, 次のことが簡単に確かめられる. 
569: \[
570: i^*:H^i\bigl((S^m)_\infty;\Lambda\bigr)\to H^i\bigl((S^m)_{p-1};\Lambda\bigr)
571: \ \ \text{は} \ 
572: i<pm \ \text{で同型 .}
573: \]
574: \[
```

### R48 #123（第2章 574行）

- 帰属案: `UNNUMBERED_ASSERTION_CASE`
- 集約先（暫定）: `ch2:cohomology-maps:560-578`
- 根拠: h* の単射性に関する式。#122 と同じ Reference 内の別 Assertion 候補。

```tex
\[
h^*:H^i\bigl((S^{pm})_\infty;\Lambda\bigr)\to H^i\bigl((S^m)_{\infty};\Lambda\bigr)
\ \ \text{は} \ 
\text{任意の } i \ \text{で単射同型 .}
\]
```

```text
571: \ \ \text{は} \ 
572: i<pm \ \text{で同型 .}
573: \]
574: \[
575: h^*:H^i\bigl((S^{pm})_\infty;\Lambda\bigr)\to H^i\bigl((S^m)_{\infty};\Lambda\bigr)
576: \ \ \text{は} \ 
577: \text{任意の } i \ \text{で単射同型 .}
578: \]
579: 
```

### R48 #140（第2章 994行）

- 帰属案: `UNNUMBERED_ASSERTION_CASE`
- 集約先（暫定）: `ch2:relative-composition:991-999`
- 根拠: 境界写像と h_m* の合成に関する二つの関係。1つの出典段落に2 Assertion の可能性。

```tex
\[
\partial(\alpha'\circ\partial_0^{-1}\beta) = \partial(\alpha')\circ \beta,\quad


h_{m*}(\alpha'\circ\partial_0^{-1}\beta) = h_{m*}(\alpha')\circ E\beta .
\]
```

```text
991: 相対ホモトピー群の中での合成とみなすことにより, 
992: \(\alpha'\in\pi_i((S^m)_\infty, S^m)\)
993: に対して, 
994: \[
995: \partial(\alpha'\circ\partial_0^{-1}\beta) = \partial(\alpha')\circ \beta,\quad
996: 
997: 
998: h_{m*}(\alpha'\circ\partial_0^{-1}\beta) = h_{m*}(\alpha')\circ E\beta .
999: \]
```

### R48 #142（第2章 1024行）

- 帰属案: `CONCLUSION_OF_NUMBERED_PROOF`
- 集約先（暫定）: `ch2:delta-proof:1021-1026`
- 根拠: \qed と同じ式中にある証明の結論。既存番号付き主張との一致を確認する。

```tex
\[
\Delta(E^2\gamma)=\pm[\,\iota_m,\iota_m\,]\circ\gamma.\qquad \qed
\]
```

```text
1021: \Delta(\iota_{2m+1})=\pm[\,\iota_m,\iota_m\,]
1022: \)
1023: が直ちに従い, 特に,
1024: \[
1025: \Delta(E^2\gamma)=\pm[\,\iota_m,\iota_m\,]\circ\gamma.\qquad \qed
1026: \]
1027: 
1028: \switchcolumn
1029: 
```

### R48 #256（第4章 286行）

- 帰属案: `EHP_EXACTNESS_PROOF_FRAGMENT`
- 集約先（暫定）: `ch4:ehp-proof:283-291`
- 根拠: 『残る問題は』に続く完全列の一部分。完全性を証明する文脈に帰属。

```tex
\[
\pit{2n}{n}\ \xrightarrow{\ \Ex\ }\ \pit{2n+1}{n+1}\
\xrightarrow{\ H\ }\ \pit{2n+1}{2n+1}\
\xrightarrow{\ \Delta\ }\ \pit{2n-1}{n}\
\xrightarrow{E} \ \pit{2n}{n+1}
\]
```

```text
283: \]
284: の完全性を得る. 
285: 残る問題は,
286: \[
287: \pit{2n}{n}\ \xrightarrow{\ \Ex\ }\ \pit{2n+1}{n+1}\
288: \xrightarrow{\ H\ }\ \pit{2n+1}{2n+1}\
289: \xrightarrow{\ \Delta\ }\ \pit{2n-1}{n}\
290: \xrightarrow{E} \ \pit{2n}{n+1}
291: \]
```

## 未完了事項

- 引用原本の照合、番号付き命題との境界、数学的妥当性はいずれも未検証。
- R74 の残り54件および R73 の172件を変更せず、正式登録を行わない。
