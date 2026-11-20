# Phase 176 R3R21 監査計画

## 変更対象

- 新規ディレクトリ `phase176_r3r21_hopf_right_composition_audit/` のみ。
- `audit.py`: `names_in_file`、`inspect`、`git_value`、`report_path`、`execute`、`main`。
- `run.ps1`: 実行入口。
- `README.md`、`AUDIT_PLAN_JA.md`: 説明文書。

## 数学的監査の範囲

Toda Proposition 2.2 の右合成公式

$$H(\alpha\circ E\gamma)=H(\alpha)\circ E\gamma$$

に対して、$\alpha=\nu'\eta_6$、$\gamma=\eta_6$ を検討する。

$$H(\nu'\eta_6\eta_7)=\eta_5\eta_6\eta_7$$

は現段階では型付き導出の候補とし、共有探索で証明済みとは扱わない。さらに $\eta_5\eta_6\eta_7$ の位数、Hopf 写像の核・単射性、元の群の生成の網羅性を別々の未解決義務とする。

## 完了条件

`source_guard` と限定 pytest の成功。公開群証明の完成は要求せず、全体 pytest は行わない。

## 次段階との境界

R3R22 以降で型付き特殊化・出典連結・共有 Proof Search への接続を個別に監査する。本段階では推論規則も GIVEN も追加しない。
