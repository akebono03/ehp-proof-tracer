# Phase 165 R14-R25 — Proposition 4.2 出典照合

## 対象の完全列

`pi_3^3 --Delta--> pi_1^1 --E--> pi_2^2`

## 出典候補の全文と確認項目

### phase163:archive:toda:tex:ch4:0002

- Locator: (4.2)
- 完全性語彙: False
- Delta 記号: False
- E / 矢印記号: False
- 次数条件らしき表記: False
- 数学的適用条件の確認: **未実施**

```tex
\begin{equation}\label{4.2}
% (4.2).\
\pis{i}{S^n}\ \text{は,} \ i=n \ \text{または} \ 
i=2n-1 \ \text{のとき以外は, 有限群である. }
\end{equation}
```

### phase163:archive:toda:tex:ch4:0005

- Locator: Proposition 4.2
- 完全性語彙: True
- Delta 記号: False
- E / 矢印記号: False
- 次数条件らしき表記: False
- 数学的適用条件の確認: **未実施**

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

## 判定

記号の出現だけでは exactness（完全性）・添字範囲を認証できない。
該当文の原文と対象の Δ→E を照合するまでは ProofStep を作らない。
