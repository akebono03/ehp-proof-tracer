# Phase 149 / RC3-1 — Narrative ordering audit

目的は `pi_6^3` の contribution insertion ordering（寄与の挿入順序）の現状を監査することです。

このパッケージは production code を変更しません。

監査対象:

- Argument の表示順
- Narrative block の保存順
- RC2 exactness component の ownership / exposure
- exactness display contribution の種類
- 既存 hidden contribution ordering の placement
- base markdown と contribution 挿入後 markdown における各要素の位置
- `pi_6^3` の短完全列と群構造結論の前後関係

Phase 149 の境界:

- RC2 exposure classification は変更しない
- RC4 reason prose は扱わない
- RC5 EHP semantic naming は扱わない
- RC6 equation numbering / formatting は扱わない
- repository-wide test は Phase 149 の最後だけ実行する

実行後、`rc3_1_output.txt` と focused pytest の出力を ChatGPT に貼り付けてください。
